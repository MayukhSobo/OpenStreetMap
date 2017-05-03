#!/usr/bin/env python


def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db


def make_pipeline():
    # complete the aggregation pipeline
    match = {"$match": {"created": {"$exists": 1}}}
    group = {"$group": {"_id": "$created.user", "total": {"$sum": 1}}}
    sort = {"$sort": {"total": -1}}
    limit = {"$limit": 5}
    pipeline = [match, group, sort, limit]
    return pipeline


def aggregate(db, pipeline):
    return [doc for doc in db.openStreetDataMap.aggregate(pipeline)]


if __name__ == '__main__':
    db = get_db('udacity')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    # print(type(result))
    # assert len(result) == 1
    import pprint
    pprint.pprint(result)
