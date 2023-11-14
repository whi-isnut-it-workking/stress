# database
문서 작성자 : 윤준현  
최종 수정자 : 윤준현  
최종 수정일 : 2023.11.14  
  
데이터베이스에 관련된 파일이 모여있는 디렉토리  

## db.py
DBMS에 연결, 세션을 생성하는 기본 db 설정 파일  
  
## db_config.json
db.py에서 DB에 접근하기 위해 읽어들이는 URL 정보가 담겨있는 json 파일.  
**!!!절 대 Github Public Repository에 올라가지 않도록 할 것!!!**  
.gitignore 파일에 'db_config*'으로 추가되어 있으므로 파일 이름을 똑같이 맞추어 외부에 공개되지 않도록 할 것.  
  
## db_setting_backup.json
db_config.json 파일의 형식만 저장해둔 파일.  
이 파일에 자신이 사용할 DB의 URL을 작성하고 파일 이름을 'db_config.json'으로 변경하여 사용한다.  

## board
게시판 기능을 담당하는 파일을 모아둔 폴더

## comment
댓글 기능을 담당하는 파일을 모아둔 폴더

## data
수집한 데이터를 처리하는 파일을 모아두는 폴더

## preprocessing
전처리를 담당하는 파일을 모아두는 폴더
