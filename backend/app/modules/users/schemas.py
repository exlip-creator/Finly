from pydantic import BaseModel, EmailStr, SecretStr, Field, field_validator, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: SecretStr = Field(min_length=8, max_length=128)

    @field_validator("email")
    @staticmethod
    def normalize_email(email: str) -> str:
        return email.strip().lower()

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime