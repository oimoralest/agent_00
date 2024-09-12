from http import HTTPStatus
from json import dumps
from types import SimpleNamespace
from typing import Annotated, Dict, List, Union

from fastapi import Depends
from fastapi.exceptions import HTTPException

from models.node.main import BaseNode
from repositories.node import NodeRepository
from models.agent import Agent
from repositories.agent import AgentRepository

from utils.context import inject_context


def handler(
    id: str, context: Annotated[SimpleNamespace, Depends(inject_context)]
) -> Dict:
    """
    Lambda handler
    """
    # TODO: Validate if agent belongs to the project
    agent_repository: AgentRepository = AgentRepository(context=context)
    agent: Union[Agent, None] = agent_repository.get(id)
    if not agent:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Agent not found",
        )

    node_repository: NodeRepository = NodeRepository(context=context)
    nodes: Union[List[BaseNode], None] = node_repository.get_all(
        {"agent_id": str(agent.id)}
    )
    if not nodes:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="No nodes found for this agent",
        )

    agent.run(nodes)

    # TODO: What should be returned?
    return {
        "statusCode": 200,
        "body": dumps(
            agent.graph.get_state({"configurable": {"thread_id": str(agent.id)}})
        ),
    }
