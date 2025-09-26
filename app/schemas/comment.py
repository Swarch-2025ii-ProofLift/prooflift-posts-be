import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class CommentBase(BaseModel):
    body: str = Field(...)


class CommentCreate(CommentBase):
    post_id: uuid.UUID


class CommentUpdate(BaseModel):
    body: Optional[str] = Field(None)
