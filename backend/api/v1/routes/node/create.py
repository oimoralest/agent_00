"""
Defines lambda to create a node
"""

from http import HTTPStatus
from types import SimpleNamespace
from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException

from models.node.main import BaseNode
from repositories.node import NodeRepository
from utils.context import inject_context


def handler(
    node: BaseNode, context: Annotated[SimpleNamespace, Depends(inject_context)]
) -> BaseNode:
    """
    Lambda for node creation

    Args:
        - event: request data
        - context: request context with injected dependencies
    """
    node_repository: NodeRepository = NodeRepository(context)
    if not node_repository.create(node):
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to create node",
        )

    return node
