# import pandas as pd
#
# movies_df = pd.read_csv('./.data/data_v.2.0.csv')
# print('Old df:', movies_df.info(verbose=True), '\n\n\n')
#
# movies_df = movies_df.drop_duplicates(subset=['nameRu'])
# print('New df:', movies_df.info(verbose=True))
#
# movies_df.to_csv('./.data/data_v.2.0.csv')