from pymongo import MongoClient
import utils

URI = utils.env.URI
DB_NAME = utils.env.DB_NAME
mongo_client = MongoClient(URI)
db = mongo_client[DB_NAME]
