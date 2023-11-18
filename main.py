from fastapi import FastAPI, HTTPException

from apis import board_router, comment_router

app = FastAPI()

app.include_router(router=board_router.router)
app.include_router(router=comment_router.router)