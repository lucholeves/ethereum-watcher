import logging
import random
from functools import wraps

from celery import shared_task

from app.celery import app

from .services import BlockchainEthService

logger = logging.getLogger(__name__)


def retry_task(func):
    """Decorator that logs a task call and retry it if fails"""

    @wraps(func)
    def wrapper(task, *args, **kwargs):
        retries = task.request.retries
        exponential = 2 ** retries
        exponential_backoff = random.randint(exponential, exponential * 2)
        try:
            result = func(task, *args, **kwargs)
        except Exception as e:
            logger.error(
                f"Retriying {task.request.id} after {exponential_backoff} seconds"
            )
            raise task.retry(countdown=exponential_backoff, exc=e, max_retries=5)

        return result

    return wrapper


@retry_task
@shared_task(bind=True, rate_limit="1/s")
def update_blocks(self):
    logger.info("Running update blocks.")
    block_ids = BlockchainEthService.update_blocks()

    # NOTE: internal transactions aren't transactions per se.
    # We need to change the approach :(
    # app.send_task(
    #     BlockchainEthService.get_update_internal_transactions_name(),
    #     kwargs={"block_ids": block_ids},
    # )

    # after create the new block would update the transactions
    app.send_task(
        BlockchainEthService.get_update_normal_transactions_name(),
        kwargs={"block_ids": block_ids},
    )


@retry_task
@shared_task(bind=True, rate_limit="1/s")
def update_internal_transactions(self, block_ids: list):
    logger.info("Running update INTERNAL transactions.")
    BlockchainEthService.update_internal_transactions(block_ids=block_ids)


@retry_task
@shared_task(bind=True, rate_limit="1/s")
def update_normal_transactions(self, block_ids: list):
    logger.info("Running update NORMAL transactions.")
    BlockchainEthService.update_normal_transactions(block_ids=block_ids)
