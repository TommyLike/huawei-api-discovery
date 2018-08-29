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
        except:
            self.app.logger.error("Failed to initialize mongodb client.")
            raise

    def insert_discovery_item(self, document):
        self.collection.insert_one(document)

    def get_discovery_item(self, name):
        return self.collection.find_one({'name': name})

    def get_discovery_item_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def get_all_discovery_items(self, name=None):
        if name:
            return self.collection.find({"name": {'$regex': "%s" % name}})
        return self.collection.find()

    def remove_deleted_discovery_item(self, name):
        self.collection.delete_one({'name': name})

    def update_discovery_item(self, name, update_item):
        self.collection.update_one(
            {'name': name},
            {'$set': update_item}, upsert=True)
