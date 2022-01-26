from pymongo import MongoClient


class BaseSystem(object):

    def __init__(self):
        self.client = MongoClient()
        self._db = self.client.avacord

    @property
    def db(self):
        return self._db

    @property
    def collection(self):
        raise NotImplementedError
