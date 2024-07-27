import pandas as pd

# Load the datasets
dahi_df = pd.read_csv('./data/raw_data/dahi/dahi.csv')
country_agreements_df = pd.read_csv('./data/processed_data/country_agreements_classified_summary.csv')

# Ensure numeric_code is an integer
country_agreements_df['numeric_code'] = country_agreements_df['numeric_code'].astype('Int64')

# Merge the datasets on the 'Code' column
merged_df = dahi_df.merge(country_agreements_df[['Code', 'numeric_code']], on='Code', how='left')

# Save the resulting dataframe to a new CSV file
merged_df.to_csv('./data/processed_data/dahi_with_numeric_code.csv', index=False)

print("Merge completed and saved to 'dahi_with_numeric_code.csv'.")
