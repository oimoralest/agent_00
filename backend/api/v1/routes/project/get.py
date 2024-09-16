"""
Defines lambda handler for GET /projects?id={id}
"""

from http import HTTPStatus
from types import SimpleNamespace
from typing import Annotated, Union

from fastapi import Depends
from fastapi.exceptions import HTTPException

from repositories.agent import AgentRepository
from models.project import Project
from repositories.project import ProjectRepository
from utils.context import inject_context


def handler(
    id: str, context: Annotated[SimpleNamespace, Depends(inject_context)]
) -> Project:
    """
    Lambda handler for GET /projects?id={id}

    Args:
        - event: Lambda event
        - context: Lambda context
    """
    context.logger.info("Getting projects...")
    project_repository: ProjectRepository = ProjectRepository(context)
    project: Union[Project, None] = project_repository.get(id)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Project not found",
        )

    agent_repository: AgentRepository = AgentRepository(context)
    project.agents = agent_repository.get_all({"project_id": id})

    return project
