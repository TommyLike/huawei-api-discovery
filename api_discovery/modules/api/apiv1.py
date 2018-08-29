from flask import Blueprint
from flask_restplus import Api

from api_discovery.modules.api.controllers import apis

blueprint = Blueprint('discovery', __name__, url_prefix='/discovery/v1')
api = Api(blueprint,
          title='Huawei Cloud API Discovery Service',
          version='1.0',
          contact='tommylikehu@gmail.com',
          description='This service is used to record all API schemas which '
                      'are published on Huawei Cloud.')

api.namespaces.clear()
api.add_namespace(apis.api)
