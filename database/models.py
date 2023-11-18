from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base

# 게시글 모델
class Board(Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30))
    body = Column(String(10000))
    date = Column(DateTime, default=datetime.now())
    username = Column(String(14), default="ㅇㅇ")
    password = Column(String(20))
    recomment = Column(Integer, default=0)
    disapproval = Column(Integer, default=0)
    views = Column(Integer, default=0)
    tag = Column(String(500))

    comments = relationship("Comment", back_populates="board")

# 댓글 모델
class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(String(30))
    date = Column(DateTime, default=datetime.now())
    username = Column(String(14), default="ㅇㅇ")
    password = Column(String(20))
    board_index = Column(Integer, ForeignKey("board.id"), nullable=False)
    
    board = relationship("Board", back_populates="comments")