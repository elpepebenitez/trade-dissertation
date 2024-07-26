import pandas as pd

# Load the datasets
country_agreements_df = pd.read_csv('./output_data/country_agreements_classified_summary.csv')
dahi_df = pd.read_csv('./input_data/dahi/dahi.csv')

# Rename the 'Code' column in dahi_df to match the 'Code' column in country_agreements_df
dahi_df.rename(columns={'Code': 'Code'}, inplace=True)

# Merge the dataframes on the 'Code' column
merged_df = pd.merge(country_agreements_df, dahi_df[['Code', 'Cat']], left_on='Code', right_on='Code', how='left')

# Rename the 'Cat' column to 'dahi'
merged_df.rename(columns={'Cat': 'dahi'}, inplace=True)

# Save the final DataFrame to a new CSV file
output_path = './output_data/ptas_per_country_summary/ptas_per_country_and_classifications.csv'
merged_df.to_csv(output_path, index=False)
