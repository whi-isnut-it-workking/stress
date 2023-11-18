from typing import List
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from database.comment import crud, schema
from database.db import SessionLocal, engine
from database import models

models.Base.metadata.create_all(bind=engine)

# URL 앞을 /board/{board_id:int}/comment로 지정
router = APIRouter(
    prefix="/board/{board_id:int}/comment"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        print("Comment DB Session Connected")
        yield db
    finally:
        print("Comment DB Session Closed")
        db.close()

def get_password_from_header(password: str = Header(...)):
    return password

def get_current_user_password(password: Header = Depends(get_password_from_header)):
    return password

# id와 일치하는 댓글 한 개를 읽는 API
@router.get("/{comment_id:int}", response_model=schema.Comment, tags=["comments"])
def read_one_comment_api(
    comment_id: int, 
    board_id: int, 
    db: Session = Depends(get_db)
):
    return crud.get_one_comment(
        db=db, 
        comment_id=comment_id, 
        board_id=board_id
    )

# 특정 게시글의 모든 댓글을 읽는 API
@router.get("/all", response_model=List[schema.Comment], tags=["comments"])
def read_all_comments_api(
    board_id: int, 
    db: Session = Depends(get_db)
):
    return crud.get_all_comments(
        db=db, 
        board_id=board_id
    )

# 댓글 생성 API
@router.post("", response_model=schema.CommentCreate, tags=["comments"])
def create_comment_api(
    comment: schema.CommentCreate, 
    board_id: int, 
    db: Session = Depends(get_db)
):
    return crud.create_comment(
        db=db, 
        comment=comment, 
        board_id=board_id
    )

# 댓글 수정 API
@router.patch("/{comment_id:int}", response_model=schema.CommentUpdate, tags=["comments"])
def update_comment_api(
    comment_id: int,
    board_id: int,
    update_data: schema.CommentUpdate, 
    comment_password: str = Depends(get_current_user_password), 
    db: Session = Depends(get_db)
):
    return crud.update_comment(
        db=db, 
        comment_id=comment_id,
        comment_password=comment_password, 
        update_data=update_data, 
        board_id=board_id
    )

# 댓글 삭제 API
@router.delete("/{comment_id:int}", response_model=schema.CommentDelete, tags=["comments"])
def delete_board_api(
    board_id: int, 
    comment_id: int,
    comment_password: str = Depends(get_current_user_password), 
    db: Session = Depends(get_db)
):
    return crud.delete_comment(
        db, 
        board_id=board_id, 
        comment_id=comment_id,
        comment_password=comment_password
    )
