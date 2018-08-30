import fcntl
import yaml
import os
import json

from api_discovery.modules.objects import oas_v2


class FileUtils(object):

    @classmethod
    def _read_yaml_content(cls, file_path):
        with open(file_path, 'r') as stream:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
            return yaml.load(stream)

    @classmethod
    def _create_oas_v2_object(cls, file_path, content):
        return oas_v2.OASV2({
            'name': os.path.basename(file_path),
            'm_time': os.path.getmtime(file_path),
            'title': content.get('info', {}).get('title'),
            'version': content.get('info', {}).get('version'),
            'description': content.get('info', {}).get('description'),
            'schema': json.dumps(content)
        })

    @classmethod
    def create_object_from_file(cls, file_path):
        _, extension = os.path.splitext(file_path)
        if extension in ['.yaml']:
            yaml_content = cls._read_yaml_content(file_path=file_path)
            return cls._create_oas_v2_object(file_path,
                                             yaml_content)
        else:
            raise Exception("Unrecognized file type:%s in scan "
                            "folder." % extension)
