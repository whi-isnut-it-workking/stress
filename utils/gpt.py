import os
import re
import urllib.request
from openai import OpenAI

# Papago Client ID & Secret
papago_client_id = os.getenv("NAVER_PAPAGO_CLIENT_ID") # 개발자센터에서 발급받은 Client ID 값
papago_client_secret = os.getenv("NAVER_PAPAGO_CLIENT_SECRET") # 개발자센터에서 발급받은 Client Secret 값
# GPT API key 설정
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

# Papago 이용해서 한국어를 영어로 번역하는 함수
def get_translate_KRtoEN(originalText: str) -> str:
    encText = urllib.parse.quote(originalText)
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",papago_client_id)
    request.add_header("X-Naver-Client-Secret",papago_client_secret)

    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        # 정규표현식을 사용하여 'translatedText' 뒤의 문자열 추출
        match = re.search(r'"translatedText":"([^"]+)"', response_body.decode('utf-8'))
        # 결과 출력
        if match:
            translated_text = match.group(1)
            # print(translated_text)
            return translated_text
        else:
            print("No match found")
            return "Null"
    else:
        print("Error Code:" + rescode)
        return "Papago Error"
        
# Papago 이용해서 영어를 한국어로 번역하는 함수
def get_translate_ENtoKR(originalText: str) -> str:
    encText = urllib.parse.quote(originalText)
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",papago_client_id)
    request.add_header("X-Naver-Client-Secret",papago_client_secret)

    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        # 정규표현식을 사용하여 'translatedText' 뒤의 문자열 추출
        match = re.search(r'"translatedText":"([^"]+)"', response_body.decode('utf-8'))
        # 결과 출력
        if match:
            translated_text = match.group(1)
            # print(translated_text)
            return translated_text
        else:
            print("No match found")
            return "Null"
    else:
        print("Error Code:" + rescode)
        return "Papago Error"

# GPT API 이용해서 답변을 받는 함수
def get_answer(translatedText: str):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer Gartner's IT analysis data questions. Please always respond in Korean"},
            {"role": "user", "content": translatedText}
        ]
    )

    # print(completion.choices[0].message)
    return(completion.choices[0].message.content)