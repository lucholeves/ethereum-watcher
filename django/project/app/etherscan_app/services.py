import logging
import time
from typing import Iterable, List

from etherscan import Etherscan

logger = logging.getLogger(__name__)

RECORDS_BY_REQUEST = 10_000
PAGE_LIMIT = 5_000


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
    def get_internal_transactions_by_block_range(
        *, start_block=int, end_block=int
    ) -> Iterable:
        eth = EtherscanService.create_ethercan_session()

        # TODO: validate range
        try:
            return eth.get_internal_txs_by_block_range_paginated(
                startblock=start_block, endblock=end_block, page=1, offset=0, sort="asc"
            )
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def get_normal_transactions_by_block_number(*, block_number: int) -> Iterable:
        eth = EtherscanService.create_ethercan_session()

        try:
            block = eth.get_proxy_block_by_number(tag=hex(block_number))
            if block:
                return block["transactions"]
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def _eth_request_auto_pagination_iterator(
        eth_paginated_method, limit_records=RECORDS_BY_REQUEST, **kwargs
    ):
        # remove page and offset
        kwargs.pop("page", None)
        kwargs.pop("offset", None)
        # this approach uses a page limit number
        for page in range(1, PAGE_LIMIT):
            try:
                yield eth_paginated_method(page=page, offset=limit_records, **kwargs)
            except AssertionError as e:
                # etherscan-python exception for 'No transactions found'
                print(e)
                return []

    @staticmethod
    def get_transaction_count_by_address(*, address: str) -> int:
        eth = EtherscanService.create_ethercan_session()
        return int(eth.get_proxy_transaction_count(address=address), 0)

    @staticmethod
    def get_historical_normal_transactions_by_address(*, address: str) -> List:
        """
        Returns the list of transactions performed by an address

        Note: this method searches the entire blockchain. Be carefull
        since this method could be run for a long time
        """

        PAGE_SIZE = 5_000
        eth = EtherscanService.create_ethercan_session()

        count_transactions = EtherscanService.get_transaction_count_by_address(
            address=address
        )
        last_block = EtherscanService.get_last_block_created()
        block_pages = list(range(0, last_block, PAGE_SIZE))
        block_pages = list(
            map(
                lambda x: (
                    x,
                    x + PAGE_SIZE - 1 if x != block_pages[-1] else last_block,
                ),
                block_pages,
            )
        )

        transactions = []
        # TODO: should be remove this
        startTime = time.time()

        print(f"Address transaction count: {count_transactions}")

        for start, end in block_pages:
            print(start, " - ", end)
            try:
                page_result_iterator = EtherscanService._eth_request_auto_pagination_iterator(
                    eth.get_normal_txs_by_address_paginated,
                    limit_records=5_000,
                    address=address,
                    startblock=start,
                    endblock=end,
                    sort="asc",
                )
                for result in page_result_iterator:
                    transactions.extend(result)
                # keep searching only if the number of transactions founded
                # is minor to the address transactions count
                if len(transactions) >= count_transactions:
                    print(f"Stop searching {len(transactions)} >= {count_transactions}")
                    break
            except Exception as e:
                logger.exception(e)

        executionTime = time.time() - startTime
        print("Execution time in seconds: " + str(executionTime))

        return transactions
