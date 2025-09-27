import uuid
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.reaction import Reaction, ReactionType
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
        db_obj = Reaction(
            post_id=reaction_in.post_id,
            user_id=user_id,
            type=reaction_in.type,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update_reaction(self, reaction: Reaction, type: ReactionType) -> Reaction:
        reaction.type = type
        self.db.commit()
        self.db.refresh(reaction)
        return reaction

    def remove_reaction(self, reaction: Reaction) -> Reaction:
        self.db.delete(reaction)
        self.db.commit()
        return reaction

    def list_for_post(self, post_id: uuid.UUID, type: Optional[ReactionType] = None) -> List[Reaction]:
        stmt = select(Reaction).where(Reaction.post_id == post_id)
        if type is not None:
            stmt = stmt.where(Reaction.type == type)
        return self.db.scalars(stmt).all()

    def count_for_post(self, post_id: uuid.UUID, type: Optional[ReactionType] = None) -> int:
        stmt = select(func.count()).select_from(Reaction).where(Reaction.post_id == post_id)
        if type is not None:
            stmt = stmt.where(Reaction.type == type)
        return self.db.scalar(stmt) or 0
