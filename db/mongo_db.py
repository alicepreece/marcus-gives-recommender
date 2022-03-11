from pymongo import MongoClient


class MongoDB:

    def __init__(self):
        self.connection = None
        self.db = None

    def connect(self):
        uri = 'mongodb+srv://qmulssdc1:pw-qmulssdc1@qmulssdc1.' \
              'ou1k2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
        self.connection = MongoClient(uri)
        self.db = self.connection['marcus-gives']
        return self

    @property
    def projects(self):
        return self.db.projects

    @property
    def scores(self):
        return self.db.scores

    @property
    def clients(self):
        return self.db.clients

    @property
    def users(self):
        return self.db.users
