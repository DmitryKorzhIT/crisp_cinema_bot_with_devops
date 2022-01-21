import numpy as np
import pandas as pd


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

# Save data.
df.to_csv('./.data/data_v.3.0.csv', index=False)
