from pydantic import BaseModel, Field
from typing import List

class Message(BaseModel):
    level: str
    content: str

class Chatsummary(BaseModel):
    details: str
    messages: List[Message] = Field(default_factory=list)


class InstructionOutput(BaseModel):
    """
    Structured response model for conversation handling.
    Used to store both the conversation summary and next prompt.
    """
    summary: str = Field(..., description="Brief summary of the last conversation turn.")
    next_prompt: str = Field(..., description="Prompt or message to continue or escalate the conversation.")
