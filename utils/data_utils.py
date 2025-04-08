import pandas as pd
import re 

def read_excel_file(file_path):
    df = pd.read_excel(file_path)
    print(f"File loaded successfully with shape: {df.shape}\n")
    print(df.head())
    print('\n')
    return df

#  'SKU Type' and 'Pack Size'
def split_product_column(df, original_column):
    def split_row(text):
        
        '''if not isinstance(text, str):
            return text, ''
        '''
        match = re.search(r'\d', text)
        
        if match:
            index = match.start()
            product_name = text[:index].strip()
            pack_size = text[index:].strip()     
            return product_name, pack_size
        else:
            return text.strip(), ''
    
    # Apply the function and create two new columns as a temporary DataFrame
    new_cols = df[original_column].apply(lambda x: pd.Series(split_row(x), index=['Product Name', 'Pack Size']))
    
    # Find the index position of the original column
    col_index = df.columns.get_loc(original_column)
    
    # Insert the new columns right after the original column
    for i, col_name in enumerate(new_cols.columns):
        df.insert(col_index + 1 + i, col_name, new_cols[col_name])
    
    return df
    

    
