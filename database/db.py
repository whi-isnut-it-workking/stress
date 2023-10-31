from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

with open("database/db_config.json", "r") as f:
    dbConfig = json.load(f)

# MySQL 데이터베이스 연결 설정
DATABASE_URL = f"{dbConfig['dbms']}+{dbConfig['driver']}://{dbConfig['user']}:{dbConfig['password']}@{dbConfig['host']}:{dbConfig['port']}/{dbConfig['database']}?charset=utf8"

engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()