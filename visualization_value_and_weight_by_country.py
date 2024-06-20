import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the path to the main folder containing the country subfolders
main_folder_path = './data/'

# Initialize dictionaries to store the results
value_counts = {}
weight_counts = {}

# Loop through all subfolders in the main folder
for country_folder in os.listdir(main_folder_path):
    country_folder_path = os.path.join(main_folder_path, country_folder)
    
    if os.path.isdir(country_folder_path):
        # Initialize dictionaries to store the results for this country
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
                        
                        # Sum the total value of exports and total net weight of exports for the year
                        total_value = year_data['PrimaryValue'].sum()
                        total_weight = year_data['NetWgt'].sum()
                        
                        # Store the results in the dictionaries for the country and year
                        value_counts[country_folder][year] = total_value
                        weight_counts[country_folder][year] = total_weight
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

# Function to plot the data
def plot_data(data_dict, y_label, title):
    years = sorted({year for country in data_dict for year in data_dict[country]})
    countries = list(data_dict.keys())

    data_for_plot = {
        'Country': [],
        'Year': [],
        'Value': []
    }

    for country in data_dict:
        for year in years:
            data_for_plot['Country'].append(country)
            data_for_plot['Year'].append(year)
            data_for_plot['Value'].append(data_dict[country].get(year, 0))

    # Create a DataFrame for the data to be plotted
    df_plot = pd.DataFrame(data_for_plot)

    # Plot the data
    plt.figure(figsize=(12, 8))
    for country in countries:
        subset = df_plot[df_plot['Country'] == country]
        plt.plot(subset['Year'], subset['Value'], marker='o', label=country)

    plt.xlabel('Year')
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot Total Value of Exports
plot_data(value_counts, 'Total Value of Exports (PrimaryValue)', 'Total Value of Exports by Year for Each Country')

# Plot Total Net Weight of Exports
plot_data(weight_counts, 'Total Net Weight of Exports (NetWgt)', 'Total Net Weight of Exports by Year for Each Country')
