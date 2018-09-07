from flask import Blueprint
from flask_restplus import Api

from api_discovery.modules.api.controllers import schemas
from api_discovery.modules.api.controllers import proxy
from api_discovery.modules import exception

blueprint = Blueprint('discovery', __name__, url_prefix='/discovery/v1')
api = Api(blueprint,
          title='Huawei Cloud API Discovery Service',
          version='1.0',
          contact='tommylikehu@gmail.com',
          description='This service is used to record all API schemas which '
                      'are published on Huawei Cloud.')


# register error handle
@schemas.api.errorhandler(exception.APIDiscoveryException)
def register_error(error):
    return error.to_dict(), error.code


api.namespaces.clear()
api.add_namespace(schemas.api)
api.add_namespace(proxy.api)
