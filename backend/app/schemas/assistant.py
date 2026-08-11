"""Skema Business Assistant (API Contract bab 18)."""
from typing import Literal

from pydantic import BaseModel, Field


class AssistantHistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class AssistantChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    conversation_id: int | None = None
    history: list[AssistantHistoryMessage] = Field(default_factory=list, max_length=50)
