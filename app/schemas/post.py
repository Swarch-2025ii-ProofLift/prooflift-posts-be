import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class PostBase(BaseModel):
    body: str = Field(...)
    exercise_ids: Optional[List[uuid.UUID]] = Field(default=[])

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    body: Optional[str] = Field(None)
    exercise_ids: Optional[List[uuid.UUID]] = None

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
