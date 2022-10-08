from mongo_connection import mongo_connection, rating_collection

collection = mongo_connection()


def filter_by_type(type_to_filter):
    return list(collection.find({"type": type_to_filter}))


def find_by_genres(genre):
    return list(collection.find({"genres": {'$regex': ".*" + genre + ".*", "$options": "i"}}))


def find_by_title(title):
    # return list(
    #   collection.aggregate([
    #      {"$match": {"title": {"$regex": ".*" + title + ".*", "$options": "i"}}},
    #      {"$lookup": {"from": "rating", "localField": "rating", "foreignField":{"$toString": "id"}, "as": "rating"}}
    # ])
    # )
    return list(collection.find({"title": {"$regex": ".*" + title + ".*", "$options": "i"}}))


def find_series_by_at_least_season_count(num_season):
    return list(collection.find({"type": "TV Show", "number_of_seasons": {"$lte": num_season}}))


def find_by_year_range(min, max):
    return list(collection.find({"year": {"$lte": min}, "year": {"$lte": max}}))


def find_by_director(director):
    return list(collection.find({"director": {"$regex": ".*" + director + ".*", "$options": "i"}}))


def find_by_title_equals(title):
    return collection.find_one({"title": title})


def find_by_rating(rating):
    r_collection = rating_collection()
    return list(collection.find({"rating": {'$lte': rating}}))


def find_series_by_season_count(num_season):
    return list(collection.find({"type": "TV Show", "duration": num_season}))


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

    collection.update_one({"title": title}, new_row)

    return find_by_title(title)


def delete_by_title(title):
    collection.delete_one({"title": title})
    return find_by_title(title)


def find_film_by_at_least_duration(duration):
    return collection.find({"type": "Movie", "film_duration": {"$lte": duration}})


def find_by_year_range(min_year, max_year):
    return list(collection.find({"release_year": {"$gte": min_year, "$lte": max_year}}))


def find_by_year(year):
    return list(collection.find({"release_year": year}))


def find_by_cast(cast):
    return collection.find({"cast": {"$regex": ".*" + cast + ".*"}})


def find_by_genres(genre):
    return list(collection.find({"genres": {'$regex': ".*" + genre + ".*", "$options": "i"}}))


def find_orderby_date(order):
    return list(collection.find().sort("release_year", int(order)))


def find_orderby_date_limited(order, limit, page):
    result = collection.find().sort("release_year", int(order)).skip(limit*page).limit(limit)
    return list(result)


def find_by_rating_less_than(age):
    db = collection.find()
    for row in list(db):
        if "G" in row['rating']:
            print('mammt')
