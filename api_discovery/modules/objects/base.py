from api_discovery.modules.database import mongo_client


class Model(dict):

    __getattr__ = dict.get
    __delattr__ = dict.__delitem__

    required_attributes = []
    collection = None

    def __setattr__(self, key, value):
        if key == '_client':
            super(Model, self).__setattr__(key, value)
        else:
            super(Model, self).update({key: value})

    @property
    def id(self):
        try:
            return self['_id']
        except:
            return None

    @id.setter
    def id(self, value):
        raise Exception("object's id attribute can't be set.")

    def __init__(self, *args, **kwargs):
        object_attributes = {}
        for attribute in self.required_attributes:
            object_attributes[attribute] = args[0].pop(attribute, None)
        if args[0].get("_id", None):
            object_attributes['_id'] = args[0].get("_id", None)
        if kwargs:
            raise Exception("Only %s attributes are allowed for %s object." % (
                self.required_attributes, self.__class__))
        self._client = mongo_client.MongoClient.get_instance()
        super(Model, self).__init__(object_attributes, **kwargs)

    def save(self):
        if not self.id:
            self._client.object_create(self, self.collection)
        else:
            self._client.object_update(self.id, self, self.collection)

    def reload(self):
        if self.id:
            self.update(self._client.object_get(self.id, self.collection))

    def remove(self):
        if self.id:
            self._client.object_remove(self.id, self.collection)
            self.clear()

    @classmethod
    def get_by_id(cls, id):
        client = mongo_client.MongoClient.get_instance()
        ob = client.object_get(id, cls.collection)
        if ob is None:
            return None
        return cls(ob)


class Collection(object):

    model_class = None

    @classmethod
    def get_all_filtered(cls, filter=None):
        print(filter)
        client = mongo_client.MongoClient.get_instance()
        if filter is None:
            return [cls.model_class(item) for item in
                    client.collection_get_all(
                        cls.model_class.collection)]
        else:
            return [cls.model_class(item) for item in
                    client.collection_regex_query(
                        cls.model_class.collection, filter)]
