import uuid
import strawberry
from datetime import datetime
from typing import Optional

from app.models.reaction import ReactionKind as ReactionKindModel


@strawberry.type
class ReactionType:
    id: uuid.UUID
    post_id: uuid.UUID
    user_id: uuid.UUID
    kind: ReactionKindModel

    created_at: datetime
    updated_at: Optional[datetime]
