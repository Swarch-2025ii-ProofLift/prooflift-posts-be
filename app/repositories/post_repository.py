import uuid
from sqlalchemy import select, func
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: uuid.UUID, post_in: PostCreate) -> Post:
        db_post = Post(
            user_id=user_id,
            body=post_in.body,
            exercise_ids=post_in.exercise_ids,
        )
       
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        
        return db_post

    def get(self, post_id: uuid.UUID) -> Optional[Post]:
        return self.db.scalar(select(Post).where(Post.id == post_id))

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Post]:
        return self.db.scalars(select(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit)).all()

    def get_by_user(self, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Post]:
        return self.db.scalars(select(Post).where(Post.user_id == user_id).order_by(Post.created_at.desc()).offset(skip).limit(limit)).all()
    
    def count_by_user(self, user_id: uuid.UUID) -> int:
        return self.db.scalar(select(func.count()).select_from(Post).where(Post.user_id == user_id)) or 0
    
    def update(self, post: Post, post_in: PostUpdate) -> Post:
        if post_in.body is not None:
            post.body = post_in.body
        if post_in.exercise_ids is not None:
            post.exercise_ids = post_in.exercise_ids
        
        self.db.commit()
        self.db.refresh(post)
        
        return post

    def delete(self, post: Post) -> Post:
        self.db.delete(post)
        self.db.commit()

        return post
