from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

class AccountRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    start_balance: Decimal
    currency: str
    created_at: datetime

class AccountCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=50)
    start_balance: Decimal = Field(max_digits=18, decimal_places=2, default=Decimal("0"))