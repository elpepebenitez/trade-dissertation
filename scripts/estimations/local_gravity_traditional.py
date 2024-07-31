# Requirements:
# PPML estimator
# International and intra-trade data for dependent trade variable
# Export data as reported by destination country
# exporter-year, importer-year fixed effects
# Calculate x-year intervals
# Filtered data for only 1995-2015 and S countries with at least one NS and one SS

# Saving aggregated results in CSV. Removing post processing: significance and latex table
import gme as gm
import pandas as pd
import numpy as np
from pathlib import Path

# Define file paths
local_merged_data_file_path = './data/processed_data/sample_merged_trade_gravity_NS_SS.csv'
results_file_path = './data/estimations_results/local_gravity_traditional_results.csv'

# Define chunk size
chunk_size = 100000  # Adjust this value based on your memory capacity

# Filter years
interval_years = [1995, 2000, 2005, 2010, 2015]

# Initialize lists to store coefficients and standard errors
coef_list = []
se_list = []
nobs_list = []

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
    chunk = chunk.dropna(subset=['trade_comb', 'fta_wto'])

    # Set distance values of zero to a very small positive number (e.g., 1e-10) before log transformation
    chunk['dist'] = chunk['dist'].replace(0, 1e-10)
    chunk['log_dist'] = np.log(chunk['dist'])

    # Create EstimationData object
    est_data = gm.EstimationData(data_frame=chunk,
                                 imp_var_name='iso3num_d',
                                 exp_var_name='iso3num_o',
                                 trade_var_name='trade_comb',
                                 year_var_name='year')

    # Define the gravity model
    model = gm.EstimationModel(
        estimation_data=est_data,
        lhs_var='trade_comb',  # Dependent variable
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
        
        # Extract the coefficients and standard errors for all variables
        for var in ['log_dist', 'contig', 'comlang_off', 'col_dep_ever', 'fta_wto']:
            coef = coef_df.loc[var, 'coef']
            se = coef_df.loc[var, 'std err']
            nobs = results.nobs
            
            # Append to lists
            coef_list.append((var, coef))
            se_list.append((var, se))
            nobs_list.append(nobs)
        
        # Print diagnostics
        print(model.ppml_diagnostics)
    except Exception as e:
        print(f"An error occurred: {e}")

# Compute weighted averages for coefficients and standard errors
if coef_list:
    total_nobs = sum(nobs_list)
    final_results = []

    variable_names = ['log_dist', 'contig', 'comlang_off', 'col_dep_ever', 'fta_wto']
    for var in variable_names:
        var_coefs = [coef for name, coef in coef_list if name == var]
        var_ses = [se for name, se in se_list if name == var]
        weighted_avg_coef = sum(c * n for c, n in zip(var_coefs, nobs_list)) / total_nobs
        
        # Calculate the variance for each chunk
        var_list = [se ** 2 for se in var_ses]
        
        # Calculate the weighted average variance
        weighted_avg_var = sum(var * n for var, n in zip(var_list, nobs_list)) / total_nobs
        
        # Calculate the combined standard error from the weighted average variance
        weighted_avg_se = np.sqrt(weighted_avg_var)
        
        final_results.append([var, weighted_avg_coef, weighted_avg_se, total_nobs])

    # Create final results DataFrame
    final_results_df = pd.DataFrame(final_results, columns=['Variable', 'Coefficient', 'Standard Error', 'Observations'])
    
    # Save results to CSV
    results_file_path = './data/estimations_results/EC2_gravity_traditional_results.csv'
    final_results_df.to_csv(results_file_path, index=False)
    print(f"Estimation completed and results saved to {results_file_path}.")
else:
    print("No results to combine.")