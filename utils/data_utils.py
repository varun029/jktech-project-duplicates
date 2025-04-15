import pandas as pd
import re 

def read_excel_file(file_path):
    df = pd.read_excel(file_path)
    print(f"File loaded successfully with shape: {df.shape}\n")
    print(df.head())
    print('\n')
    return df

def split_product_column(df, column_name):
    # Pattern to catch quantity + unit
    quantity_pattern = re.compile(r'(\d+(\.\d+)?\s*(PK|CN|CAN|OZ|Z|BTL|FLOZ|FL\s?OZ|L|LTR|LIT|LITER))', re.IGNORECASE)

    def extract(text):
        # Extract quantity parts
        quantity_matches = quantity_pattern.findall(text)
        quantities = [match[0].replace(" ", "").upper() for match in quantity_matches]  # Clean spacing

        # Remove quantity parts from text
        text_without_quantity = quantity_pattern.sub('', text)

        # Clean up extra spaces
        product_name = re.sub(r'\s+', ' ', text_without_quantity).strip()

        return pd.Series([product_name.title(), ' / '.join(quantities)])

    # Apply function
    new_columns = df[column_name].apply(extract)
    new_columns.columns = ['Product Name', 'Pack Size']

    # Insert new columns next to the original
    col_idx = df.columns.get_loc(column_name)
    for i, col_name in enumerate(new_columns.columns):
        df.insert(col_idx + i + 1, col_name, new_columns.iloc[:, i])

    return df


def save_dataframe(df, file_path):

    df.to_excel(file_path,index=False)
    print(f"DataFrame saved to {file_path}\n")


import pandas as pd
import re

def split_fd_data(df, original_column):
    def split_row(text):
        if not isinstance(text, str):
            return '', ''
        
        # Special case handling
        if text.strip() == '6 PK 1/2 LIT DASANI WATER':
            return 'DASANI WATER', '6 PK 1/2 LIT'
        
        # General rule: split at first digit
        match = re.search(r'\d', text)
        if match:
            index = match.start()
            product_name = text[:index].strip()
            pack_size = text[index:].strip()
            return product_name, pack_size
        else:
            return text.strip(), ''
    
    # Apply the function and create two new columns
    new_cols = df[original_column].apply(lambda x: pd.Series(split_row(x), index=['Product Name', 'Pack Size']))
    
    # Find the index position of the original column
    col_index = df.columns.get_loc(original_column)
    
    # Insert the new columns right after the original column
    for i, col_name in enumerate(new_cols.columns):
        df.insert(col_index + 1 + i, col_name, new_cols[col_name])
    
    return df

def sort_ascending(df,column_name):
    sorted_df=df.sort_values(by=column_name, ascending=True)
    
    return sorted_df


    
