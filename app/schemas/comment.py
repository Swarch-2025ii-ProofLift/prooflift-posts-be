import uuid
from typing import Optional
from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    body: str = Field(...)


class CommentCreate(CommentBase):
    post_id: uuid.UUID


class CommentUpdate(BaseModel):
    body: Optional[str] = Field(None)
