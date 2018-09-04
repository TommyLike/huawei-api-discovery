import time
import json
import os
from flask_restplus import fields, Model
from flask import current_app


class UpdateTime(fields.Raw):
    def format(self, value):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value))


class JsonContent(fields.Raw):
    def format(self, value):
        return json.loads(value)


class SpecName(fields.Raw):
    def format(self, value):
        return os.path.splitext(value)[0]


class SchemaHref(fields.Raw):
    def format(self, value):
        return "http://{host}/discovery/v1/schemas/{id}".format(
            host=current_app.config['HOST'], id=value)


class SchemaPayload(fields.Raw):
    def format(self, value):
        return "http://{host}/discovery/v1/schemas/{id}/payload".format(
            host=current_app.config['HOST'], id=value)


schema_base = Model('SchemaBase', {
    'name': SpecName,
    'version': fields.String,
    'format': fields.String,
    'description': fields.String,
    'id': fields.String,
    'title': fields.String,
    'updated': UpdateTime(attribute='m_time')
})


schema = schema_base.clone('Schema', {
    'href': SchemaHref(attribute='id'),
    'payload_href': SchemaPayload(attribute='id')
})


schema_detail = schema_base.clone('SchemaDetail', {
    'schema': JsonContent(),
})
