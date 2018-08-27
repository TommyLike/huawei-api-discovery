import os
import connexion
import logging
from logging.handlers import RotatingFileHandler
import threading

from api_discovery import encoder
from api_discovery.services import file_task


def main():
    # Initialize APP within swagger specification
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={
        'title': 'HuaweiCloud API Discovery Service'})

    # Import config
    config_collections = os.environ.get("API_DISCOVERY_CONFIG",
                                        default="DevelopmentConfig")
    app.app.config.from_object(
        "api_discovery.config.api_config.%s" % config_collections)

    # Setup log
    formatter = logging.Formatter(
        app.app.config['LOG_FORMAT'])
    log_handler = RotatingFileHandler(app.app.config['LOG_FILE'],
                                      maxBytes=10000000, backupCount=6)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(formatter)
    app.app.logger.addHandler(log_handler)
    app.app.logger.setLevel(logging.DEBUG)

    # Start the periodic task to scan folders
    scan_task = file_task.FileTask(app=app.app,
                                   folder=app.app.config['SAMPLE_FOLDER'],
                                   interval=app.app.config['SCAN_INTERVAL'])
    threading.Thread(target=scan_task.loop_scan).start()

    # Start application
    app.run(port=8080)


if __name__ == '__main__':
    main()
