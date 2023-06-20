from app.utils.mongodb import async_mongodb


async def get_database():
    return async_mongodb