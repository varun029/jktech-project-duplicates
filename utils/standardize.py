import pandas as pd
import re


def standardize_text(df,column_name):
    df[column_name]=df[column_name].astype(str).str.strip().str.lower().replace(r'\s+',' ',regex=True)
    return df

def remove_spaces(df,column_name):
    
    df[column_name] = df[column_name].astype(str).str.replace(' ', '', regex=False)
    return df

def clean_pack_size_column(df, column_name):
    def extract_numbers(text):
        if not isinstance(text, str) or text.strip() == '':
            return ''  
        return re.sub(r'[^0-9]', '', text)
    df[column_name] = df[column_name].apply(extract_numbers)
    return df


def fill_value(df, column_name):

    df[column_name] = df[column_name].replace('', '1')
    df[column_name] = df[column_name].fillna('1')
    return df


def convert_pack_size_to_number(df, column_name):
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
    return df

def convert_column_to_str(df,column_name):
    df[column_name]=df[column_name].astype(str)
    return df 