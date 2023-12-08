# apis
문서 작성자 : 윤준현  
최종 수정자 : 윤준현  
최종 수정일 : 2023.12.07  
  
API 라우터 내용을 설명해둔 README  
  
공통 정보  
- response_model: Pydantic 모델을 반환해야 함. schema.~~ 사용
- {board_id:int}: Path Parameter의 type을 명시적으로 지정하는 FastAPI의 기능
- tags: FastAPI docs의 라우트별 태그 구분
  
## board.py
게시글 기능을 담당하는 API  
### read_one_board_api
id와 일치하는 게시글 한 개를 읽는 API  
일치하는 id가 없을 경우 상태 코드 404 반환  
URL ex) http://localhost:8000/board/14  
Response ex)  
```
{
    "id": 14,
    "title": "title",
    "body": "body",
    "username": "ㅇㅇ",
    "date": "2023-11-14T11:14:51",
    "recomment": 0,
    "disapproval": 0,
    "views": 0,
    "tag": "string"
}
```
### read_all_boards_api
모든 게시글을 읽는 API  
존재하는 게시글이 없을 경우 빈 리스트([]) 반환  
URL ex) http://localhost:8000/board/all  
Response ex)  
```
[
  {
    "id": 14,
    "title": "title",
    "body": "body",
    "username": "ㅇㅇ",
    "date": "2023-11-14T11:14:51",
    "recomment": 0,
    "disapproval": 0,
    "views": 0,
    "tag": "string"
  },
  {
    "id": 15,
    "title": "title",
    "body": "body",
    "username": "ㅇㅇ",
    "date": "2023-11-14T18:04:41",
    "recomment": 0,
    "disapproval": 0,
    "views": 0,
    "tag": "#Test #IT #고토히토리 #後藤ひとり"
  }
]
```
### create_board_api
게시글 생성 API  
생성에 성공할 경우 생성한 Request body 반환  
실패할 경우 상황별 에러 상태 코드 반환  
URL ex) http://localhost:8000/board  
Request body ex)  
```
{
  "title": "title",
  "body": "body",
  "username": "ㅇㅇ",
  "password": "pwd"
}
```
Required: title, body, username, password  
Optional: tag  
Response ex)  
```
{
  "title": "title",
  "body": "body",
  "username": "ㅇㅇ",
  "password": "pwd",
  "tag": null
}
```
### update_board_api
게시글 수정 API  
id, password를 입력받고 Request body에 입력한 부분만 업데이트  
id는 URL에 Path Parameter로 명시, password는 Header에 'password'로 전달  
제목, 본문, 태그만 변경 가능  
성공하면 업데이트한 요청 반환, 실패하면 실패 원인에 따라 상태 코드 반환  
URL ex) http://localhost:8000/board/14  
Header ex) 'password: pwd'  
Request body ex)  
```
{
  "title": "변경한 제목",
  "body": "변경한 내용",
  "tag": "#Updated"
}
```  
Required: 없음  
Optional: title, body, tag  
Response ex)  
```
{
  "title": "변경한 제목",
  "body": "변경한 내용",
  "tag": "#Updated"
}
```  
### delete_board_api
게시글 삭제 API  
id, password를 입력받고 게시글 한 개를 삭제  
id는 URL에 Path Parameter로 명시, password는 Header에 'password'로 전달  
성공하면 삭제한 Request body 반환, 실패하면 원인에 따라 상태 코드 반환  
URL ex) http://localhost:8000/board/15  
Header ex) 'password: pwd'  
Response ex)  
```
{
  "id": 0,
  "title": "string",
  "body": "string",
  "username": "string",
  "date": "2023-11-14T10:48:11.723Z",
  "recomment": 0,
  "disapproval": 0,
  "views": 0,
  "tag": "string"
}
```  
### increment_like
추천 수를 1 증가  
### increment_dislike
비추천 수를 1 증가

## comment.py
댓글 기능 담당 API  
  
### read_one_comment_api
id와 일치하는 댓글 한 개를 읽는 API  
댓글의 id(comment_id), 게시글 id(board_id)와 일치하는 댓글 1개를 읽음  
성공하면 Request body 반환, 실패하면 원인에 따라 상태 코드 반환  
URL ex) http://localhost:8000/board/23/comment/18  
Response ex)  
```
{
  "id": 18,
  "body": "시팔 게시글에 시팔번 댓글",
  "username": "ㅇㅇ",
  "date": "2023-11-18T23:57:10",
  "board_index": 23
}
```  
### read_all_comments_api
특정 게시글의 모든 댓글을 읽는 API  
게시글 id를 받고 해당 게시글의 모든 댓글을 읽음  
해당 게시글에 댓글이 없다면 빈 리스트 반환  
URL ex) http://localhost:8000/board/23/comment/all  
Response ex)  
```
[
  {
    "id": 18,
    "body": "시팔 게시글에 시팔번 댓글",
    "username": "ㅇㅇ",
    "date": "2023-11-18T23:57:10",
    "board_index": 23
  },
  {
    "id": 19,
    "body": "잘되냐1",
    "username": "ㅇㅇ",
    "date": "2023-11-18T23:57:10",
    "board_index": 23
  }
]
```  
### create_comment_api
댓글 생성 API  
게시글 id를 받고, 해당 게시글 id를 FK로 하는 댓글 생성  
URL ex) http://localhost:8000/board/28/comment  
Request body ex)  
```
{
  "body": "body",
  "username": "ㅇㅇ",
  "password": "pwd"
}
```
Response ex)  
```
{
  "body": "body",
  "username": "ㅇㅇ",
  "password": "pwd"
}
```  
### update_comment_api
댓글 수정 API  
게시글 id, 댓글 id, 댓글 비밀번호(password)를 받고 댓글을 수정  
password는 Header에 'password'로 전달  
URL ex) http://localhost:8000/board/28/comment/25  
Header ex) 'password: pwd'  
Request body ex)  
```
{
  "body": "변경된 댓글 내용"
}
```
Response ex)  
```
{
  "body": "변경된 댓글 내용"
}
```  
### delete_comment_api
댓글 삭제 API  
게시글 id, 댓글 id, 댓글 비밀번호(password)를 받고 댓글을 삭제  
password는 Header에 'password'로 전달  
URL ex) http://localhost:8000/board/28/comment/25  
Header ex) 'password: pwd'  
Response ex)  
```
{
  "id": 25,
  "body": "변경된 댓글 내용",
  "username": "ㅇㅇ",
  "date": "2023-11-19T00:56:51",
  "board_index": 28
}
```  
## utils.py
기타 기능을 위한 API  
### gpt_answer
GPT API를 사용해서 답변을 받아옴  
Gartner의 IT 데이터를 기반으로 답하라고 명령한 상태  
URL에 Path Parameter 'question'에 질문 입력  
반환된 문자열에 이스케이프 문자 \\n이 들어있으므로, 사용하기 전에 "\\n"을 "\n"으로 치환해야 함  
```answerKR = answerKR.replace("\\n", "\n")```  
Response ex)  
```
"GPT의 답변\n\n1.어쩌고\n\n2.저쩌고..."
```  

## data.py
DB data 테이블에 수집한 데이터를 삽입하는 API  
### read_data
data 테이블의 모든 레코드를 읽음  
### insert_data
특정 폴더에 있는 csv 파일을 읽어서 data 테이블에 삽입  
  
## preprocessing.py
data 테이블의 레코드를 읽어서 전처리 후 preprocessing 테이블의 레코드를 관리하는 API  
### read_data
data 테이블로부터 레코드를 읽고 전처리가 완료된 단어 데이터를 불러옴  
### insert_data
data 테이블로부터 레코드를 읽고 전처리가 완료된 단어 데이터를 preprocessing 테이블에 넣음  
### insert_data_with_keyowrd
data 테이블로부터 레코드를 읽고 전처리가 완료된 단어 데이터를 preprocessing 테이블에 넣음  

## wordcloud.py
### make_wordcloud
워드클라우드를 생성하는 API  

## ai.py
연관어 분석 관련 API
### train_ass_model
preprocessing 테이블에서 전처리가 완료된 데이터를 읽고, 연관어 모델을 학습
### result_ass_model
학습된 모델을 사용해 연관어 분석 결과를 출력
### result_emo_model
학습된 모델을 사용해 감성 분석 결과를 출력