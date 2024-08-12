import os
import pandas as pd

# Directories
stata_directory = "./data/processed_data/stata/"
hs2_directory = "./data/processed_data/comtrade/HS2/"
output_directory = "./data/processed_data/comtrade/stata_uvr/"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Loop through each regional file in the Stata directory
for stata_filename in os.listdir(stata_directory):
    if stata_filename.endswith("_stata.csv"):
        # Load the Stata file data
        stata_filepath = os.path.join(stata_directory, stata_filename)
        stata_df = pd.read_csv(stata_filepath)
        
        # Ensure consistent case and remove leading/trailing spaces
        stata_df['iso3_tp_o'] = stata_df['iso3_tp_o'].str.strip().str.upper()
        stata_df['iso3_tp_d'] = stata_df['iso3_tp_d'].str.strip().str.upper()

        # Initialize an empty DataFrame to store merged data for this region
        merged_df = pd.DataFrame()

        # Loop through each year
        for year in [1995, 2000, 2005, 2010, 2015]:
            # Load the corresponding HS2 data for the year
            hs2_filename = f"comtrade_data_{year}.csv"
            hs2_filepath = os.path.join(hs2_directory, hs2_filename)
            hs2_df = pd.read_csv(hs2_filepath)
            
            # Ensure consistent case and remove leading/trailing spaces
            hs2_df['reporterISO'] = hs2_df['reporterISO'].str.strip().str.upper()
            hs2_df['partnerISO'] = hs2_df['partnerISO'].str.strip().str.upper()
            
            # Filter Stata data for the current year
            stata_df_year = stata_df[stata_df['year'] == year]
            
            # Perform an inner merge to keep only matching rows
            merged = hs2_df.merge(
                stata_df_year,
                how='inner',
                left_on=['period', 'reporterISO', 'partnerISO'],
                right_on=['year', 'iso3_tp_o', 'iso3_tp_d']
            )
            
            # Calculate the UVR column
            merged['uvr'] = merged['primaryValue'] / merged['netWgt']
            
            # Append the merged data to the overall DataFrame for this region
            merged_df = pd.concat([merged_df, merged], ignore_index=True)
        
        # Select and reorder columns to match the desired output structure
        columns_to_keep = [
            'year', 'iso3_tp_o', 'iso3_tp_d', 'trade_comb', 'PTA_ever', 'PTA_year', 'PTA_id', 'PTA', 
            'PTA_lag', 'int', 'NS_o', 'NS_d', 'NNpair', 'NSpair', 'SSpair', 'NNPTA', 'NSPTA', 'SSPTA', 
            'NNPTA_lag', 'NSPTA_lag', 'SSPTA_lag', 'hs2', 'netWgt', 'primaryValue', 'uvr'
        ]
        merged_df = merged_df[columns_to_keep]
        
        # Save the final merged DataFrame to a new CSV file
        output_filepath = os.path.join(output_directory, stata_filename.replace("_stata.csv", "_final.csv"))
        merged_df.to_csv(output_filepath, index=False)
        
        print(f"Processed data saved to {output_filepath}")
