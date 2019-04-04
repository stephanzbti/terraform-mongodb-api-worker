from pymongo import MongoClient
from decouple import config

MONGODB = config('MONGODB', 'mongodb://localhost:27017/MaxMilhas')

client = MongoClient(MONGODB)
db = client['ASG']


def clientDB():
    return db
