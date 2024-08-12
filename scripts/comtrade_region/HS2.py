import os
import pandas as pd

# Input and output directories
input_directory = "./data/processed_data/comtrade/HS6/"
output_directory = "./data/processed_data/comtrade/HS2/"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Iterate through each CSV file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(".csv"):
        # Construct the full file path
        filepath = os.path.join(input_directory, filename)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(filepath)
        
        # Ensure the cmdCode column is treated as a string
        df['cmdCode'] = df['cmdCode'].astype(str)
        
        # Create the hs2 column by extracting the first two digits of cmdCode
        df['hs2'] = df['cmdCode'].str[:2]
        
        # Group by the necessary columns and aggregate netWgt and primaryValue
        aggregated_df = df.groupby(
            ["period", "reporterCode", "reporterISO", "reporterDesc",
             "partnerCode", "partnerISO", "partnerDesc", "hs2"],
            as_index=False
        ).agg(
            netWgt=pd.NamedAgg(column="netWgt", aggfunc="sum"),
            primaryValue=pd.NamedAgg(column="primaryValue", aggfunc="sum")
        )
        
        # Select the columns to keep in the final output
        columns_to_keep = [
            "period", "reporterCode", "reporterISO", "reporterDesc",
            "partnerCode", "partnerISO", "partnerDesc", "netWgt",
            "primaryValue", "hs2"
        ]
        aggregated_df = aggregated_df[columns_to_keep]
        
        # Construct the output file path
        output_filepath = os.path.join(output_directory, filename)
        
        # Save the aggregated DataFrame to a new CSV file
        aggregated_df.to_csv(output_filepath, index=False)
        
        print(f"Processed data saved to {output_filepath}")
