"""
Defines context utility
"""

from types import SimpleNamespace

from utils.logger import LOGGER
from utils.mongodb_client import get_mongodb_client


async def inject_context() -> SimpleNamespace:
    """
    Inject the context to the handler
    """
    context: SimpleNamespace = SimpleNamespace()
    context.logger = LOGGER
    context.mongodb_client = get_mongodb_client()
    return context
