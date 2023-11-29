from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text
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

# 데이터 테이블 모델
class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    body = Column(Text)
    section = Column(String(3))
    url = Column(String(200))
    title = Column(String(200))

# 전처리 모델
class Preprocessing(Base):
    __tablename__ = "preprocessing"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    for_wordcloud = Column(Text)
    for_word_association_analysis = Column(Text)