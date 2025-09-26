import uuid
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.reaction import Reaction, ReactionKind
from app.schemas.reaction import ReactionSet


class ReactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, reaction_id: uuid.UUID) -> Optional[Reaction]:
        return self.db.scalar(select(Reaction).where(Reaction.id == reaction_id))

    def get_for_user_post(self, user_id: uuid.UUID, post_id: uuid.UUID) -> Optional[Reaction]:
        return self.db.scalar(
            select(Reaction).where(Reaction.user_id == user_id, Reaction.post_id == post_id)
        )

    def set_reaction(self, user_id: uuid.UUID, reaction_in: ReactionSet) -> Reaction:
        existing = self.get_for_user_post(user_id, reaction_in.post_id)
        if existing:
            existing.kind = reaction_in.kind
            self.db.commit()
            self.db.refresh(existing)
            return existing

        db_obj = Reaction(
            post_id=reaction_in.post_id,
            user_id=user_id,
            kind=reaction_in.kind,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def remove_reaction(self, user_id: uuid.UUID, post_id: uuid.UUID) -> Optional[Reaction]:
        existing = self.get_for_user_post(user_id, post_id)
        if not existing:
            return None
        self.db.delete(existing)
        self.db.commit()
        return existing

    def list_for_post(self, post_id: uuid.UUID, kind: Optional[ReactionKind] = None) -> List[Reaction]:
        stmt = select(Reaction).where(Reaction.post_id == post_id)
        if kind is not None:
            stmt = stmt.where(Reaction.kind == kind)
        return self.db.scalars(stmt).all()

    def count_for_post(self, post_id: uuid.UUID, kind: Optional[ReactionKind] = None) -> int:
        stmt = select(func.count()).select_from(Reaction).where(Reaction.post_id == post_id)
        if kind is not None:
            stmt = stmt.where(Reaction.kind == kind)
        return self.db.scalar(stmt) or 0
