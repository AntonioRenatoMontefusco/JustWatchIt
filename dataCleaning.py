from os.path import isfile, join

import pandas as pd
import os
from os import path, listdir
import JWILogger
from numpy import nan

jwi_logger = JWILogger.get_jwi_logger(__name__)

project_path = os.getcwd()

COLUMNS_NUMBER = 12


def main_proc():
    datasets = []
    for s in listdir(project_path + "/dataset/test"):
        ds = clean_dataset(s)
        datasets.append(ds)
    merge_datasets(datasets)


# generic method that does data cleaning on the dataset
def clean_dataset(dataset_name):
    try:
        jwi_logger.info("Starting cleaning process of dataset: %s", dataset_name)

        dataset = pd.read_csv(path.join(project_path + "/dataset/test", dataset_name))

        dataset = drop_missing_values(dataset)
        dataset = drop_unused_columns(dataset)
        return dataset

    except Exception as error:
        jwi_logger.error("An error occurred during cleaning of dataset %s", dataset_name)
        jwi_logger.error(error)


# delete all null values.
def drop_missing_values(dataset):
    for row in dataset.iloc():

        for i in range(COLUMNS_NUMBER):

            if row[i] is nan and i != 2 and i != 3:

                row[i] = pd.NA
            elif type(row[i]) == str:
                row[i].lower()
                row[i].strip()
    dataset = dataset.dropna()
    return dataset


# Funzione che elimina colonne non utili
def drop_unused_columns(dataset):
    # Inutli, duplicate nei dataset e di conseguenza potenzialmente
    dataset = dataset.drop(columns='show_id')
    return dataset


def merge_datasets(datasets):
    ds = pd.concat(datasets)
    ds.to_csv("complete_dataset.csv", index=False)



