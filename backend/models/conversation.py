from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel, Field


class ConversationMessage(BaseModel):
    role: str
    message: str
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class Conversation(BaseModel):
    student_id: str
    messages: List[ConversationMessage] = Field(
        default_factory=list
    )