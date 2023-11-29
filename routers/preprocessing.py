from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd
from sqlalchemy import Date, Text
import time
import re
from ckonlpy.tag import Twitter

from database.preprocessing import crud as crud_preprocessing
from database.data import crud as crud_data
from database.db import SessionLocal, engine
from database import models

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/preprocessing",
	tags=["Preprocessing"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        print("Preprocessing DB Session Connected")
        yield db
    finally:
        print("Preprocessing DB Session Closed")
        db.close()

#DB에 접근해서 전처리가 완료된 단어 데이터를 불러옴
@router.get("/read_data")
def read_data(db: Session = Depends(get_db)):
	raw_data = crud_preprocessing.get_items(db)
	return raw_data

#DB에 접근해서 전처리가 완료된 단어 데이터를 DB에 넣음
@router.post("/insert_data")
def insert_data(db: Session = Depends(get_db)):
	start = time.time()
	raw_data = crud_data.get_items(db)

	end = time.time()
	data = [item.__dict__ for item in raw_data]
	print(type(data))
	print(f"{end - start:.5f} sec")
	df = pd.DataFrame(data)
	df['combined_text'] = df['body'] + ' ' + df['title']

	# 명사를 추출하기 위해 텍스트를 결합한 후에 Okt를 사용합니다.
	with open(r"/Users/main/coding/stress/stress/lib/python3.11/site-packages/konlpy/java/addwords.txt",'r',encoding='utf-8') as f:
		words = f.read()

	wordss = words.split("\n")
	twitter = Twitter()
	twitter.add_dictionary(wordss, 'Noun')
	word = []
	association = []
	#wordcloud를 생성하기 위한 전처리 레코드를 생성
	with open('texts/ko_stopword.txt', 'r', encoding='utf-8') as f:
		stop_words = f.read()
	stop_words = stop_words.split("\n")
	start = time.time()
	c = 0
	for rec in df['combined_text']:
		#문장에 필요없는 특수기호 삭제
		rec = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", rec).lower()
		if c%100 == 0 : print(c)
		c = c+1
		#레코드 하나마다 명사 추출 적용
		stopped_tokens_w = [i for i in list(set(twitter.nouns(rec))) if not i in stop_words]
		word.append(','.join(stopped_tokens_w))
		#연관어 모델을 학습하기 위한 전처리 레코드 생성
		# 문장 구분을 위해 .으로 문장들을 나눠준다.
		sentences = rec.split(".")
		# 전체 문장을 저장하는 tokens
		tokens = []
		# 문장마다 토크나이즈한 후 tokens에 " "를 추가하고 저장
		for sentence in sentences :
			token = twitter.morphs(sentence, stem =True)
			token.append("겗룱")
			tokens = tokens + token
		stopped_tokens = [i for i in list(set(tokens)) if not i in stop_words]
		association.append(','.join(stopped_tokens))

	#df를 테이블 구조에 맞게 재설정
	end = time.time()
	print(f"{end - start:.5f} sec")
	preprodata = pd.DataFrame({'date':df['date'], 'for_wordcloud':word,'for_word_association_analysis':association})
	#try :
	preprodata.to_sql(name='preprocessing', con=engine, if_exists='append', index=False,
	dtype={
	'date' : Date,
		'for_worldcloud' : Text,
		'for_word_association_analysis' : Text
	})
	print("inset_success")

#DB에 접근해서 전처리가 완료된 단어 데이터를 DB에 넣음
@router.post("/insert_data_with_keyword")
def insert_data_with_keyowrd(db: Session = Depends(get_db), keyword : str = ""):
	start = time.time()
	raw_data = crud_data.get_items_with_keyword_for_preprocessing(db, keyword)

	end = time.time()
	data = [item.__dict__ for item in raw_data]
	print(type(data))
	print(f"{end - start:.5f} sec")
	df = pd.DataFrame(data)
	df['combined_text'] = df['body'] + ' ' + df['title']

	# 명사를 추출하기 위해 텍스트를 결합한 후에 Okt를 사용합니다.
	with open(r"/Users/main/coding/stress/stress/lib/python3.11/site-packages/konlpy/java/addwords.txt",'r',encoding='utf-8') as f:
		words = f.read()

	wordss = words.split("\n")
	twitter = Twitter()
	twitter.add_dictionary(wordss, 'Noun')
	word = []
	association = []
	#wordcloud를 생성하기 위한 전처리 레코드를 생성
	with open('texts/ko_stopword.txt', 'r', encoding='utf-8') as f:
		stop_words = f.read()
	stop_words = stop_words.split("\n")
	start = time.time()
	c = 0
	for rec in df['combined_text']:
		#문장에 필요없는 특수기호 삭제
		rec = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", rec).lower()
		if c%100 == 0 : print(c)
		c = c+1
		#레코드 하나마다 명사 추출 적용
		stopped_tokens_w = [i for i in list(set(twitter.nouns(rec))) if not i in stop_words]
		word.append(','.join(stopped_tokens_w))
		#연관어 모델을 학습하기 위한 전처리 레코드 생성
		# 문장 구분을 위해 .으로 문장들을 나눠준다.
		sentences = rec.split(".")
		# 전체 문장을 저장하는 tokens
		tokens = []
		# 문장마다 토크나이즈한 후 tokens에 " "를 추가하고 저장
		for sentence in sentences :
			token = twitter.morphs(sentence, stem =True)
			token.append("겗룱")
			tokens = tokens + token
		stopped_tokens = [i for i in list(set(tokens)) if not i in stop_words]
		association.append(','.join(stopped_tokens))

	#df를 테이블 구조에 맞게 재설정
	end = time.time()
	print(f"{end - start:.5f} sec")
	preprodata = pd.DataFrame({'date': df['date'], 'for_wordcloud': word[:len(df)], 'for_word_association_analysis': association[:len(df)]})
	#try :
	preprodata.to_sql(name='preprocessing', con=engine, if_exists='append', index=False,
	dtype={
	'date' : Date,
		'for_worldcloud' : Text,
		'for_word_association_analysis' : Text
	})
	print("inset_success")