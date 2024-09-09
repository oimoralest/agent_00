"""
Defines model for Agent
"""

from typing import Dict, List, Optional, Tuple, TypedDict, Union

from langgraph.graph.state import StateGraph
from pydantic import BaseModel, Field, ConfigDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.graph import CompiledGraph

from models.node.input import InputNode
from models.node.llm import LLMNode
from models.node.prompt import PromptNode
from utils.logger import LOGGER
from constants.pyobjectid import PyObjectId


class Agent(BaseModel):
    """
    Represents an Agent
    """

    model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    description: Optional[str] = "Agent description"
    nodes: Optional[List[Union[LLMNode, InputNode, PromptNode]]] = Field(default=[])
    project_id: str

    state: Optional[TypedDict] = None
    memory: Optional[MemorySaver] = None
    graph: Optional[CompiledGraph] = None

    # TODO: Add support for messages history
    # TODO: Implement export to JSON
    def build_flow(self) -> Union[Tuple[CompiledGraph, TypedDict], None]:
        """
        Builds a LangGraph flow

        Args:
            - nodes: List of nodes
        """
        LOGGER.info(f"Building flow for Agent: {self.name}")
        LOGGER.info(f"Nodes: {self.nodes}")
        annotations: Dict = {}

        if not self.nodes:
            LOGGER.error("No nodes found")
            return

        for node in self.nodes:
            if node.output:
                annotations[node.output.name] = node.output.type

        LOGGER.info(f"Annotations: {annotations}")
        self.state = TypedDict("AgentState", annotations)
        graph: StateGraph = StateGraph(self.state)

        for node in self.nodes:
            LOGGER.info(f"Adding node: {node.name}")
            graph.add_node(str(node.id), node.action)
            if node.start:
                graph.set_entry_point(str(node.id))
            if node.end:
                graph.set_finish_point(str(node.id))
            if node.target_id:
                graph.add_edge(str(node.id), node.target_id)

        self.memory = MemorySaver()

        self.graph = graph.compile(checkpointer=self.memory)

    def run(self) -> Dict:
        """
        Runs the Agent
        """
        LOGGER.info(f"Running Agent: {self.name}")

        self.build_flow()

        initial_state = {key: "" for key in self.state.__annotations__}

        response = self.graph.invoke(
            initial_state, {"configurable": {"thread_id": str(self.id)}}
        )

        LOGGER.info(f"Agent response: {response}")

        return self.state
