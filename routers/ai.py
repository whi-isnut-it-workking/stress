from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd
from gensim.models.word2vec import Word2Vec
import re
import json
from konlpy.tag import Okt
from keras.utils import pad_sequences
from keras.preprocessing.text import Tokenizer
import pickle
import keras

from database.preprocessing import crud
from database.db import SessionLocal, engine
from database import models
from routers.wordcloud import mk_association_c

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/ai",
	tags=["AIs"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        print("AI DB Session Connected")
        yield db
    finally:
        print("AI DB Session Closed")
        db.close()

#연관어 모델 학습
#학습 전체 데이터 불러오기 - db에서 전처리가 완료된 데이터를 가져온다.
@router.post("/train_ass_model")
def train_ass_model(db: Session = Depends(get_db)):
    raw_data = crud.get_items(db)
    
    data = [item.__dict__ for item in raw_data]
    df = pd.DataFrame(data)
    total_data = ""
    for raw in df['for_word_association_analysis'] :
        total_data = total_data + raw
    #' '로 split을 실행해준다.
    temp1 = total_data.split('겗룱')
    sentences = []
    for temp2 in temp1 :
        sentences.append(temp2.split(','))
    model = Word2Vec(sentences, sg=1, window=2, min_count=3)
    model.init_sims(replace=True)
    model.save("association_model.model")
    print("훈련완료")
    
#연관어 모델 결과 출력
@router.get("/result_ass_model")
def result_ass_model(keyword : str = ""):
	model = Word2Vec.load("association_model.model")
	temp = model.wv.most_similar(keyword, topn=20)
	result = []
	for rec in temp :
		result.append([keyword, rec[0],rec[1]])
	return result

#감성분석 모델 결과 출력
@router.get("/result_emo_model")
def result_emo_model(db: Session = Depends(get_db), keyword : str = ""):
	okt = Okt()
	tokenizer  = Tokenizer()

	DATA_CONFIGS = '/data_configs.json'
	prepro_configs = json.load(open(r'CLEAN_DATA'+DATA_CONFIGS,'r', encoding='utf-8'))

	with open(r'CLEAN_DATA/tokenizer.pickle','rb') as handle:
		word_vocab = pickle.load(handle)

	with open('texts/ko_stopword.txt', 'r', encoding='utf-8') as f:
		stop_words = f.read()
	stop_words = stop_words.split("\n")

	prepro_configs['vocab'] = word_vocab

	tokenizer.fit_on_texts(word_vocab)

	MAX_LENGTH = 8 #문장최대길이

	#연관어 검색 결과 리스트, 빈도수
	c = mk_association_c(db, keyword)
	#연관어 결과의 긍/부정 딕셔너리 생성
	result = {'긍정' : [], '부정' : []} #학습한 모델 불러오기
	model = keras.models.load_model(r'emotion_model')
	model.load_weights(r'cnn_classifier_kr/weights.h5')
	for sentence in c :
		try :
			sentence_c = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣\\s ]','', sentence[0])
			sentence_c = okt.morphs(sentence_c, stem=True) # 토큰화
			sentence_c = [word for word in sentence_c if not word in stop_words] # 불용어 제거
			vector  = tokenizer.texts_to_sequences(sentence_c)
			pad_new = pad_sequences(vector, maxlen = MAX_LENGTH) # 패딩

		
			predictions = model.predict(pad_new)
			predictions = float(predictions.squeeze(-1)[0])
			if(predictions > 0.5): 
				result['긍정'].append([sentence[0],sentence[1]])
			else :
				result['부정'].append([sentence[0],sentence[1]])
		except Exception as e :
			print(e)
			continue
	return result
