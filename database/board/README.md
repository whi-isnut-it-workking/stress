# database/board
문서 작성자 : 윤준현  
최종 수정자 : 윤준현  
최종 수정일 : 2023.11.20  
  
board 관련 DB 코드를 설명  
## schema.py
FastAPI에서 사용하는 Pydantic 모델을 정의  
Pydantic은 데이터 검증과 직렬화를 지원하는 라이브러리  
  
BoardBase: 모든 Board 모델의 기본이 되는 모델로, 공통적으로 사용되는 설정들을 정의  
- orm_mode: Pydantic이 ORM(Object Relationship mapping) 모드를 사용하도록 설정하여, ORM에서 모델을 가져올 때 필요한 설정
- arbitrary_types_allowed: datetime과 같은 임의의 타입을 처리할 수 있도록 허용
  
Board: 게시판의 기본적인 정보들을 담고 있는 모델  
id, title, body, username, date 등 게시판에 필요한 정보들을 포함  
몇 가지 필드는 Optional(선택적)일 수 있으며, tag는 선택적인 문자열 필드임  
  
BoardCreate: 게시판을 생성할 때 사용되는 모델로, BoardBase를 상속받아 필수 필드를 제공  
여기서 기본값(default)이 설정되어 있어, 이 모델을 사용할 때 일부 필드를 제외하고도 생성할 수 있다.  
  
BoardUpdate: 게시판 정보를 업데이트할 때 사용하는 모델  
필드들이 모두 Optional이기 때문에 업데이트하려는 특정 필드만 변경할 수 있다.  
  
BoardDelete: 삭제할 때 사용되는 모델  
Board 모델을 상속받고 있지만, 여기서는 추가적인 필드가 없으며 기본적으로 Board와 동일한 필드를 가지고 있다.  
  
이 모델들을 통해 요청된 데이터가 예상대로 구조화되고 유효한지 검증하고, 응답할 때도 일관된 형식으로 데이터를 반환할 수 있다.  
## crud.py
FastAPI 애플리케이션에서 게시글(Board) 데이터에 대한 CRUD 연산을 처리하기 위한 함수들을 담고 있다.  
각 함수는 SQLAlchemy를 통해 데이터베이스와 상호작용하며, 요청된 작업을 수행한다.  
  
공통 매개변수
- db(Session): 함수를 호출한 곳에서 넘겨 받는 DB 세션
- id(int): 게시글의 Primary key인 id
- password(str): 게시글의 비밀번호
  
response_error: HTTPException을 발생시키는 함수  
주어진 상태 코드와 상세 메시지를 받아 예외를 발생시킨다.  
- status_code(int): 상황에 맞는 적절한 상태 코드(401, 404 등)  
- detail(str): 적절한 에러 메시지  
  
check_board_by_password: 게시글의 비밀번호 일치 여부를 확인하는 함수  
주어진 게시글과 입력된 비밀번호를 비교하고, 일치하지 않으면 401 상태 코드로 예외를 발생시킨다.  
- db_board(Board): Board 타입의 게시글 객체
  
get_one_board: 특정 ID에 해당하는 게시글을 데이터베이스에서 조회  
해당 ID에 해당하는 게시글이 없을 경우 404 상태 코드로 예외를 발생  
  
get_all_board: 모든 게시글을 데이터베이스에서 조회  
DB에 게시글이 없을 경우 빈 리스트를 반환  
  
create_board: 새로운 게시글을 데이터베이스에 생성  
제공된 BoardCreate 모델의 인스턴스를 생성하고 데이터베이스에 추가한 후, 생성된 게시글을 반환  
- board(schema.BoardCreate): schema.py에 정의된 BoardCreate 모델의 인스턴스
  
update_board: 특정 ID에 해당하는 게시글을 업데이트  
주어진 ID에 해당하는 게시글을 가져온 후, 비밀번호 일치 여부를 확인하고, 주어진 데이터로 필드를 업데이트하고 반환  
- update_data(schema.BoardUpdate): schema.py에 정의된 BoardUpdate 모델의 인스턴스  
  
delete_board: 특정 ID에 해당하는 게시글을 삭제  
주어진 ID에 해당하는 게시글을 가져온 후, 비밀번호 일치 여부를 확인하고, 해당 게시글을 데이터베이스에서 삭제한 후 삭제된 게시글을 반환  