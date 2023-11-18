from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.board import schema
from database import models
# Board 모델 가져옴
Board = models.Board

# Error Message 모음
BOARD_NOT_FOUND = "게시글이 존재하지 않음"
PASSWORD_NOT_MATCH = "비밀번호가 일치하지 않음"

# Status Code
STATUS_CODE_404 = 404
STATUS_CODE_401 = 401

# Error Response
def response_error(status_code, detail: str):
    raise HTTPException(status_code=status_code, detail=detail)
## password가 일치하지 않음. 401 응답 반환
def check_board_by_password(db_board: Board, password: str):
    if db_board.password != password: 
        response_error(STATUS_CODE_401, PASSWORD_NOT_MATCH)

# 특정 id에 해당하는 게시글 조회
def get_one_board(db: Session, id: int):
    try: # 주어진 id에 해당하는 게시글이 없을 경우 404 응답 반환
        db_board = db.query(Board).filter(Board.id == id).one()
    except:
        response_error(STATUS_CODE_404, BOARD_NOT_FOUND)
    
    return db_board

# 모든 게시글 조회: 게시글이 존재하지 않으면 반환되는 List가 텅 비어있음
def get_all_board(db: Session):
    return db.query(Board).all()

# 게시글 생성
def create_board(db: Session, board: schema.BoardCreate):
    # 기본값이 존재하는 BoardCreate 모델의 인스턴스를 생성
    db_board = Board(
        title=board.title,
        body=board.body,
        username=board.username,
        password=board.password,
        tag=board.tag
    )

    # 변경사항을 커밋
    db.add(db_board)
    db.commit()
    # 데이터베이스로부터 최신 정보로 새로운 게시글을 리프레시
    db.refresh(db_board)
    # 생성된 게시글 반환
    return db_board

# 게시글 업데이트
def update_board(db: Session, id: int, password: str, update_data: schema.BoardUpdate):
    db_board = get_one_board(db, id)
    
    check_board_by_password(db_board, password)
    
    # 주어진 데이터로 필드를 업데이트
    for field, value in update_data.__dict__.items():
        if value is not None:
            setattr(db_board, field, value)

    # 데이터베이스에 변경사항을 커밋
    db.commit()
    # 최신 변경 내용을 반영하기 위해 게시글 인스턴스를 리프레시
    db.refresh(db_board)
    return db_board

# 게시글 삭제
def delete_board(db: Session, id: int, password: str):
    db_board = get_one_board(db, id)
    
    check_board_by_password(db_board, password)
    
    db.delete(db_board)
    db.commit()
    return db_board