"""
Defines Node routes
"""

from http import HTTPStatus
from fastapi import APIRouter

from api.v1.routes.node.create import handler as create_handler


router = APIRouter()

router.add_api_route(
    "/node/input",
    create_handler,
    methods=["POST"],
    status_code=HTTPStatus.CREATED,
    response_model_by_alias=False,
)
router.add_api_route(
    "/node/llm",
    create_handler,
    methods=["POST"],
    status_code=HTTPStatus.CREATED,
    response_model_by_alias=False,
)
