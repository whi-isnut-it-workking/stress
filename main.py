from fastapi import FastAPI, HTTPException

from apis import board_router

app = FastAPI()

app.include_router(router=board_router.router)