import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.repositories.post_repository import PostRepository

class PostService:
    def __init__(self, db: Session):
        self.repo = PostRepository(db)

    def create_post(self, user_id: uuid.UUID, post_in: PostCreate) -> Post:
        return self.repo.create(user_id, post_in)

    def get_post(self, post_id: uuid.UUID) -> Optional[Post]:
        return self.repo.get(post_id)

    def list_posts(self, skip: int = 0, limit: int = 100) -> List[Post]:
        return self.repo.get_all(skip=skip, limit=limit)

    def list_posts_by_user(self, user_id: uuid.UUID) -> List[Post]:
        return self.repo.get_by_user(user_id)

    def update_post(self, post_id: uuid.UUID, user_id: uuid.UUID, post_in: PostUpdate) -> Optional[Post]:
        db_post = self.repo.get(post_id)
        
        if not db_post:
            return None
        if db_post.user_id != user_id:
            raise PermissionError("You are not allowed to edit this post")
        
        return self.repo.update(post_id, post_in)

    def delete_post(self, post_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        db_post = self.repo.get(post_id)
        
        if not db_post:
            return False
        if db_post.user_id != user_id:
            raise PermissionError("You are not allowed to delete this post")
        
        return self.repo.delete(post_id)
