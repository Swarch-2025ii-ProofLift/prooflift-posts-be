import uuid
from pydantic import BaseModel, Field

from app.models.reaction import ReactionType


class ReactionBase(BaseModel):
    type: ReactionType = Field(...)


class ReactionSet(ReactionBase):
    post_id: uuid.UUID
