"""
Defines model for Project
"""

from typing import Annotated, List, Optional

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

from models.agent import Agent
from constants.pyobjectid import PyObjectId


AgentList = Annotated[
    List[Agent],
    PlainSerializer(
        lambda agents: [str(agent.id) for agent in agents] if agents else [],
        return_type=List,
        when_used="json",
    ),
]


class Project(BaseModel):
    """
    Represents a Project
    """

    model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    description: str
    agents: Optional[List[Agent]] = Field(default=[])
