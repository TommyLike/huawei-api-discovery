import time
import json
import os
from flask_restplus import fields, Model


class UpdateTime(fields.Raw):
    def format(self, value):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value))


class JsonContent(fields.Raw):
    def format(self, value):
        return json.loads(value)


class SpecName(fields.Raw):
    def format(self, value):
        return os.path.splitext(value)[0]


schema = Model('Schema', {
    'name': SpecName,
    'version': fields.String,
    'format': fields.String,
    'description': fields.String,
    'id': fields.String,
    'title': fields.String,
    'updated': UpdateTime(attribute='m_time'),
})

schema_detail = schema.clone('SchemaDetail', {
    'schema': JsonContent()
})
