from app.utils.mongodb import mongodb
from app.data.batch_35 import students, assignments


def run():
    mongodb.db['students'].insert_many(students)
    mongodb.db['assignments'].insert_many(assignments)