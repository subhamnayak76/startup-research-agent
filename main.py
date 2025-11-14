
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import connect_to_mongo, close_mongo_connection
from routes import user

@asynccontextmanager
async def lifespan(app: FastAPI):

    await connect_to_mongo()
    try:
        yield
    finally:
        await close_mongo_connection()

app = FastAPI(lifespan=lifespan)


app.include_router(user.router)
