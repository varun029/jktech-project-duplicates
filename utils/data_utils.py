import pandas as pd
import re 

def read_excel_file(file_path):
    df = pd.read_excel(file_path)
    print(f"File loaded successfully with shape: {df.shape}\n")
    print(df.head())
    print('\n')
    return df


def split_dt_data(df, column_name):
    import re
    import pandas as pd
    
    pattern = re.compile(
        r'^(.*?)[ ]+(\d+(?:\.\d+)?(?:\/\d+)?[ ]*(?:Z|OZ|ML|L|LT|LTR)[ ]*(?:Can|CN|BTL|Bottle)?)$',
        re.IGNORECASE
    )
    start_pattern = re.compile(
        r'^(20Z)[ ]+(.*)$',
        re.IGNORECASE
    )
    
    def extract(text):
        if not isinstance(text, str):
            return pd.Series(['', ''])
        text = text.strip()

        if text.upper() == "COKE ZERO SUG COLA 13.2OZ BTL":
            return pd.Series(["Coke Zero Sug Cola BTL", "13.2OZ"])
        
        if text.strip() == '6 PK 1/2 LIT DASANI WATER':
            return pd.Series(['DASANI WATER', '1/2 LIT 6 PK'])
        
        if text.upper() == "POWERWATER LEMON 20 Z SPRTSCAP":
            return pd.Series(["Powerwater Lemon Sprtscap", "20 Z"])
        if text.upper() == "POWERADE LEMON LIME 20Z SPRTS":
            return pd.Series(["Powerade Lemon Lime Sprts", "20Z"])
            
        can_match = re.match(r'^(.*?)\s+(\d+(?:\.\d+)?Z)\s+CAN$', text, re.IGNORECASE)
        if can_match:
            product_name = can_match.group(1) + " Can"
            pack_size = can_match.group(2)
            return pd.Series([product_name.title(), pack_size.upper()])
            
        pk_cn_match = re.match(r'^(.*?)\s+(\d+PK)\s+CN$', text, re.IGNORECASE)
        if pk_cn_match:
            product_name = pk_cn_match.group(1) + " Cn"
            pack_size = pk_cn_match.group(2)
            return pd.Series([product_name.title(), pack_size.upper()])
            
        btl_match = re.match(r'^(.*?)\s+(\d+(?:\.\d+)?Z)\s+BTL$', text, re.IGNORECASE)
        if btl_match:
            product_name = btl_match.group(1) + " Btl"
            pack_size = btl_match.group(2)
            return pd.Series([product_name.title(), pack_size.upper()])
        
        start_match = start_pattern.match(text)
        if start_match:
            pack_size = start_match.group(1).strip()
            product_name = start_match.group(2).strip()
            return pd.Series([product_name.title(), pack_size.upper()])
        
        match = pattern.match(text)
        if match:
            product_name = match.group(1).strip()
            pack_size = match.group(2).strip()
            return pd.Series([product_name.title(), pack_size.upper()])
        
        number_match = re.search(r'[ ]+\d+', text)
        if number_match:
            split_point = number_match.start()
            product_name = text[:split_point].strip()
            pack_size = text[split_point:].strip()
            return pd.Series([product_name.title(), pack_size.upper()])
            
        return pd.Series([text.title(), ''])
    
    new_columns = df[column_name].apply(extract)
    new_columns.columns = ['Product Name', 'Pack Size']
    
    col_idx = df.columns.get_loc(column_name)
    for i, col_name in enumerate(new_columns.columns):
        df.insert(col_idx + i + 1, col_name, new_columns.iloc[:, i])
    
    return df


def save_dataframe(df, file_path):

    df.to_excel(file_path,index=False)
    print(f"DataFrame saved to {file_path}\n")


def split_fd_data(df, original_column):
    def split_row(text):
        if not isinstance(text, str):
            return '', ''
        
        text = text.strip()
        
        if text == '6 PK 1/2 LIT DASANI WATER':
            return 'DASANI WATER', '1/2 LIT 6 PK'
        
        fanta_match = re.search(r'(FANTA\s+\w+)\s+(\d+(?:\.\d+)?OZ)\s+CAN', text, re.IGNORECASE)
        if fanta_match:
            product_name = fanta_match.group(1) + " CAN"
            pack_size = fanta_match.group(2)
            return product_name, pack_size
        
        match = re.search(r'\d', text)
        if match:
            index = match.start()
            product_name = text[:index].strip()
            pack_size = text[index:].strip()
            return product_name, pack_size
        else:
            return text.strip(), ''
    
    new_cols = df[original_column].apply(lambda x: pd.Series(split_row(x), index=['Product Name', 'Pack Size']))
    
    col_index = df.columns.get_loc(original_column)
    
    for i, col_name in enumerate(new_cols.columns):
        df.insert(col_index + 1 + i, col_name, new_cols[col_name])
    
    return df


def sort_ascending(df,column_name):
    sorted_df=df.sort_values(by=column_name, ascending=True)
    
    return sorted_df


def split_volume_and_pack_size(df):
  
    def extract_pack_info(text):
        if not isinstance(text, str) or pd.isna(text) or text.strip() == '':
            return ('', '')
        text = text.strip()
        
        slash_pattern = re.search(r'(\d+(?:\s*)?(?:pk|pack|pck))/(\d+(?:\.\d+)?(?:\s*)?(?:z|oz))', text, re.IGNORECASE)
        if slash_pattern:
            pack_size = slash_pattern.group(1).strip()
            volume = slash_pattern.group(2).strip()
            return (volume, pack_size)
        
        match = re.search(r'(\d+(?:\.\d+)?)(?:\s*)(pack|pk|pck)$', text, re.IGNORECASE)
        if match:
            split_point = match.start()
            volume = text[:split_point].strip()
            pack_size = text[split_point:].strip()
            return (volume, pack_size)
        else:
            return (text, '')

    df[['Volume', 'Pack Size']] = df['Pack Size'].apply(lambda x: pd.Series(extract_pack_info(x)))

    sku_col = 'SKU_NAME' if 'SKU_NAME' in df.columns else 'SKU_ID'
    col_order = [sku_col, 'Product Name', 'Volume', 'Pack Size']
    other_cols = [col for col in df.columns if col not in col_order]
    df = df[col_order + other_cols]

    return df


def normalize_volume_column(df, column_name):
    """
    Converts the volume column to milliliters (ml) and replaces the original column.
    """

    # Conversion factors to milliliters
    conversion_factors = {
        'oz': 29.5735,
        'floz': 29.5735,
        'z': 29.5735,
        'l': 1000,
        'lit': 1000,
        'ltr': 1000,
        'liter': 1000,
        'ml': 1,
        'fl': 29.5735  # If 'fl' is used as 'fl oz'
    }

    def extract_value_and_unit(column_name):
        if not isinstance(column_name, str):
            return None
        
        match = re.search(r'(\d+(?:\.\d+)?(?:/\d+(?:\.\d+)?)?)\s*([a-zA-Z]+)', column_name)
        if match:
            value = match.group(1)
            unit = match.group(2).lower()
            if '/' in value:
                value = value.split('/')[-1]
            try:
                value = float(value)
            except:
                return None
            
            for u in conversion_factors:
                if unit.startswith(u):
                    return value, u
        return None

    def convert_volume_to_ml(column_name):
        result = extract_value_and_unit(column_name)
        if result:
            value, unit = result
            return round(value * conversion_factors[unit], 2)
        return None

    df[column_name] = df[column_name].apply(convert_volume_to_ml)
    return df
