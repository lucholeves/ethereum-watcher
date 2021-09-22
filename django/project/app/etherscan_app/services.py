import logging
import time

from etherscan import Etherscan

logger = logging.getLogger(__name__)


class EtherscanService:
    """ """

    @staticmethod
    def create_ethercan_session():
        eth = Etherscan("2H342TNQHSRRBSYVISHKJ9BTE2IA42PNHQ")
        return eth

    @staticmethod
    def get_last_block_created() -> int:
        eth = EtherscanService.create_ethercan_session()
        time_stamps = int(time.time())

        last_block_created = int(
            eth.get_block_number_by_timestamp(time_stamps, closest="before")
        )
        return last_block_created

    @staticmethod
    def get_blocks_iterator(*, start_block: int, end_block: int):
        eth = EtherscanService.create_ethercan_session()

        for block in range(start_block, end_block + 1):
            try:
                block_reward = eth.get_block_reward_by_block_number(block)
                yield block_reward
            except Exception as e:
                logger.exception(e)

    @staticmethod
    def get_internal_transactions_by_block_range(*, start_block=int, end_block=int):
        eth = EtherscanService.create_ethercan_session()

        # TODO: validate range
        try:
            return eth.get_internal_txs_by_block_range_paginated(
                startblock=start_block, endblock=end_block, page=1, offset=0, sort="asc"
            )
        except Exception as e:
            logger.exception(e)
