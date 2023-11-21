# database/comment
문서 작성자 : 윤준현  
최종 수정자 : 윤준현  
최종 수정일 : 2023.11.21  
  
댓글(Comment) 관련 DB 코드를 설명  
## schema.py
FastAPI에서 사용하는 Pydantic 모델을 정의  
Pydantic은 데이터 검증과 직렬화를 지원하는 라이브러리  
  
CommentBase: 모든 Comment 모델의 기본이 되는 모델로, 공통적으로 사용되는 설정들을 정의  
- orm_mode: Pydantic이 ORM(Object Relationship mapping) 모드를 사용하도록 설정하여, ORM에서 모델을 가져올 때 필요한 설정
- arbitrary_types_allowed: datetime과 같은 임의의 타입을 처리할 수 있도록 허용
  
Comment: 댓글의 기본적인 정보들을 담고 있는 모델  
id, body, username, date, board_index 댓글에 필요한 정보들을 포함  
board_index는 해당하는 게시글의 id인 Foreign key
  
CommentCreate: 댓글을 생성할 때 사용되는 모델로, CommentBase를 상속받아 필수 필드를 제공  
여기서 기본값(default)이 설정되어 있어, 이 모델을 사용할 때 일부 필드를 제외하고도 생성할 수 있다.  
  
CommentUpdate: 댓글 정보를 업데이트할 때 사용하는 모델  
필드가 모두 Optional이기 때문에 업데이트하려는 특정 필드만 변경할 수 있다.  
  
CommentDelete: 삭제할 때 사용되는 모델  
Comment 모델을 상속받고 있지만, 여기서는 추가적인 필드가 없으며 기본적으로 Comment와 동일한 필드를 가지고 있다.
## crud.py
FastAPI 애플리케이션에서 댓글(Comment) 데이터에 대한 CRUD 연산을 처리하기 위한 함수들을 담고 있다.  
각 함수는 SQLAlchemy를 통해 데이터베이스와 상호작용하며, 요청된 작업을 수행한다.  
  
공통 매개변수
- db(Session): 함수를 호출한 곳에서 넘겨 받는 DB 세션
- board_id(int): 게시글의 Primary key인 id
- comment_id(int): 댓글의 ID
- comment_password(str): 댓글의 비밀번호
  
response_error: HTTPException을 발생시키는 함수  
주어진 상태 코드와 상세 메시지를 받아 예외를 발생
- status_code(int): 상황에 맞는 적절한 상태 코드(401, 404 등)  
- detail(str): 적절한 에러 메시지  
  
check_board_by_id: 주어진 board_id에 해당하는 게시글이 데이터베이스에 있는지 확인하는 함수  
만약 없다면 404 상태 코드로 예외를 발생  
  
check_comment_by_password: 댓글의 비밀번호 일치 여부를 확인하는 함수  
주어진 댓글과 입력된 비밀번호를 비교하고, 일치하지 않으면 401 상태 코드로 예외를 발생  
- db_comment(Comment): 해당 Comment 타입의 댓글 객체
  
get_one_comment: 특정 board_id와 comment_id에 해당하는 댓글을 데이터베이스에서 조회  
없을 경우 404 상태 코드로 예외를 발생  
  
get_all_comments: 특정 board_id에 해당하는 모든 댓글을 데이터베이스에서 조회  
데이터베이스에 댓글이 없으면 빈 리스트를 반환  
  
create_comment: 새로운 댓글을 생성  
제공된 CommentCreate 모델의 인스턴스를 생성하고 데이터베이스에 추가한 후, 생성된 댓글을 반환
- comment(schema.CommentCreate): schema.py에 정의된 CommentCreate 모델의 인스턴스
  
update_comment: 특정 board_id와 comment_id에 해당하는 댓글을 업데이트  
주어진 댓글을 가져온 후, 비밀번호 일치 여부를 확인하고, 주어진 데이터로 필드를 업데이트하고 반환
- update_data(schema.CommentUpdate): 새로 업데이트할 schema.py에 정의된 CommentUpdate 모델의 인스턴스 데이터
  
delete_comment: 특정 board_id와 comment_id에 해당하는 댓글을 삭제  
주어진 댓글을 가져온 후, 비밀번호 일치 여부를 확인하고, 해당 댓글을 데이터베이스에서 삭제한 후 삭제된 댓글을 반환  