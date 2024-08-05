# https://comtradeapi.un.org/data/v1/get/{typeCode}/
# {freqCode}/{clCode}[?reporterCode][&period][&partnerCode][&partner2Code]
# [&cmdCode][&flowCode][&customsCode][&motCode][&aggregateBy][&breakdownMode][&includeDesc]

# typeCode='C' for commodities
# freqCode='A' for annual
# clCode='HS for HS codes as trade classification system
# period='2000' for a year. Multi value input should be in the form of csv (Codes separated by comma (,))
# reporterCode='36' is for M49 code of the countries separated by comma (,)). https://comtradeapi.un.org/files/v1/app/reference/Reporters.json 591 Panama
# flowCode='X' for exports. M for imports.
# cmdCode=None https://comtradeapi.un.org/files/v1/app/reference/H6.json

# Bulk
# https://comtradeapi.un.org/bulk/v1/get/{typeCode}/{freqCode}/{clCode}[?reporterCode][&period][&publishedDateFrom][&publishedDateTo]
# comtradeapicall.bulkDownloadFinalFile(subscription_key, directory, typeCode='C', freqCode='A', clCode='H6', period='1995, 1996', reporterCode=251, decompress=True)

import pandas as pd
import os
import requests
from dotenv import load_dotenv
import comtradeapicall
import time

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('COMTRADE_API_KEY')
type_code = "C"  # Commodity
freq_code = "A"  # Annual
classification_code = "HS"  # Harmonized System
trade_flow_code = "X"  # Exports
max_records = 250000

# # Read the CSV file
# csv_file_path = "./data/processed_data/country_agreements_classified_summary.csv"
# data = pd.read_csv(csv_file_path)

# # Filter the countries based on the conditions
# filtered_data = data[(data['North-South'] > 0) & (data['South-South'] > 0)]

# # Keep the specified columns
# filtered_data = filtered_data[['iso3', 'numeric_code', 'region', 'income_group']]

# # Clean the numeric_code column to remove or handle non-finite values
# filtered_data = filtered_data.dropna(subset=['numeric_code'])
# filtered_data['numeric_code'] = filtered_data['numeric_code'].astype(int)

# # Ensure the directory exists
# directory = "./data/raw_data/comtrade/"
# os.makedirs(directory, exist_ok=True)

# finished = ["8","12","24","28","32","44","48","51","52","70","72","76","84","90","96", 
#             "100","104","108","116","120","132","140","148","152","156","158","174","178","180","188","191","196",
#             "203","204","212","214","218","222","226","231","233","234","242","262","266","268","270","275","288","296",
#             "308","320","324","328","332","340","344","348","356","360","384","388","398",
#             "400","404","410","414","418","422","426","428","430","440","450","454","458","466","470","478","480","484","496","498","499",
#             "504","508","512","516","520","548","558","562","566","586","591","598",
#             "600","604","608","616","624","634","642","643","646","659","662","670","678","682","686","688","690","694",
#             "702","703","704","705","706","710","716","729","740","748","760","764","768","776","780","784","788","792","798",
#             "800","804","807","818","834","854","858","882","894"]

# # Function to fetch data for a given reporter-year combination
# def fetch_data(reporter_code, year):
#     try:
#         print(f"Fetching data for reporter {reporter_code} for year {year}")
#         data = comtradeapicall.getFinalData(
#             subscription_key=api_key,
#             typeCode=type_code,
#             freqCode=freq_code,
#             clCode=classification_code,
#             period=str(year),
#             reporterCode=str(reporter_code),
#             partnerCode=None,  # Fetch all partners
#             flowCode=trade_flow_code,
#             cmdCode=None,  # Default value
#             partner2Code=None,  # Default value
#             customsCode=None,  # Default value
#             motCode=None,  # Default value
#             maxRecords=max_records,
#             format_output='JSON',
#             aggregateBy=None,
#             breakdownMode='classic', 
#             countOnly=None, 
#             includeDesc=True
#         )
#         if not data.empty:
#             return data
#         else:
#             print(f"No data found for reporter {reporter_code} for year {year}")
#             return pd.DataFrame()
#     except Exception as e:
#         print(f"Error processing data for reporter {reporter_code} for year {year}: {e}")
#         return pd.DataFrame()

# # Filter out the finished countries
# filtered_data = filtered_data[~filtered_data['numeric_code'].astype(str).isin(finished)]

# # Loop through the filtered reporter countries and download data
# for index, row in filtered_data.iterrows():
#     reporter_code = str(row['numeric_code'])
#     country_data = []
#     for year in range(1995, 2016):
#         data = fetch_data(reporter_code, year)
#         country_data.append(data)
#         print(f"Processed data for reporter {reporter_code} for year {year}")
#         time.sleep(1)  # Respectful delay to avoid hitting rate limits

#     # Concatenate data for the country and save to a CSV file
#     country_df = pd.concat(country_data, ignore_index=True)

#     # Save the data to a CSV file for the country
#     country_csv_file_path = os.path.join(directory, f"comtrade_export_data_{reporter_code}_1995_2015.csv")
#     country_df.to_csv(country_csv_file_path, index=False)
#     print(f"Saved data for reporter {reporter_code} to {country_csv_file_path}")

# print("All data has been processed and saved.")

# # Save the data to a CSV file
# output_csv_file_path = "./data/raw_data/comtrade/comtrade_export_data_1995_2015_filtered.csv"
# df.to_csv(output_csv_file_path, index=False)


# ###################################################################################################################

# mydf = comtradeapicall.getFinalData(api_key, typeCode='C', freqCode='A', clCode='HS', period='1995',
#                                     reporterCode='591', cmdCode=None, flowCode='X', partnerCode=None,
#                                     partner2Code=None,
#                                     customsCode=None, motCode=None, maxRecords=250000, format_output='JSON',
#                                     aggregateBy=None, breakdownMode='classic', countOnly=None, includeDesc=True)

# print(mydf.head(5))
# print(mydf.count())

data = comtradeapicall.getFinalData(
            subscription_key=api_key,
            typeCode=type_code,
            freqCode=freq_code,
            clCode=classification_code,
            period="2005",
            reporterCode="760",
            partnerCode=None,  # Fetch all partners
            flowCode=trade_flow_code,
            cmdCode=None,  # Default value
            partner2Code=None,  # Default value
            customsCode=None,  # Default value
            motCode=None,  # Default value
            maxRecords=max_records,
            format_output='JSON',
            aggregateBy=None,
            breakdownMode='classic', 
            countOnly=None, 
            includeDesc=True
        )

print(data)