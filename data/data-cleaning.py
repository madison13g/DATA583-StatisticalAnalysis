import pandas as pd
import numpy as np
import re

df = pd.read_csv('NY_realestate2023-02-17-coords.csv')

#removing duplicates
print(len(df.index))
df = df.drop_duplicates(subset=['address'], keep='first', ignore_index=True)
df.reset_index(inplace=True, drop=True)
print(len(df.index))
#print(df['address'].value_counts())
#print(df.columns)


#removing unneeded columns
#red_address
#accidental index
#original string
#link
cols_drop = ['Unnamed: 0', 'link', 'red_address', 'original_str']
df = df.drop(cols_drop, axis=1)
df.reset_index(inplace=True, drop=True)


#replacing incorrect sqft with NaN
# for i in range(len(df.index)):
#     test = bool(re.search('[A-Za-z]+', df.loc[i, 'feet']))
#     if test == True:
#         df.loc[i, 'feet'] = np.NaN



df.to_csv('NY_realestate2023-02-17-cleaned.csv', index = False)
