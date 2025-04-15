import pandas as pd
from utils.data_utils import read_excel_file,split_product_column,save_dataframe,split_fd_data,sort_ascending
from utils.missing import miss_val_column, miss_val_percentage
from utils.duplicates import exact_duplicate_rows, num_exact_duplicates, find_exact_duplicates_across_df
from utils.drop import drop_unnecessary_columns
from utils.standardize import standardize_text

#Read Files
fd_df=read_excel_file('./datasets/Only_FD_Data 3.xlsx')
dt_df=read_excel_file('./datasets/Only_DT_Data 3.xlsx')

#Split into Product Name and Pack Size {for FD_DATA and DT_Data}
fd_df = split_fd_data(fd_df, 'SKU_NAME')
dt_df = split_product_column(dt_df, 'SKU Description')

#Check Missing Values
print("Missing values in FD data:")
fd_missing = miss_val_column(fd_df)
fd_missing_percent = miss_val_percentage(fd_df, fd_missing)

print("Missing values in DT data:")
dt_missing = miss_val_column(dt_df)
dt_missing_percent = miss_val_percentage(dt_df, dt_missing)

#Check Exact Duplicates
print("Exact duplicates in FD data:")
fd_duplicates = exact_duplicate_rows(fd_df)
fd_num_duplicates = num_exact_duplicates(fd_df)

print("Exact duplicates in DT data:")
dt_duplicates = exact_duplicate_rows(dt_df)
dt_num_duplicates = num_exact_duplicates(dt_df)

print(fd_df.columns)
print(dt_df.columns)

# Define columns to keep
fd_columns_to_keep = ['SKU_ID', 'SKU_NAME', 'Product Name', 'Pack Size', 'CLASS_ID', 'CLASS_NAME', 'SUBCLASS_ID', 'SUBCLASS_NAME']
dt_columns_to_keep = ['SKU Id', 'SKU Description', 'Product Name', 'Pack Size', 'Class ID', 'Class Description', 'Sub Class Id',
       'Sub Class Description']

# Drop unnecessary columns
fd_data_cleaned = drop_unnecessary_columns(fd_df, fd_columns_to_keep)
dt_data_cleaned = drop_unnecessary_columns(dt_df, dt_columns_to_keep)

#fd_data_cleaned.rename(columns={'SKU_ID': 'SKU_ID', 'CLASS_ID': 'CLASS_ID', 'CLASS_NAME': 'CLASS_NAME', 'SUBCLASS_ID': 'SUBCLASS_ID', 'SUBCLASS_NAME': 'SUBCLASS_NAME'}, inplace=True)
dt_data_cleaned.rename(columns={'SKU Id': 'SKU_ID', 'SKU Description': 'SKU_NAME', 'Class ID': 'CLASS_ID', 'Class Description': 'CLASS_NAME', 'Sub Class Id': 'SUBCLASS_ID', 'Sub Class Description': 'SUBCLASS_NAME'}, inplace=True)

for col in ['SKU_NAME','Product Name', 'Pack Size', 'CLASS_NAME', 'SUBCLASS_NAME']:
    fd = standardize_text(fd_data_cleaned, col)
    dt = standardize_text(dt_data_cleaned, col)

print(fd_data_cleaned.head())
print('\n')
print(dt_data_cleaned.head())
print('\n')

exact_dups=find_exact_duplicates_across_df(fd_data_cleaned,dt_data_cleaned)

if not exact_dups.empty:
    print(f'Exact duplicates across datasets are: {exact_dups}\n')
else:
    print("No exact duplicates across datasets.\n")

save_dataframe(fd_data_cleaned,'/Users/vandana/Desktop/fd_data_cleaned.xlsx')
save_dataframe(dt_data_cleaned, '/Users/vandana/Desktop/dt_data_cleaned.xlsx')

sorted_fd=sort_ascending(fd_data_cleaned.copy(),'SKU_NAME')
sorted_dt=sort_ascending(dt_data_cleaned.copy(),'SKU_NAME')

save_dataframe(sorted_fd,'/Users/vandana/Desktop/sorted_fd.xlsx')
save_dataframe(sorted_dt,'/Users/vandana/Desktop/sorted_dt.xlsx')