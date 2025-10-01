import strawberry

from app.api.graphql.queries.post import PostQueries
from app.api.graphql.mutations.post import PostMutations
from app.api.graphql.queries.comment import CommentQueries
from app.api.graphql.mutations.comment import CommentMutations
from app.api.graphql.queries.reaction import ReactionQueries
from app.api.graphql.mutations.reaction import ReactionMutations
from app.api.graphql.queries.aggregated_post import AggregatedPostQueries

@strawberry.type
class Query(PostQueries, CommentQueries, ReactionQueries, AggregatedPostQueries):
    pass

@strawberry.type
class Mutation(PostMutations, CommentMutations, ReactionMutations):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
