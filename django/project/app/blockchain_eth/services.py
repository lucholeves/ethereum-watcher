import logging

from project.app.blockchain_eth.interfaces import EtherscanInterface
from .models import Block

logger = logging.getLogger(__name__)

class BlockchainEthService:
    """ """

    @staticmethod
    def update_blocks():
        last_block_updated = Block.objects.last()
        last_block_created_blockchain = EtherscanInterface.get_last_block_created()

        # TODO: This API endpoint returns a maximum of 10000 records only.
        start_block = last_block_updated.number if last_block_updated else last_block_created_blockchain - 50

        if start_block < last_block_created_blockchain:
            blocks_to_create = []
            for block in EtherscanInterface.get_blocks_iterator(
                start_block=start_block, end_block=last_block_created_blockchain
            ):
                blocks_to_create.append(Block(data=block))
            created = Block.objects.bulk_create(blocks_to_create)
            logger.debug(f"{created} new blocks created.")
        else:
            logger.debug(f"No news blocks created.")
