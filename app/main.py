from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.utils.logger import logger
from app.utils.mongodb import async_mongodb
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv(f'.{os.getenv("MODE")}.env')

app = FastAPI(title="Async FastAPI")
app.include_router(api_router, prefix='/v1')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    logger.initialize()
    await async_mongodb.connect_to_database()


@app.on_event("shutdown")
async def shutdown():
    await async_mongodb.close_database_connection()


@app.get('/')
async def main():
    return 'Hello World'


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=5002, reload=True)