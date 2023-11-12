from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.board import crud, board, schema
from database.db import SessionLocal, engine

board.Base.metadata.create_all(bind=engine)

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

@router.get("", response_model=schema.Board)
def read_board(db: Session = Depends(get_db)):
    db_board = crud.get_board(db)
    return db_board

@router.post("", response_model=schema.Board)
def create_board(board: schema.BoardCreate, db: Session = Depends(get_db)):
    return crud.create_board(db=db, board=board)