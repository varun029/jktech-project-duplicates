import pandas as pd
from utils.data_utils import read_excel_file,split_product_column

fd_df=read_excel_file('./datasets/Only_FD_Data 3.xlsx')
dt_df=read_excel_file('./datasets/Only_DT_Data 3.xlsx')

fd_df=split_product_column(fd_df,'SKU_NAME')


