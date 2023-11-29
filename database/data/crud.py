from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

# from database.board import schema
from database import models
# Data 모델 가져옴
Data = models.Data

#data 테이블의 모든 레코드를 반환
def get_items(db: Session):
    return db.query(Data).all()

def get_items_with_keyword_for_preprocessing(db: Session, keyword):
    return db.query(Data).filter(or_(Data.body.contains(keyword))).all()

def add_items(db: Session, item: Data):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item