from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(min_length=1, max_length=50)
    kind: Literal["income", "expense"]
    is_archived: bool

class CategoryCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=50)
    kind: Literal["income", "expense"]