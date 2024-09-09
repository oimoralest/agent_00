"""
Defines commands to run CRUD operations against input nodes
"""

from types import SimpleNamespace
from typing import Annotated, List, Union
from rich import print
from rich.table import Table
import typer

from models.node.main import NodeType, Output
from models.node.input import InputNode
from repositories.node import NodeRepository
from utils.enum import CLI
from utils.logger import LOGGER
from utils.mongodb_client import Mongo


app = typer.Typer()


def print_nodes(nodes: Union[InputNode, List[InputNode]]) -> None:
    """
    Print nodes as a Table

    Args:
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
    table.add_column("output")
    table.add_column("value")

    nodes = [nodes] if isinstance(nodes, InputNode) else nodes
    for node in nodes:
        table.add_row(
            str(node.id),
            node.name,
            node.description,
            str(node.start),
            str(node.end),
            str(node.target_id),
            node.agent_id,
            str(node.output),
            node.value,
        )

    print(table)


@app.command()
def create(
    name: Annotated[str, typer.Option(prompt=True)],
    output_name: Annotated[str, typer.Option(prompt=True)],
    output_type: Annotated[Output.Type, typer.Option(prompt=True, show_choices=True)],
    value: Annotated[str, typer.Option(prompt=True)],
    agent_id: Annotated[str, typer.Option(prompt=True)],
    description: Annotated[str, typer.Option(prompt=True)] = "Input node description",
    start: Annotated[bool, typer.Option(prompt=True)] = False,
    end: Annotated[bool, typer.Option(prompt=True)] = False,
    target_id: Annotated[str, typer.Option(prompt=True)] = "",
) -> None:
    """
    Creates an input node

    args:
        - name: Name of the input node
        - description (optional): Description of the input node
        - start (optional): Whether the input node is a start node
        - end (optional): Whether the input node is an end node
        - target_id (optional): Identifier of the target node
        - agent_id: Identifier of the agent
    """
    LOGGER.info("Creating input node...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)

        input_node = InputNode(
            type=NodeType.input,
            name=name,
            description=description,
            start=start,
            end=end,
            target_id=target_id,
            agent_id=agent_id,
            output=Output(name=output_name, type=output_type),
            value=value,
        )
        node_repository: NodeRepository = NodeRepository(context)
        if not node_repository.create(input_node):
            LOGGER.info("Input node not created")
            return

        print_nodes(input_node)


@app.command()
def read(id: Annotated[str, typer.Option(prompt=True)]) -> None:
    """
    Gets an input node

    args:
        - id: Identifier of the input node
    """
    LOGGER.info("Getting input node...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)
        node_repository: NodeRepository = NodeRepository(context)
        input_node: Union[InputNode, None] = node_repository.get(id)
        if not input_node:
            LOGGER.info("Input node not found")
            return

        print_nodes(input_node)


@app.command()
def read_all(agent_id: Annotated[str, typer.Option(prompt=True)]) -> None:
    """
    Gets all input nodes for an agent

    args:
        - agent_id: Identifier of the agent
    """
    LOGGER.info("Getting all input nodes...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)
        node_repository: NodeRepository = NodeRepository(context)
        input_nodes: List[InputNode] = node_repository.get_all({"agent_id": agent_id})
        if not input_nodes:
            LOGGER.info("Input nodes not found")
            return

        print_nodes(input_nodes)


@app.command()
def update(
    id: Annotated[str, typer.Option(prompt=True)],
    field: Annotated[str, typer.Option(prompt=True)],
    value: Annotated[str, typer.Option(prompt=True)],
    type: Annotated[CLI.SupportedTypes, typer.Option(prompt=True, show_choices=True)],
) -> None:
    """
    Updates an input node

    args:
        - id: Identifier of the input node
        - field: Field to update
        - value: New value
        - type: Type of the field
    """
    LOGGER.info("Updating input node...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)
        node_repository: NodeRepository = NodeRepository(context)

        if not node_repository.update(
            node_id=id, update={"$set": {field: CLI.SupportedTypes.cast(value, type)}}
        ):
            LOGGER.info("Input node not updated")
            return

        input_node: Union[InputNode, None] = node_repository.get(id)
        if not input_node:
            LOGGER.info("Input node not found")
            return

        print_nodes(input_node)
