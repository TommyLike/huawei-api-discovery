import logging
from logging.handlers import RotatingFileHandler


class Logging(object):
    """
    This is a helper extension, which adjusts logging configuration for the
    application.
    """

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        """
        :param app:
        :return:
        """
        formatter = logging.Formatter(
            app.config['LOG_FORMAT'])
        log_handler = RotatingFileHandler(app.config['LOG_FILE'],
                                          maxBytes=10000000, backupCount=6)
        log_handler.setLevel(logging.DEBUG)
        log_handler.setFormatter(formatter)
        app.logger.addHandler(log_handler)
        app.logger.setLevel(logging.DEBUG)
