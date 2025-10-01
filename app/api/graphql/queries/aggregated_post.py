import uuid
import strawberry
from typing import List
from strawberry.types import Info

from app.api.graphql.types.aggregated_post import AggregatedPostType
from app.api.graphql.types.reaction import ReactionCountType
from app.services.post_service import PostService
from app.services.comment_service import CommentService
from app.services.reaction_service import ReactionService
from app.utils.graphql_helpers import handle_service_call
from app.core.exceptions import AuthenticationError

@strawberry.type
class AggregatedPostQueries:
    @strawberry.field
    def get_aggregated_post(self, info: Info, skip: int = 0, limit: int = 100) -> List[AggregatedPostType]:
        db = info.context["db"]
        user_id = info.context.get("user_id")
        if not user_id:
            raise AuthenticationError()
        
        post_service = PostService(db)
        comment_service = CommentService(db)
        reaction_service = ReactionService(db)
        
        posts = handle_service_call(post_service.list_posts, skip, limit)
        post_ids = [post.id for post in posts]

        total_comments = handle_service_call(comment_service.count_comments_batch, post_ids)
        reactions_by_type = handle_service_call(reaction_service.count_reactions_by_type_batch, post_ids)

        user_reactions = handle_service_call(reaction_service.get_user_reactions, user_id, post_ids)

        return [
            AggregatedPostType(
                post=post, 
                total_comments=total_comments.get(post.id, 0), 
                reactions_by_type=[
                    ReactionCountType(type=reaction_type, count=count) 
                    for reaction_type, count in reactions_by_type.get(post.id, {}).items()
                ],
                current_user_reaction=user_reactions.get(post.id)
            ) for post in posts
        ]
    
    @strawberry.field
    def get_aggregated_post_by_id(self, info: Info, post_id: uuid.UUID) -> AggregatedPostType:
        db = info.context["db"]
        user_id = info.context["user_id"]
        if not user_id:
            raise AuthenticationError()
        
        post_service = PostService(db)
        comment_service = CommentService(db)
        reaction_service = ReactionService(db)

        post = handle_service_call(post_service.get_post, post_id)
        total_comments = handle_service_call(comment_service.count_comments, post_id)
        reactions_by_type = handle_service_call(reaction_service.count_reactions_by_type, post_id)

        user_reaction = handle_service_call(reaction_service.get_user_reaction, user_id, post_id)

        return AggregatedPostType(
                    post=post,
                    total_comments=total_comments,
                    reactions_by_type=[
                        ReactionCountType(type=reaction_type, count=count)
                        for reaction_type, count in reactions_by_type.items()
                    ],
                    current_user_reaction=user_reaction
                )
