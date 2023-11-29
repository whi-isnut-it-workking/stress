from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd
from wordcloud import WordCloud
import base64
from io import BytesIO
from collections import Counter

from database.preprocessing import crud
from database.db import SessionLocal, engine
from database import models

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/wordcloud",
    tags=["Wordclouds"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        print("Wordcloud DB Session Connected")
        yield db
    finally:
        print("Wordcloud DB Session Closed")
        db.close()

def mk_association_c(db, keyword):
 #db에서 전처리가 완료된 데이터를 가져온다.
    raw_data = crud.get_items_with_keyword_for_association(db,keyword)
    #검색 결과가 없을 경우 -1 반환
    if raw_data == [] :
        return -1
    else :
        #db에서 가져온 데이터를 사용할 수 있게 리스트형태로 변형한다.
        data = [item.__dict__ for item in raw_data]
        df = pd.DataFrame(data)
        #전체 데이터를 1차원 배열로 만들다.
        total_data = ""
        for raw in df['for_wordcloud'] :
            total_data = total_data + "," + raw.strip()
        #','로 split을 실행해준다.
        words = total_data.split(',')
        result = Counter(words)
        del result[keyword]
        return result.most_common(20)

@router.get("/make_wordcloud")
def make_wordcloud(db: Session = Depends(get_db), keyword : str = "", wd : int = 200, hg : int = 200):
    #db에서 전처리가 완료된 데이터를 가져온다.
    raw_data = crud.get_items_with_keyword_for_wc(db, keyword)
    #검색 결과가 없을 경우 -1 반환
    if raw_data == [] :
        return -1
    else :
        #db에서 가져온 데이터를 사용할 수 있게 리스트형태로 변형한다.
        data = [item.__dict__ for item in raw_data]
        df = pd.DataFrame(data)
        #전체 데이터를 1차원 배열로 만들다.
        total_data = ""
        for raw in df['for_wordcloud'] :
            total_data = total_data + "," + raw.strip()
        #','로 split을 실행해준다.
        words = total_data.split(',')
        c = Counter(words) # 위에서 얻은 words를 처리하여 단어별 빈도수 형태의 딕셔너리 데이터를 구함
        del c[keyword]
        wc = WordCloud(font_path='/Library/Fonts/AppleGothic.ttf', width=wd, height=hg, scale=2.0, max_font_size=250)
        gen = wc.generate_from_frequencies(c)
        image = wc.to_image()
        image.save("wordcloud.png")  # 워드 클라우드를 이미지로 저장

         # 이미지를 바이트로 변환
        img_bytes = BytesIO()
        image.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
    
        # 바이너리 데이터를 base64로 인코딩하여 URL 생성
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        img_url = f'data:image/png;base64,{img_base64}'

        return img_url  # 이미지 URL 반환
    