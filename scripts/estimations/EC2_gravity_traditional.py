import gme as gm
import pandas as pd
import numpy as np
import boto3
from pathlib import Path

# Initialize boto3 S3 client
s3 = boto3.client('s3')

# S3 bucket and file paths
bucket_name = 'trade-dissertation-data'
merged_data_file_key = 'merged_trade_gravity_NS_SS.csv'

# Local path to save the downloaded file
local_merged_data_file_path = '/tmp/merged_trade_gravity_NS_SS.csv'

# Download file from S3
s3.download_file(bucket_name, merged_data_file_key, local_merged_data_file_path)

# Define chunk size
chunk_size = 100000  # Adjust this value based on your memory capacity

# Filter years
interval_years = [1995, 2000, 2005, 2010, 2015]

# Initialize lists to store aggregated results
aggregated_coefs = []
aggregated_ses = []
total_obs = 0

# Process the data in chunks
for chunk in pd.read_csv(local_merged_data_file_path, low_memory=False, chunksize=chunk_size):
    # Convert relevant columns to string type for merging
    chunk['iso3num_o'] = chunk['iso3num_o'].astype(str)
    chunk['iso3num_d'] = chunk['iso3num_d'].astype(str)

    # Filter data for 5-year intervals
    chunk = chunk[chunk['year'].isin(interval_years)]

    # Create fixed effects
    chunk['exporter_time'] = chunk['iso3num_o'] + '_' + chunk['year'].astype(str)
    chunk['importer_time'] = chunk['iso3num_d'] + '_' + chunk['year'].astype(str)
    chunk['pair'] = chunk['iso3num_o'] + '_' + chunk['iso3num_d']

    # Convert fixed effects to categorical
    chunk['exporter_time'] = chunk['exporter_time'].astype('category')
    chunk['importer_time'] = chunk['importer_time'].astype('category')
    chunk['pair'] = chunk['pair'].astype('category')

    # Handle NaN values in the merged data
    chunk = chunk.dropna(subset=['trade_comb', 'fta_wto', 'dist', 'contig', 'comlang_off', 'col_dep_ever'])

    # Create logarithmic columns
    chunk['log_trade_comb'] = np.log(chunk['trade_comb'] + 1)  # Adding 1 to avoid log(0)
    chunk['log_dist'] = np.log(chunk['dist'])

    # Create EstimationData object
    est_data = gm.EstimationData(data_frame=chunk,
                                 imp_var_name='iso3num_d',
                                 exp_var_name='iso3num_o',
                                 trade_var_name='log_trade_comb',
                                 year_var_name='year')

    # Define the gravity model
    model = gm.EstimationModel(
        estimation_data=est_data,
        lhs_var='log_trade_comb',  # Dependent variable
        rhs_var=['log_dist', 'contig', 'comlang_off', 'col_dep_ever', 'fta_wto'],  # Independent variables
        fixed_effects=[['iso3num_d', 'year'], ['iso3num_o', 'year']]  # Fixed effects
    )

    # Estimate the model and process results
    try:
        estimates = model.estimate()
        results = estimates['all']
        
        # Process and display summary
        summary = results.summary()
        coef_df = summary.tables[1]
        coef_df = pd.read_html(coef_df.as_html(), header=0, index_col=0)[0]
        
        # Extract coefficients and standard errors
        coefs = coef_df['coef'].astype(float)
        ses = coef_df['std err'].astype(float)
        
        # Append to aggregated lists
        aggregated_coefs.append(coefs)
        aggregated_ses.append(ses * ses * results.nobs)  # Variance multiplied by nobs
        
        # Add to total observations
        total_obs += results.nobs
        
        # Print diagnostics
        print(model.ppml_diagnostics)
    except Exception as e:
        print(f"An error occurred: {e}")

# Aggregate results
if aggregated_coefs:
    aggregated_coefs = pd.concat(aggregated_coefs, axis=1).mean(axis=1)
    aggregated_ses = pd.concat(aggregated_ses, axis=1).sum(axis=1) / total_obs
    aggregated_ses = np.sqrt(aggregated_ses)
    
    final_results = pd.DataFrame({
        'Coefficient': aggregated_coefs,
        'Standard Error': aggregated_ses,
    })

    final_results['Observations'] = total_obs  # Add observations column

    # Save results to CSV
    results_csv_path = Path('./data/estimations_results/EC2_gravity_traditional_results.csv')
    final_results.to_csv(results_csv_path)

    print("Estimation completed and results saved.")
else:
    print("No results to combine.")
