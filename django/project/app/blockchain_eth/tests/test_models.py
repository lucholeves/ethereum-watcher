import pytest


from app.blockchain_eth.factories import BlockFactory, TransactionFactory


@pytest.mark.django_db()
def test_create_block():
    block = BlockFactory()

    assert block.id
    assert block.number == block.data["blockNumber"]


@pytest.mark.django_db()
def test_create_transaction():
    transaction = TransactionFactory()

    assert transaction.id
    assert transaction.block.id
    assert transaction.hash == transaction.data["hash"]
