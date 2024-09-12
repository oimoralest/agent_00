"""
Defines lambda handler to create a new project
"""

from http import HTTPStatus
from types import SimpleNamespace
from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException

from models.project import Project
from repositories.project import ProjectRepository
from utils.context import inject_context


def handler(
    project: Project, context: Annotated[SimpleNamespace, Depends(inject_context)]
) -> Project:
    """
    Lambda handler
    """
    # TODO: Inject context with dependency injection
    project_repository: ProjectRepository = ProjectRepository(context)
    if not project_repository.create(project):
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to create project",
        )

    return project
