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

    # Helper function to split a single row
    def split_row(text):
        if not isinstance(text, str):
            return text, ''
        
        # Regex pattern to catch number + unit (like 100GM, 1.5L, etc.)
        pattern = r'(\d+(\.\d+)?\s?[A-Za-z]+)'
        matches = re.findall(pattern, text)

        if not matches:
            return text.strip(), ''
        
        # Take the first match
        pack_size = matches[0][0]

        # Remove only the first occurrence of the pack size pattern from the text
        product_name = re.sub(pattern, '', text, count=1).strip()
        return product_name, pack_size

    # Apply the helper to the dataframe
    new_cols = df[original_column].apply(lambda x: pd.Series(split_row(x), index=['Product Name', 'Pack Size']))

    # Insert new columns next to the original column
    col_index = df.columns.get_loc(original_column)
    for i, col_name in enumerate(new_cols.columns):
        df.insert(col_index + 1 + i, col_name, new_cols[col_name])

    return df


    
