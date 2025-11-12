import aio_pika
import uuid
import logging
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment
from app.repositories.post_repository import PostRepository
from app.repositories.comment_repository import CommentRepository
from app.schemas.comment import CommentCreate, CommentUpdate
from app.core.exceptions import NotFoundError, AuthorizationError
from app.events.events import NotificationEventPublisher

logger = logging.getLogger(__name__)

class CommentService:
    def __init__(self, db: AsyncSession, mq_channel: Optional[aio_pika.Channel] = None):
        self.repo = CommentRepository(db)
        self.post_repo = PostRepository(db)
        self.mq_channel = mq_channel

    async def get_comment(self, comment_id: uuid.UUID) -> Optional[Comment]:
        return await self.repo.get(comment_id)

    async def add_comment(self, user_id: uuid.UUID, comment_in: CommentCreate) -> Comment:
        post = await self.post_repo.get(comment_in.post_id)
        if not post:
            raise NotFoundError("Post not found")

        comment = await self.repo.create(user_id, comment_in)

        if self.mq_channel:
            try:
                await NotificationEventPublisher.publish_comment_created(
                    channel=self.mq_channel,
                    post_owner_id=post.user_id,
                    commenter_id=user_id,
                    post_id=post.id,
                    comment_id=comment.id
                )
            except Exception as e:
                logger.error(f"Failed to publish comment notification: {e}")

        return comment

    async def list_comments(self, post_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Comment]:
        return await self.repo.list_for_post(post_id, skip=skip, limit=limit)

    async def count_comments(self, post_id: uuid.UUID) -> int:
        return await self.repo.count_for_post(post_id)

    async def count_comments_batch(self, post_ids: List[uuid.UUID]) -> dict[uuid.UUID, int]:
        return await self.repo.count_for_posts(post_ids)

    async def update_comment(self, comment_id: uuid.UUID, user_id: uuid.UUID, comment_in: CommentUpdate) -> Comment:
        db_obj = await self.repo.get(comment_id)
        if not db_obj:
            raise NotFoundError("Comment not found")
        if db_obj.user_id != user_id:
            raise AuthorizationError("You are not allowed to edit this comment")
        return await self.repo.update(db_obj, comment_in)

    async def delete_comment(self, comment_id: uuid.UUID, user_id: uuid.UUID) -> Comment:
        db_obj = await self.repo.get(comment_id)
        if not db_obj:
            raise NotFoundError("Comment not found")
        if db_obj.user_id != user_id:
            raise AuthorizationError("You are not allowed to delete this comment")

        post = await self.post_repo.get(db_obj.post_id)

        result = await self.repo.delete(db_obj)

        if self.mq_channel and post:
            try:
                await NotificationEventPublisher.publish_comment_deleted(
                    channel=self.mq_channel,
                    comment_id=comment_id,
                    post_id=db_obj.post_id,
                    actor_id=user_id,
                    user_id=post.user_id
                )
            except Exception as e:
                logger.error(f"Failed to publish comment deletion notification: {e}")

        return result