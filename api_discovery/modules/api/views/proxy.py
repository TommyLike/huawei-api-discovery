from flask_restplus import fields, Model


class NestedJson(fields.Raw):
    def format(self, value):
        return value


Proxy = Model('Proxy', {
    'status_code': fields.Integer,
    'content': NestedJson,
    'success': fields.Boolean,
    'message': fields.String
})
