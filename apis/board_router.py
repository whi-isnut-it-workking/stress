from typing import List
from fastapi import APIRouter, Depends
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

# response_model: Pydantic 모델을 반환해야 함. schema.~~ 사용
@router.get("", response_model=List[schema.Board])
def read_board(db: Session = Depends(get_db)):
    db_board = crud.get_board(db)
    return db_board

@router.post("", response_model=schema.Board)
def create_board(board: schema.BoardCreate, db: Session = Depends(get_db)):
    return crud.create_board(db=db, board=board)

# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user