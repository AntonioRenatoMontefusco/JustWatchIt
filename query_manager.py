from mongo_connection import mongo_connection, rating_collection

collection = mongo_connection()


def insert(type, title, director, cast, locations, data_added, release_year, rating, genres, description,
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
        'genres': genres,
        'description': description,
        'present_in': present_in
    }
    collection.insert_one(new_row)


def modify(type, title, director, cast, locations, data_added, release_year, rating, genres, description,
           present_in):
    new_row = {"$set": {
        'type': type,
        'title': title,
        'director': director,
        'cast': cast,
        'locations': locations,
        'data_added': data_added,
        'release_year': release_year,
        'rating': rating,
        'genres': genres,
        'description': description,
        'present_in': present_in
    }}

    collection.update_one({"title": title, "release_year": release_year}, new_row)

    return find_by_title_and_year(title, release_year)


def filter_by_type(type_to_filter):
    return collection.find({"type": type_to_filter})


def find_by_title(title):
    return collection.find({"title": {"$regex": ".*" + title + ".*"}})


def find_by_title_and_year(title, year):
    return collection.find_one({"title": title, "release_year": year})


def delete_by_title_and_year(title, year):
    collection.delete_one({"title": title, "release_year": year})
    return find_by_title_and_year(title, year)


def find_by_director(director):
    return collection.find({"director": {"$regex": ".*" + director + ".*"}})


def find_series_by_season_count(num_season):
    return collection.find({"type": "TV Show", "duration": {"$regex": ".*" + num_season + ".*"}})


def find_series_by_at_least_season_count(num_season):
    return collection.find({"type": "TV Show", "duration": {"$gt": {"$split": ".*" + num_season + ".*"}}})


def find_by_cast(cast):
    return collection.find({"cast": {"$regex": ".*" + cast + ".*"}})


def find_by_rating(rating):
    r_collection = rating_collection()
    rating_id = r_collection.find_one({'rating': rating})["id"]
    return collection.find({"rating": {'$lt': rating_id}})

def find_by_rating_less_than(age):
    db = collection.find()
    for row in list(db):
        if "G" in row['rating']:
            print('mammt')
