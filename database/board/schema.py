# schema.py
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class BoardBase(BaseModel):
    title: str
    body: str
    password: str
    tag: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True  # Pydantic이 datetime을 처리하도록 하는 옵션
        extra = "forbid"

class BoardCreate(BoardBase):
    title: str
    body: str
    username: str
    password: str
    tag: Optional[str]

class Board(BoardBase):
    id: int
    date: datetime
    recomment: int
    disapproval: int
    views: int

    class Config:
        orm_mode = True
