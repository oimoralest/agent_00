"""
Defines llm node model
"""

from typing import Any, Optional

from langchain.chat_models import init_chat_model
from pydantic import BaseModel

from constants.model_providers import model_provider
from models.node.main import BaseNode, Output


class LLMModelSettings(BaseModel):
    """
    Represents a LLM Model and settings

    Attributes:
        - name: Name of the model
        - temperature: Temperature for the model
    """

    name: str
    temperature: float


class LLMNode(BaseNode):
    """
    Represents a LLM Node

    Attributes:
        - model: LLMModel. See LLMModel model.
        - inputs: List of inputs to the LLM
        - output: Output of the LLM. See Output model.
    """

    model: LLMModelSettings
    output: Output  # TODO: Add validation for output name
    input: Optional[str] = None

    # TODO: Add support for tool calls

    def action(self, state: Any) -> Any:
        """
        Action to be executed by the node
        """
        print(f"Executing LLM Node: {self.id}")
        print(f"State: {state}")

        model_config = model_provider.get(self.model.name)
        llm = init_chat_model(
            model=self.model.name,
            model_provider=model_config.get("name"),
            temperature=self.model.temperature,
            api_key=model_config.get("api_key"),
        )

        response = llm.invoke(state.get(self.input))

        print(f"Response: {response}")

        return {self.output.name: response.content}
