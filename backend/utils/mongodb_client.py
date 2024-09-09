"""
Creates a MongoDB client and database connection.
"""

from functools import wraps
from types import SimpleNamespace
from typing import Callable, Dict
import os

from pymongo import MongoClient
from rich import print

from utils.logger import LOGGER


def get_mongodb_client() -> MongoClient:
    """
    Returns a MongoDB client
    """
    return MongoClient(os.getenv("MONGODB_CLIENT_URI"))


def mongodb_client(func: Callable) -> Callable:
    """
    MongoDB client decorator

    Injects mongodb_client into the context
    """

    @wraps(func)
    def wrapper(event: Dict, context: SimpleNamespace) -> Dict:
        """
        Wrapper for func
        """
        context.logger.info("Injecting MongoDB client...")
        context.mongodb_client = MongoClient(os.getenv("MONGODB_CLIENT_URI"))
        context.logger.info(f"MongoDB is connected")

        response = func(event, context)

        context.logger.info("Closing MongoDB connection...")
        context.mongodb_client.close()

        return response

    return wrapper


class Mongo:
    """
    Context manager to handle mongo operations
    """

    def __init__(self) -> None:
        LOGGER.info("Connection to MongoDB")
        self.__client: MongoClient = get_mongodb_client()

    def __enter__(self):
        return self.__client

    def __exit__(self, exc_type, exc_val, exc_tb):
        LOGGER.info("Closing MongoDB connection")
        self.__client.close()

