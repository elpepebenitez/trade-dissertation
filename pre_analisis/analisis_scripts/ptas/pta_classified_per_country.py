import pandas as pd

# Load the datasets
countries_df = pd.read_csv('./input_data/world_bank/countries.csv')
all_df = pd.read_csv('./input_data/iso/all.csv')
classified_df = pd.read_csv('./output_data/classified_membership.csv')

# Map alpha-3 codes to numeric ISO codes using all_df
alpha_to_numeric = all_df.set_index('alpha-3')['country-code'].to_dict()

# Add numeric ISO codes to countries_df
countries_df['numeric_code'] = countries_df['Code'].map(alpha_to_numeric)

# Initialize columns for agreement counts
countries_df['North-North'] = 0
countries_df['North-South'] = 0
countries_df['South-South'] = 0

# Loop through each country
for i, country in countries_df.iterrows():
    country_code = country['numeric_code']
    
    # Loop through each agreement in classified_df
    for j, agreement in classified_df.iterrows():
        members = eval(agreement['countries'])
        if country_code in members:
            if agreement['classification'] == 'North-North':
                countries_df.at[i, 'North-North'] += 1
            elif agreement['classification'] == 'North-South':
                countries_df.at[i, 'North-South'] += 1
            elif agreement['classification'] == 'South-South':
                countries_df.at[i, 'South-South'] += 1

# Select only the required columns
final_df = countries_df[['Economy', 'Code', 'numeric_code', 'Region', 'Income group', 'North-North', 'North-South', 'South-South']]

# Save the final DataFrame to a new CSV file
output_path = './output_data/country_agreements_classified_summary.csv'
final_df.to_csv(output_path, index=False)