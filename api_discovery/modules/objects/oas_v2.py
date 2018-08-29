import os
import fcntl
import yaml
import json
from flask import current_app

from api_discovery.modules.objects import base


class OASV2(base.Model):

    attribute_types = {
        'name': str,
        'title': str,
        'version': str,
        'description': str,
        'file_name': str,
        'schema': str,
        'm_time': str
    }

    attribute_map = {
        'name': 'name',
        'title': 'title',
        'version': 'version',
        'description': 'description',
        'file_name': 'file_name',
        'schema': 'schema',
        'm_time': 'm_time'
    }

    def _read_yaml_content(self, file_path):
        with open(file_path, 'r') as stream:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
            return yaml.load(stream)

    def __init__(self, file_name=None):

        self.file_name = file_name
        if file_name is None:
            return
        try:
            self.name = os.path.basename(self.file_name)
            self.m_time = os.path.getmtime(file_name)
            schema = self._read_yaml_content(file_name)
            self.title = schema.get('info', {}).get('title')
            self.version = schema.get('info', {}).get('version')
            self.description = schema.get('info', {}).get('description')
            self.schema = json.dumps(schema)
        except Exception:
            current_app.logger.error(
                "Failed to initialize Discovery item from "
                "path:%s." % file_name)

    def refresh_schema(self):
        self.schema = self._read_yaml_content(self.file_name)
        self.m_time = os.path.getmtime(self.file_name)
        self.title = self.schema.get('info', {}).get('title')
        self.version = self.schema.get('info', {}).get('version')
        self.description = self.schema.get('info', {}).get('description')

    def collect_update_attribute(self):
        return {'m_time': self.m_time, 'schema': json.dumps(self.schema),
                'title': self.title, 'version': self.version,
                'description': self.description}
