from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.board import schema
from database import models
# Board 모델 가져옴
Board = models.Board

# Error 모음
def response404():
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
def response401():
    raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.") 

# 특정 id에 해당하는 게시글 조회
def get_one_board(db: Session, id: int):
    db_board = db.query(Board).filter(Board.id == id).first()
    if not db_board: # 주어진 id에 해당하는 게시글이 없을 경우 404 응답 반환
        response404()
    return db_board

# 모든 게시글 조회: 게시글이 존재하지 않으면 반환되는 List가 텅 비어있음
def get_all_board(db: Session):
    db_board_list = db.query(Board).all()
    return db_board_list

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
    # get_one_board 함수를 사용하여 게시글을 가져옴
    existing_board = get_one_board(db, id)
    if not existing_board: # 주어진 id에 해당하는 게시글이 없을 경우 404 응답 반환
        response404()
    if existing_board.password != password: # password가 일치하지 않음. 401 응답 반환
        response401()
    
    # 주어진 데이터로 필드를 업데이트
    for field, value in update_data.__dict__.items():
        if value is not None:
            setattr(existing_board, field, value)

    # 데이터베이스에 변경사항을 커밋
    db.commit()
    # 최신 변경 내용을 반영하기 위해 게시글 인스턴스를 리프레시
    db.refresh(existing_board)
    return existing_board

# 게시글 삭제
def delete_board(db: Session, id: int, password: str):
    # get_one_board 함수를 사용하여 게시글을 가져옴
    existing_board = get_one_board(db, id)
    if not existing_board: # 주어진 id에 해당하는 게시글이 없을 경우 404 응답 반환
        response404() 
    if existing_board.password != password: # password가 일치하지 않음. 401 응답 반환
        response401()
    
    db.delete(existing_board)
    db.commit()
    return existing_board