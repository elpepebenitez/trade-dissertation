import pandas as pd
import os
from dotenv import load_dotenv
import comtradeapicall
import time

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('COMTRADE_API_KEY')
type_code = "C"  # Commodity
freq_code = "A"  # Annual
classification_code = "HS"  # Harmonized System
trade_flow_code = "X"  # Exports
max_records = 250000

# Function to fetch data for a given reporter-year combination
def fetch_data(reporter_code, year):
    try:
        print(f"Fetching data for reporter {reporter_code} for year {year}")
        data = comtradeapicall.getFinalData(
            subscription_key=api_key,
            typeCode=type_code,
            freqCode=freq_code,
            clCode=classification_code,
            period=str(year),
            reporterCode=str(reporter_code),
            partnerCode=None,  # Fetch all partners
            flowCode=trade_flow_code,
            cmdCode=None,  # Default value
            partner2Code=None,  # Default value
            customsCode=None,  # Default value
            motCode=None,  # Default value
            maxRecords=max_records,
            format_output='JSON',
            aggregateBy=None,
            breakdownMode='classic',
            countOnly=None, 
            includeDesc=True
        )
        if not data.empty:
            return data
        else:
            print(f"No data found for reporter {reporter_code} for year {year}")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error processing data for reporter {reporter_code} for year {year}: {e}")
        return pd.DataFrame()

# Step 1: Extract unique country codes from all files
def extract_unique_country_codes(directory):
    all_country_codes = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath, dtype=str)
            
            # Clean data and combine iso1 and iso2 into a single list
            df['iso1'] = df['iso1'].str.strip().str.replace('.0', '', regex=False)
            df['iso2'] = df['iso2'].str.strip().str.replace('.0', '', regex=False)
            
            # Add all iso1 and iso2 values to the list
            all_country_codes.extend(df['iso1'].tolist())
            all_country_codes.extend(df['iso2'].tolist())
    
    # Get unique country codes from the combined list
    unique_countries = list(set(all_country_codes))
    unique_country_count = len(unique_countries)
    print(f'Count of unique countries: {unique_country_count}')
    print(f'Unique countries: {unique_countries}')
    return unique_countries

# Step 2: Fetch data for all unique country codes and save to intermediate file by year
def fetch_and_save_intermediate_data(unique_countries, years, output_directory):
    for year in years:
        all_data = []
        
        for country_code in unique_countries:
            data = fetch_data(country_code, year)
            all_data.append(data)
            time.sleep(0.5)  # Add a delay to avoid rate limits
        
        # Combine all data for the year into a single DataFrame
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # Save to a year-specific intermediate file
        year_filepath = os.path.join(output_directory, f"comtrade_data_{year}.csv")
        combined_data.to_csv(year_filepath, index=False)
        print(f"Data for year {year} saved to {year_filepath}")

# Step 3: Process the intermediate file to extract region-specific data
def process_intermediate_data(intermediate_filepath, directory, output_directory):
    # Load the intermediate data file
    intermediate_data = pd.read_csv(intermediate_filepath)
    
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath, dtype=str)
            
            # Clean data
            df['iso1'] = df['iso1'].str.strip().str.replace('.0', '', regex=False)
            df['iso2'] = df['iso2'].str.strip().str.replace('.0', '', regex=False)
            
            # Extract relevant data for iso1 and iso2 from the intermediate data
            relevant_data = intermediate_data[
                intermediate_data['reporterCode'].isin(df['iso1'].unique()) |
                intermediate_data['reporterCode'].isin(df['iso2'].unique())
            ]
            
            # Save to region-specific output file
            output_filepath = os.path.join(output_directory, filename.replace(".csv", "_comtrade.csv"))
            relevant_data.to_csv(output_filepath, index=False)
            print(f"Data for {filename} saved to {output_filepath}")

# Directory settings
data_directory = "./data/processed_data/ptas/"
output_directory = "./data/raw_data/comtrade/regions/"
intermediate_filepath = "./data/raw_data/comtrade/intermediate_comtrade_data.csv"
years = [1995, 2000, 2005, 2010, 2015]

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Step 1: Extract unique country codes
unique_countries = extract_unique_country_codes(data_directory)

# Step 2: Fetch and save intermediate data
fetch_and_save_intermediate_data(unique_countries, years, output_directory)

# Step 3: Process the intermediate data
# process_intermediate_data(intermediate_filepath, data_directory, output_directory)

# Count of unique countries: 143
# Unique countries: ['332', '784', '520', '392', '504', '170', '112', '499', '356', '442', 
# '12', '804', '8', '428', '410', '512', '591', '380', '438', '426', '752', '498', '462', 
# '196', '724', '682', '528', '152', '52', '670', '144', '372', '76', '643', '616', '376', 
# '64', '36', '308', '104', '600', '90', '328', '659', '858', '598', '214', '348', '604', 
# '840', '780', '548', '818', '352', '558', '404', '388', '740', '756', '634', '900', '608', 
# '414', '184', '40', '124', '320', '516', '234', '646', '703', '188', '156', '704', '422', 
# '360', '56', '108', '384', '116', '710', '578', '208', '760', '748', '233', '705', '688', '800',
#  '446', '296', '203', '524', '246', '84', '642', '344', '158', '96', '834', '788', '764', '762', 
# '28', '48', '31', '300', '882', '4', '400', '440', '480', '470', '32', '398', '44', '268', '212', 
# '242', '586', '418', '191', '662', '276', '807', '620', '70', '250', '340', '72', '50', '222', 
# '702', '798', '776', '862', '554', '458', '100', '570', '792', '826', '484']

################################################################################

# import pandas as pd
# import os
# from dotenv import load_dotenv
# import comtradeapicall
# import time

# # Load environment variables from .env file
# load_dotenv()

# api_key = os.getenv('COMTRADE_API_KEY')
# type_code = "C"  # Commodity
# freqCode = "A"  # Annual
# classification_code = "HS"  # Harmonized System
# trade_flow_code = "X"  # Exports
# max_records = 250000

# # Function to fetch data for a given reporter-year combination
# def fetch_data(reporter_code, year):
#     try:
#         print(f"Fetching data for reporter {reporter_code} for year {year}")
#         data = comtradeapicall.getFinalData(
#             subscription_key=api_key,
#             typeCode=type_code,
#             freqCode=freqCode,
#             clCode=classification_code,
#             period=str(year),
#             reporterCode=str(reporter_code),
#             partnerCode=None,  # Fetch all partners
#             flowCode=trade_flow_code,
#             cmdCode=None,  # Default value
#             partner2Code=None,  # Default value
#             customsCode=None,  # Default value
#             motCode=None,  # Default value
#             maxRecords=max_records,
#             format_output='JSON',
#             aggregateBy=None,
#             breakdownMode='classic', 
#             countOnly=None, 
#             includeDesc=True
#         )
#         if not data.empty:
#             return data
#         else:
#             print(f"No data found for reporter {reporter_code} for year {year}")
#             return pd.DataFrame()
#     except Exception as e:
#         print(f"Error processing data for reporter {reporter_code} for year {year}: {e}")
#         return pd.DataFrame()

# # Function to process files in the directory
# def process_files(directory, output_directory, years):
#     for filename in os.listdir(directory):
#         if filename.endswith(".csv"):
#             filepath = os.path.join(directory, filename)
#             print(f"Processing file: {filepath}")
            
#             # Read the file, ensuring all data is read as strings
#             df = pd.read_csv(filepath, dtype=str)
            
#             # Clean data: strip any trailing ".0"
#             df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
#             df['iso1'] = df['iso1'].str.replace('.0', '', regex=False)
#             df['iso2'] = df['iso2'].str.replace('.0', '', regex=False)

#             # Extract unique country codes from iso1 and iso2
#             unique_countries = pd.unique(df[['iso1', 'iso2']].values.ravel('K'))

#             # Prepare a list to collect all the fetched data
#             all_data = []

#             # Loop through each year and each unique country code
#             for year in years:
#                 for country_code in unique_countries:
#                     data = fetch_data(country_code, year)
#                     all_data.append(data)
                    
#                     # Add a delay to avoid hitting rate limits
#                     time.sleep(0.5)
            
#             # Combine all collected data into a single DataFrame
#             combined_data = pd.concat(all_data, ignore_index=True)
            
#             # Save the combined data to a new CSV file
#             output_filename = os.path.join(output_directory, filename.replace(".csv", "_comtrade.csv"))
#             combined_data.to_csv(output_filename, index=False)
#             print(f"Data saved to {output_filename}")

# # Directory where the CSV files are stored
# data_directory = "./data/processed_data/ptas/"
# output_directory = "./data/raw_data/comtrade/regions/"
# years = [1995, 2000, 2005, 2010, 2015]

# # Ensure the output directory exists
# os.makedirs(output_directory, exist_ok=True)

# # Start processing the files
# process_files(data_directory, output_directory, years)