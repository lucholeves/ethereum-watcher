import pytest
import random
from unittest.mock import patch
from typing import List, Optional

from app.blockchain_eth.factories import BlockFactory
from app.blockchain_eth.services import BlockchainEthService
from app.blockchain_eth.models import Block
from app.blockchain_eth.interfaces import EtherscanInterface


def blocks_iterator(bath: Optional[int] = None) -> List:
    if not bath:
        bath = random.randint(2, 20)
    return [EtherscanInterface.get_block_attributes() for _ in range(bath)]


@pytest.mark.django_db
@patch("app.blockchain_eth.services.logger")
@patch(
    "app.blockchain_eth.interfaces.EtherscanInterface.get_blocks_iterator",
    return_value=blocks_iterator(10),
)
@patch(
    "app.blockchain_eth.interfaces.EtherscanInterface.get_last_block_created",
    return_value=1234,
)
def test_update_blocks(path_last_block, path_get_blocks_iterator, mocked_logger):
    """Test that update_blocks creates 10 blocks"""

    # Method to test
    created_id = BlockchainEthService.update_blocks()

    assert Block.objects.count() == 10
    assert len(created_id) == 10
    mocked_logger.info.assert_called_once_with("10 new blocks created.")


@pytest.mark.django_db
@patch("app.blockchain_eth.services.logger")
@patch(
    "app.blockchain_eth.interfaces.EtherscanInterface.get_blocks_iterator",
    return_value=[],
)
@patch(
    "app.blockchain_eth.interfaces.EtherscanInterface.get_last_block_created",
    return_value=1234,
)
def test_update_blocks_empty_last_created_response(
    path_last_block, path_get_blocks_iterator, mocked_logger
):
    """Test that update_blocks creates 0 blocks"""

    # Method to test
    created_id = BlockchainEthService.update_blocks()

    assert Block.objects.count() == 0
    assert len(created_id) == 0
    mocked_logger.info.assert_called_once_with("0 new blocks created.")


@pytest.mark.django_db
@patch("app.blockchain_eth.services.logger")
@patch(
    "app.blockchain_eth.interfaces.EtherscanInterface.get_blocks_iterator",
    return_value=blocks_iterator(),
)
@patch(
    "app.blockchain_eth.interfaces.EtherscanInterface.get_last_block_created",
    return_value=1234,
)
def test_update_blocks_no_new_blocks(
    path_last_block, path_get_blocks_iterator, mocked_logger
):
    """Test that update_blocks creates 0 blocks"""
    # last block number is equal to the last block created
    last_block = BlockFactory(number=1234)
    assert last_block.number == 1234

    # Method to test
    created_id = BlockchainEthService.update_blocks()

    assert Block.objects.count() == 1
    assert len(created_id) == 0
    mocked_logger.info.assert_called_once_with("No news blocks created.")


def test_get_update_normal_transactions_name():
    name = "app.blockchain_eth.tasks.update_normal_transactions"
    assert BlockchainEthService.get_update_normal_transactions_name() == name


@pytest.mark.skip("Need to change the approach.")
def test_get_update_internal_transactions_name():
    name = "app.blockchain_eth.tasks.update_internal_transactions"
    assert BlockchainEthService.get_update_internal_transactions_name() == name


# TODO: complete tests!
