from pydantic import BaseModel, Field
from typing import List, Optional, Union, Any, Dict
import json

class Message(BaseModel):
    level: str
    content: str

class Chatsummary(BaseModel):
    details: str
    messages: List[Message] = Field(default_factory=list)

