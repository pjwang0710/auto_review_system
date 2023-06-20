from app.utils.mongodb import mongodb
from app.data.batch_35 import students, assignments
import os
from dotenv import load_dotenv

load_dotenv(f'.{os.getenv("MODE")}.env')


def run():
    mongodb.db['students'].insert_many(students)
    mongodb.db['assignments'].insert_many(assignments)


if __name__ == '__main__':
    mongodb.connect_to_database()
    run()
