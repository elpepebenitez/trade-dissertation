import pandas as pd
import matplotlib.pyplot as plt

# Load the consolidated data
file_path = './pta/desta_list_of_treaties_02_02_dyads.csv'
dyads_df = pd.read_csv(file_path)

# print(dyads_df.head())

# # Group by the 'country1' column and count the unique values in the 'base_treaty' column
# unique_treaties_by_country = dyads_df.groupby('country1')['base_treaty'].nunique().reset_index()

# # Rename the columns for clarity
# unique_treaties_by_country.columns = ['country', 'unique_treaties_signed']

# # Sort the DataFrame by 'unique_treaties_signed' in descending order
# unique_treaties_by_country = unique_treaties_by_country.sort_values(by='unique_treaties_signed', ascending=False)

# # Save the result to a new CSV file
# unique_treaties_by_country.to_csv('./pta/unique_treaties_by_country.csv', index=False)

####

# Filter for treaties signed from the year 2000 onwards
# dyads_df = dyads_df[dyads_df['year'] >= 2000]

# Group by the 'country1' column and count the unique values in the 'base_treaty' column
unique_treaties_by_country = dyads_df.groupby('country1')['base_treaty'].nunique().reset_index()
unique_treaties_by_country.columns = ['country', 'unique_treaties_signed']

# Count the number of unique countries (country2) that have a treaty with each country (country1)
country_counts = dyads_df.groupby('country1')['country2'].nunique().reset_index()
country_counts.columns = ['country', 'num_countries']

# Create a column that lists all countries which have a treaty with each country (country1)
country_lists = dyads_df.groupby('country1')['country2'].apply(lambda x: ', '.join(x.unique())).reset_index()
country_lists.columns = ['country', 'countries_with_treaties']

# Merge the dataframes
result_df = unique_treaties_by_country.merge(country_counts, on='country').merge(country_lists, on='country')

# Create columns for the years 2000 to 2022 with the number of treaties signed each year by country1
years = list(range(2000, 2023))
for year in years:
    year_data = dyads_df[dyads_df['year'] == year].groupby('country1').size().reset_index(name=f'treaties_{year}')
    result_df = result_df.merge(year_data, how='left', left_on='country', right_on='country1')
    result_df = result_df.drop(columns=['country1'])
    result_df[f'treaties_{year}'] = result_df[f'treaties_{year}'].fillna(0).astype(int)

# Add a column counting all treaties signed between 2000 and 2022 by each country
result_df['treaties_2000_2022'] = result_df[[f'treaties_{year}' for year in years]].sum(axis=1)

# Sort the DataFrame by 'unique_treaties_signed' in descending order
result_df = result_df.sort_values(by='unique_treaties_signed', ascending=False)

# Save the result to a new CSV file
result_df.to_csv('./pta/unique_treaties_by_country_with_details.csv', index=False)