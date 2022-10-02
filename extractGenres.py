import os
from os import path, listdir
import numpy as np
import pandas as pd
import re
import JWILogger
from mongo_connection import mongo_connection, initialize_db

project_path = os.getcwd()
datasets = []
dataset = pd.read_csv(path.join(project_path + "/complete_dataset.csv"))
genre_list = []
for index in dataset.index:
    row = dataset.iloc[index]
    genre_list.extend(str(row["genres"]).split(","))
print(set(genre_list))