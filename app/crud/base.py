from typing import Any, Dict, List
from bson import ObjectId


class CRUDBase():
    def __init__(self, collection):
        self.collection = collection

    async def get_by_id(self, mongodb, id: Any):
        result = await mongodb.db[self.collection].find_one({
            '_id': ObjectId(id)
        })
        return result

    async def get_one_and_project(self, mongodb, condition, projects):
        projects = {p: 1 for p in projects}
        results = mongodb.db[self.collection].aggregate([{
            '$match': condition
        }, {
            '$project': projects
        }, {
            '$limit': 1
        }])
        output = []
        async for result in results:
            result['_id'] = str(result['_id'])
            output.append(result)
        if len(output) == 0:
            return None
        return output[0]

    async def get_one(self, mongodb, condition):
        result = await mongodb.db[self.collection].find_one(condition)
        if result:
            result['_id'] = str(result['_id'])
        return result

    async def replace_one(self, mongodb, condition: Dict, data: Dict):
        result = await mongodb.db[self.collection].replace_one(condition, data)
        return result.matched_count, result.modified_count

    async def get_many(self, mongodb, condition: Dict):
        results = mongodb.db[self.collection].find(condition)
        output = []
        async for result in results:
            result['_id'] = str(result['_id'])
            output.append(result)
        return output

    async def get_many_with_sort(self, mongodb, condition: Dict, sort_condition):
        results = mongodb.db[self.collection].find(condition).sort(sort_condition[0], sort_condition[1])
        output = []
        async for result in results:
            result['_id'] = str(result['_id'])
            output.append(result)
        return output

    async def get_many_with_limit(self, mongodb, condition: Dict, limit=10):
        results = mongodb.db[self.collection].aggregate([{
            '$match': condition
        }, {
            '$limit': limit
        }])
        output = []
        async for result in results:
            result['_id'] = str(result['_id'])
            output.append(result)
        return output

    async def insert_one(self, mongodb, data: Dict):
        result = await mongodb.db[self.collection].insert_one(data)
        return str(result.inserted_id)

    async def insert_many(self, mongodb, data: List):
        result = await mongodb.db[self.collection].insert_many(data)
        return [str(inserted) for inserted in result.inserted_ids]

    async def update_one(self, mongodb, condition: Dict, data: Dict):
        result = await mongodb.db[self.collection].update_one(condition, {'$set': data})
        return result.matched_count, result.modified_count

    async def upsert_one(self, mongodb, condition: Dict, data: Dict):
        result = await mongodb.db[self.collection].replace_one(condition, data, True)
        return result.matched_count, result.modified_count, result.upserted_id

    async def update_many(self, mongodb, condition: Dict, data: Dict):
        result = await mongodb.db[self.collection].update_many(condition, {'$set': data})
        return result.matched_count, result.modified_count

    async def delete_one(self, mongodb, condition: Dict):
        result = await mongodb.db[self.collection].delete_one(condition)
        return result.deleted_count

    async def delete_many(self, mongodb, condition: Dict):
        result = await mongodb.db[self.collection].delete_many(condition)
        return result.deleted_count