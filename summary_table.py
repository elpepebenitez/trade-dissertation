import os
import pandas as pd

# Define the path to the main folder containing the country subfolders
main_folder_path = './data/'

# Initialize dictionaries to store the results
product_counts = {}
value_counts = {}
weight_counts = {}

# Loop through all subfolders in the main folder
for country_folder in os.listdir(main_folder_path):
    country_folder_path = os.path.join(main_folder_path, country_folder)
    
    if os.path.isdir(country_folder_path):
        # Initialize dictionaries to store the results for this country
        product_counts[country_folder] = {}
        value_counts[country_folder] = {}
        weight_counts[country_folder] = {}
        
        # Loop through all files in the country folder
        for filename in os.listdir(country_folder_path):
            if filename.endswith('.csv'):
                # Construct the full file path
                file_path = os.path.join(country_folder_path, filename)
                
                # Load the data with specified dtype for CmdCode and low_memory set to False
                try:
                    data = pd.read_csv(file_path, encoding='latin1', low_memory=False, dtype={'CmdCode': str})
                    
                    # Extract the year from the Period column
                    data['Year'] = data['Period'].astype(str).str[:4]
                    
                    # Convert PrimaryValue and NetWgt columns to numeric, setting errors='coerce' to handle non-numeric values
                    data['PrimaryValue'] = pd.to_numeric(data['PrimaryValue'], errors='coerce')
                    data['NetWgt'] = pd.to_numeric(data['NetWgt'], errors='coerce')
                    
                    # Loop through each year in the data
                    for year in data['Year'].unique():
                        # Filter data for the specific year
                        year_data = data[data['Year'] == year]
                        
                        # Count the total number of unique products exported in the year
                        total_products_exported = year_data['CmdCode'].nunique()
                        
                        # Sum the total value of exports and total net weight of exports for the year
                        total_value = year_data['PrimaryValue'].sum()
                        total_weight = year_data['NetWgt'].sum()
                        
                        # Store the results in the dictionaries for the country and year
                        if year not in product_counts[country_folder]:
                            product_counts[country_folder][year] = total_products_exported
                        else:
                            product_counts[country_folder][year] += total_products_exported

                        if year not in value_counts[country_folder]:
                            value_counts[country_folder][year] = total_value
                        else:
                            value_counts[country_folder][year] += total_value

                        if year not in weight_counts[country_folder]:
                            weight_counts[country_folder][year] = total_weight
                        else:
                            weight_counts[country_folder][year] += total_weight
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

# Combine all results into a single DataFrame
combined_data = {
    'Country': [],
    'Year': [],
    'Unique Products Exported': [],
    'Total Value of Exports (PrimaryValue)': [],
    'Total Net Weight of Exports (NetWgt)': []
}

for country in product_counts:
    for year in sorted(product_counts[country].keys()):
        combined_data['Country'].append(country)
        combined_data['Year'].append(year)
        combined_data['Unique Products Exported'].append(product_counts[country][year])
        combined_data['Total Value of Exports (PrimaryValue)'].append(value_counts[country][year])
        combined_data['Total Net Weight of Exports (NetWgt)'].append(weight_counts[country][year])

# Create a DataFrame for the combined data
df_combined = pd.DataFrame(combined_data)

# Save to a CSV file
df_combined.to_csv('./data/Export_Data_Summary.csv', index=False)

# Display the combined DataFrame
df_combined.head()
