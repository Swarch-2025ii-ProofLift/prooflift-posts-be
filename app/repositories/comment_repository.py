import uuid
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: uuid.UUID, comment_in: CommentCreate) -> Comment:
        db_obj = Comment(
            post_id=comment_in.post_id,
            user_id=user_id,
            body=comment_in.body,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def get(self, comment_id: uuid.UUID) -> Optional[Comment]:
        result = await self.db.execute(select(Comment).where(Comment.id == comment_id))
        return result.scalar_one_or_none()

    async def list_for_post(self, post_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Comment]:
        stmt = (
            select(Comment)
            .where(Comment.post_id == post_id)
            .order_by(Comment.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_for_post(self, post_id: uuid.UUID) -> int:
        result = await self.db.execute(select(func.count()).select_from(Comment).where(Comment.post_id == post_id))
        return result.scalar() or 0

    async def count_for_posts(self, post_ids: List[uuid.UUID]) -> dict[uuid.UUID, int]:
        if not post_ids:
            return {}

        stmt = (
            select(Comment.post_id, func.count(Comment.id))
            .where(Comment.post_id.in_(post_ids))
            .group_by(Comment.post_id)
        )
        result = await self.db.execute(stmt)

        counts = {post_id: 0 for post_id in post_ids}
        counts.update({post_id: count for post_id, count in result.all()})
        return counts

    async def update(self, comment: Comment, comment_in: CommentUpdate) -> Comment:
        if comment_in.body is not None:
            comment.body = comment_in.body
        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def delete(self, comment: Comment) -> Comment:
        await self.db.delete(comment)
        await self.db.commit()
        return comment