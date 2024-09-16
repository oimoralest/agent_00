"""
Defines lambda to create an agent
"""

from http import HTTPStatus
from typing import Annotated

from types import SimpleNamespace

from fastapi import Depends
from fastapi.exceptions import HTTPException

from models.agent import Agent
from repositories.agent import AgentRepository
from repositories.project import ProjectRepository
from utils.context import inject_context


def handler(
    agent: Agent, context: Annotated[SimpleNamespace, Depends(inject_context)]
) -> Agent:
    """
    Lambda for agent creation

    Args:
        - event: request data
        - context: request context with injected dependencies
    """
    # TODO: Validate if project_id exists
    agent_repository: AgentRepository = AgentRepository(context)
    if not agent_repository.create(agent):
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to create agent",
        )

    # Update project with new agent
    project_repository: ProjectRepository = ProjectRepository(context)
    if not project_repository.update(
        agent.project_id, {"$push": {"agents": str(agent.id)}}
    ):
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to update project",
        )

    return agent
