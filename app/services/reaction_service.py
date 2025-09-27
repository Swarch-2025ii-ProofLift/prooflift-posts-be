import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.reaction import Reaction, ReactionType
from app.repositories.post_repository import PostRepository
from app.repositories.reaction_repository import ReactionRepository
from app.schemas.reaction import ReactionSet
from app.core.exceptions import NotFoundError


class ReactionService:
    def __init__(self, db: Session):
        self.repo = ReactionRepository(db)
        self.post_repo = PostRepository(db)

    def set_reaction(self, user_id: uuid.UUID, reaction_in: ReactionSet) -> Reaction:
        if not self.post_repo.get(reaction_in.post_id):
            raise NotFoundError("Post not found")
        
        existing = self.repo.get_for_user_post(user_id, reaction_in.post_id)
        
        if existing:
            return self.repo.update_reaction(existing, reaction_in.type)
        return self.repo.set_reaction(user_id, reaction_in)

    def remove_reaction(self, user_id: uuid.UUID, post_id: uuid.UUID) -> Optional[Reaction]:
        existing = self.repo.get_for_user_post(user_id, post_id)
        if not existing:
            return None
        return self.repo.remove_reaction(existing)

    def list_reactions(self, post_id: uuid.UUID, type: Optional[ReactionType] = None) -> List[Reaction]:
        return self.repo.list_for_post(post_id, type)

    def count_reactions(self, post_id: uuid.UUID, type: Optional[ReactionType] = None) -> int:
        return self.repo.count_for_post(post_id, type)
