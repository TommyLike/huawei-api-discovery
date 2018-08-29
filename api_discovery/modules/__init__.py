from api_discovery.modules import logging
from api_discovery.modules import api
from api_discovery.modules import database
from api_discovery.modules import task

log = logging.Logging()
discovery_api = api.DiscoveryAPI()
db = database.Database()
taskhub = task.TaskHub()


def init_app(app):
    for module in [log, discovery_api, db, taskhub]:
        module.init_app(app)
