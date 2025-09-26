import uuid
from typing import List, Optional
from pydantic import BaseModel, Field

class PostBase(BaseModel):
    body: str = Field(...)
    exercise_ids: Optional[List[uuid.UUID]] = Field(default=[])

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    body: Optional[str] = Field(None)
    exercise_ids: Optional[List[uuid.UUID]] = None
