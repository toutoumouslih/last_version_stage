import pandas as pd
import json
from datetime import datetime
from decimal import Decimal

def clean_value(value):
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    if isinstance(value, str):
        value = value.strip()
        if value.lower() in ['nan', 'null', 'none', '']:
            return None
        try:
            return Decimal(value)
        except:
            return value
    return value

def convert_excel_to_json():
    # Read the Excel file
    df = pd.read_excel('myapp/management/commands/med salem.xlsx', header=3)
    
    # Initialize the result dictionary
    DEMOGRAPHIC_DATA = {}
    
    # Process each row
    for _, row in df.iterrows():
        try:
            # Extract code from the first column
            code = str(row.iloc[0]).strip()
            if not code or code.lower() in ['nan', 'none', '']:
                continue
                
            # Extract region name from the second column
            region_name = str(row.iloc[1]).strip()
            
            # Skip empty rows
            if not region_name:
                continue
                
            data = {
                'name': region_name,
                'population': clean_value(row.iloc[2]),
                'male': clean_value(row.iloc[3]),
                'female': clean_value(row.iloc[4]),
                'population_10_plus': clean_value(row.iloc[5]),
                'single_rate': clean_value(row.iloc[6]),
                'married_rate': clean_value(row.iloc[7]),
                'divorced_rate': clean_value(row.iloc[8]),
                'widowed_rate': clean_value(row.iloc[9]),
                'school_enrollment_rate': clean_value(row.iloc[10]),
                'illiteracy_rate_10_plus': clean_value(row.iloc[11]),
                'population_15_plus': clean_value(row.iloc[12]),
                'illiteracy_rate_15_plus': clean_value(row.iloc[13]),
                'no_education': clean_value(row.iloc[14]),
                'preschool': clean_value(row.iloc[15]),
                'primary': clean_value(row.iloc[16]),
                'middle_school': clean_value(row.iloc[17]),
                'high_school': clean_value(row.iloc[18]),
                'university': clean_value(row.iloc[19])
            }
            
            # Remove None values
            data = {k: v for k, v in data.items() if v is not None}
            
            # Add to dictionary
            DEMOGRAPHIC_DATA[code] = data
            
        except Exception as e:
            print(f"Error processing row: {e}")
            continue
    
    # Save to JSON file
    with open('myapp/management/commands/demographic_data_structured.json', 'w', encoding='utf-8') as f:
        json.dump(DEMOGRAPHIC_DATA, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"Successfully converted {len(DEMOGRAPHIC_DATA)} records to JSON format")

if __name__ == '__main__':
    convert_excel_to_json() 