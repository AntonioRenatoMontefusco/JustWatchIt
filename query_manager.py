from mongo_connection import mongo_connection, rating_collection

collection = mongo_connection()


def insert(type, title, director, cast, locations, data_added, release_year, rating, duration, genres, description,
           present_in):
    new_row = {
        'type': type,
        'title': title,
        'director': director,
        'cast': cast,
        'locations': locations,
        'data_added': data_added,
        'release_year': release_year,
        'rating': rating,
        'duration': duration,
        'genres': genres,
        'description': description,
        'present_in': present_in
    }
    collection.insert_one(new_row)


def delete_by_type(type):
    collection.delete_one({"type": type})


def filter_by_type(type):
    return collection.find({"type": type})


def find_by_director(director):
    return collection.find({"director": {"$regex": ".*" + director + ".*"}})


def find_by_cast(cast):
    return collection.find({"director": {"$regex": ".*" + cast + ".*"}})


def find_by_rating(rating):
    r_collection = rating_collection()
    rating_id = r_collection.find_one({'rating': rating})["id"]
    return collection.find({"rating": {'$lt': rating_id}})
