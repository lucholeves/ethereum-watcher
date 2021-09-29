from typing import Dict, Iterable, Optional

from app.etherscan_app.services import EtherscanService
from app.etherscan_app.factories import get_block_attributes, get_transaction_attributes


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

    @staticmethod
    def get_normal_transactions_by_block_number(*, block_number: int):
        return EtherscanService.get_normal_transactions_by_block_number(
            block_number=block_number
        )

    @staticmethod
    def get_block_attributes():
        return get_block_attributes()

    @staticmethod
    def get_transaction_attributes(block_number: Optional[int] = None) -> Dict:
        return get_transaction_attributes()
