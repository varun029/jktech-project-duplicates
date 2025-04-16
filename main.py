import pandas as pd
from utils.data_utils import read_excel_file,split_dt_data,save_dataframe,split_fd_data,sort_ascending,split_volume_and_pack_size,normalize_volume_column
from utils.missing import miss_val_column, miss_val_percentage
from utils.duplicates import exact_duplicate_rows, num_exact_duplicates,find_duplicates_within_df,drop_exact_within_df,find_duplicates_across_df
from utils.drop import drop_unnecessary_columns
from utils.standardize import standardize_text,remove_spaces,clean_pack_size_column,fill_value,convert_pack_size_to_number,convert_column_to_str

#Read Files
fd_df=read_excel_file('./datasets/Only_FD_Data 3.xlsx')
dt_df=read_excel_file('./datasets/Only_DT_Data 3.xlsx')

#Split into Product Name and Pack Size {for FD_DATA and DT_Data}
fd_df = split_fd_data(fd_df, 'SKU_NAME')
dt_df = split_dt_data(dt_df, 'SKU Description')

#save_dataframe(fd_df,'/Users/vandana/Desktop/fd_df.xlsx')
#save_dataframe(dt_df, '/Users/vandana/Desktop/dt_df.xlsx')

print(fd_df.describe)
print('\n')
print(dt_df.describe)
print('\n')

#Check Missing Values
print("Missing values in FD data:")
fd_missing = miss_val_column(fd_df)
fd_missing_percent = miss_val_percentage(fd_df, fd_missing)

print("Missing values in DT data:")
dt_missing = miss_val_column(dt_df)
dt_missing_percent = miss_val_percentage(dt_df, dt_missing)

#Check Exact Duplicates Rows
print("Exact duplicate rows in FD data:")
fd_duplicates = exact_duplicate_rows(fd_df)
fd_num_duplicates = num_exact_duplicates(fd_df)

print("Exact duplicate rows in DT data:")
dt_duplicates = exact_duplicate_rows(dt_df)
dt_num_duplicates = num_exact_duplicates(dt_df)

print(fd_df.columns)
print(dt_df.columns)
print('\n')

# Define columns to keep
fd_columns_to_keep = ['SKU_ID', 'SKU_NAME', 'Product Name', 'Pack Size', 'CLASS_ID', 'CLASS_NAME', 'SUBCLASS_ID', 'SUBCLASS_NAME']
dt_columns_to_keep = ['SKU Id', 'SKU Description', 'Product Name', 'Pack Size', 'Class ID', 'Class Description', 'Sub Class Id',
       'Sub Class Description']

# Drop unnecessary columns
fd_data_cleaned = drop_unnecessary_columns(fd_df, fd_columns_to_keep)
dt_data_cleaned = drop_unnecessary_columns(dt_df, dt_columns_to_keep)



#fd_data_cleaned.rename(columns={'SKU_ID': 'SKU_ID', 'CLASS_ID': 'CLASS_ID', 'CLASS_NAME': 'CLASS_NAME', 'SUBCLASS_ID': 'SUBCLASS_ID', 'SUBCLASS_NAME': 'SUBCLASS_NAME'}, inplace=True)
dt_data_cleaned.rename(columns={'SKU Id': 'SKU_ID', 'SKU Description': 'SKU_NAME', 'Class ID': 'CLASS_ID', 'Class Description': 'CLASS_NAME', 'Sub Class Id': 'SUBCLASS_ID', 'Sub Class Description': 'SUBCLASS_NAME'}, inplace=True)

print(fd_data_cleaned.columns)
print(dt_data_cleaned.columns)
print('\n')

print(fd_data_cleaned.describe)
print('\n')
print(dt_data_cleaned.describe)
print('\n')


for col in ['SKU_NAME','Product Name', 'Pack Size', 'CLASS_NAME', 'SUBCLASS_NAME']:
    fd_data_cleaned = standardize_text(fd_data_cleaned.copy(), col)
    dt_data_cleaned = standardize_text(dt_data_cleaned.copy(), col)


print(fd_data_cleaned.head())
print('\n')
print(dt_data_cleaned.head())
print('\n')

fd_data_cleaned=remove_spaces(fd_data_cleaned.copy(),'Pack Size')
fd_data_final = split_volume_and_pack_size(fd_data_cleaned.copy())

dt_data_cleaned=remove_spaces(dt_data_cleaned.copy(),'Pack Size')
dt_data_final = split_volume_and_pack_size(dt_data_cleaned.copy())


print(fd_data_final['Volume'].head())
print(dt_data_final['Volume'].head())

print(fd_data_final.describe)
print('\n')
print(dt_data_final.describe)
print('\n')


#sorted_fd=sort_ascending(fd_data_final.copy(),'SKU_NAME')
#sorted_dt=sort_ascending(dt_data_final.copy(),'SKU_NAME')

#save_dataframe(sorted_fd,'/Users/vandana/Desktop/sorted_fd.xlsx')
#save_dataframe(sorted_dt,'/Users/vandana/Desktop/sorted_dt.xlsx')

#cleaning pack size 
fd_data_final = clean_pack_size_column(fd_data_final, 'Pack Size')
dt_data_final = clean_pack_size_column(dt_data_final, 'Pack Size')

#filling values in pack size
fd_data_final=fill_value(fd_data_final.copy(),'Pack Size')
dt_data_final=fill_value(dt_data_final.copy(),'Pack Size')

#converting to numeric column
fd_data_final=convert_pack_size_to_number(fd_data_final.copy(),'Pack Size')
dt_data_final=convert_pack_size_to_number(dt_data_final.copy(),'Pack Size')

#standardizing volume colum
fd_volume_normalized=normalize_volume_column(fd_data_final,'Volume')
dt_volume_normalized=normalize_volume_column(dt_data_final,'Volume')

fd_data_normalized=convert_column_to_str(fd_volume_normalized,'Volume')
fd_data_normalized=convert_column_to_str(fd_volume_normalized,'Pack Size')

dt_data_normalized=convert_column_to_str(dt_volume_normalized,'Volume')
dt_data_normalized=convert_column_to_str(dt_volume_normalized,'Pack Size')

#save_dataframe(fd_volume_normalized,'/Users/vandana/Desktop/fd_data_normalized.xlsx')
#save_dataframe(dt_volume_normalized,'/Users/vandana/Desktop/dt_data_normalized.xlsx')

duplicates_within_fd=find_duplicates_within_df(fd_data_normalized.copy(),['Product Name','Volume','Pack Size'])
duplicates_within_dt=find_duplicates_within_df(dt_data_normalized.copy(),['Product Name','Volume','Pack Size'])

print(duplicates_within_fd.head())
print('\n')
print(duplicates_within_dt.head())

fd_exact_dropped=drop_exact_within_df(fd_data_normalized.copy(),['Product Name','Volume','Pack Size'])
dt_exact_dropped=drop_exact_within_df(dt_data_normalized.copy(),['Product Name','Volume','Pack Size'])

print(fd_exact_dropped.info())
print('\n')
print(dt_exact_dropped.info())
print('\n')

# exact dups across dfs
df1_cols = ['Product Name', 'Volume', 'Pack Size']
df2_cols = ['Product Name', 'Volume', 'Pack Size']
fd_exact_dropped,dt_exact_dropped = find_duplicates_across_df(fd_exact_dropped, dt_exact_dropped, df1_cols, df2_cols)

print(fd_exact_dropped.info())
print('\n')
print(dt_exact_dropped.info())
print('\n')

save_dataframe(fd_exact_dropped,'/Users/vandana/Desktop/fd_exact_dropped.xlsx')
save_dataframe(dt_exact_dropped,'/Users/vandana/Desktop/dt_exact_dropped.xlsx')