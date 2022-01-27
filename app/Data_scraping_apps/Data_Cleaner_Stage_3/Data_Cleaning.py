import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import psycopg2


# Create database.
engine = create_engine("postgresql://postgres:1@localhost/telegram_bot_db")

# Load data for cleaning.
df = pd.read_csv('./.data/data_v.2.0.csv')

# Replace "None" strings in to NaN values.
df = df.replace('None', np.nan)

# Replace Nan values in "description" from "shortDescription".
df.description.fillna(df.shortDescription, inplace=True)

# Remove duplicated movies.
df = df.drop_duplicates(subset=['nameRu', 'kinopoiskId'], keep='first')

# Remove movies with no data about "description" or "filmLength".
df = df.dropna(subset=['description'])
df = df.dropna(subset=['filmLength'])

# Remove movies with genre 'для взроcлых'.
for i in range(len(df.genres)):
    try:
        if 'для взрослых' in df.at[i, 'genres']:
            df = df.drop([i])
    except KeyError:
        continue

# Replace Nan values in "ratingAgeLimits" from "ratingMpaa"
df.ratingAgeLimits.fillna(df.ratingMpaa, inplace=True)

# Remove unnecessary columns.
df = df.drop(columns=['nameOriginal', 'ratingMpaa', 'ratingImdb',
                      'imdbId', 'shortDescription'])
try:
    df = df.drop(columns=['Unnamed: 0'])
except:
    pass


# Save data to a .csv file.
# df.to_csv('./.data/data_v.3.0.csv', index=False)

# Insert index column.
df.insert(loc=0, column='myIndex', value=range(1, len(df) + 1))

# Rename columns.
df.rename(columns={'myIndex': 'my_index',
                   'nameRu': 'name_ru',
                   'ratingKinopoisk': 'rating_kinopoisk',
                   'ratingKinopoiskVoteCount': 'rating_kinopoisk_vote_count',
                   'filmLength': 'film_length',
                   'ratingAgeLimits': 'rating_age_limits',
                   'kinopoiskId': 'kinopoisk_id',
                   'posterUrl': 'poster_url'}, inplace=True)
df.info()

# Save data to a PostgreSQL database.
df.to_sql('telegram_bot_db', engine, if_exists='replace', index=False)