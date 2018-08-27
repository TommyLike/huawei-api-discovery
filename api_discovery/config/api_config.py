

class DevelopmentConfig(object):
    # Log related config
    LOG_FILE = "api_discovery_development.log"
    LOG_FORMAT = "%(asctime)s | %(pathname)s:%(lineno)d | %(levelname)s | %(message)s"

    # Periodic task related config
    SCAN_INTERVAL = 1 * 60
    SAMPLE_FOLDER = "/Users/tommylike/Desktop/huawei_api_discovery/api_discovery/samples"

    # Database related config
    MONGO_IP = "139.159.224.207"
    MONGO_PORT = 27017


class ProductConfig(DevelopmentConfig):
    LOG_FILE = "api_discovery_production.log"
