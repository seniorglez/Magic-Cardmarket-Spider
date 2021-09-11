from pymongo import MongoClient
from itemadapter import ItemAdapter


class DBConnector:

    def __init__(self, db_name):
        self.client = MongoClient('localhost', 27017, username="root", password="nopassword")
        self.db = self.client[db_name]

    def push(self, item, item_storage_name):
        self.db[item_storage_name].insert_one(ItemAdapter(item).asdict())
