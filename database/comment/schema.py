from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CommentBase(BaseModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True  # Pydantic이 datetime을 처리하도록 하는 옵션
        extra = "forbid"

class Comment(CommentBase):
    id: int
    body: str
    username: str
    date: datetime
    board_index: int

class CommentCreate(CommentBase):
    body: str = "body"
    username: str = "ㅇㅇ"
    password: str = "pwd"

class CommentUpdate(CommentBase):
    body: Optional[str] = None

class CommentDelete(Comment):
    pass