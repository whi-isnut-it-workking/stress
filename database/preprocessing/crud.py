from sqlalchemy.orm import Session
from sqlalchemy import or_

from database.board import schema
from database import models
# Preprocessing 모델 가져옴
Preprocessing = models.Preprocessing


#preprocessing 테이블의 모든 레코드를 반환
def get_items(db: Session):
    return db.query(Preprocessing).all()

#keyword로 검색한 값을 반환하는 함수
def get_items_with_keyword_for_wc(db: Session, keyword):
    if keyword == "" :
        return get_items(db)
    else : 
        return db.query(Preprocessing).filter(or_(Preprocessing.for_wordcloud.contains(keyword))).all()

def get_items_with_keyword_for_association(db: Session, keyword):
    return db.query(Preprocessing).filter(or_(Preprocessing.for_word_association_analysis.contains(keyword))).all()

def add_items(db: Session, item: Preprocessing):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item