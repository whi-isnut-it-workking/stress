from sqlalchemy import Column, INT, VARCHAR, DATETIME
from sqlalchemy.orm import relationship

from ..db import Base

class Board(Base):
    __tablename__ = "board"

    id = Column(INT, primary_key=True)
    title = Column(VARCHAR(30))
    body = Column(VARCHAR(10000))
    date = Column(DATETIME)
    username = Column(VARCHAR(14))
    password = Column(VARCHAR(20))
    recomment = Column(INT)
    disapproval = Column(INT)
    views = Column(INT)
    tag = Column(VARCHAR(500))