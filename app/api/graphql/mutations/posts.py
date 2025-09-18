import strawberry

from app.api.graphql.types.post import Post
from app.api.graphql.queries.posts import FAKE_DB

@strawberry.type
class PostMutation:
    @strawberry.mutation
    def create_post(self, body: str) -> Post:
        new_post = Post(id=len(FAKE_DB) + 1, body=body)
        FAKE_DB.append(new_post)
        return new_post
    
    @strawberry.mutation
    def delete_post(self, post_id: int) -> bool:
        for post in FAKE_DB:
            if post.id == post_id:
                FAKE_DB.remove(post)
                return True
        return False
