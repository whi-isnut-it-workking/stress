from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis import board_router, comment_router, utils_router

app = FastAPI()

app.middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://125.143.133.111",
        "http://3.34.107.69",
        "http://121.128.211.44",
        "http://1.240.130.87"
    ],
    allow_credentials=True,
    allow_methods=["GET, POST, PUT, PATCH, DELETE"],
    allow_headers=["*"]
)

app.include_router(router=board_router.router)
app.include_router(router=comment_router.router)
app.include_router(router=utils_router.router)