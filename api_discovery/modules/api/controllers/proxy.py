"""Entrypoint of the main API Resources."""
from flask_restplus import Namespace
from flask_restplus import reqparse

from api_discovery.modules.api.controllers import base
from api_discovery.modules.api.views import proxy
from api_discovery.modules.task import proxy_task

# Empty name is required to have the desired url path
api = Namespace(name='proxy', description='Proxy request for API explorer.')

# Register views
api.models[proxy.Proxy.name] = proxy.Proxy


@api.route('/')
@api.header('Access-Control-Allow-Origin', '*')
class Proxy(base.BasicResouce):
    """Proxy resource class."""

    @api.doc(responses={201: 'Created',
                        500: 'Failed to proxy request'})
    @api.marshal_with(api.models[proxy.Proxy.name])
    def post(self):
        """Proxy a HTTP request."""
        # TODO: use model to validate document the parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('method', type=str, location='json', required=True)
        parser.add_argument('service', type=str, location='json',
                            required=True)
        parser.add_argument('url', type=str, location='json', required=True)
        parser.add_argument('parameter', type=dict, location='json')
        parser.add_argument('body', type=dict, location='json')
        parser.add_argument('headers', type=dict, location='json')
        parser.add_argument('region', type=str, location='json', required=True)
        args = parser.parse_args()
        try:
            result = proxy_task.HuaweiCloudProxy.get_instance().proxy_request(
                **args)
            result.update({
                'success': True,
                'message': ''
            })
            return result, 201
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }, 500
