import numpy as np
import pandas as pd
import os
from os import path, listdir
import JWILogger

jwi_logger = JWILogger.get_jwi_logger(__name__)

project_path = os.getcwd()

COLUMNS_NUMBER = 12


def main_proc():
    datasets = []
    for s in listdir(project_path + "/dataset"):
        ds = clean_dataset(s)
        datasets.append(ds)
    merge_datasets(datasets)
    return 'Hello World!'


# generic method that does data cleaning on the dataset
def clean_dataset(dataset_name):
    try:
        jwi_logger.info("Starting cleaning process of dataset: %s", dataset_name)

        dataset = pd.read_csv(path.join(project_path + "/dataset", dataset_name))

        dataset = drop_missing_values(dataset)
        dataset = drop_unused_columns(dataset)
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

def merge_datasets(datasets):
    ds = pd.concat(datasets)
    ds.to_csv("complete_dataset.csv", index=False)
