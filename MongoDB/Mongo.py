import pymongo

class Mongo():
    
    def __init__(self):
        self._client = pymongo.MongoClient("mongodb://localhost:27017/")
        self._db = None
        self._collection = None
    
    def get_db(self): 
        return self._db
    
    def set_db(self, db):
        self._db = db
        return db

    def get_collection(self): 
        return self._collection
    
    def set_collection(self, collection):
        self._collection=collection
        return collection
    
    def insert(self, doc, duplicate=False):
        result = None
        if type(doc) is dict:
            if duplicate:
                result = self._collection.insert_one(doc)
            else:
                if self.find_one(doc) is None:
                    result = self._collection.insert_one(doc)
        else:
            if duplicate:
                result = self._collection.insert_many(doc)
            else:
                new_doc = [d for d in doc if self.find_one(d) is None]
                result = self._collection.insert_many(new_doc)
        return result

    def find_one(self, doc=None):
        result = None
        if doc is not None:
            result = self._collection.find_one(doc)
        return result
    
    def find(self, doc=None):
        result = None
        if doc is not None:
            result = self._collection.find(doc)
        else:
            result = self._collection.find()
        return result
    
    def count(self, doc=None):
        if doc is not None:
            count = self._collection.find(doc).count()
        else:
            count = self._collection.find().count()
        return count