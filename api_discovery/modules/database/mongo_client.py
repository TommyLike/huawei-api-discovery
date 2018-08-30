import pymongo
from bson.objectid import ObjectId


class MongoClient(object):

    DB_NAME = "api_discovery"
    DB_COLLECTION = "discovery_items"
    _Instance = None

    @classmethod
    def initialize_client(cls, app):
        MongoClient._Instance = MongoClient(app)

    @classmethod
    def get_instance(cls):
        if MongoClient._Instance:
            return MongoClient._Instance
        raise Exception("Mongoclient uninitialized.")

    def __init__(self, app):
        try:
            self.app = app
            client = pymongo.MongoClient(
                host=self.app.config['MONGO_IP'],
                port=self.app.config['MONGO_PORT'])
            self.db = client[MongoClient.DB_NAME]
            self.collection = self.db[MongoClient.DB_COLLECTION]
        except Exception:
            self.app.logger.error("Failed to initialize mongodb client.")
            raise

    def object_create(self, item, collection):
        return self.db[collection].insert_one(item)

    def object_update(self, id, item, collection):
        return self.db[collection].update_one({"_id": ObjectId(id)},
                                              {"$set": item}, upsert=False)

    def object_get(self, id, collection):
        return self.db[collection].find_one({"_id": ObjectId(id)})

    def object_remove(self, id, collection):
        return self.db[collection].remove({"_id": ObjectId(id)})

    def collection_get_all(self, collection):
        return self.db[collection].find()

    def collection_query(self, collection, filter):
        return self.db[collection].find(filter)

    def collection_regex_query(self, collection, filter):
        db_query = {}
        for key, value in filter.items():
            db_query[key] = {'$regex': value}
        return self.db[collection].find(db_query)
