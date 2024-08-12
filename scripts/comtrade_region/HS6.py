import os
import pandas as pd

# Directory containing the CSV files
input_directory = "./data/raw_data/comtrade/regions/"
output_directory = "./data/processed_data/comtrade/HS6/"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Columns to keep
columns_to_keep = [
    "period", "reporterCode", "reporterISO", "reporterDesc", "flowDesc",
    "partnerCode", "partnerISO", "partnerDesc", "cmdCode", "cmdDesc",
    "aggrLevel", "qtyUnitAbbr", "qty", "netWgt", "fobvalue", "primaryValue"
]

# Iterate through each CSV file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(".csv"):
        # Construct the full file path
        filepath = os.path.join(input_directory, filename)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(filepath)
        
        # Filter the DataFrame where aggrLevel == 6
        filtered_df = df[df['aggrLevel'] == 6]
        
        # Keep only the specified columns
        filtered_df = filtered_df[columns_to_keep]
        
        # Construct the output file path
        output_filepath = os.path.join(output_directory, filename)
        
        # Save the filtered DataFrame to a new CSV file
        filtered_df.to_csv(output_filepath, index=False)
        
        print(f"Filtered data saved to {output_filepath}")