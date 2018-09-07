import threading
from api_discovery.modules.task.folder_scan_task import FolderTask
from api_discovery.modules.task.proxy_task import HuaweiCloudProxy


class TaskHub(object):
    """
    This is a helper extension, which adjusts logging configuration for the
    application.
    """
    Taskers = [FolderTask, ]

    def __init__(self, app=None, ):
        if app:
            self.init_app(app)

    def init_app(self, app):
        HuaweiCloudProxy.initialize_client(app)
        # Start the periodic task to scan folders
        for item in TaskHub.Taskers:
            if item.__name__ in app.config['ENABLE_TASKERS']:
                if any(app.config.get(cfg, None) is
                       None for cfg in item.REQUIRED_OPTIONS):
                    app.logger.error(
                        "Unable to initialize task: %s, since required "
                        "options %s are missing!" % (item.__name__,
                                                     item.REQUIRED_OPTIONS))
                app.logger.info("Initializing task %s." % item.__name__)
                threading.Thread(target=item(app).start).start()
