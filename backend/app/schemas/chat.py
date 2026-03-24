from typing import Dict, List, Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal['system', 'user', 'assistant']
    content: str = Field(min_length=1)


class PageContext(BaseModel):
    url: str = ''
    title: str = ''


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(default_factory=list)
    page_context: PageContext = Field(default_factory=PageContext)


class SourceItem(BaseModel):
    source_type: str
    source_id: str
    title: str


class ChatResponse(BaseModel):
    reply: str
    sources: List[SourceItem]
    meta: Dict[str, str]
