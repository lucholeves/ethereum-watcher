import logging

from celery import shared_task

from .services import BlockchainEthService

logger = logging.getLogger(__name__)


@shared_task
def update_blocks():
    logger.info("Running update blocks.")
    BlockchainEthService.update_blocks()
