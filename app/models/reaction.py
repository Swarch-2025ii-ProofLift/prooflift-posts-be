import enum
import uuid
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, ForeignKey, Enum, UniqueConstraint

from app.db.session import Base


class ReactionType(str, enum.Enum):
    LIKE = "LIKE"
    LOVE = "LOVE"
    CLAP = "CLAP"
    FIRE = "FIRE"


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    type = Column(Enum(ReactionType, name="reaction_type"), nullable=False)

    __table_args__ = (
        UniqueConstraint("post_id", "user_id", name="uq_reactions_post_user"),
    )
