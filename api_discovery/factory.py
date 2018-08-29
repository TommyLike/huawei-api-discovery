"""Factory module."""
# Flask based imports
from flask import Flask
# Plugins based imports


# API configuration imports
from api_discovery.config import config

# System based imports
import os


class Factory(object):
    """Build the instances needed for the API."""

    def __init__(self, environment='default'):
        """Initialize Factory with the proper environment."""
        # Get the running environment
        self._environment = os.getenv("APP_ENVIRONMENT")
        if not self._environment:
            self._environment = environment

    @property
    def environment(self):
        """Getter for environment attribute."""
        return self._environment

    def set_flask(self, **kwargs):
        """Flask instantiation."""
        # Flask instance creation
        self.flask = Flask(__name__, **kwargs)

        # Flask configuration
        self.flask.config.from_object(config[self._environment])

        # Swagger documentation
        self.flask.config.SWAGGER_UI_DOC_EXPANSION = 'list'
        self.flask.config.SWAGGER_UI_JSONEDITOR = True

        return self.flask

    def register(self, blueprint):
        """Register a specified blueprint."""
        self.flask.register_blueprint(blueprint)
