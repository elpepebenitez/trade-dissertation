import pandas as pd

# Local paths to the data files
# local_trade_data_file_path = './data/processed_data/filtered_TPe_V202401.csv'
# local_gravity_data_file_path = './data/processed_data/filtered_Gravity_V202211.csv'
# local_country_key_file_path = './data/raw_data/cepii/TradeProd_Gravity_country_key.csv'
# local_merged_data_file_path = './data/processed_data/merged_trade_gravity_data.csv'
# agreements_file_path = 'data/processed_data/country_agreements_classified_summary.csv'
# gravity_file_path = './data/processed_data/filtered_Gravity_V202211.csv'
# trade_file_path = './data/processed_data/filtered_TPe_V202401.csv'

# # Read the agreements file
# agreements_df = pd.read_csv(agreements_file_path)

# # Filter countries with at least one North-South and one South-South agreement
# eligible_countries = agreements_df[
#     (agreements_df['North-South'] > 0) & (agreements_df['South-South'] > 0)
# ]['iso3'].tolist()

# # print(len(eligible_countries))

# # Read the gravity and trade data
# gravity_df = pd.read_csv(gravity_file_path)
# trade_df = pd.read_csv(trade_file_path)

# print(gravity_df.shape)
# print(trade_df.shape)

# # Filter the datasets
# filtered_gravity_df = gravity_df[
#     (gravity_df['iso3_o'].isin(eligible_countries))
# ]

# filtered_trade_df = trade_df[
#     (trade_df['iso3_tp_o'].isin(eligible_countries))
# ]

# # Remove rows where 'iso3_o' is equal to 'iso3_d' in the gravity dataset
# filtered_gravity_data = filtered_gravity_df[filtered_gravity_df['iso3_o'] != filtered_gravity_df['iso3_d']]

# # Select columns to keep
# gravity_columns_to_keep = [
#     'year', 'iso3_o', 'iso3_d', 'iso3num_o', 'iso3num_d', 'dist', 
#     'contig', 'comlang_off', 'gdp_o', 'gdp_d', 'fta_wto'
# ]

# trade_columns_to_keep = [
#     'year', 'iso3_tp_o', 'iso3_tp_d', 'trade_comb'
# ]

# filtered_gravity_data = filtered_gravity_data[gravity_columns_to_keep]
# filtered_trade_df = filtered_trade_df[trade_columns_to_keep]

# Save the filtered datasets
filtered_gravity_file_path = './data/processed_data/filtered_Gravity_NS_SS.csv'
filtered_trade_file_path = './data/processed_data/filtered_Trade_NS_SS.csv'

# print(filtered_gravity_data.shape)
# print(filtered_trade_df.shape)

# filtered_gravity_data.to_csv(filtered_gravity_file_path, index=False)
# filtered_trade_df.to_csv(filtered_trade_file_path, index=False)

# # Filter rows where 'iso3_tp_o' is equal to 'iso3_tp_d'
# inter_trade_rows = filtered_gravity_data[filtered_gravity_data['iso3_o'] == filtered_gravity_data['iso3_d']]

# # Get the count of these rows
# intra_trade_count = inter_trade_rows.shape[0]

# print(f"Number of gravity rows where 'iso3_tp_o' is equal to 'iso3_tp_d': {intra_trade_count}")

# # Filter rows where 'iso3_tp_o' is equal to 'iso3_tp_d'
# intra_trade_rows = filtered_trade_df[filtered_trade_df['iso3_tp_o'] == filtered_trade_df['iso3_tp_d']]

# # Get the count of these rows
# intra_trade_count = intra_trade_rows.shape[0]

# print(f"Number of TPe rows where 'iso3_tp_o' is equal to 'iso3_tp_d': {intra_trade_count}")

# print("Filtered datasets saved.")

#########################################

# Path to save the merged data
merged_file_path = "./data/processed_data/merged_trade_gravity_NS_SS.csv"

# # Chunksize for processing data in chunks
# chunk_size = 10000

# # Read the gravity data into a DataFrame
# gravity_data = pd.read_csv(filtered_gravity_file_path)

# # Function to process and merge chunks
# def process_chunk(chunk, gravity_data):
#     # Merge the chunk with the gravity data
#     merged_chunk = pd.merge(
#         chunk, 
#         gravity_data, 
#         left_on=['iso3_tp_o', 'iso3_tp_d', 'year'], 
#         right_on=['iso3_o', 'iso3_d', 'year'], 
#         how='left'
#     )

#     # Identify rows where iso3_tp_o is equal to iso3_tp_d
#     self_trade_mask = merged_chunk['iso3_tp_o'] == merged_chunk['iso3_tp_d']

#     # Fill missing values for control variables in those rows with 0
#     columns_to_fill = ['dist', 'contig', 'comlang_off', 'fta_wto', 'gdp_d']
#     merged_chunk.loc[self_trade_mask, columns_to_fill] = 0

#     return merged_chunk

# # Initialize an empty DataFrame to store the merged data
# merged_data = pd.DataFrame()

# # Process the trade data in chunks
# for chunk in pd.read_csv(filtered_trade_file_path, chunksize=chunk_size):
#     merged_chunk = process_chunk(chunk, gravity_data)
#     merged_data = pd.concat([merged_data, merged_chunk])

# # Save the merged data to a new CSV file
# merged_data.to_csv(merged_file_path, index=False)

# print(f"Merged data saved to {merged_file_path}")

#########################################

merged_df = pd.read_csv(merged_file_path)

print(merged_df.shape)
print(merged_df.columns)











