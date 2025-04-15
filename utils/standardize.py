import pandas as pd


def standardize_text(df,column_name):
    df[column_name]=df[column_name].astype(str).str.strip().str.lower().replace(r'\s+',' ',regex=True)
    return df

#.replace(r'[^\w\s]', '', regex=True)