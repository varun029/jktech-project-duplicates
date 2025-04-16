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


def find_duplicates_within_df(df, columns):
    
    duplicates = df[df.duplicated(subset=columns, keep=False)]
    return duplicates

def drop_exact_within_df(df, columns):

    return df.drop_duplicates(subset=columns, keep='first').reset_index(drop=True)


def find_duplicates_across_df(df1, df2, df1_columns=None, df2_columns=None):
   
    if df1_columns is None or df2_columns is None:
        raise ValueError("Must specify columns for both dataframes")
    
    if len(df1_columns) != len(df2_columns):
        raise ValueError("Must specify exactly 3 columns for each dataframe")
    
    for col in df1_columns:
        if col not in df1.columns:
            raise ValueError(f"Column '{col}' not found in first dataframe")
    
    for col in df2_columns:
        if col not in df2.columns:
            raise ValueError(f"Column '{col}' not found in second dataframe")
    
    temp_df1 = df1.copy()
    temp_df2 = df2.copy()
    
    column_mapping = {df2_columns[i]: df1_columns[i] for i in range(len(df1_columns))}
    temp_df2 = temp_df2.rename(columns=column_mapping)
    
    matches = pd.merge(temp_df1, temp_df2, on=df1_columns, how='inner')
    print('Exact Duplicates across datasets are:\n')
    print(matches.info())
    print('\n')
    
    if not matches.empty:
    
        full_matches_df1 = pd.merge(df1 , matches[df1_columns], on=df1_columns, how='left',indicator=True)
        full_matches_df1 = full_matches_df1[full_matches_df1["_merge"]=='left_only'].drop(columns=['_merge'])
        
        return full_matches_df1,temp_df2
    
    return temp_df1,temp_df2 


