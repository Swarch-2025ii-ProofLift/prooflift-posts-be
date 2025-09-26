import uuid
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.core.config import settings

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM

def create_test_token(user_id: uuid.UUID, expires_minutes: int = 60) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

token_1 = create_test_token(uuid.UUID("99999999-9999-9999-9999-999999999999"))
token_2 = create_test_token(uuid.UUID("88888888-8888-8888-8888-888888888888"))

print(f"\nToken 1:\n{token_1}\n")
print(f"Token 2:\n{token_2}\n")
