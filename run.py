"""Main entrypint of the application."""
# Api factory import
import os
from api_discovery import factory

# Eventually force the environment
# factory.environment = 'default'

# Get flask instance
app = factory.flask

if __name__ == '__main__':
    # Actually run the application
    app.run(host=os.getenv("APP_HOST", default='127.0.0.1'),
            port=os.getenv("APP_PORT", default=5000))
