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

# response_model: Pydantic 모델을 반환해야 함. schema.~~ 사용
# {board_id:int}: Path Parameter의 type을 명시적으로 지정하는 FastAPI의 기능
##########################################################
# id와 일치하는 게시글 한 개를 읽는 API
# 일치하는 id가 없을 경우 상태 코드 404 반환
# ex) http://localhost:8000/board/14
# Response ex)
# {
#     "id": 14,
#     "title": "title",
#     "body": "body",
#     "username": "ㅇㅇ",
#     "date": "2023-11-14T11:14:51",
#     "recomment": 0,
#     "disapproval": 0,
#     "views": 0,
#     "tag": "string"
# }
##########################################################
@router.get("/{board_id:int}", response_model=schema.Board)
def read_one_board_api(board_id: int, db: Session = Depends(get_db)):
    db_board = crud.get_one_board(db, id=board_id)
    return db_board

##########################################################
# 모든 게시글을 읽는 API
# 존재하는 게시글이 없을 경우 빈 리스트([]) 반환
# URL ex) http://localhost:8000/board/all
# Response ex)
# [
#   {
#     "id": 14,
#     "title": "title",
#     "body": "body",
#     "username": "ㅇㅇ",
#     "date": "2023-11-14T11:14:51",
#     "recomment": 0,
#     "disapproval": 0,
#     "views": 0,
#     "tag": "string"
#   },
#   {
#     "id": 15,
#     "title": "title",
#     "body": "body",
#     "username": "ㅇㅇ",
#     "date": "2023-11-14T18:04:41",
#     "recomment": 0,
#     "disapproval": 0,
#     "views": 0,
#     "tag": "#Test #IT #고토히토리 #後藤ひとり"
#   }
# ]
##########################################################
@router.get("/all", response_model=List[schema.Board])
def read_all_board_api(db: Session = Depends(get_db)):
    db_board_list = crud.get_all_board(db)
    return db_board_list

##########################################################
# 게시글 생성 API
# 생성에 성공할 경우 생성한 Request body 반환
# 실패할 경우 상황별 에러 상태 코드 반환
# URL ex) http://localhost:8000/board
# Request body ex)  
# {
#   "title": "title",
#   "body": "body",
#   "username": "ㅇㅇ",
#   "password": "pwd"
# }
# Required: title, body, username, password
# Optional: tag
# 
# Response ex)
# {
#   "title": "title",
#   "body": "body",
#   "username": "ㅇㅇ",
#   "password": "pwd",
#   "tag": null
# }
##########################################################
@router.post("", response_model=schema.BoardCreate)
def create_board_api(board: schema.BoardCreate, db: Session = Depends(get_db)):
    return crud.create_board(db=db, board=board)

##########################################################
# 게시글 수정 API
# id, password를 입력받고 Request body에 입력한 부분만 업데이트
# id는 URL에 Path Parameter로 명시, password는 Header에 'password'로 전달
# 제목, 본문, 태그만 변경 가능
# 성공하면 업데이트한 요청 반환, 실패하면 실패 원인에 따라 상태 코드 반환
# URL ex) http://localhost:8000/board/14
# Header ex) 'password: pwd' 
# {
#   "title": "변경한 제목",
#   "body": "변경한 내용",
#   "tag": "#Updated"
# }
# Required: 없음
# Optional: title, body, tag
# 
# Response ex)
# {
#   "title": "변경한 제목",
#   "body": "변경한 내용",
#   "tag": "#Updated"
# }
# 
# Error ex) 404 = id 불일치, 401 = 비밀번호 불일치
##########################################################
@router.patch("/{board_id:int}", response_model=schema.BoardUpdate)
def update_board_api(
    board_id: int, 
    update_data: schema.BoardUpdate, 
    password: str = Depends(get_current_user_password), 
    db: Session = Depends(get_db)
):
    updated_board = crud.update_board(db, id=board_id, password=password, update_data=update_data)
    return updated_board

##########################################################
# 게시글 삭제 API
# id, password를 입력받고 게시글 한 개를 삭제
# id는 URL에 Path Parameter로 명시, password는 Header에 'password'로 전달
# 성공하면 삭제한 Request body 반환, 실패하면 원인에 따라 상태 코드 반환
# URL ex) http://localhost:8000/board/15
# Header ex) 'password: pwd' 
# Response ex)
# {
#   "id": 0,
#   "title": "string",
#   "body": "string",
#   "username": "string",
#   "date": "2023-11-14T10:48:11.723Z",
#   "recomment": 0,
#   "disapproval": 0,
#   "views": 0,
#   "tag": "string"
# }
# Error ex) 404 = id 불일치, 401 = 비밀번호 불일치
##########################################################
@router.delete("/{board_id:int}", response_model=schema.BoardDelete)
def delete_board_api(
    board_id: int, 
    password: str = Depends(get_current_user_password), 
    db: Session = Depends(get_db)
):
    deleted_board = crud.delete_board(db, id=board_id, password=password)
    return deleted_board