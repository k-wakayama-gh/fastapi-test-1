from typing import Optional
from sqlmodel import SQLModel, Field


class ItemBase(SQLModel):
    name: str
    price: float


class Items(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    name: Optional[str]
    price: Optional[float]


class ItemOut(ItemBase):
    id: int


