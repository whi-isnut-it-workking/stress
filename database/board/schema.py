from pydantic import BaseModel

class BoardBase(BaseModel):
    id: int

    class Config:
        orm_mode = True

class BoardCreate(BoardBase):
    password: str
    title: str

class Board(BoardBase):
    title: str
    body: str