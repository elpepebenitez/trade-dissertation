import boto3
import pandas as pd
import os
import glob

# Initialize the S3 client
s3_client = boto3.client('s3')

# Define the S3 bucket and folder
bucket_name = 'trade-dissertation-data'
folder_name = 'products/'

# List all files in the S3 bucket folder
response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
files = [item['Key'] for item in response.get('Contents', []) if item['Key'].endswith('.csv')]

# Function to read and process a single file
def process_file(key):
    try:
        # Download the file
        local_file_name = key.split('/')[-1]
        s3_client.download_file(bucket_name, key, local_file_name)

        # Read the file into a DataFrame
        df = pd.read_csv(local_file_name)

        # Check if the DataFrame contains data
        if not df.empty:
            # Exclude rows where partnerCode == 0
            df = df[df['partnerCode'] != 0]

            # Extract specific columns
            df = df[[
                'period',
                'reporterCode',
                'reporterISO',
                'reporterDesc',
                'partnerCode',
                'partnerISO',
                'partnerDesc',
                'cmdCode',
                'cmdDesc',
                'aggrLevel',
                'netWgt',
                'fobvalue'
            ]]
            
            return df
    except Exception as e:
        print(f"Error processing file {key}: {e}")
        return pd.DataFrame()
    finally:
        # Remove the downloaded file
        if os.path.exists(local_file_name):
            os.remove(local_file_name)

# Chunk size (number of files to process at once)
chunk_size = 10

# Process files in chunks
chunk_number = 0
for i in range(0, len(files), chunk_size):
    chunk_files = files[i:i + chunk_size]
    dataframes = []

    for file in chunk_files:
        df = process_file(file)
        if not df.empty:
            dataframes.append(df)

    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)

        # Count unique cmdCode values where aggrLevel == 6 for each importer country
        aggr6_df = combined_df[combined_df['aggrLevel'] == 6]
        unique_cmd_counts = aggr6_df.groupby('partnerCode')['cmdCode'].nunique().reset_index()
        unique_cmd_counts.columns = ['partnerCode', 'uniqueCmdCount']

        # Merge the unique counts back to the combined DataFrame
        combined_df = combined_df.merge(unique_cmd_counts, on='partnerCode', how='left')

        # Keep only rows where aggrLevel == 2
        combined_df = combined_df[combined_df['aggrLevel'] == 2]

        # Save the combined DataFrame to a CSV file
        chunk_csv_path = f'combined_comtrade_data_chunk_{chunk_number}.csv'
        combined_df.to_csv(chunk_csv_path, index=False)
        print(f"Chunk {chunk_number} saved to {chunk_csv_path}")

        # Upload the chunk CSV back to S3
        s3_client.upload_file(chunk_csv_path, bucket_name, f'{folder_name}{chunk_csv_path}')

        # Remove the local chunk CSV file
        os.remove(chunk_csv_path)

        chunk_number += 1

# List of intermediate result files
chunk_files = [file for file in glob.glob("combined_comtrade_data_chunk_*.csv")]

# Combine all chunk files into a single DataFrame
combined_dataframes = []
for chunk_file in chunk_files:
    df = pd.read_csv(chunk_file)
    combined_dataframes.append(df)
    os.remove(chunk_file)  # Remove the local chunk file after reading

if combined_dataframes:
    final_combined_df = pd.concat(combined_dataframes, ignore_index=True)

    # Save the final combined DataFrame to a CSV file
    final_combined_csv_path = 'final_combined_comtrade_data.csv'
    final_combined_df.to_csv(final_combined_csv_path, index=False)

    # Upload the final combined CSV back to S3
    s3_client.upload_file(final_combined_csv_path, bucket_name, f'{folder_name}{final_combined_csv_path}')

    # Remove the local final combined CSV file
    os.remove(final_combined_csv_path)

    print(f"Final combined data saved to {final_combined_csv_path} and uploaded to S3 as {folder_name}{final_combined_csv_path}")
else:
    print("No data to combine.")

###############################################################################################

# import boto3
# import pandas as pd
# import os

# # Initialize the S3 client
# s3_client = boto3.client('s3')

# # Define the S3 bucket and folder
# bucket_name = 'trade-dissertation-data'
# folder_name = 'products/'

# # List all files in the S3 bucket folder
# response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
# files = [item['Key'] for item in response.get('Contents', []) if item['Key'].endswith('.csv')]

# # Initialize an empty list to store dataframes
# dataframes = []

# # Function to read and process a single file
# def process_file(key):
#     try:
#         # Download the file
#         local_file_name = key.split('/')[-1]
#         s3_client.download_file(bucket_name, key, local_file_name)

#         # Read the file into a DataFrame
#         df = pd.read_csv(local_file_name)

#         # Check if the DataFrame contains data
#         if not df.empty:
#             # Exclude rows where partnerCode == 0
#             df = df[df['partnerCode'] != 0]

#             # Extract specific columns
#             df = df[[
#                 'period',
#                 'reporterCode',
#                 'reporterISO',
#                 'reporterDesc',
#                 'partnerCode',
#                 'partnerISO',
#                 'partnerDesc',
#                 'cmdCode',
#                 'cmdDesc',
#                 'aggrLevel',
#                 'netWgt',
#                 'fobvalue'
#             ]]
            
#             # Append the DataFrame to the list
#             dataframes.append(df)
#     except Exception as e:
#         print(f"Error processing file {key}: {e}")
#     finally:
#         # Remove the downloaded file
#         if os.path.exists(local_file_name):
#             os.remove(local_file_name)

# # Process each file
# for file in files:
#     process_file(file)

# # Concatenate all DataFrames
# if dataframes:
#     combined_df = pd.concat(dataframes, ignore_index=True)

#     # Count unique cmdCode values where aggrLevel == 6 for each importer country
#     aggr6_df = combined_df[combined_df['aggrLevel'] == 6]
#     unique_cmd_counts = aggr6_df.groupby('partnerCode')['cmdCode'].nunique().reset_index()
#     unique_cmd_counts.columns = ['partnerCode', 'unique_HS6cmd_count']

#     # Merge the unique counts back to the combined DataFrame
#     combined_df = combined_df.merge(unique_cmd_counts, on='partnerCode', how='left')

#     # Keep only rows where aggrLevel == 2
#     combined_df = combined_df[combined_df['aggrLevel'] == 2]

#     # Save the combined DataFrame to a CSV file
#     combined_csv_path = 'combined_comtrade_data.csv'
#     combined_df.to_csv(combined_csv_path, index=False)

#     # Upload the combined CSV back to S3
#     s3_client.upload_file(combined_csv_path, bucket_name, f'{folder_name}combined_comtrade_data.csv')

#     # Remove the local combined CSV file
#     os.remove(combined_csv_path)

#     print(f"Combined data saved to {combined_csv_path} and uploaded to S3 as {folder_name}combined_comtrade_data.csv")
# else:
#     print("No data to combine.")