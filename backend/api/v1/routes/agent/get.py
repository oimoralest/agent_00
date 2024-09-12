"""
Defines lambda to get an agent
"""

from http import HTTPStatus
from types import SimpleNamespace
from typing import Annotated, Union

from fastapi import Depends
from fastapi.exceptions import HTTPException

from repositories.agent import AgentRepository
from models.agent import Agent
from repositories.node import NodeRepository
from utils.context import inject_context


def handler(
    id: str, context: Annotated[SimpleNamespace, Depends(inject_context)]
) -> Agent:
    """
    Lambda handler for GET /agents?id={id}

    Args:
        - event: Lambda event
        - context: Lambda context
    """
    context.logger.info("Getting agents...")
    agent_repository: AgentRepository = AgentRepository(context)
    agent: Union[Agent, None] = agent_repository.get(id)
    if not agent:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Agent not found",
        )

    node_repository: NodeRepository = NodeRepository(context)
    agent.nodes = node_repository.get_all({"agent_id": id})
    print(f"agent.nodes: {agent.nodes}")

    return agent
