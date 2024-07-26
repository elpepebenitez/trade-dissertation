# import pandas as pd

# # Load the data
# file_path = './data/Argentina/AG6 Argentina 2000.csv'
# data = pd.read_csv(file_path, encoding='latin1', low_memory=False, dtype={'CmdCode': str})

# # Count the total number of unique products exported in the year 2000
# total_products_exported = data['CmdCode'].nunique()

# # Print the result
# print("Total number of unique products exported in the year 2000:", total_products_exported)

import pandas as pd

# Load the data with different settings
file_path = './data/Mexico/AG6 Mexico 2000-2001.csv'
data = pd.read_csv(file_path, encoding='latin1', low_memory=False)

# Display the first few rows of the dataset to understand its structure
print(data.head())
