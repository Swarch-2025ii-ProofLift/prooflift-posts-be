import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.reaction import Reaction, ReactionKind
from app.repositories.reaction_repository import ReactionRepository
from app.schemas.reaction import ReactionSet


class ReactionService:
    def __init__(self, db: Session):
        self.repo = ReactionRepository(db)

    def set_reaction(self, user_id: uuid.UUID, reaction_in: ReactionSet) -> Reaction:
        return self.repo.set_reaction(user_id, reaction_in)

    def remove_reaction(self, user_id: uuid.UUID, post_id: uuid.UUID) -> Optional[Reaction]:
        return self.repo.remove_reaction(user_id, post_id)

    def list_reactions(self, post_id: uuid.UUID, kind: Optional[ReactionKind] = None) -> List[Reaction]:
        return self.repo.list_for_post(post_id, kind)

    def count_reactions(self, post_id: uuid.UUID, kind: Optional[ReactionKind] = None) -> int:
        return self.repo.count_for_post(post_id, kind)
