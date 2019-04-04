from src.configs.loadBD import clientDB

db = clientDB()


def find(filter):
    sugestions = []
    response = db['sugestion'].find_one(filter)
    for resp in response:
        sugestions.append({
            '_id': resp['_id'],
            'messageId': resp['messageId'],
            'message': resp['message']
        })
    return sugestions


def findOne(filter):
    sugestion = {}
    response = db['sugestion'].find_one(filter)
    for resp in response:
        sugestion['_id'] = resp['_id']
        sugestion['messageId'] = resp['messageId']
        sugestion['message'] = resp['message']
    return sugestion


def insert(data):
    response = db['sugestion'].insert_one(data)
    return response


def insertMany(data):
    response = db['sugestion'].insert_many(data)
    return response


def update(data):
    response = db['sugestion'].update_one(
        {'_id': data['_id']}, {'$set': data}
    )
    return response
