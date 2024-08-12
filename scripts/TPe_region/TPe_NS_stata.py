import os
import pandas as pd

# Define the path to the directory containing the CSV files
data_dir = './data/processed_data/stata/'

# List of CSV files to process
csv_files = [
    'Africa_stata.csv', 'Americas_stata.csv', 'Asia_stata.csv', 
    'Europe_stata.csv', 'Intercontinental_stata.csv', 'Oceania_stata.csv'
]

# List of northern countries
north_iso3 = [
    'AUS', 'AUT', 'BEL', 'CAN', 'DNK', 'FIN', 'FRA', 'DEU', 'GRC', 'ISL', 'ISR', 
    'ITA', 'JPN', 'LUX', 'NLD', 'NZL', 'NOR', 'PRT', 'ESP', 'SWE', 'CHE', 'GBR', 'USA'
]

for file_name in csv_files:
    # Construct the full path to the CSV file
    file_path = os.path.join(data_dir, file_name)
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Add 'int' column
    df['internationaltrade'] = (df['iso3_tp_o'] != df['iso3_tp_d']).astype(int)
    
    # Add 'NS_o' and 'NS_d' columns
    df['NS_o'] = df['iso3_tp_o'].apply(lambda x: 'N' if x in north_iso3 else 'S')
    df['NS_d'] = df['iso3_tp_d'].apply(lambda x: 'N' if x in north_iso3 else 'S')
    
    # Add 'NNpair', 'NSpair', and 'SSpair' columns
    df['NNpair'] = ((df['NS_o'] == 'N') & (df['NS_d'] == 'N')).astype(int)
    df['NSpair'] = ((df['NS_o'] == 'N') ^ (df['NS_d'] == 'N')).astype(int)  # Use XOR to check if only one is 'N'
    df['SSpair'] = ((df['NS_o'] == 'S') & (df['NS_d'] == 'S')).astype(int)
    
    # Initialize 'NNPTA', 'NSPTA', and 'SSPTA' columns with 0
    df['NNPTA'] = 0
    df['NSPTA'] = 0
    df['SSPTA'] = 0

    # Assign values for 'NNPTA', 'NSPTA', and 'SSPTA' only where 'PTA' == 1
    df.loc[df['PTA'] == 1, 'NNPTA'] = df['NNpair']
    df.loc[df['PTA'] == 1, 'NSPTA'] = df['NSpair']
    df.loc[df['PTA'] == 1, 'SSPTA'] = df['SSpair']

    # Initialize 'NNPTA_lag', 'NSPTA_lag', and 'SSPTA_lag' columns with 0
    df['NNPTA_lag'] = 0
    df['NSPTA_lag'] = 0
    df['SSPTA_lag'] = 0
    
    # Assign values for 'NNPTA_lag', 'NSPTA_lag', and 'SSPTA_lag' only where 'PTA_lag' == 1
    df.loc[df['PTA_lag'] == 1, 'NNPTA_lag'] = df['NNpair']
    df.loc[df['PTA_lag'] == 1, 'NSPTA_lag'] = df['NSpair']
    df.loc[df['PTA_lag'] == 1, 'SSPTA_lag'] = df['SSpair']
    
    # Save the modified DataFrame back to a CSV file
    df.to_csv(file_path, index=False)
