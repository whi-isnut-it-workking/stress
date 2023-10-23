# stress
캡스톤디자인 팀 '외않됀데?'의 팀프로젝트 주제 '텍스트 인사이트를 통한 트렌드 분석'의 웹 개발 프로젝트

문서 작성자 : ikaman3  
참여인원 : 3명  
작업 기간 : 2023.09.20~2023.11.27  
사용 기술 : Data analysis(Python), Frontend(HTML, CSS, JS), Backend(Python, FastAPI), Server(AWS EC2)  
  
프로젝트 목표:
1. 웹 사이트를 실제로 서비스 가능한 POC（Proof of Concept)까지 개발
2. 텍스트 데이터 분석의 기본적인 개념 및 개발 방법 학습
3. 클라우드 서비스를 이용한 서버 구축과 배포 방법 학습
4. Git, Github을 이용한 효율적인 협업 방식 학습
5. 원활한 유지보수를 위한 문서화 습관 들이기
    
## How to Use
Required : Python 3.6+
  
### Install
터미널에서 프로젝트의 실행파일이 있는 경로까지 이동하고, 아래의 명령어를 입력하여 필요한 모듈을 설치한다.  
```
pip3 install fastapi uvicorn wordcloud matplotlib konlpy
```
- fastapi : 백엔드 API 개발에 사용하는 프레임워크(Node.js의 express)
- uvicorn : lightweight(매우 가벼운) ASGI 서버
    - fastapi framework만으로는 웹 개발을 할 수 없고, ASGI와 호환되는 웹 서버가 필요함
    - 비동기 방식이 가능한 python web server framework(Fastapi가 대표적)와 application 간의 표준 interface를 제공함
- wordcloud, matplotlib, konlpy : 데이터 분석에 필요한 모듈
  
### Run
터미널에 아래의 명령어를 입력하여 서버를 시작한다.
```
uvicorn main:app --reload
```
- main : 파일 main.py (파이썬 "모듈"). 확장자가 .py이라면 다른 이름으로도 가능하다.
- app : main.py 내부의 app = FastAPI() 줄에서 생성한 오브젝트. 오브젝트 이름을 app 이외의 다른 이름으로 선언했다면 그 이름을 사용한다.
- --reload : 코드 변경 후 서버 재시작. 개발에만 사용한다.
  
### API Test Docs
FastAPI는 Swagger UI를 사용하여 자동 대화형 API 문서를 제공한다. 해당 문서에서 빠르게 API를 테스트할 수 있다.  
서버를 시작하고 아래의 링크를 브라우저에 입력하여 접속한다.  
python 파일을 저장하여 서버를 reload 해야 수정된 소스코드가 적용된다.  
  
http://127.0.0.1:8000/docs  
    
## Git & Github collaboration
### How to Use Github
[Reference](https://velog.io/@dongvelop/Github-협업하기-PR부터-merge까지)  
  
Required : Github Oraganization을 만들고 레포지토리를 생성한다. 참여자들이 해당 레포지토리의 멤버로 등록되어야 한다.  

1. Fork : Github의 협업 계정 Repository에서 Fork 버튼을 눌러 자신의 레포지토리로 가져온다.
2. Clone 및 Remote : 자신의 레포지토리 주소를 로컬의 Git과 연결한다. (CLI, GUI 알아서 사용)
3. Branch : 원본 repository의 main 브랜치를 안전하게 관리하기 위해 반드시 dev 브랜치에서 작업하고 push한다. 
  - ```dev```라는 이름의 브랜치를 만들고, 체크아웃(브랜치 이동)까지 동시에 할 경우 : ```git checkout -b dev```
  - ```dev```라는 이름의 브랜치를 생성만 하고 싶을 경우 혹은 이미 생성된 ```dev``` 브랜치로 이동할 경우 : ```git checkout dev```
  - 브랜치 목록 조회 및 현재 작업 중인 브랜치 확인 : ```git branch```
4. 작업 후 add & commit & push : 자신의 레포지토리의 ```dev``` 브랜치에 작업을 하고 add & commit & push 한다. 이때 ```dev``` 브랜치에 push하는 것을 명시적으로 작성할 것
  - ```git push origin dev```
5. Pull Request(PR) : 4번까지 완료했다면 자신의 Github 레포지토리로 돌아가자. 초록색으로 Compare & pull request 버튼이 활성화되어 있을 것이다. 해당 버튼을 눌러 메시지를 작성하고 PR을 보내자.  
(이후로는 원본 저장소의 관리자가 할 일)
  
6. 코드 리뷰 및 Merge PR : 원본 저장소 관리자는 PR을 받으면 변경내역을 확인하고 Merge 여부를 결정한다.
  - Github Oraganization의 repository에 브랜치를 여러개 만드는 것이 아니었다. 협업 계정은 main 브랜치 하나만 유지하고 각자의 레포지토리에서 dev 브랜치로 작업하는 것
7. Merge 이후 동기화 및 branch 삭제 : 원본 저장소에 Merge가 완료되면 로컬 ```main``` 브랜치와 원본 저장소의 코드를 동기화해야 한다.
  - 현재 변경 사항은 dev 브랜치에서 작성하여 적용되었으니, main 브랜치도 내용을 동기화한다. 자신의 Github repository에 들어가 브랜치가 main임을 확인하고, Sync fork를 눌러 Update branch 버튼을 누르자.
  - 이후, 로컬에 있는 main 브랜치와도 동기화를 시키기 위해 아래 명령어를 실행하자.
  ```
      git checkout main
      git pull origin main
  ```
  - 로컬 브랜치 삭제(필수 아님) : ```git branch -D dev```
  - 원격 브랜치 삭제(필수 아님) : ```git push origin --delete dev```
8. 이후 작업 : 코딩하기 전에 항상 자신의 Github repository에서 Sync fork 버튼을 확인하고, 활성화되어 있다면 버튼을 눌러 동기화하자. 그리고 ```git pull origin main```을 통해 로컬과 동기화를 시킨 후 3번 ~ 7번 작업을 반복한다.
  
### Writing Commit Messages
[Reference](https://velog.io/@msung99/Git-Commit-Message-Convension)  
(나중에 작성)  
