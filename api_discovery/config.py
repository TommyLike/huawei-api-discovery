"""Application Configuration."""
import os


class Config(object):
    """Parent configuration class."""

    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')

    TITLE = "Flask API skeleton"
    VERSION = "0.1.0"
    DESCRIPTION = "An API Skeleton."
    LOG_FILE = "api_discovery_development.log"
    LOG_FORMAT = "%(asctime)s | %(pathname)s:%(lineno)d | %(levelname)s | %(message)s"

    MONGO_IP = "139.159.224.207"
    MONGO_PORT = 27017

    # Periodic task related config
    SCAN_INTERVAL = 1 * 60
    SAMPLE_FOLDER = "/Users/tommylike/Desktop/huawei_api_discovery/api_discovery/samples"

    ENABLE_TASKERS = 'FolderTask,'


class DevelopmentConfig(Config):
    """Configurations for Development."""

    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing."""

    TESTING = True
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""

    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""

    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
