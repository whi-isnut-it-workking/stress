from datetime import datetime
from sqlalchemy import Column, INT, VARCHAR, DATETIME
from sqlalchemy.orm import relationship

from database.db import Base

class Board(Base):
    __tablename__ = "board"

    id = Column(INT, primary_key=True, index=True)
    title = Column(VARCHAR(30))
    body = Column(VARCHAR(10000))
    date = Column(DATETIME, default=datetime.now())
    username = Column(VARCHAR(14), default="ㅇㅇ")
    password = Column(VARCHAR(20))
    recomment = Column(INT, default=0)
    disapproval = Column(INT, default=0)
    views = Column(INT, default=0)
    tag = Column(VARCHAR(500))