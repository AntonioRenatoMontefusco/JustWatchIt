import pandas as pd
import os
from os import path
import JWILogger

jwi_logger = JWILogger.get_jwi_logger(__name__)

project_path = os.getcwd()

COLUMNS_NUMBER = 12

# generic method that does data cleaning on the dataset
def clean_dataset(dataset_name):

    try:
        jwi_logger.info("Starting cleaning process of dataset: {}", dataset_name)

        dataset = pd.read_csv(path.join(project_path, dataset_name))
        drop_unused_columns(dataset)
        dataset = drop_missing_values(dataset)
        dataset = drop_unused_columns(dataset)
        
    except Exception as error:
        jwi_logger.error("An error occurred during cleaning of dataset {}", dataset_name)
        jwi_logger.error(error)


# delete all null values.
def drop_missing_values(dataset):

    for row in dataset.iloc():

        for i in range(COLUMNS_NUMBER):

            if not str(row[i]):
                row[i] = pd.NA
            else:
                row[i].lower()

    dataset = dataset.dropna()
    return dataset


# Funzione che elimina colonne non utili
def drop_unused_columns(dataset):
    #Inutli, duplicate nei dataset e di conseguenza potenzialmente
    dataset = dataset.drop(columns='show_id')
    return dataset


def merge_datasets(datasets):
    dataset=[]
    for ds in datasets:
        dataset.append(ds)
