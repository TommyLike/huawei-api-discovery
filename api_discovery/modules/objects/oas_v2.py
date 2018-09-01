from api_discovery.modules.objects import base


class OASV2(base.Model):

    collection = 'discovery_items'
    format = "OpenAPI V2"

    required_attributes = [
        'name',
        'title',
        'version',
        'description',
        'schema',
        'm_time'
    ]


class OASV2List(base.Collection):

    collection = 'discovery_items'
    model_class = OASV2

    @classmethod
    def get_all_ovs(cls, filter=None):
        return cls.get_all_filtered(filter=filter)
