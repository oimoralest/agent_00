"""
Defines repository for Project collection
"""

from types import SimpleNamespace
from typing import Dict, List, Union

from bson import ObjectId
from pymongo.collection import Collection

from models.agent import Agent
from models.project import Project
from utils.enum import Mongo as MongoEnum


class ProjectRepository:
    """
    Repository for Project collection
    """

    def __init__(self, context: SimpleNamespace):
        self.__context: SimpleNamespace = context

        self.__collection: Collection = self.__context.mongodb_client[
            MongoEnum.Database.AGENT_00
        ][MongoEnum.Collection.PROJECTS]

        self.__collection.create_index("name", unique=True)

    def create(self, project: Project) -> bool:
        """
        Create a new project in DB

        Args:
            - project: Project data
        """
        self.__context.logger.info("Creating a new project...")

        result = self.__collection.insert_one(
            project.dict(by_alias=True, exclude={"id"})
        )
        project.id = result.inserted_id
        if not project.id:
            self.__context.logger.warning("Project not created")
            return False

        self.__context.logger.info("Project created")

        return True

    def get(self, project_id: str) -> Union[Project, None]:
        """
        Get a project by ID

        Args:
            - project_id: Project ID
        """
        self.__context.logger.info(f"Getting project with ID: {project_id}...")
        # Avoid circular imports
        from repositories.agent import AgentRepository

        project = self.__collection.find_one(
            {"_id": ObjectId(project_id)},
            projection={"agents": 0},
        )
        if not project:
            self.__context.logger.warning("Project not found")
            return None

        agent_repository: AgentRepository = AgentRepository(self.__context)
        agents: List[Agent] = agent_repository.get_all({"project_id": project_id})
        project["agents"] = agents

        return Project(**project)

    def get_all(self) -> Union[List[Project], None]:
        """
        Get all projects

        Args:
            - query: Query to filter projects
        """
        self.__context.logger.info("Getting all projects...")
        # Avoid circular imports
        from repositories.agent import AgentRepository

        raw_projects = self.__collection.find()
        if not raw_projects:
            self.__context.logger.warning("Projects not found")
            return []

        projects: List[Project] = []
        agent_repository: AgentRepository = AgentRepository(self.__context)
        for project in raw_projects:
            agents: List[Agent] = agent_repository.get_all(
                {"project_id": str(project["_id"])}
            )
            project["agents"] = agents
            projects.append(Project(**project))

        return projects

    def update(self, id: str, query: Dict) -> bool:
        """
        Update a project

        Args:
            - id: Project ID
            - query: Query to update project
        """
        self.__context.logger.info("Updating project...")

        result = self.__collection.update_one({"_id": ObjectId(id)}, query)
        if result.modified_count == 0:
            self.__context.logger.warning("Project not updated")
            return False

        self.__context.logger.info("Project updated")

        return True

    def delete(self, id: str) -> bool:
        """
        Delete a project

        Args:
            - id: Project ID
        """
        self.__context.logger.info("Deleting project...")

        result = self.__collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            self.__context.logger.warning("Project not deleted")
            return False

        self.__context.logger.info("Project deleted")

        return True
