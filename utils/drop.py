import pandas as pd

def drop_all_rows(df):
    df.dropna()
    print(df)
    print('\n')
    return df

def drop_column_missVal(df):
    columns_w_dropped_na=df.dropna(axis=1)
    print('head after dropping columns with atleast one missing value:')
    print(columns_w_dropped_na.head())
    print('\n')
    return columns_w_dropped_na

def drop_column(df,column_name):
    df_dropped=df.drop(columns=[column_name])
    print(df_dropped.head())
    print('\n')
    return df_dropped

def drop_unnecessary_columns(df,columns_to_keep):
    return df[columns_to_keep].copy()