
class APIDiscoveryException(Exception):

    code = 500
    description = "Exception occured in service backend."

    def __init__(self, **kwargs):
        if kwargs:
            self.description = self.description % kwargs

    def to_dict(self):
        return {'message': self.description}


class NotFound(APIDiscoveryException):
    description = "Resource could not be found."
    code = 404


class Invalid(APIDiscoveryException):
    description = "Unacceptable parameters."
    code = 400


class SchemaNotFound(NotFound):

    description = "Specified schema :%(schema)s is not found."


class InvalidParameter(Invalid):

    description = "Invalid parameters %(key)s are provided."
