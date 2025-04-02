from dataclasses import MISSING, dataclass, field
from typing import Annotated, Type, Union

from pydantic import BaseModel, Field, Discriminator
from pydantic_ai.messages import ModelRequest, ModelResponse


class Idea(BaseModel):
    subject: str
    context: str
    action: str
    style: str
    camera_motion: str
    composition: str
    ambiance: str


class Inceptions(BaseModel):
    ideas: list[Idea] = Field(..., description="A list of ideas")


class Scripts(BaseModel):
    production_ready: list[str] = Field(..., description="A list of scripts ready for production")


class StoryBoard(BaseModel):
    at_0_secs: str
    at_1_secs: str
    at_2_secs: str


class DirectorEdit(BaseModel):
    video: list[StoryBoard] = []


@dataclass
class POVGenState:
    user_prompt: str = ""
    inceptions: Inceptions | None = None

    inception_agent_messages: list[Annotated[Union[ModelRequest, ModelResponse], Discriminator("kind")]] = field(
        default_factory=list
    )
    writer_agent_messages: list[Annotated[Union[ModelRequest, ModelResponse], Discriminator("kind")]] = field(
        default_factory=list
    )
    director_agent_messages: list[Annotated[Union[ModelRequest, ModelResponse], Discriminator("kind")]] = field(
        default_factory=list
    )
