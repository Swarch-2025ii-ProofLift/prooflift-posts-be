import enum
import uuid
import strawberry
from datetime import datetime
from typing import Optional

from app.models.reaction import ReactionType

@strawberry.type
class ReactionObjectType:
    id: uuid.UUID
    post_id: uuid.UUID
    user_id: uuid.UUID
    type: ReactionType

    created_at: datetime
    updated_at: Optional[datetime]
