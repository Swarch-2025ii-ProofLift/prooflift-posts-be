import uuid
import strawberry
from datetime import datetime
from typing import Optional


@strawberry.type
class CommentType:
    id: uuid.UUID
    post_id: uuid.UUID
    user_id: uuid.UUID
    body: str

    created_at: datetime
    updated_at: Optional[datetime]
