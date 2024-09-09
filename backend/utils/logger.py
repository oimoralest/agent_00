"""
Defines logger functionality for the application.
"""
from functools import wraps
import logging
from types import SimpleNamespace
from typing import Callable, Dict
import sys


logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def logger(func: Callable) -> Callable:
    """
    Logger decorator

    Injects logger into the context
    """
    @wraps(func)
    def wrapper(event: Dict, context: SimpleNamespace) -> Dict:
        """
        Wrapper for func
        """
        LOGGER.info("Injecting logger...")
        context.logger = LOGGER

        return func(event, context)

    return wrapper
