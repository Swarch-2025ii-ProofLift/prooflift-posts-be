import uuid
from jose import jwt, JWTError

from app.core.config import settings
from app.core.exceptions import AuthenticationError

def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise AuthenticationError("Invalid or expired token")

def get_user_id_from_token(token: str) -> uuid.UUID:
    payload = decode_jwt(token)
    user_id = payload.get("sub") 
    if not user_id:
        raise AuthenticationError("Invalid token: no subject found")
    return uuid.UUID(user_id)
