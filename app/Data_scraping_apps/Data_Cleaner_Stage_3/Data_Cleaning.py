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

# Save all movies to a .csv file.
df.to_csv('./.data/data_v.3.0.csv', index=False)

# Save all movies to a PostgreSQL database 'telegram_bot_db_all'.
df.to_sql('telegram_bot_all_movies_db', engine, if_exists='replace', index=False)


def filter_only_good_movies():
    """Delete movies with adult content and
    bad quality movies. Save it as a new
    .csv file and a new database.
    """

    df = pd.read_csv('./.data/data_v.3.0.csv')

    # Remove adult bad quality movies and bad quality movies.
    for i in range(len(df)):
        command = 'stay'

        # Remove adult bad quality movies.
        if (df.loc[i, 'rating_age_limits'] == 'r' or
            df.loc[i, 'rating_age_limits'] == 'age18' or
            str(df.loc[i, 'rating_age_limits']) == 'nan') and \
                ((df.loc[i, 'rating_kinopoisk_vote_count'] < 2000) or \
                 (df.loc[i, 'rating_kinopoisk'] < 5.5) or \
                 (df.loc[i, 'year'] < 2000)):
            command = 'delete'

        # Remove bad quality movies.
        if (df.loc[i, 'rating_kinopoisk_vote_count'] < 1000) or \
                (df.loc[i, 'rating_kinopoisk'] < 5.0) or \
                (df.loc[i, 'year'] < 2000):
            command = 'delete'

        if command == 'delete':
            df = df.drop(i, axis=0)

    # Save data to a .csv file.
    df.to_csv('./.data/data_v.3.1.csv', index=False)

    # Save all movies to a PostgreSQL database 'telegram_bot_db_all'.
    df.to_sql('telegram_bot_good_quality_movies_db', engine, if_exists='replace', index=False)


filter_only_good_movies()