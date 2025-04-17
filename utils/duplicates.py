import pandas as pd
from rapidfuzz import fuzz,process

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


def find_partial_duplicates_within(df, col1, col2, col3, threshold=90):
    matches = []
    n = len(df)
    
    # Create a combined column for comparison
    df['combined'] = df[col1].astype(str).str.lower().str.strip() + ' ' + \
                     df[col2].astype(str).str.strip() + ' ' + \
                     df[col3].astype(str).str.strip()

    for i in range(n):
        val_i = df.iloc[i]['combined']
        
        for j in range(i + 1, n):  # Avoid re-checking and self-match
            val_j = df.iloc[j]['combined']
            score = fuzz.token_set_ratio(val_i, val_j)

            if score >= threshold:
                matches.append({
                    'Index_1': df.index[i],
                    'Index_2': df.index[j],
                    'Combined_1': val_i,
                    'Combined_2': val_j,
                    'Score': score
                })

    # Drop the temporary column
    df.drop(columns=['combined'], inplace=True)

    return pd.DataFrame(matches)


def find_partial_duplicates_by_combination(df, name_col='Product Name', vol_col='Volume', pack_col='Pack Size', threshold=85, scorer=fuzz.token_set_ratio, limit=10):
   
    df = df.dropna(subset=[name_col, vol_col, pack_col])
    combined = df[[name_col, vol_col, pack_col]].astype(str).agg(' '.join, axis=1).str.lower().str.strip()
    
    unique_values = combined.unique()
    partial_duplicates = {}
    processed = set()

    for value in unique_values:
        if value in processed:
            continue

        matches = process.extract(value, unique_values, scorer=scorer, limit=limit)
        similar = [match[0] for match in matches if match[1] >= threshold and match[0] != value]

        if similar:
            partial_duplicates[value] = similar
            processed.update([value] + similar)

    return partial_duplicates


def find_partial_duplicates_across(df1, df2, threshold=85):
    # Reset index to avoid index errors
    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)

    # Create combined columns
    df1['combined'] = df1['Product Name'].astype(str).str.lower() + ' ' + \
                      df1['Volume'].astype(str) + ' ' + df1['Pack Size'].astype(str)

    df2['combined'] = df2['Product Name'].astype(str).str.lower() + ' ' + \
                      df2['Volume'].astype(str) + ' ' + df2['Pack Size'].astype(str)

    partial_duplicates = {}

    for idx1, val1 in df1['combined'].items():
        matches = process.extract(val1, df2['combined'], scorer=fuzz.token_set_ratio, limit=5)
        similar_matches = [(df2.iloc[idx2], score) for match, score, idx2 in matches if score >= threshold]

        if similar_matches:
            partial_duplicates[val1] = [(match['combined'], score) for match, score in similar_matches]

    return partial_duplicates

