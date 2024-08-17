import os
import pandas as pd
import csv

# Define the folder path
folder_path = "./data/processed_data/ptas/"

# Initialize dictionaries to store data
unique_countries_by_region = {}
unique_agreements_by_region = {}
agreement_country_mapping = {}

# Initialize sets to store unique values across all regions
all_unique_countries = set()

# Iterate through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        
        # Load the data
        df = pd.read_csv(file_path)
        
        # Get the region name from the filename (assuming region name is part of the filename)
        region = os.path.splitext(filename)[0]
        
        # Unique countries in this file
        unique_countries = set(df['country1']).union(set(df['country2']))
        unique_countries_by_region[region] = len(unique_countries)
        
        # Add to the global set of unique countries
        all_unique_countries.update(unique_countries)
        
        # Unique agreements and their member countries in this file
        for agreement in df['wto_name'].unique():
            if agreement not in agreement_country_mapping:
                agreement_country_mapping[agreement] = set()
            agreement_countries = set(df.loc[df['wto_name'] == agreement, 'country1']).union(
                                  set(df.loc[df['wto_name'] == agreement, 'country2']))
            agreement_country_mapping[agreement].update(agreement_countries)

# Convert sets to sorted lists for easier readability
all_unique_countries = sorted(all_unique_countries)
agreement_country_mapping = {k: sorted(v) for k, v in agreement_country_mapping.items()}

# Display the list of all unique countries
print(f"Total Unique Countries (All Regions): {len(all_unique_countries)}")
print("\nList of All Unique Countries:")
for country in all_unique_countries:
    print(country)

# Save the agreements and their respective countries to a CSV file
output_file = "./data/processed_data/ptas/pta_list.csv"
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Agreement Name', 'Countries'])
    for agreement, countries in agreement_country_mapping.items():
        writer.writerow([agreement, ', '.join(countries)])

print(f"\nThe list of agreements and their respective countries has been saved to {output_file}")


# import os
# import pandas as pd

# # Define the folder path
# folder_path = "./data/processed_data/ptas/"

# # Initialize dictionaries to store counts by region
# unique_countries_by_region = {}
# unique_agreements_by_region = {}

# # Initialize sets to store unique values across all regions
# all_unique_countries = set()
# all_unique_agreements = set()

# # Iterate through each file in the folder
# for filename in os.listdir(folder_path):
#     if filename.endswith(".csv"):
#         file_path = os.path.join(folder_path, filename)
        
#         # Load the data
#         df = pd.read_csv(file_path)
        
#         # Get the region name from the filename (assuming region name is part of the filename)
#         region = os.path.splitext(filename)[0]
        
#         # Unique countries in this file
#         unique_countries = set(df['iso1']).union(set(df['iso2']))
#         unique_countries_by_region[region] = len(unique_countries)
        
#         # Add to the global set of unique countries
#         all_unique_countries.update(unique_countries)
        
#         # Unique agreements in this file
#         unique_agreements = set(df['base_treaty'])
#         unique_agreements_by_region[region] = len(unique_agreements)
        
#         # Add to the global set of unique agreements
#         all_unique_agreements.update(unique_agreements)

# # Final counts
# total_unique_countries = len(all_unique_countries)
# total_unique_agreements = len(all_unique_agreements)

# # Display results
# print(f"Total Unique Countries (All Regions): {total_unique_countries}")
# print(f"Total Unique Agreements (All Regions): {total_unique_agreements}")
# print("\nUnique Countries by Region:")
# for region, count in unique_countries_by_region.items():
#     print(f"{region}: {count}")
# print("\nUnique Agreements by Region:")
# for region, count in unique_agreements_by_region.items():
#     print(f"{region}: {count}")

# import pandas as pd

# # Load the dataset
# file_path = "./data/raw_data/pta/desta_list_of_treaties_02_02_dyads.csv"
# df = pd.read_csv(file_path)

# # 1) Earliest and oldest years in the dataset using the "year" column
# earliest_year = df['year'].min()
# latest_year = df['year'].max()

# # 2) Total count of unique countries combining the "iso1" and "iso2" columns
# unique_countries = pd.concat([df['iso1'], df['iso2']]).nunique()

# # 3) Total count of unique agreements using the "base_treaty" column
# unique_agreements = df['base_treaty'].nunique()

# # 4) Total count of unique countries that appear in the data between the year 2000 and 2010
# filtered_df_2000_2010 = df[(df['year'] >= 2000) & (df['year'] <= 2010)]
# unique_countries_2000_2010 = pd.concat([filtered_df_2000_2010['iso1'], filtered_df_2000_2010['iso2']]).nunique()

# # 5) Total count of unique agreements between the year 2000 and 2010
# unique_agreements_2000_2010 = filtered_df_2000_2010['base_treaty'].nunique()

# # Display results
# print(f"Earliest Year: {earliest_year}")
# print(f"Latest Year: {latest_year}")
# print(f"Total Unique Countries: {unique_countries}")
# print(f"Total Unique Agreements: {unique_agreements}")
# print(f"Unique Countries (2000-2010): {unique_countries_2000_2010}")
# print(f"Unique Agreements (2000-2010): {unique_agreements_2000_2010}")