from flask_restplus import Resource
from flask import current_app

from api_discovery.modules.database import mongo_client


class BasicResouce(Resource):

    def __init__(self, api=None, *args, **kwargs):
        self.db_client = mongo_client.MongoClient.get_instance()
        self.logger = current_app.logger
        super(BasicResouce, self).__init__(api=api, *args, **kwargs)
