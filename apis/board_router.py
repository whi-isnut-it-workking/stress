from typing import List
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from database.board import crud, board, schema
from database.db import SessionLocal, engine

board.Base.metadata.create_all(bind=engine)

# URL 앞을 /board로 지정
router = APIRouter(
    prefix="/board"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        print("DB Session Connected")
        yield db
    finally:
        print("DB Session Closed")
        db.close()

def get_password_from_header(password: str = Header(...)):
    return password

def get_current_user_password(password: Header = Depends(get_password_from_header)):
    return password

# id와 일치하는 게시글 한 개를 읽는 API
@router.get("/{board_id:int}", response_model=schema.Board, tags=["boards"])
def read_one_board_api(board_id: int, db: Session = Depends(get_db)):
    db_board = crud.get_one_board(db, id=board_id)
    return db_board

# 모든 게시글을 읽는 API
@router.get("/all", response_model=List[schema.Board], tags=["boards"])
def read_all_board_api(db: Session = Depends(get_db)):
    db_board_list = crud.get_all_board(db)
    return db_board_list

# 게시글 생성 API
@router.post("", response_model=schema.BoardCreate, tags=["boards"])
def create_board_api(board: schema.BoardCreate, db: Session = Depends(get_db)):
    return crud.create_board(db=db, board=board)

# 게시글 수정 API
@router.patch("/{board_id:int}", response_model=schema.BoardUpdate, tags=["boards"])
def update_board_api(
    board_id: int, 
    update_data: schema.BoardUpdate, 
    password: str = Depends(get_current_user_password), 
    db: Session = Depends(get_db)
):
    updated_board = crud.update_board(db, id=board_id, password=password, update_data=update_data)
    return updated_board

# 게시글 삭제 API
@router.delete("/{board_id:int}", response_model=schema.BoardDelete, tags=["boards"])
def delete_board_api(
    board_id: int, 
    password: str = Depends(get_current_user_password), 
    db: Session = Depends(get_db)
):
    deleted_board = crud.delete_board(db, id=board_id, password=password)
    return deleted_board
