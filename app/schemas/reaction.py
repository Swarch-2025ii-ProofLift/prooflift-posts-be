import uuid
from pydantic import BaseModel, Field

from app.models.reaction import ReactionKind


class ReactionBase(BaseModel):
    kind: ReactionKind = Field(...)


class ReactionSet(ReactionBase):
    post_id: uuid.UUID
