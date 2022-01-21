import requests
import os
import time
from datetime import datetime
from pprint import pprint
import json
import pandas as pd

from config import KEY
from additional_functions import json_to_csv


# Config data.
URL_MOVIES = 'https://kinopoiskapiunofficial.tech/api/v2.2/films'


# Headers and params values for an API.
headers_value = {
    'X-API-KEY': '3bb02829-73f8-4599-b841-657276210588',
    'Content-Type': 'application/json'
}


# Variables.
rating_from_value = 1
rating_to_value = 10
year_from_value = 1980
year_to_value = 2023
page_value = 1
order_value = 'NUM_VOTE'


# Parcing part.
for year in range(year_from_value,year_to_value):
    for rating in range(rating_from_value, rating_to_value):
        rating_from = rating
        rating_to = rating + 1

        params_value = {
            'ratingFrom': rating_from,
            'ratingTo': rating_to,
            'yearFrom': year,
            'yearTo': year,
            'page': page_value,
            'order': order_value
        }

        pages = requests.get(URL_MOVIES, headers=headers_value, params=params_value).json()['totalPages']
        time.sleep(0.25)

        for page in range(1, pages+1):

            params_value = {
                'ratingFrom': rating_from,
                'ratingTo': rating_to,
                'yearFrom': year,
                'yearTo': year,
                'page': page,
                'order': order_value
            }

            # Get data from the API in .json format.
            r = requests.get(URL_MOVIES, headers=headers_value, params=params_value)
            # time.sleep(0.25)
            json_result = r.json()

            # Columns for pandas.DataFrame.
            attributes = ['nameRu',
                          'nameOriginal',
                          'nameEn',

                          'ratingKinopoisk',
                          'ratingImdb',

                          'kinopoiskId',
                          'imdbId',

                          'type',
                          'year',

                          'posterUrl',
                          'posterUrlPreview',

                          'countries',
                          'genres']

            movies_df = pd.DataFrame(columns=attributes)

            # Convert .json format to pandas.DataFrame with editing countries and genres attributes.
            movies_df = json_to_csv(json_result=json_result,
                                    attributes=attributes,
                                    movies_df=movies_df)

            # Save pd.DataFrame to a .csv file.
            if os.path.isfile('./.data/data_v.1.0.csv'):  # if file exist.
                movies_df.to_csv('./.data/data_v.1.0.csv', mode='a', index=False, header=False)
            else:  # if file doesn't exist
                movies_df.to_csv('./.data/data_v.1.0.csv', mode='w', index=False, header=True)

            # Write data in to a log file.
            file_log = open('./.data_v.1.0_log.log', mode='a')
            file_log.write(f'Done!\t\t'
                           f'Time: {datetime.now().time()};\t\t'
                           f'Year: {year};\t\t'
                           f'Rating: {rating};\t\t'
                           f'Page number {page} out of {pages} pages.\n')
            file_log.close()
