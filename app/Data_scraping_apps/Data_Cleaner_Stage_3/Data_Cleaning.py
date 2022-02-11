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


# 📍Filter from all movies only good quality movies.
def filter_only_good_movies():
    """Delete movies, which ARE NOT:
    df_v1_1 - "rating>=7.2" and "votes>=3000".
    df_v1_2 - "rating>=6.5" and "votes>=5000".
    df_v1_3 - "rating>=5.5" and "votes>=10000".
    df_v2_1 - "rating>=7.4" and "votes>=15000" for "year<=2004".
    df_v2_2 - "rating>=7.2" and "votes>=10000" for "year>=2005" and "year<=2011".

    Save it as a new .csv file and as a new PostgreSQL database.
    """

    df = pd.read_csv('./.data/data_v.3.0.csv')


    # Delete movies, which ARE NOT: "rating>=7.2" and "votes>=3000".
    df_v1_1 = df.drop(df[(df.rating_kinopoisk_vote_count < 3000) |
                         (df.rating_kinopoisk < 7.2)].index)

    # Delete movies, which ARE NOT: "rating>=6.5" and "votes>=5000".
    df_v1_2 = df.drop(df[(df.rating_kinopoisk_vote_count < 5000) |
                         (df.rating_kinopoisk < 6.5)].index)

    # Delete movies, which ARE NOT: "rating>=5.5" and "votes>=10000".
    df_v1_3 = df.drop(df[(df.rating_kinopoisk_vote_count < 10000) |
                         (df.rating_kinopoisk < 5.5)].index)

    # Concatenate df_v1_1, df_v1_2 and df_v1_3 into a single dataframe.
    df_v2 = pd.concat([df_v1_1, df_v1_2, df_v1_3]).drop_duplicates().reset_index(drop=True)
    df_v2

    # Filter only movies on years 1980 - 2004 with "rating>=7.4" and "votes>=15000".
    df_v2_1 = df_v2.drop(df_v2[(df_v2.year > 2004)].index)

    df_v2_1 = df_v2_1.drop(df_v2_1[(df_v2_1.rating_kinopoisk_vote_count < 15000) |
                                   (df_v2_1.rating_kinopoisk < 7.4)].index)

    # Filter only movies on years 2005 - 2011 with "rating>=7.2" and "votes>=10000".
    df_v2_2 = df_v2.drop(df_v2[(df_v2.year < 2005) | (df_v2.year > 2011)].index)

    df_v2_2 = df_v2_2.drop(df_v2_2[(df_v2_2.rating_kinopoisk_vote_count < 10000) |
                                   (df_v2_2.rating_kinopoisk < 7.2)].index)

    # Filter only movies on years 2012 and higher.
    df_v2_3 = df_v2.drop(df_v2[(df_v2.year < 2012)].index)

    # Concatenate df_v2_1, df_v2_2 and df_v2_3 into a single dataframe.
    df_v3 = pd.concat([df_v2_1, df_v2_2, df_v2_3]).drop_duplicates().reset_index(drop=True)


    # Remove an old index column.
    df_v3 = df_v3.drop(['my_index'], axis=1)

    # Insert a new index column.
    df_v3.insert(loc=0, column='my_index', value=range(1, len(df_v3) + 1))

    # Save data to a .csv file.
    df_v3.to_csv('./.data/data_v.3.1.csv', index=False)

    # Save all movies to a PostgreSQL database 'telegram_bot_db_all'.
    df_v3.to_sql('telegram_bot_good_quality_movies_db', engine, if_exists='replace', index=False)

    print("Data Cleaning is done!")


filter_only_good_movies()
