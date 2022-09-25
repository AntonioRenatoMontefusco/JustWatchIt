import os
from os import path, listdir

import pandas as pd

import JWILogger
from mongo_connection import mongo_connection, initialize_db

jwi_logger = JWILogger.get_jwi_logger(__name__)

project_path = os.getcwd()


def main_proc():
    datasets = []
    for s in listdir(project_path + "/dataset"):
        ds = clean_dataset(s)
        datasets.append(ds)
    dataset = merge_datasets(datasets)
    coll = mongo_connection()
    initialize_db(dataset, coll)

    return 'Hello World!'


# generic method that does data cleaning on the dataset
def clean_dataset(dataset_name):
    try:
        jwi_logger.info("Starting cleaning process of dataset: %s", dataset_name)

        dataset = pd.read_csv(path.join(project_path + "/dataset", dataset_name))
        dataset = drop_missing_values(dataset)
        dataset = drop_unused_columns(dataset)
        dataset = delete_dot_zero(dataset)
        dataset = change_columns_name(dataset)
        dataset = create_column(dataset, dataset_name)
        dataset = modify_rating(dataset)
        return dataset

    except Exception as error:
        jwi_logger.error("An error occurred during cleaning of dataset %s", dataset_name)
        jwi_logger.error(error)


# delete all null values.
def drop_missing_values(dataset):
    obligatory_columns = ["type", "title", "release_year", "rating", "duration", "listed_in"]
    dataset.dropna(subset=obligatory_columns, inplace=True)

    return dataset


# Funzione che elimina colonne non utili
def drop_unused_columns(dataset):
    # Inutli, indici dei dataset originali non piú utili nel nostro caso
    dataset = dataset.drop(columns=['show_id', 'duration'])
    return dataset


def change_columns_name(dataset):
    dataset.rename(columns={'listed_in': 'genres'}, inplace=True)
    dataset.rename(columns={'country': 'locations'}, inplace=True)

    return dataset


def merge_datasets(datasets):
    ds = pd.concat(datasets)
    ds = test_dup(ds)
    ds.to_csv("complete_dataset.csv", index=False)
    return ds


def delete_dot_zero(dataset):
    dataset['release_year'] = dataset['release_year'].astype(int)
    return dataset


def create_column(dataset, dataset_name):
    # Creazione della colonna present_in che aiuta a capire dove trovare un film
    platform = ''
    if 'amazon' in dataset_name:
        platform = 'Amazon Prime Video'
    elif 'disney' in dataset_name:
        platform = 'Disney +'
    elif 'hulu' in dataset_name:
        platform = 'Hulu'
    elif 'netflix' in dataset_name:
        platform = 'Netflix'

    dataset.insert(10, 'present_in', platform)
    return dataset


def test_dup(dataset):
    for index, row in dataset.iterrows():
        title = row["title"]
        dups = []
        platforms = ''
        jwi_logger.info('Checking row %s', index)
        dataset.reset_index(drop=True, inplace=True)
        for index_, row_ in dataset.iterrows():

            if row_["title"] == title:
                dups.append(index_)
                platforms += row_['present_in'] + ','

        if dups.__len__() > 1:
            new_row = dataset.iloc[dups[0]].copy(deep=True)
            new_row['present_in'] = platforms[:-1]

            for i in dups:
                dataset.drop(index=i, inplace=True);
        new_dataset = dataset.append(new_row);

    return new_dataset


# 0 General
# 1 dai 7 in su
# 2 dagli 11 in poi                 TV_Y7
# 3 fino ai 13 con supervisione     PG
# 4 dai 16 in su
# 5 fino ai 17 con supervisione     R
# 6 sotto i 17 non ammessi
# 7 dai 18 in su
# 8 not rated


def modify_rating(dataset):
    for index, row in dataset.iterrows():
        if "G" in row['rating']:
            dataset.loc[index, 'rating'] = 0
        elif "TV-Y" in row['rating']:
            dataset.loc[index, 'rating'] = 0
        elif "ALL" in row['rating']:
            dataset.loc[index, 'rating'] = 0
        elif "ALL_AGES" in row['rating']:
            dataset.loc[index, 'rating'] = 0
        elif "7+" in row['rating']:
            dataset.loc[index, 'rating'] = 1
        elif "TV-Y7" in row['rating']:
            dataset.loc[index, 'rating'] = 2
        elif "PG" in row['rating']:
            dataset.loc[index, 'rating'] = 3
        elif "PG-13" in row['rating']:
            dataset.loc[index, 'rating'] = 3
        elif "13+" in row['rating']:
            dataset.loc[index, 'rating'] = 3
        elif "16+" in row['rating']:
            dataset.loc[index, 'rating'] = 4
        elif "AGES_16_" in row['rating']:
            dataset.loc[index, 'rating'] = 4
        elif "R" in row['rating']:
            dataset.loc[index, 'rating'] = 5
        elif "NC-17" in row['rating']:
            dataset.loc[index, 'rating'] = 6
        elif "TV_MA" in row['rating']:
            dataset.loc[index, 'rating'] = 6
        elif "18+" in row['rating']:
            dataset.loc[index, 'rating'] = 7
        elif "AGES_18_" in row['rating']:
            dataset.loc[index, 'rating'] = 7
        else:
            dataset.loc[index, 'rating'] = 8

    return dataset
