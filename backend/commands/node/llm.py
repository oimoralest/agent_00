"""
Defines commands to run CRUD operations against llm nodes
"""

from types import SimpleNamespace
from typing import Annotated, List, Union

from rich import print
from rich.table import Table
import typer

from constants.model_providers import LLMModel
from models.node.main import Output, NodeType
from models.node.llm import LLMModelSettings, LLMNode
from repositories.node import NodeRepository
from utils.enum import CLI
from utils.logger import LOGGER
from utils.mongodb_client import Mongo


app = typer.Typer()


def print_nodes(nodes: Union[LLMNode, List[LLMNode]]) -> None:
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
    table.add_column("model")
    table.add_column("input")

    nodes = [nodes] if isinstance(nodes, LLMNode) else nodes
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
            str(node.model),
            node.input,
        )

    print(table)


@app.command()
def create(
    name: Annotated[str, typer.Option(prompt=True)],
    output_name: Annotated[str, typer.Option(prompt=True)],
    output_type: Annotated[Output.Type, typer.Option(prompt=True, show_choices=True)],
    agent_id: Annotated[str, typer.Option(prompt=True)],
    llm_model: Annotated[LLMModel, typer.Option(prompt=True, show_choices=True)],
    input: Annotated[str, typer.Option(prompt=True)] = "",
    temperature: Annotated[float, typer.Option(prompt=True)] = 0.1,
    description: Annotated[str, typer.Option(prompt=True)] = "LLM node description",
    start: Annotated[bool, typer.Option(prompt=True)] = False,
    end: Annotated[bool, typer.Option(prompt=True)] = False,
    target_id: Annotated[str, typer.Option(prompt=True)] = "",
) -> None:
    """
    Creates a llm node

    args:
        - name: Name of the llm node
        - output_name: Name of the output
        - output_type: Type of the output
        - agent_id: Agent id
        - llm_model: LLM model name
        - prompt_id: Prompt id
        - temperature (optional): Temperature for the model
        - description (optional): Description of the llm node
        - start (optional): Whether the llm node is a start node
        - end (optional): Whether the llm node is an end node
        - target_id (optional): Target id
    """
    LOGGER.info("Creating llm node")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)

        node_repository: NodeRepository = NodeRepository(context)
        llm_node = LLMNode(
            type=NodeType.llm,
            name=name,
            description=description,
            start=start,
            end=end,
            target_id=target_id,
            agent_id=agent_id,
            output=Output(name=output_name, type=output_type),
            model=LLMModelSettings(name=llm_model, temperature=temperature),
            input=input,
        )
        if not node_repository.create(llm_node):
            LOGGER.warning("LLM node not created")
            return

        print_nodes(llm_node)


@app.command()
def read(id: Annotated[str, typer.Option(prompt=True)]) -> None:
    """
    Gets a llm node

    args:
        - id: Identifier of the llm node
    """
    LOGGER.info("Getting llm node...")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)
        node_repository: NodeRepository = NodeRepository(context)
        llm_node: Union[LLMNode, None] = node_repository.get(id)
        if not llm_node:
            LOGGER.warning("LLM node not found")
            return

        print_nodes(llm_node)


@app.command()
def update(
    id: Annotated[str, typer.Option(prompt=True)],
    field: Annotated[str, typer.Option(prompt=True)],
    value: Annotated[str, typer.Option(prompt=True)],
    type: Annotated[CLI.SupportedTypes, typer.Option(prompt=True, show_choices=True)],
) -> None:
    """
    Updates a llm node

    args:
        - id: Identifier of the llm node
        - field: Field to update
        - value: Value to update
        - type: Type of the value
    """
    LOGGER.info(f"Updating field {field} with value {value}")
    with Mongo() as client:
        context: SimpleNamespace = SimpleNamespace(mongodb_client=client, logger=LOGGER)
        node_repository: NodeRepository = NodeRepository(context)
        if not node_repository.update(
            node_id=id, update={"$set": {field: CLI.SupportedTypes.cast(value, type)}}
        ):
            LOGGER.warning("LLM node not updated")
            return

        llm_node: Union[LLMNode, None] = node_repository.get(id)
        if not llm_node:
            LOGGER.warning("LLM node not found")
            return

        print_nodes(llm_node)
