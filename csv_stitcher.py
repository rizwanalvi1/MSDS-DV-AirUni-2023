import os
import pandas as pd

dir = '.'
df_list = []

for filename in os.listdir(dir):
    if 'part' in filename:
        print(filename)
        df = pd.read_csv(filename)
        df_list.append(df)

combined_df = pd.concat(df_list)

combined_df.to_csv('fbr_combined.csv')
print(combined_df.head())