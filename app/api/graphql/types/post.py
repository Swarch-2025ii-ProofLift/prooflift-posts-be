import strawberry

@strawberry.type
class Post:
    id: int
    body: str
