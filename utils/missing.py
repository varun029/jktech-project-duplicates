import pandas as pd
import numpy as np

def miss_val_column(df):
    missing_vals=df.isnull().sum()
    print('The number of missing values per column are: ')
    print(missing_vals)
    print('\n')
    return missing_vals

def miss_val_percentage(df,missing_vals):
    total_cells=np.prod(df.shape)
    total_missing_val=missing_vals.sum()

    percent_missing=(total_missing_val/total_cells)*100
    print(f'The percentage of missing values in the dataset are: {percent_missing}%')
    print('\n')
    return percent_missing