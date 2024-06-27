import os
import pandas as pd

# Define the path to the main folder containing the country subfolders
main_folder_path = './data/'

# Initialize a dictionary to store the results
product_counts = {}

# Loop through all subfolders in the main folder
for country_folder in os.listdir(main_folder_path):
    country_folder_path = os.path.join(main_folder_path, country_folder)
    
    if os.path.isdir(country_folder_path):
        # Initialize a dictionary to store the results for this country
        product_counts[country_folder] = {}
        
        # Loop through all files in the country folder
        for filename in os.listdir(country_folder_path):
            if filename.endswith('.csv'):
                # Construct the full file path
                file_path = os.path.join(country_folder_path, filename)
                
                # Extract the year from the filename (assuming the year is part of the filename)
                year = filename.split('.')[0].split()[-1]
                
                # Load the data with specified dtype for CmdCode and low_memory set to False
                try:
                    data = pd.read_csv(file_path, encoding='latin1', low_memory=False, dtype={'CmdCode': str})
                    
                    # Count the total number of unique products exported in the year
                    total_products_exported = data['CmdCode'].nunique()
                    
                    # Store the result in the dictionary for the country and year
                    product_counts[country_folder][year] = total_products_exported
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

# Print the results
for country in product_counts:
    print(f"Country: {country}")
    for year in product_counts[country]:
        print(f"  Year: {year}")
        print(f"    Total number of unique products exported: {product_counts[country][year]}")
