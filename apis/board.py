from typing import List
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from database.board import crud, schema
from database.db import SessionLocal, engine
from database import models

models.Base.metadata.create_all(bind=engine)

# URL 앞을 /board로 지정
router = APIRouter(
    prefix="/board"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        print("Board DB Session Connected")
        yield db
    finally:
        print("Board DB Session Closed")
        db.close()

def get_password_from_header(password: str = Header(...)):
    return password

def get_current_user_password(password: Header = Depends(get_password_from_header)):
    return password

# id와 일치하는 게시글 한 개를 읽는 API
@router.get("/{board_id:int}", response_model=schema.Board, tags=["boards"])
def read_one_board_api(
    board_id: int, 
    db: Session = Depends(get_db)
):
    return crud.get_one_board(
        db=db, 
        id=board_id
    )

# 모든 게시글을 읽는 API
@router.get("/all", response_model=List[schema.Board], tags=["boards"])
def read_all_boards_api(db: Session = Depends(get_db)):
    return crud.get_all_board(db)

# 게시글 생성 API
@router.post("", response_model=schema.BoardCreate, tags=["boards"])
def create_board_api(
    board: schema.BoardCreate, 
    db: Session = Depends(get_db)
):
    return crud.create_board(
        db=db, 
        board=board
    )

# 게시글 수정 API
@router.patch("/{board_id:int}", response_model=schema.BoardUpdate, tags=["boards"])
def update_board_api(
    board_id: int, 
    update_data: schema.BoardUpdate, 
    password: str = Depends(get_current_user_password), 
    db: Session = Depends(get_db)
):
    return crud.update_board(
        db=db, 
        id=board_id, 
        password=password, 
        update_data=update_data
    )

# 게시글 삭제 API
@router.delete("/{board_id:int}", response_model=schema.BoardDelete, tags=["boards"])
def delete_board_api(
    board_id: int, 
    password: str = Depends(get_current_user_password), 
    db: Session = Depends(get_db)
):
    return crud.delete_board(
        db=db, 
        id=board_id, 
        password=password)

# 추천 1 증가 API
@router.patch("/{board_id:int}/like", response_model=schema.Board, tags=["boards"])
def increment_like(
    board_id: int, 
    db: Session = Depends(get_db)
):
    return crud.increment_like(db, board_id)
    
# 비추천 1 증가 API
@router.patch("/{board_id:int}/dislike", response_model=schema.Board, tags=["boards"])
def increment_dislike(
    board_id: int, 
    db: Session = Depends(get_db)
):
    return crud.increment_dislike(db, board_id)