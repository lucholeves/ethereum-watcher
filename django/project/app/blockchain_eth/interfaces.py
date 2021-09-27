from typing import Iterable

from app.etherscan_app import apis


class EtherscanInterface:
    @staticmethod
    def get_last_block_created():
        return apis.EtherscanAPI.get_last_block_created()

    @staticmethod
    def get_blocks_iterator(*, start_block: int, end_block: int):
        return apis.EtherscanAPI.get_blocks_iterator(
            start_block=start_block, end_block=end_block
        )

    @staticmethod
    def get_internal_transactions_by_block_range(
        *, start_block=int, end_block=int
    ) -> Iterable:
        return apis.EtherscanAPI.get_internal_transactions_by_block_range(
            start_block=start_block, end_block=end_block
        )

    @staticmethod
    def get_normal_transactions_by_block_number(*, block_number: int) -> Iterable:
        return apis.EtherscanAPI.get_normal_transactions_by_block_number(
            block_number=block_number
        )
