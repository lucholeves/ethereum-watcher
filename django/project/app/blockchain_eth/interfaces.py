from project.app.etherscan_app import apis

class EtherscanInterface:

    @staticmethod
    def get_last_block_created():
        return apis.EtherscanAPI.get_last_block_created()

    @staticmethod
    def get_blocks_iterator(*, start_block: int, end_block: int):
        return apis.EtherscanAPI.get_blocks_iterator(start_block=start_block, end_block=end_block)
