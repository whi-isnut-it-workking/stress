from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class DataBase(BaseModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True  # Pydantic이 datetime을 처리하도록 하는 옵션
        extra = "forbid"

class Board(DataBase):
    id: int
    title: str
    body: str
    username: str
    date: datetime
    recomment: int
    disapproval: int
    views: int
    tag: Optional[str] = None

class BoardCreate(DataBase):
    title: str = "title"
    body: str = "body"
    username: str = "ㅇㅇ"
    password: str = "pwd"
    tag: Optional[str] = None

class BoardUpdate(DataBase):
    title: Optional[str] = None
    body: Optional[str] = None
    tag: Optional[str] = None

class BoardDelete(Board):
    pass