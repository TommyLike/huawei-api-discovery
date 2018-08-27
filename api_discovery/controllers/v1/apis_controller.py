from flask import current_app

from api_discovery.database import mongodb_client
from api_discovery.controllers.v1 import view_builder


def list_apis(service_name=None):
    current_app.logger.info("API 'list_apis' has been "
                            "called with service_name: %s" % service_name)
    items = mongodb_client.MongoClient.get_instance().get_all_discovery_items(
        service_name)
    return view_builder.build_discovery_items(items)


def get_api(id):
    current_app.logger.info("API 'get_api' has been "
                            "called with ID: %s" % id)
    item = mongodb_client.MongoClient.get_instance().get_discovery_item_by_id(
        id)
    return view_builder.build_discovery_item(item)
