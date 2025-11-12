import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.repositories.post_repository import PostRepository
from app.core.exceptions import AuthorizationError, NotFoundError

class PostService:
    def __init__(self, db: AsyncSession):
        self.repo = PostRepository(db)

    async def create_post(self, user_id: uuid.UUID, post_in: PostCreate) -> Post:
        return await self.repo.create(user_id, post_in)

    async def get_post(self, post_id: uuid.UUID) -> Optional[Post]:
        return await self.repo.get(post_id)

    async def list_posts(self, skip: int = 0, limit: int = 100) -> List[Post]:
        return await self.repo.get_all(skip=skip, limit=limit)

    async def list_posts_by_user(self, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Post]:
        return await self.repo.get_by_user(user_id, skip=skip, limit=limit)

    async def count_posts_by_user(self, user_id: uuid.UUID) -> int:
        return await self.repo.count_by_user(user_id)

    async def update_post(self, post_id: uuid.UUID, user_id: uuid.UUID, post_in: PostUpdate) -> Post:
        db_post = await self.repo.get(post_id)

        if not db_post:
            raise NotFoundError("Post not found")
        if db_post.user_id != user_id:
            raise AuthorizationError("You are not allowed to edit this post")

        return await self.repo.update(db_post, post_in)

    async def delete_post(self, post_id: uuid.UUID, user_id: uuid.UUID) -> Post:
        db_post = await self.repo.get(post_id)

        if not db_post:
            raise NotFoundError("Post not found")
        if db_post.user_id != user_id:
            raise AuthorizationError("You are not allowed to delete this post")

        return await self.repo.delete(db_post)