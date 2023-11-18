# apis
문서 작성자 : 윤준현  
최종 수정자 : 윤준현  
최종 수정일 : 2023.11.19  
  
API 라우터 내용을 설명해둔 README  
  
공통 정보  
- response_model: Pydantic 모델을 반환해야 함. schema.~~ 사용
- {board_id:int}: Path Parameter의 type을 명시적으로 지정하는 FastAPI의 기능
- tags: FastAPI docs의 라우트별 태그 구분
  
## board_router.py
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
## comment_router.py
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