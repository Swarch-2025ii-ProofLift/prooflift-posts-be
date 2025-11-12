import uuid
from sqlalchemy import select, func
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: uuid.UUID, post_in: PostCreate) -> Post:
        db_post = Post(
            user_id=user_id,
            body=post_in.body,
            exercise_ids=post_in.exercise_ids,
        )

        self.db.add(db_post)
        await self.db.commit()
        await self.db.refresh(db_post)

        return db_post

    async def get(self, post_id: uuid.UUID) -> Optional[Post]:
        result = await self.db.execute(select(Post).where(Post.id == post_id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Post]:
        result = await self.db.execute(select(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_by_user(self, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Post]:
        result = await self.db.execute(select(Post).where(Post.user_id == user_id).order_by(Post.created_at.desc()).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def count_by_user(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(select(func.count()).select_from(Post).where(Post.user_id == user_id))
        return result.scalar() or 0

    async def update(self, post: Post, post_in: PostUpdate) -> Post:
        if post_in.body is not None:
            post.body = post_in.body
        if post_in.exercise_ids is not None:
            post.exercise_ids = post_in.exercise_ids

        await self.db.commit()
        await self.db.refresh(post)

        return post

    async def delete(self, post: Post) -> Post:
        await self.db.delete(post)
        await self.db.commit()

        return post
