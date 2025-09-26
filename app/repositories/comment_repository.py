import uuid
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: uuid.UUID, comment_in: CommentCreate) -> Comment:
        db_obj = Comment(
            post_id=comment_in.post_id,
            user_id=user_id,
            body=comment_in.body,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get(self, comment_id: uuid.UUID) -> Optional[Comment]:
        return self.db.scalar(select(Comment).where(Comment.id == comment_id))

    def list_for_post(self, post_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Comment]:
        stmt = (
            select(Comment)
            .where(Comment.post_id == post_id)
            .order_by(Comment.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        return self.db.scalars(stmt).all()

    def count_for_post(self, post_id: uuid.UUID) -> int:
        return self.db.scalar(select(func.count()).select_from(Comment).where(Comment.post_id == post_id)) or 0

    def update(self, comment: Comment, comment_in: CommentUpdate) -> Comment:
        if comment_in.body is not None:
            comment.body = comment_in.body
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete(self, comment: Comment) -> Comment:
        self.db.delete(comment)
        self.db.commit()
        return comment