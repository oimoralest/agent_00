"""
Defines commands to run CRUD operations against prompt nodes
"""

from types import SimpleNamespace
from typing import Annotated, List, Union

from rich import print
from rich.table import Table
import typer

from models.node.prompt import PromptNode
from repositories.node import NodeRepository
from models.node.main import NodeType, Output
from utils.enum import CLI
from utils.logger import LOGGER
from utils.mongodb_client import Mongo

app = typer.Typer()


def print_nodes(nodes: Union[List[PromptNode], PromptNode]) -> None:
    """
    Print nodes as a table

    args:
        - nodes: Node data
    """
    table = Table(title="Nodes")
    table.add_column("id")
    table.add_column("name")
    table.add_column("description")
    table.add_column("start")
    table.add_column("end")
    table.add_column("target_id")
    table.add_column("agent_id")
    table.add_column("prompt")
    table.add_column("version")
    table.add_column("inputs")
    table.add_column("output")

    if isinstance(nodes, PromptNode):
        nodes = [nodes]

    for nodes in nodes:
        table.add_row(
            str(nodes.id),
            nodes.name,
            nodes.description,
            str(nodes.start),
            str(nodes.end),
            str(nodes.target_id),
            nodes.agent_id,
            nodes.prompt,
            nodes.version,
            str(nodes.inputs),
            str(nodes.output),
        )

    print(table)


@app.command()
def create(
    name: Annotated[str, typer.Option(prompt=True)],
    agent_id: Annotated[str, typer.Option(prompt=True)],
    prompt: Annotated[str, typer.Option(prompt=True)],
    version: Annotated[str, typer.Option(prompt=True)],
    output_name: Annotated[str, typer.Option(prompt=True)],
    output_type: Annotated[Output.Type, typer.Option(prompt=True, show_choices=True)],
    inputs: Annotated[
        str,
        typer.Option(
            prompt=True,
        ),
    ] = "",
    description: Annotated[str, typer.Option(prompt=True)] = "Prompt description",
    start: Annotated[bool, typer.Option(prompt=True)] = False,
    end: Annotated[bool, typer.Option(prompt=True)] = False,
    target_id: Annotated[str, typer.Option(prompt=True)] = "",
) -> None:
    """
    Creates a prompt node

    args:
        - name: Name of the node
        - agent_id: Agent id
        - prompt: Prompt for the node
        - version: Version of the prompt
        - output_name: Name of the output
        - output_type: Type of the output
        - description (optional): Description of the node
        - start (optional): Whether the node is a start node
        - end (optional): Whether the node is an end node
        - target_id (optional): Target node id
    """
    LOGGER.info("Creating prompt node...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)

        node_repository: NodeRepository = NodeRepository(context)
        prompt_node = PromptNode(
            type=NodeType.prompt,
            name=name,
            description=description,
            start=start,
            end=end,
            target_id=target_id,
            agent_id=agent_id,
            prompt=prompt,
            version=version,
            output=Output(name=output_name, type=output_type),
            inputs=inputs.split(",") if inputs else [],
        )
        if not node_repository.create(prompt_node):
            LOGGER.warning("Prompt node not created")
            return

        print_nodes(prompt_node)


@app.command()
def read(id: Annotated[str, typer.Option(prompt=True)]) -> None:
    """
    Gets a prompt node

    args:
        - id: Identifier of the node
    """
    LOGGER.info("Getting prompt node...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)
        node_repository: NodeRepository = NodeRepository(context)
        prompt_node: Union[PromptNode, None] = node_repository.get(id)
        if not prompt_node:
            LOGGER.warning("Prompt node not found")
            return

        print_nodes(prompt_node)


@app.command()
def update(
    id: Annotated[str, typer.Option(prompt=True)],
    field: Annotated[str, typer.Option(prompt=True)],
    value: Annotated[str, typer.Option(prompt=True)],
    type: Annotated[CLI.SupportedTypes, typer.Option(prompt=True, show_choices=True)],
) -> None:
    """
    Updates a prompt node

    args:
        - id: Identifier of the node
        - field: Field to update
        - value: New value for the field
        - type: Type of the field
    """
    LOGGER.info("Updating prompt node...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)

        node_repository: NodeRepository = NodeRepository(context)
        if not node_repository.update(
            node_id=id,
            update={"$set": {field: CLI.SupportedTypes.cast(value, type)}},
        ):
            LOGGER.warning("Prompt node not updated")
            return

        prompt_node: Union[PromptNode, None] = node_repository.get(id)
        if not prompt_node:
            LOGGER.warning("Prompt node not found")
            return

        print_nodes(prompt_node)
