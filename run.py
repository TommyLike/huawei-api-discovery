"""Main entrypint of the application."""
# Api factory import
from api_discovery import factory

# Eventually force the environment
# factory.environment = 'default'

# Get flask instance
app = factory.flask

if __name__ == '__main__':
    # Actually run the application
    app.run()
