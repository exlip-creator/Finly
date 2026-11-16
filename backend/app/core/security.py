import jwt
from pwdlib import PasswordHash
from datetime import datetime, UTC, timedelta

from app.core.config import settings

password_hasher = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)

def create_access_token(user_id: int) -> str:
    meta_data = {
        "sub": str(user_id),
        "exp": datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    secret_key = settings.JWT_SECRET_KEY.get_secret_value()

    return jwt.encode(meta_data, secret_key, algorithm="HS256")

def decode_access_token(token: str) -> int:
    meta_data = jwt.decode(
        token,
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithms=["HS256"],
        options={
            "require": ["sub", "exp"]
        }
    )

    return int(meta_data["sub"])

