import uuid
import strawberry
from datetime import datetime
from typing import List, Optional

@strawberry.type
class PostType:
    id: uuid.UUID
    user_id: uuid.UUID
    body: str
    exercise_ids: List[uuid.UUID]

    created_at: datetime
    updated_at: Optional[datetime]
