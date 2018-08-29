"""Entrypoint of the main API Resources."""
# Flask based imports
from flask_restplus import Namespace
from flask import Response
import yaml
import json
from api_discovery.modules.api.controllers import view_builder
from api_discovery.modules.api.controllers import base
from flask_restplus import reqparse

# Empty name is required to have the desired url path
api = Namespace(name='schemas', description='All Service schemas.')


@api.route('/')
class SchemaCollection(base.BasicResouce):
    """Schema resource class."""

    @api.doc(params={'name': 'The name of the service, default is None'},
             responses={200: 'OK', 403: 'Unauthorized'})
    def get(self):
        """Get all service schemas."""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='service_name')
        args = parser.parse_args()
        self.logger.info("Get all schemas....")
        items = self.db_client.get_all_discovery_items(name=args['name'])
        return view_builder.build_discovery_items(items)


@api.route('/<id>')
@api.doc(params={'id': 'The id of service schema.'})
@api.param('id', 'The id of service schema.')
class Schema(base.BasicResouce):
    """Get single service schema."""

    @api.doc(responses={200: 'OK', 403: 'Unauthorized'})
    def get(self, id):
        """Get one specific service schema."""
        item = self.db_client.get_discovery_item_by_id(id)
        return view_builder.build_discovery_item(item)


@api.route('/<id>/payload')
@api.doc(params={'id': 'The id of service schema.'})
@api.param('id', 'The id of service schema.')
class Schema(base.BasicResouce):
    """Get single service raw schema."""

    @api.doc(responses={200: 'OK', 403: 'Unauthorized'})
    def get(self, id):
        """Get raw schema of one specific service."""
        item = self.db_client.get_discovery_item_by_id(id)
        return Response(yaml.dump(json.loads(item['schema'])),
                        mimetype='application/x-yaml')
