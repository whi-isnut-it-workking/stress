from pydantic import BaseModel

class BoardBase(BaseModel):
    id: int


class BoardCreate(BoardBase):
    password: str
    title: str


class Board(BoardBase):
    id: int

    class Config:
        orm_mode = True