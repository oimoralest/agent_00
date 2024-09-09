"""
Defines enum for the app
"""

from enum import Enum
from json import loads
from typing import Any


class Mongo:
    """
    Enum for MongoDB
    """

    class Database(str, Enum):
        """
        Enum for Databases
        """

        AGENT_00 = "agent_00"

    class Collection(str, Enum):
        """
        Enum for Collections
        """

        PROJECTS = "projects"
        AGENTS = "agents"
        NODES = "nodes"


class CLI:
    """
    Enum for CLI tool
    """

    class SupportedTypes(str, Enum):
        """
        Enum for supported types to pass through CLI
        """

        string = "str"
        number = "int"
        json = "json"
        array = "list"

        @staticmethod
        def cast(value: Any, type: str) -> Any:
            """
            Casts a value to the supplied type
            """
            types_mapper = {
                CLI.SupportedTypes.string: str,
                CLI.SupportedTypes.number: int,
                CLI.SupportedTypes.json: loads,
                CLI.SupportedTypes.array: lambda x: x.split(","),
            }
            return types_mapper[type](value)
