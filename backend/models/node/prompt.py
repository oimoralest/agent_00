"""
Defines prompt node model
"""

from typing import Any, List, Optional

from langchain_core.prompts import PromptTemplate

from models.node.main import BaseNode, Output


class PromptNode(BaseNode):
    """
    Represents a Prompt Node

    Attributes:
        - prompt: Prompt for the Node
        - version: Version of the prompt
        - inputs: List of inputs to the Node
    """

    prompt: str
    version: str
    inputs: Optional[List[str]] = []
    output: Output

    def action(self, state: Any) -> Any:
        """
        Action to be executed by the node
        """
        print(f"Executing Prompt Node: {self.id}")
        print(f"State: {state}")

        prompt: str = PromptTemplate.from_template(
            template=self.prompt,
        ).format(**{input: state[input] for input in self.inputs})

        return {self.output.name: prompt}
