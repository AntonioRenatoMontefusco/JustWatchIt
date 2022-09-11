from datetime import date

import numpy as np
import pandas as pd
import os
from os import path, listdir
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
        dataset = create_column(dataset, dataset_name)
        dataset = change_columns_name(dataset)
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
    dataset = dataset.drop(columns='show_id')
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

    dataset.insert(11, 'present_in', platform)
    return dataset


def test_dup(dataset):
    for index, row in dataset.iterrows():
        title = row["title"]
        dups = []
        for index, row in dataset.iterrows():
            if row["title"] == title:
                dups.append({({index: row})})

        if dups.__len__() > 1:
            platforms = ''
            for dic in dups:
                print(dic)
                platforms += dic[row]['present_in'] + ','
            print(platforms)
            new_row = dups[0]
            new_row['present_in'] = platforms
            for i in range(dups.__len__()):
                dataset.drop(dups[i])

    return dataset


def modify_rating(dataset):
    for index, row in dataset.iterrows():
        if "G" in row['rating']:
            dataset.loc[index, 'rating'] = "G - General"
        elif "PG" in row['rating']:
            dataset.loc[index, 'rating'] = "PG - Parental Guidance"
        elif "PG-13" in row['rating']:
            dataset.loc[index, 'rating'] = "PG-13 - Parental Guidance Under 13"
        elif "R" in row['rating']:
            dataset.loc[index, 'rating'] = "R - Parental Guidance Under 17"
        elif "NC-17" in row['rating']:
            dataset.loc[index, 'rating'] = "Under 17 Not Admitted"
        elif "TV_MA" in row['rating']:
            dataset.loc[index, 'rating'] = "Under 17 Not Admitted"
        elif "TV-Y" in row['rating']:
            dataset.loc[index, 'rating'] = "G - General"
        elif "TV-Y7" in row['rating']:
            dataset.loc[index, 'rating'] = "TV_Y7 - Children Over 11"
        elif "ALL" in row['rating']:
            dataset.loc[index, 'rating'] = "G - General"
        elif "+" not in row['rating']:
            dataset.loc[index, 'rating'] = "Not Rated"

    return dataset
