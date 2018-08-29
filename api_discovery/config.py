"""Application Configuration."""
import os


class Config(object):
    """Parent configuration class."""

    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')

    TITLE = "Huawei Cloud API Discovery"
    VERSION = "0.1.0"
    DESCRIPTION = "Huawei Cloud API Discovery"
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
    LOG_FILE = "api_discovery_production.log"

    env_host = os.getenv("MONGO_IP", default=None)
    MONGO_IP = env_host if env_host else "127.0.0.1"
    env_port = os.getenv("MONGO_PORT", default=None)
    MONGO_PORT = env_port if env_port else 27017
    SAMPLE_FOLDER = "/etc/api_discovery/samples"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
