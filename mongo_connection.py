import pymongo
import pandas as pd


# define connection pool
def mongo_connection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    collection = client["JustWatchIT"]["JustWatchIT"]
    return collection


def initialize_db(dataset, collection):
    for index, row in dataset.iterrows():
        element = {
            "type": row["type"],
            "title": row["title"],
            "director": row["director"],
            "cast": row["cast"],
            "locations": row["locations"],
            "date_added": row["date_added"],
            "release_year": row["release_year"],
            "rating": row["rating"],
            "description": row["description"],
            "duration": row["duration"],
            "genres": row["genres"],
            "present_in": row["present_in"],
        }
        collection.insert_one(element)
    return None
