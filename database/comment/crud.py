from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from database.comment import schema
from database import models

# 모델 가져오는 부분
Board = models.Board
Comment = models.Comment

# Error Message 모음
BOARD_NOT_FOUND = "게시글이 존재하지 않음"
COMMENT_NOT_FOUND = "댓글이 존재하지 않음"
PASSWORD_NOT_MATCH = "비밀번호가 일치하지 않음"

# Status Code
STATUS_CODE_404 = 404
STATUS_CODE_401 = 401

# Error Response
def response_error(status_code: int, detail: str):
    raise HTTPException(status_code=status_code, detail=detail)
## 게시글이 존재하는지 확인
def check_board_by_id(db: Session, board_id: int):
    try: 
        db.query(Board).filter(Board.id == board_id).one()
    except:
        response_error(STATUS_CODE_404, BOARD_NOT_FOUND)
## 댓글의 비밀번호가 불일치면 에러
def check_comment_by_password(db_comment: Comment, comment_password: str):
    if db_comment.password != comment_password: 
        response_error(STATUS_CODE_401, PASSWORD_NOT_MATCH)

# 특정 id에 해당하는 댓글 읽기
def get_one_comment(db: Session, comment_id: int, board_id: int):
    check_board_by_id(db, board_id)

    try: # id가 일치하는 댓글 한 개 읽기
        comments = (
            db.query(Comment)
            .filter(Comment.board_index == board_id, Comment.id == comment_id)
            .one()
        )
    except:
        response_error(STATUS_CODE_404, COMMENT_NOT_FOUND)

    return comments

# 모든 댓글 조회: 댓글이 존재하지 않으면 반환되는 List가 텅 비어있음
def get_all_comments(db: Session, board_id: int):
    check_board_by_id(db, board_id)

    comments = (
        db.query(Comment)
        .filter(Comment.board_index == board_id)
        .all()
    )
    
    return comments

# 댓글 생성
def create_comment(db: Session, comment: schema.CommentCreate, board_id: int):
    check_board_by_id(db, board_id)

    # 기본값이 존재하는 CommentCreate 모델의 인스턴스를 생성
    db_comment = Comment(
        body=comment.body,
        username=comment.username,
        password=comment.password,
        board_index=board_id
    )

    # 변경사항을 커밋
    db.add(db_comment)
    db.commit()
    # 데이터베이스로부터 최신 정보로 새로운 댓글을 리프레시
    db.refresh(db_comment)
    # 생성된 댓글 반환
    return db_comment

# 댓글 업데이트
def update_comment(db: Session, comment_id: int, comment_password: str, update_data: schema.CommentUpdate, board_id: int):
    db_comment = get_one_comment(db, comment_id, board_id)

    check_comment_by_password(db_comment, comment_password)
    
    # 주어진 데이터로 필드를 업데이트
    for field, value in update_data.__dict__.items():
        if value is not None:
            setattr(db_comment, field, value)

    # 데이터베이스에 변경사항을 커밋
    db.commit()
    # 최신 변경 내용을 반영하기 위해 댓글 인스턴스를 리프레시
    db.refresh(db_comment)
    return db_comment

# 댓글 삭제
def delete_comment(db: Session, board_id: int, comment_id: int, comment_password: str):
    db_comment = get_one_comment(db, comment_id, board_id)
    
    check_comment_by_password(db_comment, comment_password)

    db.delete(db_comment)
    db.commit()
    return db_comment