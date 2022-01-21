import requests
import os
import time
from datetime import datetime
from pprint import pprint
import json
import pandas as pd
import numpy as np

from config import KEY


# Headers values and URL info for the API.
url_movies = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/'
headers_value = {
    'X-API-KEY': KEY,
    'Content-Type': 'application/json'
}

# Load a .csv file in to a pandas DataFrame.
movies_df = pd.read_csv('./.data/data_v.1.0.csv')
movies_df_len = len(movies_df['kinopoiskId'])
atribute_list = ['ratingKinopoiskVoteCount', 'filmLength', 'ratingMpaa',
                 'ratingAgeLimits', 'shortDescription', 'description']

# Convert movies_df series in to string format.
for i in atribute_list:
    movies_df[i] = movies_df[i].astype('string')

for i in range(0, movies_df_len):

    progress = (100/movies_df_len)*i
    print(str("{:.2f}".format(progress)) + '%')

    movie_id = movies_df.at[i, 'kinopoiskId']
    url_movies_id = url_movies + str(movie_id)

    # Get data from the API in .json format.
    r = requests.get(url_movies_id, headers=headers_value)

    # Get data from json API and write data to movies_df.
    for atribute in atribute_list:

        try:
            movies_df.at[i, atribute] = str(r.json()[atribute])

        except ValueError:
            movies_df.at[i, atribute] = ''



movies_df.to_csv('./.data/data_v.2.0.csv')























