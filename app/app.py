from time import time
from etherscan import Etherscan

eth = Etherscan("2H342TNQHSRRBSYVISHKJ9BTE2IA42PNHQ")

time_stamps = int(time())
last_block_created = int(
    eth.get_block_number_by_timestamp(time_stamps, closest="before")
)
print(f"Las block created: {last_block_created}")
print("\n")
# Get the last 10 blocks added to the blockchain
def get_block_iterator(last_block_number: int):
    start_block = last_block_number - 10
    for block in range(start_block, last_block_number + 1):
        try:
            block_reward = eth.get_block_reward_by_block_number(block)
            yield block_reward
        except Exception as e:
            print(e)


for i, block in enumerate(get_block_iterator(last_block_created)):
    print(f"{i} === {block}")

print("\n")
print(f"Transactions for block {last_block_created}")
# Get transaction from a block
transactions = eth.get_internal_txs_by_block_range_paginated(
    startblock=last_block_created,
    endblock=last_block_created,
    page=0,
    offset=0,
    sort="asc",
)
for i, transaction in enumerate(transactions):
    print(f"{i} === {transaction}")