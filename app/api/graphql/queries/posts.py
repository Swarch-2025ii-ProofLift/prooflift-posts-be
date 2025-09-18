import strawberry
from typing import List
from app.api.graphql.types.post import Post

FAKE_DB: List[Post] = []

@strawberry.type
class PostQuery:
    @strawberry.field
    def posts(self) -> List[Post]:
        return FAKE_DB
    
    @strawberry.field
    def post(self, post_id: int) -> Post | None:
        for post in FAKE_DB:
            if post.id == post_id:
                return post
        return None
