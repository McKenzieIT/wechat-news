import threading

from Mongo import Mongo


class MongoDouban(Mongo):
    __instance_lock = threading.Lock()
    __init_flag = False

    def __init__(self):
        if not self.__init_flag:
            super(MongoDouban, self).__init__()
            self.set_db(self._client["douban"])
            self.__init_flag = True

    def __new__(cls, *args, **kwargs):
        if not hasattr(MongoDouban, "_instance"):
            with MongoDouban.__instance_lock:
                if not hasattr(MongoDouban, "_instance"):
                    MongoDouban._instance = object.__new__(cls)
        return MongoDouban._instance


class MovieCollection(MongoDouban):

    def __init__(self):
        super(DoubanMovieCollection, self).__init__()
        self.set_collection(self._db['movie'])


class BookCollection(MongoDouban):

    def __init__(self):
        super(DoubanMovieCollection, self).__init__()
        self.set_collection(self._db['book'])
