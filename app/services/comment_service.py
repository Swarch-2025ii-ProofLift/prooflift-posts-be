import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.repositories.comment_repository import CommentRepository
from app.schemas.comment import CommentCreate, CommentUpdate
from app.core.exceptions import NotFoundError, AuthorizationError


class CommentService:
    def __init__(self, db: Session):
        self.repo = CommentRepository(db)

    def add_comment(self, user_id: uuid.UUID, comment_in: CommentCreate) -> Comment:
        return self.repo.create(user_id, comment_in)

    def list_comments(self, post_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Comment]:
        return self.repo.list_for_post(post_id, skip=skip, limit=limit)

    def count_comments(self, post_id: uuid.UUID) -> int:
        return self.repo.count_for_post(post_id)

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
        self.repo.delete(db_obj)
        return db_obj
