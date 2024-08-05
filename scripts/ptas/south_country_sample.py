import pandas as pd

# Define the file paths
file_path_treaties = "./data/raw_data/pta/desta_list_of_treaties_02_02_dyads.csv"
file_path_country_summary = "./data/processed_data/country_agreements_classified_summary.csv"
file_path_comtrade = "./data/raw_data/comtrade/final_combined_comtrade_data.csv"
file_path_gravity = "./data/processed_data/final_merged_trade_gravity_NS_SS.csv"

# Read the CSV files
df_treaties = pd.read_csv(file_path_treaties)
df_country_summary = pd.read_csv(file_path_country_summary)
df_comtrade = pd.read_csv(file_path_comtrade)
df_gravity = pd.read_csv(file_path_gravity)

# Convert iso1 and iso2 to strings
df_treaties['iso1'] = df_treaties['iso1'].astype(str)
df_treaties['iso2'] = df_treaties['iso2'].astype(str)

# Filter rows where the year is between 2000 and 2010 (inclusive)
filtered_df = df_treaties[(df_treaties['year'] >= 2000) & (df_treaties['year'] <= 2010)]


# excluded_iso3 = [
#     'AUS', 'AUT', 'BEL', 'CAN', 'DNK', 'FIN', 'FRA', 'DEU', 'GRC', 'ISL', 'ISR', 'ITA', 'JPN',
#     'LUX', 'NLD', 'NZL', 'NOR', 'PRT', 'ESP', 'SWE', 'CHE', 'GBR', 'USA'
# ]

excluded_iso3num = [
    '36', '40', '56', '124', '208', '246', '250', '276', '300', '352', '376', '380', '392',
    '442', '528', '554', '578', '620', '724', '752', '756', '826', '840'
]

# Create pairs of ISO codes and ensure they are unique
iso_pairs = filtered_df[['iso1', 'iso2']].drop_duplicates()

# Exclude pairs where both ISO codes are in the excluded list
iso_pairs_filtered = iso_pairs[~((iso_pairs['iso1'].isin(excluded_iso3num)) & (iso_pairs['iso2'].isin(excluded_iso3num)))]

# Convert the DataFrame of ISO pairs to a list of tuples
iso_pairs_list = [tuple(x) for x in iso_pairs_filtered.to_records(index=False)]

# Print the total count of unique pairs
total_pairs_count = len(iso_pairs_list)
print(f"Total number of unique pairs (excluding NN agreements): {total_pairs_count}")

# Extract unique ISO codes from the filtered pairs that are not in the excluded list
unique_countries = set(iso_pairs_filtered['iso1']).union(set(iso_pairs_filtered['iso2']))
unique_countries_not_excluded = {str(code) for code in unique_countries} - set(excluded_iso3num)

# Print the count of unique countries not in the excluded list
total_unique_countries_count = len(unique_countries_not_excluded)
print(f"Total number of unique countries not in the excluded list: {total_unique_countries_count}")

# Ensure numeric_code in df_country_summary is treated as string and remove '.0' suffix
df_country_summary['numeric_code'] = df_country_summary['numeric_code'].astype(str).str.replace('.0', '', regex=False)

# Filter the countries based on North-South and South-South agreements
filtered_countries_summary = df_country_summary[
    (df_country_summary['numeric_code'].isin(unique_countries_not_excluded)) &
    ((df_country_summary['North-South'] > 0) & (df_country_summary['South-South'] > 0))
]

# Extract the numeric codes of the remaining countries
filtered_country_codes = set(filtered_countries_summary['numeric_code'])

# Filter the iso_pairs_list to only include pairs with the filtered countries
filtered_iso_pairs_list = [pair for pair in iso_pairs_list if pair[0] in filtered_country_codes or pair[1] in filtered_country_codes]
# Print the total count of unique pairs with the filtered countries
filtered_pairs_count = len(filtered_iso_pairs_list)
print(f"Filtered number of unique pairs (excluding NN agreements and with North-South or South-South agreements > 0): {filtered_pairs_count}")

# Print the count of the filtered countries
total_filtered_countries_count = len(filtered_country_codes)
print(f"Total number of unique countries not in the excluded list with North-South or South-South agreements > 0: {total_filtered_countries_count}")

# Filter countries from filtered_country_codes which have data for every year between 1995 and 2015 in the comtrade file
years_required = ['1995','2000','2005', '2010', '2015']
df_comtrade['period'] = df_comtrade['period'].astype(str)
df_comtrade['reporterCode'] = df_comtrade['reporterCode'].astype(str)

available_countries = set()
for country_code in filtered_country_codes:
    country_years = df_comtrade[df_comtrade['reporterCode'] == country_code]['period'].unique()
    if all(year in country_years for year in years_required):
        available_countries.add(country_code)

# Print the count of the filtered countries with complete data
total_available_countries_count = len(available_countries)
print(f"Total number of unique countries with complete data for 1995, 2000, 2005, 2010, and 2015: {total_available_countries_count}")

# Print available countries
# print(f"Available countries: {available_countries}")

# Check for the same countries in the gravity file
df_gravity['year'] = df_gravity['year'].astype(str)
df_gravity['iso3num_o'] = df_gravity['iso3num_o'].astype(str).str.replace('.0', '', regex=False)
df_gravity['iso3num_d'] = df_gravity['iso3num_d'].astype(str).str.replace('.0', '', regex=False)
df_gravity['iso3_tp_o'] = df_gravity['iso3_tp_o'].astype(str)
df_gravity['iso3_tp_d'] = df_gravity['iso3_tp_d'].astype(str)

# Create a mapping from iso3num_o to iso3_tp_o
iso3num_to_iso3tp = df_gravity.dropna(subset=['iso3num_o', 'iso3_tp_o'])[['iso3num_o', 'iso3_tp_o']].drop_duplicates().set_index('iso3num_o')['iso3_tp_o'].to_dict()

# Print unique values of iso3num_o and year in gravity data for debugging
# print(f"Unique iso3num_o in gravity data: {df_gravity['iso3num_o'].unique()}")
# print(f"Unique years in gravity data: {df_gravity['year'].unique()}")

final_available_countries = set()
for country_code in available_countries:
    country_years = df_gravity[df_gravity['iso3num_o'] == country_code]['year'].unique()
    iso3_tp_o_code = iso3num_to_iso3tp.get(country_code)
    self_trade_years = df_gravity[(df_gravity['iso3_tp_o'] == iso3_tp_o_code) & (df_gravity['iso3_tp_o'] == df_gravity['iso3_tp_d'])]['year'].unique()
    # print(f"Country: {country_code}, Country years: {country_years}, Self-trade years: {self_trade_years}")
    if all(year in country_years for year in years_required) and all(year in self_trade_years for year in years_required):
        final_available_countries.add(country_code)

# Print the count of the filtered countries with complete data in gravity
total_final_available_countries_count = len(final_available_countries)
print(f"Total number of unique countries with complete data for 1995, 2000, 2005, 2010, and 2015 in both comtrade and gravity files: {total_final_available_countries_count}")

# # Print final available countries
print(f"Final available countries: {final_available_countries}")

# Filter filtered_iso_pairs_list to only include pairs with at least one country in final_available_countries
final_filtered_iso_pairs_list = [pair for pair in filtered_iso_pairs_list if pair[0] in final_available_countries or pair[1] in final_available_countries]
final_filtered_pairs_count = len(final_filtered_iso_pairs_list)
print(f"Filtered number of unique pairs (excluding NN agreements and with North-South or South-South agreements > 0): {final_filtered_pairs_count}")

# Print the final list of filtered unique ISO pairs
# print(final_filtered_iso_pairs_list)

# {'348', '440', '188', '792', '484', '191', '498', '428', '591', '218', '703', '32', '705', 
#  '788', '854', '410', '196', '398', '140', '152', '600', '450', '807', '120', '702', '642', 
#  '740', '344', '470', '400', '508', '558', '170', '222', '108', '320', '818', '504', '800', 
#  '764', '340', '233', '616', '203', '156', '682', '84', '360', '512', '894', '458', '454', 
#  '562', '231', '270', '780', '384', '604', '12', '716', '662', '480', '858', '76'}