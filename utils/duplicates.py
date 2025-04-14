import pandas as pd

def exact_duplicate_rows(df):
    exact_duplicates=df[df.duplicated()]
    print(exact_duplicates.head())
    print('\n')
    return exact_duplicates

def num_exact_duplicates(df):
    num_exact_duplicates=df.duplicated().sum()
    print(f'The number of exact duplicate rows are: {num_exact_duplicates}')
    print('\n')
    return num_exact_duplicates

import pandas as pd

def find_exact_duplicates_across_df(df1, df2):
    
    duplicates = pd.merge(df1, df2, how='inner')
    duplicates = duplicates.drop_duplicates()

    return duplicates