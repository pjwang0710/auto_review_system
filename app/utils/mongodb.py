# install:
#   pymongo: pip install pymongo
#   motor: pip install motor
import os

from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class MongoDB():
    """
    Environment Variables:
        MONGODB__PATH
        MONGODB__DBNAME
    """
    client: None
    db: None

    def connect_to_database(self, mongo_path=None, db_name=None):
        mongo_path = mongo_path or os.getenv('MONGODB__PATH')
        db_name = db_name or os.getenv('MONGODB__DBNAME')
        self.client = MongoClient(mongo_path)
        assert self.client.config.command('ping')['ok'] == 1.0
        self.db = self.client[db_name]


class AsyncMongoDB():
    """
    Environment Variables:
        MONGODB__PATH
        MONGODB__DBNAME
    """

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, mongo_path=None, db_name=None):
        mongo_path = mongo_path or os.getenv('MONGODB__PATH')
        db_name = db_name or os.getenv('MONGODB__DBNAME')
        self.client = AsyncIOMotorClient(
            mongo_path,
            maxPoolSize=10,
            minPoolSize=10)
        self.db = self.client[db_name]

    async def close_database_connection(self):
        self.client.close()


mongodb = MongoDB()
async_mongodb = AsyncMongoDB()