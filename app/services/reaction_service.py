import aio_pika
import uuid
import logging
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reaction import Reaction, ReactionType
from app.repositories.post_repository import PostRepository
from app.repositories.reaction_repository import ReactionRepository
from app.schemas.reaction import ReactionSet
from app.core.exceptions import NotFoundError
from app.events.events import NotificationEventPublisher

logger = logging.getLogger(__name__)

class ReactionService:
    def __init__(self, db: AsyncSession, mq_channel: Optional[aio_pika.Channel] = None):
        self.repo = ReactionRepository(db)
        self.post_repo = PostRepository(db)
        self.mq_channel = mq_channel

    async def set_reaction(self, user_id: uuid.UUID, reaction_in: ReactionSet) -> Reaction:
        post = await self.post_repo.get(reaction_in.post_id)
        if not post:
            raise NotFoundError("Post not found")

        existing = await self.repo.get_for_user_post(user_id, reaction_in.post_id)

        is_new_reaction = existing is None

        if existing:
            reaction = await self.repo.update_reaction(existing, reaction_in.type)
        else:
            reaction = await self.repo.set_reaction(user_id, reaction_in)

        if is_new_reaction and self.mq_channel:
            try:
                await NotificationEventPublisher.publish_reaction_added(
                    channel=self.mq_channel,
                    post_owner_id=post.user_id,
                    reactor_id=user_id,
                    post_id=post.id
                )
            except Exception as e:
                logger.error(f"Failed to publish reaction notification: {e}")

        return reaction

    async def remove_reaction(self, user_id: uuid.UUID, post_id: uuid.UUID) -> Optional[Reaction]:
        existing = await self.repo.get_for_user_post(user_id, post_id)
        if not existing:
            return None

        post = await self.post_repo.get(post_id)

        result = await self.repo.remove_reaction(existing)

        if self.mq_channel and post:
            try:
                await NotificationEventPublisher.publish_reaction_removed(
                    channel=self.mq_channel,
                    post_id=post_id,
                    actor_id=user_id,
                    user_id=post.user_id
                )
            except Exception as e:
                logger.error(f"Failed to publish reaction removal notification: {e}")

        return result

    async def list_reactions(self, post_id: uuid.UUID, type: Optional[ReactionType] = None) -> List[Reaction]:
        return await self.repo.list_for_post(post_id, type)

    async def count_reactions(self, post_id: uuid.UUID, type: Optional[ReactionType] = None) -> int:
        return await self.repo.count_for_post(post_id, type)

    async def count_reactions_batch(self, post_ids: List[uuid.UUID], type: Optional[ReactionType] = None) -> dict[uuid.UUID, int]:
        return await self.repo.count_for_posts(post_ids, type)

    async def count_reactions_by_type(self, post_id: uuid.UUID) -> Dict[ReactionType, int]:
        return await self.repo.count_by_type_for_post(post_id)

    async def count_reactions_by_type_batch(self, post_ids: List[uuid.UUID]) -> Dict[uuid.UUID, Dict[ReactionType, int]]:
        return await self.repo.count_by_type_for_posts(post_ids)

    async def get_user_reactions(self, user_id: uuid.UUID, post_ids: List[uuid.UUID]) -> Dict[uuid.UUID, Reaction]:
        return await self.repo.get_user_reactions(user_id, post_ids)

    async def get_user_reaction(self, user_id: uuid.UUID, post_id: uuid.UUID) -> Optional[Reaction]:
        return await self.repo.get_for_user_post(user_id, post_id)