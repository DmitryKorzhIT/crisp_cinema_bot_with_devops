from datetime import datetime

# Convert .json format to pandas.DataFrame with editing countries and genres attributes.
def json_to_csv(json_result, attributes, movies_df):

    for movie in range(len(json_result['items'])):

        # Check, do we have year data.
        if json_result['items'][movie]['year'] == None:
            continue
        # Check, do we have rating data.
        elif json_result['items'][movie]['ratingKinopoisk'] == None:
            continue
        elif json_result['items'][movie]['nameRu'] == None:
            continue

        for attribute in attributes:
            movies_df.at[movie, attribute] = json_result['items'][movie][attribute]

        # Convert countries from dictionaries format to string format.
        countries_list = []
        for county_index in range(len(json_result['items'][movie]['countries'])):
            countries_list.append(json_result['items'][movie]['countries'][county_index]['country'])
        movies_df.at[movie, 'countries'] = countries_list

        # Convert genres from dictionaries format to string format.
        genres_list = []
        for genre_index in range(len(json_result['items'][movie]['genres'])):
            genres_list.append(json_result['items'][movie]['genres'][genre_index]['genre'])
        movies_df.at[movie, 'genres'] = genres_list

    return movies_df
