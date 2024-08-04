import boto3
import pandas as pd
import os

# Initialize the S3 client
s3_client = boto3.client('s3')

# Define the S3 bucket and folder
bucket_name = 'trade-dissertation-data'
folder_name = 'products/'

# List all files in the S3 bucket folder
response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
files = [item['Key'] for item in response.get('Contents', []) if item['Key'].endswith('.csv')]

# Initialize an empty list to store dataframes
dataframes = []

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
            
            # Append the DataFrame to the list
            dataframes.append(df)
    except Exception as e:
        print(f"Error processing file {key}: {e}")
    finally:
        # Remove the downloaded file
        if os.path.exists(local_file_name):
            os.remove(local_file_name)

# Process each file
for file in files:
    process_file(file)

# Concatenate all DataFrames
if dataframes:
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Count unique cmdCode values where aggrLevel == 6 for each importer country
    aggr6_df = combined_df[combined_df['aggrLevel'] == 6]
    unique_cmd_counts = aggr6_df.groupby('partnerCode')['cmdCode'].nunique().reset_index()
    unique_cmd_counts.columns = ['partnerCode', 'unique_HS6cmd_count']

    # Merge the unique counts back to the combined DataFrame
    combined_df = combined_df.merge(unique_cmd_counts, on='partnerCode', how='left')

    # Keep only rows where aggrLevel == 2
    combined_df = combined_df[combined_df['aggrLevel'] == 2]

    # Save the combined DataFrame to a CSV file
    combined_csv_path = 'combined_comtrade_data.csv'
    combined_df.to_csv(combined_csv_path, index=False)

    # Upload the combined CSV back to S3
    s3_client.upload_file(combined_csv_path, bucket_name, f'{folder_name}combined_comtrade_data.csv')

    # Remove the local combined CSV file
    os.remove(combined_csv_path)

    print(f"Combined data saved to {combined_csv_path} and uploaded to S3 as {folder_name}combined_comtrade_data.csv")
else:
    print("No data to combine.")