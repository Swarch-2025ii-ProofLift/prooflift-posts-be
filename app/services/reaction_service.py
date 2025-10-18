import pika
import uuid
import logging
from typing import List, Optional, Dict
from sqlalchemy.orm import Session

from app.models.reaction import Reaction, ReactionType
from app.repositories.post_repository import PostRepository
from app.repositories.reaction_repository import ReactionRepository
from app.schemas.reaction import ReactionSet
from app.core.exceptions import NotFoundError
from app.events.events import NotificationEventPublisher

logger = logging.getLogger(__name__)

class ReactionService:
    def __init__(self, db: Session, mq_channel: Optional[pika.channel.Channel] = None):
        self.repo = ReactionRepository(db)
        self.post_repo = PostRepository(db)
        self.mq_channel = mq_channel

    def set_reaction(self, user_id: uuid.UUID, reaction_in: ReactionSet) -> Reaction:
        post = self.post_repo.get(reaction_in.post_id)
        if not post:
            raise NotFoundError("Post not found")

        existing = self.repo.get_for_user_post(user_id, reaction_in.post_id)

        is_new_reaction = existing is None

        if existing:
            reaction = self.repo.update_reaction(existing, reaction_in.type)
        else:
            reaction = self.repo.set_reaction(user_id, reaction_in)

        if is_new_reaction and self.mq_channel:
            try:
                NotificationEventPublisher.publish_reaction_added(
                    channel=self.mq_channel,
                    post_owner_id=post.user_id,
                    reactor_id=user_id,
                    post_id=post.id
                )
            except Exception as e:
                logger.error(f"Failed to publish reaction notification: {e}")

        return reaction

    def remove_reaction(self, user_id: uuid.UUID, post_id: uuid.UUID) -> Optional[Reaction]:
        existing = self.repo.get_for_user_post(user_id, post_id)
        if not existing:
            return None
        return self.repo.remove_reaction(existing)

    def list_reactions(self, post_id: uuid.UUID, type: Optional[ReactionType] = None) -> List[Reaction]:
        return self.repo.list_for_post(post_id, type)

    def count_reactions(self, post_id: uuid.UUID, type: Optional[ReactionType] = None) -> int:
        return self.repo.count_for_post(post_id, type)
    
    def count_reactions_batch(self, post_ids: List[uuid.UUID], type: Optional[ReactionType] = None) -> dict[uuid.UUID, int]:
        return self.repo.count_for_posts(post_ids, type)
    
    def count_reactions_by_type(self, post_id: uuid.UUID) -> Dict[ReactionType, int]:
        return self.repo.count_by_type_for_post(post_id)
    
    def count_reactions_by_type_batch(self, post_ids: List[uuid.UUID]) -> Dict[uuid.UUID, Dict[ReactionType, int]]:
        return self.repo.count_by_type_for_posts(post_ids)
    
    def get_user_reactions(self, user_id: uuid.UUID, post_ids: List[uuid.UUID]) -> Dict[uuid.UUID, Reaction]:
        return self.repo.get_user_reactions(user_id, post_ids)

    def get_user_reaction(self, user_id: uuid.UUID, post_id: uuid.UUID) -> Optional[Reaction]:
        return self.repo.get_for_user_post(user_id, post_id)