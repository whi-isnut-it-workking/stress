from typing import Union
from enum import Enum
from typing import Annotated
from fastapi import FastAPI, Query
from fastapi import APIRouter # Router
from pydantic import BaseModel # Request Body
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt
from PIL import Image
import numpy as np
import konlpy
from konlpy.tag import Komoran

app = FastAPI()

router = APIRouter(
    prefix="",
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/test")
def test() :
    with open('testfile.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    okt = Okt(max_heap_size= 1024 * 6)
    nouns = okt.nouns(text) # 명사만 추출

    words = [n for n in nouns if len(n) > 1] # 단어의 길이가 1개인 것은 제외

    c = Counter(words) # 위에서 얻은 words를 처리하여 단어별 빈도수 형태의 딕셔너리 데이터를 구함
    return c

# @app.get("/test2/:{item_id}")
# def read_item(item_id: int):
#     return {"item_id":item_id}

# 열거형 매개변수
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# 경로 매개변수
@app.get("/public/img/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# 쿼리 매개변수
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]

# 선택적 매개변수
# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Union[str, None] = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}

# 필수 쿼리 매개변수
# 쿼리 매개변수를 필수로 입력하게 하려면 기본값을 선언하지 않으면 된다.
#

# 쿼리 매개변수 형변환: 1, true, on, yes, t, TRUE 등 다 true로 처리됨
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# 여러 경로/쿼리 매개변수: 순서 상관없이 이름으로 감지됨
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# Create data model
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# Use the model
# dict(){Pydantic} 메서드는 model_dump로 대체되었다.
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Request body + path parameters
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}

# Request body + path + query parameters
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

# Query Parameters and String Validations
## Additional validation: Import Query and Annotated
### 최소, 최대 길이, 정규 표현식을 지정한 예
### ^: 문자열의 시작. 이전에는 문자가 없음
### fixedquery: 임의의 문자열. 대소문자까지 정확히 일치해야 함
### $: 문자열의 끝. 이후에는 문자가 없음
# @app.get("/items/")
# async def read_items(
#     q: Annotated[
#         str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
#     ] = None
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

## Default values: None을 포함한 모든 타입의 기본값을 가진다는 의미는 해당 파라미터는 필수가 아닌 것이다(not required)
# @app.get("/items/")
# async def read_items(q: Annotated[str, Query(min_length=3)] = "fixedquery"):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

## Required with Ellipsis(...): 기본값을 리터럴 값으로 선언하여 명시적으로 필수 값임을 나타내는 방법
# @app.get("/items/")
# async def read_items(q: Annotated[str, Query(min_length=3)] = ...):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

## Query parameter list / multiple values
## 예와 같이 list type으로 쿼리 매개변수를 선언하려면 쿼리를 명시적으로 사용해야 한다. 그렇지 않으면 요청 본문으로 해석된다.
# @app.get("/items/")
# async def read_items(q: Annotated[list[str] | None, Query()] = None):
#     query_items = {"q": q}
#     return query_items

## Query parameter list / multiple values with defaults
@app.get("/items/")
async def read_items(q: Annotated[list[str] | None, Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items

## Declare more metadata
@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        ),
    ] = ["foo", "bar"]
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results