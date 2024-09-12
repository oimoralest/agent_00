"""
Defines Project routes
"""

from http import HTTPStatus
from fastapi import APIRouter
from api.v1.routes.project.create import handler as create_handler
from api.v1.routes.project.get import handler as get_handler

router = APIRouter()

router.add_api_route(
    "/project",
    create_handler,
    methods=["POST"],
    status_code=HTTPStatus.CREATED,
    response_model_by_alias=False,
)
router.add_api_route(
    "/project",
    get_handler,
    methods=["GET"],
    status_code=HTTPStatus.OK,
    response_model_by_alias=False,
)
