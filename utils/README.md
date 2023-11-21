# utils
문서 작성자 : 윤준현  
최종 수정자 : 윤준현  
최종 수정일 : 2023.11.21  
  
프로젝트에 필요한 부가 기능을 모아둔 디렉토리에 대한 설명  
## gpt.py
GPT API를 사용해서 사용자의 질문을 받고 답변을 반환하는 코드  

### API keys
API를 사용할 때 필요한 고유한 Key  
환경 변수로부터 가져와서, 코드를 실행하는 환경에 따라 각 API에 대한 인증 정보를 환경 변수로 설정해야 한다.  
.bashrc, .zshrc 등에 해당 명령어를 채워넣고 적용한다.  
ex)  
```export OPENAI_API_KEY="..."```  
```source .zshrc```  

### get_translate_KRtoEN
Papago 이용해서 한국어를 영어로 번역하는 함수  
- originalText(str) : 한국어를 문자열로 입력 받는다.

### get_translate_ENtoKR
Papago 이용해서 영어를 한국어로 번역하는 함수  
- originalText(str) : 영어를 문자열로 입력 받는다.

### get_answer
GPT API 이용해서 질문을 받고 답변을 반환하는 함수    
시스템 규칙으로 Gartner의 IT 분석 데이터에 관한 질문에 답변하도록 설정해두었다.  
- translatedText(str) : 사용자의 질문이 최종적으로 영어 번역된 문자열