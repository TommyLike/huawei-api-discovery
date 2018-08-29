from api_discovery.modules.database import mongo_client


class Database(object):

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        mongo_client.MongoClient.initialize_client(app)
