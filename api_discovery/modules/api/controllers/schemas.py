"""Entrypoint of the main API Resources."""
# Flask based imports
from flask_restplus import Namespace
from flask_restplus import reqparse
from flask import Response
import yaml
import json
import bson

from api_discovery.modules.api.controllers import base
from api_discovery.modules.objects import oas_v2
from api_discovery.modules.api.views import schemas
from api_discovery.modules import exception

# Empty name is required to have the desired url path
api = Namespace(name='schemas', description='All Service schemas.')

# Register views
api.models[schemas.schema.name] = schemas.schema
api.models[schemas.schema_detail.name] = schemas.schema_detail


@api.route('/')
@api.header('Access-Control-Allow-Origin', '*')
class SchemaCollection(base.BasicResouce):
    """Schema resource class."""

    @api.doc(params={'name': 'The name of the service, default is None'},
             responses={200: 'OK'})
    @api.marshal_with(api.models[schemas.schema.name], envelope="schemas")
    def get(self):
        """Get all service schemas."""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='service_name')
        args = parser.parse_args()
        self.logger.info("Getting all schemas....")
        items = oas_v2.OASV2List.get_all_filtered(
            filter={'name': args['name']} if args['name'] else None)
        return items, 200, {"Access-Control-Allow-Origin": "*"}


@api.route('/<id>')
@api.doc(params={'id': 'The id of service schema.'})
@api.param('id', 'The id of service schema.')
@api.header('Access-Control-Allow-Origin', '*')
class Schema(base.BasicResouce):
    """Get single service schema."""

    @api.doc(responses={200: 'OK',
                        400: 'Parameter is invalid',
                        404: 'Resource not found.'})
    @api.marshal_with(api.models[schemas.schema_detail.name],
                      envelope="schema")
    def get(self, id):
        """Get one specific service schema."""
        if not bson.objectid.ObjectId.is_valid(id):
            raise exception.InvalidParameter(key="id")
        item = oas_v2.OASV2.get_by_id(id)
        return item, 200, {"Access-Control-Allow-Origin": "*"}


@api.route('/<id>/payload')
@api.doc(params={'id': 'The id of service schema.'})
@api.param('id', 'The id of service schema.')
@api.header('Access-Control-Allow-Origin', '*')
class SchemaPayload(base.BasicResouce):
    """Get single service raw schema."""

    @api.doc(responses={200: 'OK',
                        400: 'Parameter is invalid',
                        404: 'Resource not found'})
    def get(self, id):
        """Get raw schema of one specific service."""
        if not bson.objectid.ObjectId.is_valid(id):
            raise exception.InvalidParameter(key="id")
        item = oas_v2.OASV2.get_by_id(id)
        return Response(
            response=yaml.dump(json.loads(item['schema'])),
            status=200,
            mimetype='text/yaml',
            headers={"Access-Control-Allow-Origin": "*"})
