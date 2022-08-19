import pymongo

from pymongo import MongoClient

# make a connection with MongoClient
client = MongoClient('localhost', 27017)

# get database
db = client.UKCP18_test

# get collection
collection = db.clt

# insert a document
collection.insert_one(
    {
        "period":'',
        "season":'',
        "authority":'',
        "min_val":'',
        "max_val":'',
        "mean_val":'',
        "std_val":''
    }
)