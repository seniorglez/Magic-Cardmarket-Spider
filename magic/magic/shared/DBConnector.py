from pymongo import MongoClient


class DBConnector:

    def __init__(self, db_name):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[db_name]

    def push(self, item, item_storage_name):
        self.db[item_storage_name].insert_one(item)
