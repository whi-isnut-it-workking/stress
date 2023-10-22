# stress
캡스톤디자인 팀 '외않됀데?'의 팀프로젝트 주제 '텍스트 인사이트를 통한 트렌드 분석'의 웹 개발 프로젝트

문서 작성자 : ikaman
참여인원 : 3명  
작업 기간 : 2023.08.20~2023.11.27  
사용 기술 : Data analysis(Python), Frontend(HTML, CSS, JS), Backend(Python, FastAPI), Server(AWS EC2)  
  
프로젝트 목표:
1. Git, Github을 이용한 효율적인 협업 방식 학습
2. 웹 사이트를 실제로 서비스 가능한 MVP 수준까지 개발
3. 텍스트 데이터 분석의 기본적인 개념 및 개발 방법 학습
4. 클라우드 서비스를 이용한 서버 구축과 배포 방법 학습
5. 원활한 유지보수를 위한 문서화 습관 들이기
  
## How to Use
Required : Python 3.6+
  
### Install
터미널에 아래의 명령어를 입력하여 필요한 모듈을 설치한다.  
```
pip3 install fastapi uvicorn wordcloud matplotlib konlpy
```
- fastapi : 백엔드 API 개발에 사용하는 프레임워크(Node.js의 express)
- uvicorn : lightweight(매우 가벼운) ASGI 서버
    - fastapi framework만으로는 웹 개발을 할 수 없고, ASGI와 호환되는 웹 서버가 필요함
    - 비동기 방식이 가능한 python web server framework(Fastapi가 대표적)와 application 간의 표준 interface를 제공함
- wordcloud, matplotlib, konlpy : 데이터 분석에 필요한 모듈
  
### Start
터미널에 아래의 명령어를 입력하여 서버를 시작한다.
```
uvicorn main:app --reload
```
- main : 파일 main.py (파이썬 "모듈"). 확장자가 .py이라면 다른 이름으로도 가능하다.
- app : main.py 내부의 app = FastAPI() 줄에서 생성한 오브젝트. 오브젝트 이름을 app 이외의 다른 이름으로 선언했다면 그 이름을 사용한다.
- --reload : 코드 변경 후 서버 재시작. 개발에만 사용한다.
  
### Docs
FastAPI는 Swagger UI를 사용하여 자동 대화형 API 문서를 제공한다. 해당 문서에서 빠르게 API를 테스트할 수 있다.  
서버를 시작하고 아래의 링크를 브라우저에 입력하여 접속한다.  
python 파일을 저장하여 서버를 reload 해야 수정된 소스코드가 적용된다.  
  
http://127.0.0.1:8000/docs  
