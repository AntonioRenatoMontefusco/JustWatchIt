import pymongo
import pandas as pd


# define connection pool
def mongo_connection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    create_rating_collection()
    collection = client["JustWatchIT"]["JustWatchIT"]
    return collection


def rating_collection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    collection = client["JustWatchIT"]["Rating"]
    return rating_collection


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


def create_rating_collection():
    collection = rating_collection()
    indexs = [0, 1, 2, 3, 4, 5]
    ratings = ['G - General', 'TV_Y7 - Children Over 11', 'PG - Parental Guidance', 'R - Parental Guidance Under 17',
               'Under 17 Not Admitted', 'Not Rated']
    for i in indexs:
        element = {
            "id": i,
            "rating": ratings[i]
        }
        collection.insert_one(element)
