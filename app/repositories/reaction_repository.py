import uuid
from typing import List, Optional, Dict
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
    
    def count_for_posts(self, post_ids: List[uuid.UUID], type: Optional[ReactionType] = None) -> dict[uuid.UUID, int]:
        if not post_ids:
            return {}
        
        stmt = (
            select(Reaction.post_id, func.count(Reaction.id))
            .where(Reaction.post_id.in_(post_ids))
        )
        if type:
            stmt = stmt.where(Reaction.type == type)

        stmt = stmt.group_by(Reaction.post_id)
        result = self.db.execute(stmt).all()

        counts = {post_id: 0 for post_id in post_ids}
        counts.update({post_id: count for post_id, count in result})
        return counts
    
    def count_by_type_for_post(self, post_id: uuid.UUID) -> Dict[ReactionType, int]:
        stmt = (
            select(Reaction.type, func.count(Reaction.id))
            .where(Reaction.post_id == post_id)
            .group_by(Reaction.type)
        )
        result = self.db.execute(stmt).all()
        return {reaction_type: count for reaction_type, count in result}
    
    def count_by_type_for_posts(self, post_ids: List[uuid.UUID]) -> Dict[uuid.UUID, Dict[ReactionType, int]]:
        if not post_ids:
            return {}
        
        stmt = (
            select(Reaction.post_id, Reaction.type, func.count(Reaction.id))
            .where(Reaction.post_id.in_(post_ids))
            .group_by(Reaction.post_id, Reaction.type)
        )
        result = self.db.execute(stmt).all()

        counts: Dict[uuid.UUID, Dict[ReactionType, int]] = {}
        for post_id, reaction_type, count in result:
            counts.setdefault(post_id, {})[reaction_type] = count
        return counts

