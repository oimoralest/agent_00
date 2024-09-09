"""
Defines repository for Agent collection
"""

from types import SimpleNamespace
from typing import Dict, Union

from bson.objectid import ObjectId
from pymongo import ASCENDING
from pymongo.collection import Collection

from models.agent import Agent
from models.project import Project
from utils.enum import Mongo as MongoEnum


class AgentRepository:
    """
    Repository for Agent collection
    """

    def __init__(self, context: SimpleNamespace):
        self.__context: SimpleNamespace = context

        self.__collection: Collection = self.__context.mongodb_client[
            MongoEnum.Database.AGENT_00
        ][MongoEnum.Collection.AGENTS]

        self.__collection.create_index(
            [("name", ASCENDING), ("project_id", ASCENDING)], unique=True
        )

    def create(self, agent: Agent) -> bool:
        """
        Creates a new Agent

        Args:
            - agent: Agent data
        """
        self.__context.logger.info("Creating a new agent...")
        # Avoid circular imports
        from repositories.project import ProjectRepository

        project_repository: ProjectRepository = ProjectRepository(self.__context)
        project: Union[Project, None] = project_repository.get(agent.project_id)
        if not project:
            return False

        result = self.__collection.insert_one(agent.dict(by_alias=True, exclude={"id"}))
        agent.id = result.inserted_id

        if not project_repository.update(
            agent.project_id, {"$push": {"agents": str(agent.id)}}
        ):
            return False

        self.__context.logger.info("Agent created")

        return result.inserted_id is not None

    def get(self, agent_id: str) -> Union[Agent, None]:
        """
        Gets an Agent by ID

        Args:
            - agent_id: Agent ID
        """
        self.__context.logger.info(f"Getting agent with ID: {agent_id}")
        # Avoid circular imports
        from repositories.node import NodeRepository

        agent_data = self.__collection.find_one({"_id": ObjectId(agent_id)})
        if not agent_data:
            self.__context.logger.warning("Agent not found")
            return None

        node_repository: NodeRepository = NodeRepository(self.__context)
        agent_data["nodes"] = node_repository.get_all({"agent_id": agent_id})

        return Agent(**agent_data)

    def get_all(self, query: Dict, project: Union[Dict, None] = None) -> list[Agent]:
        """
        Gets all Agents

        Args:
            - query: Query to filter Agents
        """
        self.__context.logger.info("Getting all agents...")
        self.__context.logger.info(f"Query: {query}")

        # Avoid circular imports
        from repositories.node import NodeRepository

        agents = list(self.__collection.find(query, project))

        node_repository: NodeRepository = NodeRepository(self.__context)
        for agent in agents:
            agent["nodes"] = node_repository.get_all({"agent_id": str(agent["_id"])})

        return [Agent(**agent) for agent in agents]

    def update(self, agent_id: str, query: Dict) -> bool:
        """
        Updates an Agent

        Args:
            - agent_id: Agent ID
            - query: Update query
        """
        self.__context.logger.info(f"Updating agent with ID: {agent_id}")
        result = self.__collection.update_one({"_id": ObjectId(agent_id)}, query)
        if result.modified_count == 0:
            self.__context.logger.warning("Agent not updated")
            return False

        return True

    def delete(self, id: str) -> bool:
        """
        Deletes an Agent

        Args:
            - id: Agent ID
        """
        self.__context.logger.info(f"Deleting agent with ID: {id}")
        result = self.__collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            self.__context.logger.warning("Agent not deleted")
            return False

        return True
