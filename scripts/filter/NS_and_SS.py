import pandas as pd

# # Load main data
# main_data_path = "./data/processed_data/merged_trade_gravity_NS_SS.csv"
# main_data = pd.read_csv(main_data_path, low_memory=False)

# # Load DESTA data
# desta_data_path = "./data/raw_data/pta/desta_list_of_treaties_02_02_dyads.csv"
# desta_data = pd.read_csv(desta_data_path, low_memory=False)

# # Define the list of North countries
# north_countries = [
#     'AUS', 'AUT', 'BEL', 'CAN', 'DNK', 'FIN', 'FRA', 'DEU', 'GRC', 'ISL', 'ISR', 'ITA', 'JPN',
#     'LUX', 'NLD', 'NZL', 'NOR', 'PRT', 'ESP', 'SWE', 'CHE', 'GBR', 'USA'
# ]

# # Create a new variable for ordered pairs in the main dataset
# main_data['pair1'] = main_data['iso3num_o'] + main_data['iso3num_d']
# main_data['pair2'] = main_data['iso3num_d'] + main_data['iso3num_o']

# # Create a new variable for ordered pairs in the DESTA dataset
# desta_data['desta_pair1'] = desta_data['iso1'] + desta_data['iso2']
# desta_data['desta_pair2'] = desta_data['iso2'] + desta_data['iso1']

# # Create an empty NS and SS columns in the main dataset
# main_data['NS'] = 0
# main_data['SS'] = 0

# # Sort DESTA data by year in descending order
# desta_data = desta_data.sort_values(by='year', ascending=False)

# # Function to update NS and SS columns
# def update_ns_ss(desta_row, main_df, north_countries):
#     year = desta_row['year']
#     pair1 = desta_row['desta_pair1']
#     pair2 = desta_row['desta_pair2']
    
#     # Find relevant rows in the main data
#     relevant_rows = main_df[(main_df['pair1'].isin([pair1, pair2])) | (main_df['pair2'].isin([pair1, pair2]))]
    
#     for index, row in relevant_rows.iterrows():
#         if row['year'] >= year:
#             if row['iso3_d'] in north_countries:
#                 main_df.at[index, 'NS'] = 1
#             else:
#                 main_df.at[index, 'SS'] = 1

# # Iterate over the DESTA data and update the main dataset
# for _, desta_row in desta_data.iterrows():
#     update_ns_ss(desta_row, main_data, north_countries)

# Save the updated dataset
updated_data_path = "./data/processed_data/updated_merged_trade_gravity_NS_SS.csv"
main_data = pd.read_csv(updated_data_path, low_memory=False)

# print(data.shape)
# print(data.columns)

# # Count the number of rows where NS is 1
# ns_count = data[data['NS'] == 1].shape[0]

# # Count the number of rows where SS is 1
# ss_count = data[data['SS'] == 1].shape[0]

# total = ns_count + ss_count

# # Print the results
# print(f"Number of rows where NS is 1: {ns_count}")
# print(f"Number of rows where SS is 1: {ss_count}")
# print(f"Total {total}")

# Define the list of North countries
north_countries = [
    'AUS', 'AUT', 'BEL', 'CAN', 'DNK', 'FIN', 'FRA', 'DEU', 'GRC', 'ISL', 'ISR', 'ITA', 'JPN',
    'LUX', 'NLD', 'NZL', 'NOR', 'PRT', 'ESP', 'SWE', 'CHE', 'GBR', 'USA'
]

# Initialize the Post column
main_data['Post'] = 0

# Update the Post column
for index, row in main_data.iterrows():
    if row['NS'] == 1 or row['SS'] == 1:
        main_data.at[index, 'Post'] = 1

# Function to determine if a country pair is NS or SS
def determine_ns_ss(row):
    if (row['iso3_o'] in north_countries and row['iso3_d'] not in north_countries) or (row['iso3_o'] not in north_countries and row['iso3_d'] in north_countries):
        return 'NS'
    elif row['iso3_o'] not in north_countries and row['iso3_d'] not in north_countries:
        return 'SS'
    else:
        return None

# Determine NS and SS for each row
main_data['pair_type'] = main_data.apply(determine_ns_ss, axis=1)

# Save the updated dataset
main_data.to_csv("./data/processed_data/final_merged_trade_gravity_NS_SS.csv", index=False)

# Print the results for verification
ns_count = main_data[main_data['NS'] == 1].shape[0]
ss_count = main_data[main_data['SS'] == 1].shape[0]
post_count = main_data[main_data['Post'] == 1].shape[0]

print(f"Number of rows where NS is 1: {ns_count}")
print(f"Number of rows where SS is 1: {ss_count}")
print(f"Number of rows where Post is 1: {post_count}")