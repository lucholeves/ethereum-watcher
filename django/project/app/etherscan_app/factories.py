from faker import Faker
from typing import Dict, Optional

faker = Faker()


def get_block_attributes(block_number: Optional[int] = None) -> Dict:
    """Returns the a block response from Etherscan"""

    attributes = {
        "uncles": faker.pylist(value_types=["pyint", "pybool"]),
        "timeStamp": faker.pyint(),
        "blockMiner": f"0x{faker.sha1()}",
        "blockNumber": block_number or faker.pyint(),
        "blockReward": faker.pyint(),
        "uncleInclusionReward": "0",
    }
    return attributes


def get_transaction_attributes() -> Dict:
    """Returns the a transaction response from Etherscan"""

    return {
        "r": f"0x{faker.sha1()}",
        "s": f"0x{faker.sha1()}",
        "v": hex(faker.pyint()),
        "to": f"0x{faker.sha1()}",
        "gas": hex(faker.pyint()),
        "from": f"0x{faker.sha1()}",
        "hash": f"0x{faker.sha1()}",
        "type": hex(faker.pyint()),
        "input": "0x095ea7b300000000000000000000000000",
        "nonce": hex(faker.pyint()),
        "value": hex(faker.pyint()),
        "chainId": hex(faker.pyint()),
        "gasPrice": hex(faker.pyint()),
        "blockHash": f"0x{faker.sha1()}",
        "accessList": [],
        "blockNumber": hex(faker.pyint()),
        "maxFeePerGas": hex(faker.pyint()),
        "transactionIndex": hex(faker.pyint()),
        "maxPriorityFeePerGas": hex(faker.pyint()),
    }
