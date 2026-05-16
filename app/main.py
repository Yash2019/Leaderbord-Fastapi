from fastapi import FastAPI
from app.database.db import create_table
from app.crud.routes import router
from app.database.redis_client import redis

app = FastAPI()

@app.on_event('startup')
async def on_startup() -> None:
    await create_table()

@app.on_event('shutdown')
async def on_shutdown() -> None:
    await redis.close()


app.include_router(
    router
)