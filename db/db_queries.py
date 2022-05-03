from .mongo_db import MongoDB


def all_project_scores():
    db = MongoDB()
    db.connect()
    return db.projects.aggregate([{"$replaceRoot": {"newRoot": "$scores"}}])

