from typing import Union
from fastapi import FastAPI
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt
from PIL import Image
import numpy as np
import konlpy
from konlpy.tag import Komoran

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/test")
def test() :
    with open('testfile.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    okt = Okt(max_heap_size= 1024 * 6)
    nouns = okt.nouns(text) # 명사만 추출

    words = [n for n in nouns if len(n) > 1] # 단어의 길이가 1개인 것은 제외

    c = Counter(words) # 위에서 얻은 words를 처리하여 단어별 빈도수 형태의 딕셔너리 데이터를 구함
    return c