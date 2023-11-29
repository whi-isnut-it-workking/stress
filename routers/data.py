from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd
from sqlalchemy import String, Date
from datetime import datetime
import os

from database.data import crud
from database.db import SessionLocal, engine
from database import models

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/data",
    tags=["Datas"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        print("Data DB Session Connected")
        yield db
    finally:
        print("Data DB Session Closed")
        db.close()


@router.get("/read_data")
def read_data(db: Session = Depends(get_db)):
	return crud.get_items(db)

#DB에 접근해서 csv파일을 한 번에 올림
@router.post("/insert_data")
def insert_data(db: Session = Depends(get_db)):
	# CSV 파일이 있는 폴더 경로를 지정합니다.
    folder_path = r'csvfiles'

    # 폴더 내의 모든 파일을 가져옵니다.
    files = os.listdir(folder_path)

    # 파일 중에서 .csv 파일만 골라냅니다.
    csv_files = [file for file in files if file.endswith('.csv')]

    # 파일 이름으로 정렬합니다.
    csv_files.sort()

    # 각각의 CSV 파일을 순서대로 읽어옵니다.
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path, encoding="utf-8", on_bad_lines='skip')
        #어떤 열이든 nan이 들어있으면 그 행을 지운다.
        df = df.dropna()
        df= df.astype('str')
        # '%Y.%m.%d' 형식의 날짜 데이터로 변환하는 함수 정의
        def parse_date(date_str):
            try:
                return datetime.strptime(date_str[:10], '%Y.%m.%d').date()
            except ValueError:
                # 오류 발생 시 처리
                return None  # 또는 오류 처리 로직을 추가하여 반환값을 조정

        # apply 함수를 이용하여 데이터프레임의 'date' 컬럼에 적용
        df['date'] = df['date'].apply(parse_date)
        df.rename(columns={"main": "body"}, inplace=True)
        #csv에 저장된 값이 완벽하게 오류가 걸러지지 않아서 try문으로 예외를 처리했다.
        try :
            #con 부분에는 db.session에 있는 engine을 넣어준다.
            #name은 테이블명이다.
            #if_exists는 이미 있는 테이블일 경우 어떻게 할 것인지 선택하는 파라미터다.
            #append : 기존 테이블에 값 추가
            #replace : 테이블 지우고 새로 생성 후 값 저장
            df.iloc[-10000:].to_sql(name='data', con=engine, if_exists='append', index=False,
            dtype={
            'date' : Date,
                'body' : String(20000),
                'section' : String(3),
                'url' : String(200),
                'title' : String(200)
            })
        except Exception as e :
            print(e)
            print(csv_file)
            continue
