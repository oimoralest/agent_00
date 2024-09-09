"""
Defines commands to run CRUD operations against project
"""

from types import SimpleNamespace
from typing import Annotated, List, Union

import typer
from rich import print
from rich.table import Table

from models.project import Project
from repositories.project import ProjectRepository
from utils.logger import LOGGER
from utils.mongodb_client import Mongo
from utils.enum import CLI

app = typer.Typer()


def print_project(projects: Union[Project, List[Project]]) -> None:
    """
    Print project as a Table

    Args:
        - project: Project data
    """
    table = Table(title="Projects")
    table.add_column("id")
    table.add_column("name")
    table.add_column("description")
    table.add_column("agents")

    if isinstance(projects, Project):
        projects = [projects]

    for project in projects:
        table.add_row(
            str(project.id), project.name, project.description, str(project.agents)
        )
    print(table)


@app.command()
def create(
    name: Annotated[str, typer.Option(prompt=True)],
    description: Annotated[str, typer.Option(prompt=True)] = "Project description",
) -> None:
    """
    Creates a project

    args:
        - name: Name of the project
        - description (optional): Description of the projection
    """
    LOGGER.info("Creating project...")

    project = Project(name=name, description=description)
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)
        project_repository: ProjectRepository = ProjectRepository(context)
        project: Project = Project(name=name, description=description)

        project_repository.create(project)

    print_project(project)


@app.command()
def read(id: Annotated[str, typer.Option(prompt=True)]) -> None:
    """
    Gets a project

    args:
        - id: Identifier of the project
    """
    LOGGER.info("Getting project...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)
        project_repository: ProjectRepository = ProjectRepository(context)
        project: Union[Project, None] = project_repository.get(id)
        if not project:
            LOGGER.info("Project not found")
            return

    print_project(project)


@app.command()
def read_all() -> None:
    """
    Gets all projects
    """
    LOGGER.info("Getting all projects...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)
        project_repository: ProjectRepository = ProjectRepository(context)
        projects: list[Project] = project_repository.get_all()

    if not projects:
        LOGGER.info("No projects found")
        return

    print_project(projects)


@app.command()
def update(
    id: Annotated[str, typer.Option(prompt=True)],
    field: Annotated[str, typer.Option(prompt=True)],
    value: Annotated[str, typer.Option(prompt=True)],
    type: Annotated[CLI.SupportedTypes, typer.Option(prompt=True, show_choices=True)],
) -> None:
    """
    Updates a field in a project document

    args:
        - id: Project identifier
        - field: Name of the field to update
        - value: Value of the field to update
        - type: Type of the value
    """
    LOGGER.info(f"Updating field {field} with value {value}")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)
        project_repository: ProjectRepository = ProjectRepository(context)
        if not project_repository.update(
            id, {"$set": {field: CLI.SupportedTypes.cast(value, type)}}
        ):
            LOGGER.info("Project not found")
            return

        project: Project = project_repository.get(id)
        print_project(project)


@app.command()
def delete(id: Annotated[str, typer.Option(prompt=True)]) -> None:
    """
    Deletes a project

    args:
        - id: Identifier of the project
    """
    LOGGER.info("Deleting project...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)
        project_repository: ProjectRepository = ProjectRepository(context)
        if not project_repository.delete(id):
            LOGGER.info("Project not found")
            return
