import uuid
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.post_service import PostService
from app.schemas.post import PostCreate

def seed_posts():
    db: Session = SessionLocal()
    service = PostService(db)

    user_1 = uuid.UUID("99999999-9999-9999-9999-999999999999")
    user_2 = uuid.UUID("88888888-8888-8888-8888-888888888888")

    posts_data = [
        PostCreate(
            body="Hello! This is my post.",
            exercise_ids=["11111111-1111-1111-1111-111111111111"]
        ),
        PostCreate(
            body="Today I did these exercises.",
            exercise_ids=[
                "11111111-1111-1111-1111-111111111111",
                "22222222-2222-2222-2222-222222222222"
            ]
        ),
        PostCreate(
            body="Just finished a workout routine!",
            exercise_ids=[
                "33333333-3333-3333-3333-333333333333",
                "44444444-4444-4444-4444-444444444444",
                "55555555-5555-5555-5555-555555555555"
            ]
        ),
        PostCreate(
            body="Feeling great today.",
            exercise_ids=[
                "22222222-2222-2222-2222-222222222222",
                "33333333-3333-3333-3333-333333333333"
            ]
        )
    ]

    service.create_post(user_1, posts_data[0])
    service.create_post(user_1, posts_data[1])
    service.create_post(user_2, posts_data[2]) 
    service.create_post(user_2, posts_data[3])

    db.commit()
    db.close()

    print("Seeded posts successfully.")

seed_posts()