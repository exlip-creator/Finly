from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class AccountRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    start_balance: Decimal
    currency: str
    created_at: datetime
    is_archived: bool

class AccountCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=50)
    start_balance: Decimal = Field(max_digits=18, decimal_places=2, default=Decimal("0"))
    currency: Literal["RUS"]

class AccountUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=50)

class AccountArchive(BaseModel):
    is_archived: bool