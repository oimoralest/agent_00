"""
Defines repository for Node collection
"""

from types import SimpleNamespace
from typing import List, Union
import os

from bson import ObjectId
from pymongo import ASCENDING
from pymongo.collection import Collection

from models.node.input import InputNode
from models.node.main import BaseNode, NodeType
from models.node.llm import LLMNode
from models.node.prompt import PromptNode

NODES_MAP = {
    NodeType.input: InputNode,
    NodeType.llm: LLMNode,
    NodeType.prompt: PromptNode,
}


class NodeRepository:
    """
    Repository for Node collection
    """

    def __init__(self, context: SimpleNamespace) -> None:
        self.__context: SimpleNamespace = context
        self.__collection: Collection = self.__context.mongodb_client[
            os.getenv("MONGODB_DATABASE")
        ]["nodes"]

        self.__collection.create_index(
            [("name", ASCENDING), ("agent_id", ASCENDING)], unique=True
        )

    def create(self, node: BaseNode) -> bool:
        """
        Create a new node in DB

        Args:
            - node: Node data
        """
        self.__context.logger.info("Creating a new node...")
        # Avoid circular import
        from repositories.agent import AgentRepository

        agent_repository = AgentRepository(self.__context)
        agent = agent_repository.get(node.agent_id)
        if not agent:
            return False

        result = self.__collection.insert_one(
            node.dict(by_alias=True, exclude={"id"}),
        )
        node.id = result.inserted_id
        if not node.id:
            self.__context.logger.warning("Node not created")
            return False

        if not agent_repository.update(
            node.agent_id, {"$push": {"nodes": str(node.id)}}
        ):
            return False

        self.__context.logger.info("Node created")

        return True

    def get(self, node_id: str) -> Union[BaseNode, None]:
        """
        Get a node by ID

        Args:
            - node_id: Node ID
        """
        self.__context.logger.info(f"Getting node with ID: {node_id}...")

        node = self.__collection.find_one(
            {"_id": ObjectId(node_id)},
        )
        if not node:
            self.__context.logger.warning("Node not found")
            return None

        self.__context.logger.info("Node found")

        return NODES_MAP.get(node.get("type"), {})(**node)

    def get_all(self, query: dict, project: Union[dict, None] = None) -> List[BaseNode]:
        """
        Get all nodes

        Args:
            - query: filter query
            - project: projection query
        """
        self.__context.logger.info("Getting all nodes...")
        self.__context.logger.info(f"Query: {query}")

        nodes = list(self.__collection.find(query, project))
        if not nodes:
            self.__context.logger.warning("Nodes not found")
            return []

        return [NODES_MAP.get(node.get("type"), {})(**node) for node in nodes]

    def update(self, node_id: str, update: dict) -> bool:
        """
        Update a node by ID

        Args:
            - node_id: Node ID
            - update: Update query
        """
        self.__context.logger.info(f"Updating node with ID: {node_id}...")

        result = self.__collection.update_one(
            {"_id": ObjectId(node_id)},
            update,
        )
        if not result.modified_count:
            self.__context.logger.warning("Node not updated")
            return False

        self.__context.logger.info("Node updated")

        return True
