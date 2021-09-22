import logging

from django.db import transaction
from django.db.utils import IntegrityError

from app.blockchain_eth.interfaces import EtherscanInterface

from .models import Block, Transaction

logger = logging.getLogger(__name__)


class BlockchainEthService:
    """ """

    @staticmethod
    def update_blocks():
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
        else:
            logger.info(f"No news blocks created.")

    @staticmethod
    def update_transactions():
        blocks_to_update = Block.objects.filter(transactions_updated=False).order_by(
            "id"
        )
        if blocks_to_update:
            start_block = blocks_to_update.first().number
            end_block = blocks_to_update.last().number

            transactions_to_create = EtherscanInterface.get_internal_transactions_by_block_range(
                start_block=start_block, end_block=end_block
            )
            new_transactions = []
            for txn_data in transactions_to_create:
                block_number = txn_data.get("blockNumber")
                try:
                    block = Block.objects.get(data__blockNumber=block_number)
                except Exception:
                    import pdb

                    pdb.set_trace()
                new_transactions.append(Transaction(block=block, data=txn_data))

            try:
                with transaction.atomic():
                    created = Transaction.objects.bulk_create(new_transactions)
                    logger.info(f"{len(created)} new transaction created.")

                    blocks_transaction_updated = Transaction.objects.all().values_list(
                        "block__id"
                    )
                    updated = Block.objects.filter(
                        id__in=blocks_transaction_updated
                    ).update(transactions_updated=True)
                    logger.info(f"{updated} blocks updated.")
            except IntegrityError:
                logger.exception(f"Database error!")
        else:
            logger.info("All transactions are updated.")
