import pika
import uuid
import logging
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.repositories.post_repository import PostRepository
from app.repositories.comment_repository import CommentRepository
from app.schemas.comment import CommentCreate, CommentUpdate
from app.core.exceptions import NotFoundError, AuthorizationError
from app.events.events import NotificationEventPublisher

logger = logging.getLogger(__name__)

class CommentService:
    def __init__(self, db: Session, mq_channel: Optional[pika.channel.Channel] = None):
        self.repo = CommentRepository(db)
        self.post_repo = PostRepository(db)
        self.mq_channel = mq_channel

    def get_comment(self, comment_id: uuid.UUID) -> Optional[Comment]:
        return self.repo.get(comment_id)

    def add_comment(self, user_id: uuid.UUID, comment_in: CommentCreate) -> Comment:
        post = self.post_repo.get(comment_in.post_id)
        if not post:
            raise NotFoundError("Post not found")

        comment = self.repo.create(user_id, comment_in)

        if self.mq_channel:
            try:
                NotificationEventPublisher.publish_comment_created(
                    channel=self.mq_channel,
                    post_owner_id=post.user_id,
                    commenter_id=user_id,
                    post_id=post.id,
                    comment_id=comment.id
                )
            except Exception as e:
                logger.error(f"Failed to publish comment notification: {e}")

        return comment

    def list_comments(self, post_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Comment]:
        return self.repo.list_for_post(post_id, skip=skip, limit=limit)

    def count_comments(self, post_id: uuid.UUID) -> int:
        return self.repo.count_for_post(post_id)
    
    def count_comments_batch(self, post_ids: List[uuid.UUID]) -> dict[uuid.UUID, int]:
        return self.repo.count_for_posts(post_ids)

    def update_comment(self, comment_id: uuid.UUID, user_id: uuid.UUID, comment_in: CommentUpdate) -> Comment:
        db_obj = self.repo.get(comment_id)
        if not db_obj:
            raise NotFoundError("Comment not found")
        if db_obj.user_id != user_id:
            raise AuthorizationError("You are not allowed to edit this comment")
        return self.repo.update(db_obj, comment_in)

    def delete_comment(self, comment_id: uuid.UUID, user_id: uuid.UUID) -> Comment:
        db_obj = self.repo.get(comment_id)
        if not db_obj:
            raise NotFoundError("Comment not found")
        if db_obj.user_id != user_id:
            raise AuthorizationError("You are not allowed to delete this comment")
        return self.repo.delete(db_obj)