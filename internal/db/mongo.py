"""
This module setup the MongoDb configuration and Connection.
"""
import os
from pymongo import MongoClient

URI = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME") if os.getenv("DB_NAME") else "qa_test"
mongo_client = MongoClient(URI)
db = mongo_client[DB_NAME]
