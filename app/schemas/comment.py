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


class CommentResponse(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    post_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
