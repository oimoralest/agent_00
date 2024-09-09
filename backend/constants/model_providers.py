"""
Defines mapper for llm providers
"""

from enum import Enum
import os

from dotenv import load_dotenv
from typing import Dict

load_dotenv()


class LLMModel(str, Enum):
    """
    Enum for Model Types
    """

    GPT_4O = "gpt-4o"


# TODO: Is there a better way to load the model config?
model_provider: Dict = {
    # OPENAI
    LLMModel.GPT_4O: {
        "name": "openai",
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
}
