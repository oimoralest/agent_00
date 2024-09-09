"""
Deines the Input Node model
"""

from typing import Any


from models.node.main import BaseNode, Output


class InputNode(BaseNode):
    """
    Represents an Input Node

    Attributes:
        - output: Output of the Input Node. See Output model.
        - value: Value of the Input Node
    """

    output: Output
    value: str

    def action(self, state: Any) -> Any:
        """
        Action to be executed by the node
        """
        print(f"Executing Input Node: {self.id}")
        print(f"State: {state}")

        return {self.output.name: self.value}
