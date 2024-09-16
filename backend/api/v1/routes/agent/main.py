"""
Defines Agent routes
"""

from http import HTTPStatus
from fastapi import APIRouter

from api.v1.routes.agent.create import handler as create_handler
from api.v1.routes.agent.get import handler as get_handler
from api.v1.routes.agent.run import handler as run_handler

router = APIRouter()

router.add_api_route(
    "/agent",
    create_handler,
    methods=["POST"],
    status_code=HTTPStatus.CREATED,
    response_model_by_alias=False,
)
router.add_api_route(
    "/agent",
    get_handler,
    methods=["GET"],
    status_code=HTTPStatus.OK,
    response_model_by_alias=False,
)
router.add_api_route(
    "/agent/run",
    run_handler,
    methods=["POST"],
    status_code=HTTPStatus.CREATED,
    response_model_by_alias=False,
)
