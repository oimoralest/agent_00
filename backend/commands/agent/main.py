"""
Defines commands to run CRUD operations against agents
"""

import tempfile
from types import SimpleNamespace
from typing import Annotated, List, Union

from PIL import Image
from rich import print
from rich.table import Table
import typer

from models.agent import Agent
from repositories.agent import AgentRepository
from utils.logger import LOGGER
from utils.mongodb_client import Mongo
from utils.enum import CLI

app = typer.Typer()


def print_agents(agents: Union[List[Agent], Agent]) -> None:
    """
    Print agent as a Table

    Args:
        - agent: Agent data
    """
    if not agents:
        print("Agent not found")
        return

    table = Table(title="Agent Found")
    table.add_column("id")
    table.add_column("name")
    table.add_column("description")
    table.add_column("project_id")
    table.add_column("nodes")
    if isinstance(agents, Agent):
        agents = [agents]

    for agent in agents:
        table.add_row(
            str(agent.id),
            agent.name,
            agent.description,
            agent.project_id,
            str(agent.nodes),
        )

    print(table)


@app.command()
def create(
    name: Annotated[str, typer.Option(prompt=True)],
    project_id: Annotated[str, typer.Option(prompt=True)],
    description: Annotated[str, typer.Option(prompt=True)] = "Agent description",
) -> None:
    """
    Creates an agent

    args:
        - name: Name of the agent
        - description (optional): Description of the agent
        - project_id: Identifier of the project
    """
    LOGGER.info("Creating agent...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)

        agent_repository: AgentRepository = AgentRepository(context)
        agent = Agent(name=name, project_id=project_id, description=description)
        if not agent_repository.create(agent):
            LOGGER.info("Agent not created")
            return

        print_agents(agent)


@app.command()
def read(id: Annotated[str, typer.Option(prompt=True)]) -> None:
    """
    Gets an agent

    args:
        - id: Identifier of the agent
    """
    LOGGER.info("Getting agent...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)
        agent_repository: AgentRepository = AgentRepository(context)
        agent: Union[Agent, None] = agent_repository.get(id)
        if not agent:
            LOGGER.info("Agent not found")
            return

        print_agents(agent)


@app.command()
def read_all(project_id: Annotated[str, typer.Option(prompt=True)]) -> None:
    """
    Gets all agents

    args:
        - project_id: Identifier of the project
    """
    LOGGER.info("Getting all agents...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)
        agent_repository: AgentRepository = AgentRepository(context)
        agents: List[Agent] = agent_repository.get_all({"project_id": project_id})
        if not agents:
            LOGGER.info("Agents not found")
            return

        print_agents(agents)


@app.command()
def update(
    id: Annotated[str, typer.Option(prompt=True)],
    field: Annotated[str, typer.Option(prompt=True)],
    value: Annotated[str, typer.Option(prompt=True)],
    type: Annotated[CLI.SupportedTypes, typer.Option(prompt=True, show_choices=True)],
) -> None:
    """
    Updates a field in an agent document

    args:
        - id: Agent identifier
        - field: Name of the field to update
        - value: Value of the field to update
        - type: Type of the value
    """
    LOGGER.info(f"Updating field {field} with value {value}")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)

        agent_repository: AgentRepository = AgentRepository(context)
        if not agent_repository.update(
            id, {"$set": {field: CLI.SupportedTypes.cast(value, type)}}
        ):
            LOGGER.info("Agent not updated")
            return

        agent: Agent = agent_repository.get(id)
        print_agents(agent)


@app.command()
def delete(id: Annotated[str, typer.Option(prompt=True)]) -> None:
    """
    Deletes an agent

    args:
        - id: Identifier of the agent
    """
    LOGGER.info("Deleting agent...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)

        agent_repository: AgentRepository = AgentRepository(context)
        if not agent_repository.delete(id):
            LOGGER.info("Agent not deleted")
            return

        LOGGER.info("Agent deleted")


@app.command()
def visualize(id: Annotated[str, typer.Option(prompt=True)]) -> None:
    """
    Visualizes an agent flow

    args:
        - id: Identifier of the agent
    """
    LOGGER.info("Visualizing agent flow...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)

        agent_repository: AgentRepository = AgentRepository(context)
        agent: Union[Agent, None] = agent_repository.get(agent_id=id)
        if not agent:
            LOGGER.info("Agent not found")
            return

        agent.build_flow()
        if not agent.graph and not agent.state:
            LOGGER.info("Flow not built")
            return

        LOGGER.info(f"State: {agent.state.__dict__}")
        with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
            tmp.write(agent.graph.get_graph().draw_mermaid_png())
            tmp.seek(0)
            img = Image.open(tmp.name)
            img.show()


@app.command()
def run(id: Annotated[str, typer.Option(prompt=True)]) -> None:
    """
    Runs an agent

    args:
        - id: Identifier of the agent
    """
    LOGGER.info("Running agent...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)

        agent_repository: AgentRepository = AgentRepository(context)
        agent: Union[Agent, None] = agent_repository.get(agent_id=id)
        if not agent:
            LOGGER.info("Agent not found")
            return

        agent.run()
