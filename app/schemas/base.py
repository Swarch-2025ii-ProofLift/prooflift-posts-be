"""
Pydantic/Strawberry schemas for data validation and typing.
"""

from pydantic import BaseModel

class BaseSchema(BaseModel):
    """Common attributes for all schemas."""
    id: str
