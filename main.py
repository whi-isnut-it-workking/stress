from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis import board_router, comment_router, utils_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["GET, POST, PUT, PATCH, DELETE"],
    allow_headers=["*"]
)

app.include_router(router=board_router.router)
app.include_router(router=comment_router.router)
app.include_router(router=utils_router.router)