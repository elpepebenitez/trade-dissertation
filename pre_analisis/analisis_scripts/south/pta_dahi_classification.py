# 2. Classify PTAs by NN, NS and SS
import pandas as pd

# Load the datasets
dahi_df = pd.read_csv('./input_data/dahi/dahi.csv')
all_df = pd.read_csv('./input_data/iso/all.csv')
latest_entries_df = pd.read_csv('./output_data/pta_updated_membership.csv')

# Create a mapping from alpha-3 codes to numeric ISO codes
alpha_to_numeric = all_df.set_index('alpha-3')['country-code'].to_dict()

# Create a dictionary to classify countries as North or South
north_countries = dahi_df[dahi_df['Cat'] == 'N']['Code'].tolist()
south_countries = dahi_df[dahi_df['Cat'] != 'N']['Code'].tolist()

# Map alpha-3 codes in dahi_df to numeric ISO codes
dahi_df['numeric_code'] = dahi_df['Code'].map(alpha_to_numeric)

# Convert the lists of numeric country codes to sets for efficient membership testing
north_numeric_codes = set(dahi_df[dahi_df['Cat'] == 'N']['numeric_code'].dropna().astype(int))
south_numeric_codes = set(dahi_df[dahi_df['Cat'] != 'N']['numeric_code'].dropna().astype(int))

# Function to classify treaties based on member countries
def classify_treaty(countries):
    north_count = len(set(countries) & north_numeric_codes)
    south_count = len(set(countries) & south_numeric_codes)
    if north_count > 0 and south_count == 0:
        return 'North-North'
    elif north_count > 0 and south_count > 0:
        return 'North-South'
    elif north_count == 0 and south_count > 0:
        return 'South-South'
    else:
        return 'Unknown'

# Apply classification to the latest_entries_df
latest_entries_df['classification'] = latest_entries_df['countries'].apply(lambda x: classify_treaty(eval(x)))

# Save the updated DataFrame to a new CSV file
latest_entries_df.to_csv('./output_data/classified_membership.csv', index=False)