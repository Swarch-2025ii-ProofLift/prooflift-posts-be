import strawberry
from typing import List

from app.api.graphql.types.post import PostType
from app.api.graphql.types.reaction import ReactionCountType

@strawberry.type
class AggregatedPostType:
    post: PostType
    total_comments: int
    reactions_by_type: List[ReactionCountType]

    @strawberry.field
    def total_reactions(self) -> int:
        return sum(reaction.count for reaction in self.reactions_by_type)

