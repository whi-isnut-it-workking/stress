from sqlalchemy.orm import Session

from database.board import board, schema

def get_board(db: Session):
    return db.query(board.Board).all()

def create_board(db: Session, board: schema.BoardCreate):
    fake_hashed_password = board.password + "notreally"
    db_board = board.Board(title="Random title", body="한글로 작성한 본문", password=fake_hashed_password)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
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