import logging
from typing import List

from django.db import transaction
from django.db.utils import IntegrityError

from app.blockchain_eth.interfaces import EtherscanInterface

from .models import Block, Transaction

logger = logging.getLogger(__name__)


class BlockchainEthService:
    """ """

    @staticmethod
    def update_blocks() -> List[int]:
        last_block_updated = Block.objects.last()
        last_block_created_blockchain = EtherscanInterface.get_last_block_created()

        # TODO: This API endpoint returns a maximum of 10000 records only.
        limit_blocks = 100
        start_block = (
            last_block_updated.number + 1
            if last_block_updated
            and (
                last_block_created_blockchain - last_block_updated.number
                <= limit_blocks
            )
            else last_block_created_blockchain - 5
        )
        if start_block < last_block_created_blockchain:
            blocks_to_create = []
            for block in EtherscanInterface.get_blocks_iterator(
                start_block=start_block, end_block=last_block_created_blockchain
            ):
                # TODO: instance block with number
                blocks_to_create.append(
                    Block(data=block, number=int(block["blockNumber"]))
                )
            created = Block.objects.bulk_create(blocks_to_create)
            logger.info(f"{len(created)} new blocks created.")
            return [block.id for block in created]
        else:
            logger.info(f"No news blocks created.")

        return []

    @staticmethod
    def get_update_internal_transactions_name() -> str:
        return "app.blockchain_eth.tasks.update_internal_transactions"

    @staticmethod
    def get_update_normal_transactions_name() -> str:
        return "app.blockchain_eth.tasks.update_normal_transactions"

    @staticmethod
    def update_internal_transactions(*, block_ids: List[int]):
        blocks_to_update = Block.objects.filter(id__in=block_ids).order_by("id")

        if blocks_to_update:
            start_block = blocks_to_update.first().number
            end_block = blocks_to_update.last().number

            transactions_to_create = EtherscanInterface.get_internal_transactions_by_block_range(
                start_block=start_block, end_block=end_block
            )
            new_transactions = []
            for txn_data in transactions_to_create:
                block_number = txn_data.get("blockNumber")
                block = Block.objects.get(data__blockNumber=block_number)

                new_transactions.append(
                    Transaction(block=block, type=Transaction.INTERNAL, data=txn_data)
                )
            if new_transactions:
                try:
                    with transaction.atomic():
                        transaction_created = Transaction.objects.bulk_create(
                            new_transactions
                        )
                        blocks_transaction_updated = [
                            transaction.block_id for transaction in transaction_created
                        ]
                        updated = Block.objects.filter(
                            id__in=blocks_transaction_updated
                        ).update(transactions_updated=True)
                        logger.info(
                            f"{len(transaction_created)} new INTERNAL transaction created. {updated} blocks updated."
                        )
                except IntegrityError:
                    logger.exception(f"Database error!")
            else:
                logger.info("No created news NORMAL transactions.")
        else:
            logger.info("Transactions updated.")

    @staticmethod
    def update_normal_transactions(*, block_ids: List[int]):
        blocks_to_update = Block.objects.filter(id__in=block_ids).order_by("id")

        if blocks_to_update:
            new_transactions = []
            for block in blocks_to_update:
                #  Specify a smaller startblock and endblock range for faster search results.
                transactions_to_create = EtherscanInterface.get_normal_transactions_by_block_number(
                    block_number=block.number
                )
                for txn_data in transactions_to_create:
                    # TODO: some data came in HEX numbers
                    block_number = str(int(txn_data.get("blockNumber"), 0))
                    block = Block.objects.get(data__blockNumber=block_number)

                    new_transactions.append(
                        Transaction(block=block, type=Transaction.NORMAL, data=txn_data)
                    )
            if new_transactions:
                try:
                    with transaction.atomic():
                        transaction_created = Transaction.objects.bulk_create(
                            new_transactions
                        )
                        blocks_transaction_updated = [
                            transaction.block_id for transaction in transaction_created
                        ]
                        updated = Block.objects.filter(
                            id__in=blocks_transaction_updated
                        ).update(transactions_updated=True)
                        logger.info(
                            f"{len(transaction_created)} new NORMAL transaction created. {updated} blocks updated."
                        )
                except IntegrityError:
                    logger.exception(f"Database error!")
            else:
                logger.info("No created news NORMAL transactions.")
        else:
            logger.info("Transactions updated.")
