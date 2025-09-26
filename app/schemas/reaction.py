import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from app.models.reaction import ReactionKind


class ReactionBase(BaseModel):
    kind: ReactionKind = Field(...)


class ReactionSet(ReactionBase):
    post_id: uuid.UUID


class ReactionResponse(ReactionBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    post_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
