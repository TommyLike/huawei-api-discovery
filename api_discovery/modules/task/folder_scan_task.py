import os
import time

from api_discovery.modules.database import mongo_client
from api_discovery.modules.task import base
from api_discovery.modules.objects import oas_v2


class FolderTask(base.BaseTask):

    REQUIRED_OPTIONS = ['SAMPLE_FOLDER', 'SCAN_INTERVAL']

    def __init__(self, app, *args, **kwargs):
        self.yaml_folder = app.config['SAMPLE_FOLDER']
        self.app = app
        self.interval = app.config['SCAN_INTERVAL']
        self.client = mongo_client.MongoClient.get_instance()

    def get_all_files(self):
        return [oas_v2.OASV2.from_dict(item) for
                item in self.client.get_all_discovery_items()]

    def update_file(self, item):
        self.app.logger.info("going to update discovery item into "
                             "database: %s." % item.name)
        item.refresh_schema()
        self.client.update_discovery_item(item.name,
                                          item.collect_update_attribute())

    def remove_deleted_file(self, item):
        self.app.logger.info("going to delete discovery item from "
                             "database: %s" % item.name)
        self.client.remove_deleted_discovery_item(item.name)

    def add_new_file(self, item):
        self.app.logger.info("going to insert discovery item into "
                             "database: %s" % item.name)
        self.client.insert_discovery_item(item.to_dict())

    def do_scan_folder(self):
        self.app.logger.info("Start to perform periodic task "
                             "to scan folder: %s." % self.yaml_folder)
        items = self.get_all_files()
        try:
            for name in os.listdir(self.yaml_folder):
                if name == '.' or name == '..':
                    continue
                file_name = os.path.join(self.yaml_folder, name)
                selected_item = next((x for x in items if x.name == name),
                                     None)
                if selected_item is None:
                    self.add_new_file(oas_v2.OASV2(file_name=file_name))
                    continue
                current_m_time = os.path.getmtime(file_name)
                if str(current_m_time) != selected_item.m_time:
                    self.update_file(selected_item)
                items.remove(selected_item)
            # Remove deleted file from database
            for item in items:
                self.remove_deleted_file(item)
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