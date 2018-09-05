from flask_cors import CORS
from api_discovery.modules.api.apiv1 import blueprint  # noqa: E402


class DiscoveryAPI(object):

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        # Register v1 blueprint
        app.register_blueprint(blueprint)
        # Wrap v1 APIs with CORS
        CORS(app)
