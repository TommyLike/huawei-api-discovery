
class BaseTask(object):

    REQUIRED_OPTIONS = []

    def init_app(self, app, *args, **kwargs):
        pass

    def start(self):
        pass
