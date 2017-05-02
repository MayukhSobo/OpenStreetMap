#!/usr/bin/env python


def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db


def make_pipeline():
    # complete the aggregation pipeline
    match1 = {"$match": {"amenity": {"$exists": 1, "$in": ["atm", "bank"]}}}
    group = {"$group": {"_id": "$name", "total": {"$sum": 1}}}
    sort = {"$sort": {"total": -1}}
    project = {"$project": {"_id": 0, "bank_or_atm": "$_id", "count": "$total"}}
    pipeline = [match1, group, sort, project]
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
