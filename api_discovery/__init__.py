"""Initialization module of the package."""
# API Factory imports
from api_discovery.factory import Factory

# API configuration imports
from api_discovery.config import Config
from api_discovery import modules
# Version handling
import pkg_resources

try:
    # If the app is packaged
    # Get the version of the setup package
    __version__ = pkg_resources.get_distribution('api_discovery').version
except pkg_resources.DistributionNotFound:  # pragma: no cover
    # If app is not used as a package
    # Hardcode the version from the configuration file
    __version__ = Config.VERSION


# Instantiation of the factory
factory = Factory()

# Enable flask instance
app = factory.set_flask()

# Enable of the desired modules
modules.init_app(app)

