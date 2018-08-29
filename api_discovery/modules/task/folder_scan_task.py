import os
import time

from api_discovery.modules.database import mongo_client
from api_discovery.modules.task import base
from api_discovery.modules.objects import oas_v2
from api_discovery.modules.task import file_util


class FolderTask(base.BaseTask):

    REQUIRED_OPTIONS = ['SAMPLE_FOLDER', 'SCAN_INTERVAL']

    def __init__(self, app, *args, **kwargs):
        self.yaml_folder = app.config['SAMPLE_FOLDER']
        self.app = app
        self.interval = app.config['SCAN_INTERVAL']
        self.client = mongo_client.MongoClient.get_instance()

    def do_scan_folder(self):
        self.app.logger.info("Start to perform periodic task "
                             "to scan folder: %s." % self.yaml_folder)
        items = oas_v2.OASV2List.get_all_ovs()
        try:
            for name in os.listdir(self.yaml_folder):
                if name == '.' or name == '..':
                    continue
                file_name = os.path.join(self.yaml_folder, name)
                selected_item = next((x for x in items if x.name == name),
                                     None)
                if selected_item is None:
                    oas_object = file_util.FileUtils.create_object_from_file(
                        file_name)
                    self.app.logger.info("going to insert schema item into "
                                         "database: %s" % name)
                    oas_object.save()
                    continue
                current_m_time = os.path.getmtime(file_name)
                if current_m_time != selected_item.m_time:
                    oas_object = file_util.FileUtils.create_object_from_file(
                        file_name)
                    self.app.logger.info("going to update schema item into "
                                         "database: %s." % selected_item.name)
                    selected_item.update(oas_object)
                    selected_item.save()
                items.remove(selected_item)
            # Remove deleted file from database
            for item in items:
                self.app.logger.info("going to delete schema item from "
                                     "database: %s" % item.name)
                item.remove()
        except Exception as e:
            self.app.logger.error("Failed to scan file in specified "
                                  "folder: %s" % e)

    def loop_scan(self):
        try:
            while True:
                self.do_scan_folder()
                time.sleep(self.interval)
        except Exception as e:
            self.app.logger.error("Failed to execute periodic task: %s" % e)

    def start(self):
        self.loop_scan()
