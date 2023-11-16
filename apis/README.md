# apis
문서 작성자 : 윤준현  
최종 수정자 : 윤준현  
최종 수정일 : 2023.11.16  
  
각 소스코드 안의 내용을 설명해둔 README
  
## board_router.py
게시글 기능을 담당하는 API  
  
공통 적용  
- response_model: Pydantic 모델을 반환해야 함. schema.~~ 사용
- {board_id:int}: Path Parameter의 type을 명시적으로 지정하는 FastAPI의 기능
- tags: FastAPI docs의 라우트별 태그 구분
  
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
  
### read_all_board_api
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
Error ex) 404 = id 불일치, 401 = 비밀번호 불일치
  
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
Error ex) 404 = id 불일치, 401 = 비밀번호 불일치   
