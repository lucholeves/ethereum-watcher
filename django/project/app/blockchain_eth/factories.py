import factory
from app.blockchain_eth.models import Block, Transaction
from app.blockchain_eth.interfaces import EtherscanInterface


class BlockFactory(factory.django.DjangoModelFactory):
    number = factory.Faker("pyint")
    data = factory.LazyAttribute(
        lambda o: EtherscanInterface.get_block_attributes(o.number)
    )

    class Meta:
        model = Block


class TransactionFactory(factory.django.DjangoModelFactory):
    block = factory.SubFactory(BlockFactory)
    data = factory.LazyAttribute(
        lambda o: EtherscanInterface.get_transaction_attributes()
    )

    class Meta:
        model = Transaction
