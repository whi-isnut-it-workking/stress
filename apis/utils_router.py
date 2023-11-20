from fastapi import APIRouter, Depends, Header

from utils.gpt import get_translate_KRtoEN, get_translate_ENtoKR, get_answer

# URL 앞을 /board/{board_id:int}/comment로 지정
router = APIRouter(
    prefix="/utils"
)

def get_password_from_header(password: str = Header(...)):
    return password

def get_current_user_password(password: Header = Depends(get_password_from_header)):
    return password

@router.get("/gpt", tags=["utils"])
def gpt_answer(question: str):
    questionEN = get_translate_KRtoEN(question)
    answerEN = get_answer(questionEN)
    answerKR = get_translate_ENtoKR(answerEN)
    return answerKR