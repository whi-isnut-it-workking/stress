from fastapi import APIRouter, Depends, Header
import datetime
import requests
from bs4 import BeautifulSoup
import random

from utils.gpt import get_translate_KRtoEN, get_translate_ENtoKR, get_answer

router = APIRouter(
    prefix="/utils",
    tags=["Utils"]
)

# Header
def get_password_from_header(password: str = Header(...)):
    return password

def get_current_user_password(password: Header = Depends(get_password_from_header)):
    return password

# Functions

SID1_IT = 105 # 분야: IT/과학
# 세부 분야: IT/과학 밑의 모바일, 인터넷 등 분야 밑의 세부 분야
SID2_IT = [731, 226, 227, 230, 732, 283, 229, 228]

### 뉴스 분야(sid1)와 세부 분야(sid2), 페이지(page), 날짜(date)를 입력하면 그에 대한 링크들을 리스트로 추출하고, 리스트 반환하는 함수 ###
def ex_tag(sid1, sid2, page, date):
    ## 1.
    url = f"https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1={sid1}&sid2={sid2}&date={date}&page={page}"
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")
    a_tag = soup.find_all("a")
    
    ## 2.
    tag_lst = []
    for a in a_tag:
        if "href" in a.attrs:  # href가 있는것만 고르는 것
            if (f"sid={sid1}" in a["href"]) and ("article" in a["href"]):
                tag_lst.append(a["href"])
    
    return tag_lst

def art_crawl(href):
    art_dic = {}
    
    ## 1.
    title_selector = "#title_area > span"
    # image_selector = "#img1"  # 이미지 선택자 추가

    url = href
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0\
        (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)\
        Version/17.0 Safari/605.1.15"})
    soup = BeautifulSoup(html.text, "lxml")
    
    ## 2.
    # 제목 수집
    title = soup.select(title_selector)
    title_lst = [t.text for t in title]
    title_str = "".join(title_lst)
    
    ## 3.
    # 이미지 URL 수집
    # image = soup.select_one(image_selector)
    # if image and image.has_attr("src"):  # 이미지가 있을 경우에만 URL 가져오기
    #     image_url = image["src"]  # 이미지 태그에서 src 속성 가져오기
    # else:
    #     image_url = None
    
    art_dic["href"] = href
    art_dic["title"] = title_str
    # art_dic["image_url"] = image_url

    # print(art_dic["href"] , art_dic["title"], art_dic["image_url"])
    print(art_dic["href"] , art_dic["title"])
    return art_dic

# APIs
@router.get("/gpt")
def gpt_answer(question: str):
    # questionEN = get_translate_KRtoEN(question)
    # answerEN = get_answer(questionEN)
    # answerKR = get_translate_ENtoKR(answerEN)
    answerKR = get_answer(question)
    return answerKR

@router.get("/news")
def get_news():
    # 스크랩 날짜 생성 (년, 월, 일을 순서대로 넣어주세요)
    today = datetime.date.today()
    date = today.strftime("%Y%m%d")
    sid2s_IT = random.choice(SID2_IT)

    all_hrefs = ex_tag(SID1_IT, sid2s_IT, page=1, date=date)
    # 중복 제거
    re_set = set(all_hrefs)
    re_lst = list(re_set)
    news_list = []
    for i in range(5):
        news_list.append(art_crawl(re_lst[i]))
    
    return news_list