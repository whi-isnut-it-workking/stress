from sqlalchemy.orm import Session

from database.board import board, schema
# Board 모델을 가져옴
Board = board.Board

# 특정 id에 해당하는 게시글 조회
def get_one_board(db: Session, id: int):
    return db.query(Board).filter(Board.id == id).first()

# 모든 게시글 조회
def get_all_board(db: Session):
    return db.query(Board).all()

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

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user