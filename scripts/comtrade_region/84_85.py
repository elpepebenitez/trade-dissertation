import os
import pandas as pd

# Directory containing the final region files
input_directory = "./data/processed_data/comtrade/stata_uvr/"
output_directory = "./data/processed_data/comtrade/stata_uvr/"

# Ensure the output directory exists (though we are saving in the same directory)
os.makedirs(output_directory, exist_ok=True)

# Loop through each file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith("_final.csv"):
        # Load the region file
        filepath = os.path.join(input_directory, filename)
        df = pd.read_csv(filepath)
        
        # Filter rows where hs2 == 84
        df_84 = df[df['hs2'] == 84]
        
        # Filter rows where hs2 == 85
        df_85 = df[df['hs2'] == 85]
        
        # Define output file paths
        output_filepath_84 = os.path.join(output_directory, filename.replace("_final.csv", "_84.csv"))
        output_filepath_85 = os.path.join(output_directory, filename.replace("_final.csv", "_85.csv"))
        
        # Save the filtered DataFrames to new CSV files
        df_84.to_csv(output_filepath_84, index=False)
        df_85.to_csv(output_filepath_85, index=False)
        
        print(f"Files saved: {output_filepath_84}, {output_filepath_85}")
