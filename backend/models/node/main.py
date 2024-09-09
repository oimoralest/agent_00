"""
Defines model for Nodes
"""

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from pydantic import ConfigDict

from constants.pyobjectid import PyObjectId

# TODO: Add examples to call the model


class NodeType(str, Enum):
    """
    Enum for Node Types
    """

    llm = "llm"
    input = "input"
    conditional = "conditional"
    prompt = "prompt"


class BaseNode(BaseModel):
    """
    Represents a Base Node

    Attributes:
        - id: Identifier of the Node
        - type: Type of the Node
        - name: Name of the Node
        - description: Description of the Node
        - start: Indicates if the Node is a start Node
        - end: Indicates if the Node is an end Node
        - target_id: Identifier of the target Node
        - agent_id: Identifier of the Agent
        - output: Output of the Node. See Output model.
    """

    model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    type: Optional[str] = None
    name: str
    description: Optional[str] = "Node description"
    start: Optional[bool] = False
    end: Optional[bool] = False
    target_id: Optional[str] = None
    agent_id: str
    output: Optional["Output"] = None

    def action(self, state: Any) -> Any:
        """
        Action to be executed by the node
        """
        raise NotImplementedError


class Output(BaseModel):
    """
    Represents an Output from a Node

    Attributes:
        - name: Name of the Output
        - type: Type of the Output. E.g. str, int, float, json, etc. # TODO: Add validation for type
    """

    name: str
    type: str

    class Type(str, Enum):
        """
        Enum for Output Types
        """

        str = "str"
        int = "int"
        float = "float"
        json = "json"


class Condition(BaseModel):
    """
    Represents a Condition

    Attributes:
        - operator: Operator for the condition. # TODO: Add validation for operator
        - value: Value for the condition
    """

    operator: str
    value: str


class ConditionalNode(BaseNode):
    """
    Represents a Conditional Node

    Attributes:
        - input: Input for the Conditional Node
        - conditionals: List of conditions. See Condition model.
    """

    input: str
    conditionals: Dict[str, Condition]
