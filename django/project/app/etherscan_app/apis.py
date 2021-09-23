from typing import Iterable

from app.etherscan_app.services import EtherscanService


class EtherscanAPI:
    @staticmethod
    def get_last_block_created() -> int:
        return EtherscanService.get_last_block_created()

    @staticmethod
    def get_blocks_iterator(*, start_block: int, end_block: int):
        return EtherscanService.get_blocks_iterator(
            start_block=start_block, end_block=end_block
        )

    @staticmethod
    def get_internal_transactions_by_block_range(
        *, start_block=int, end_block=int
    ) -> Iterable:
        return EtherscanService.get_internal_transactions_by_block_range(
            start_block=start_block, end_block=end_block
        )
