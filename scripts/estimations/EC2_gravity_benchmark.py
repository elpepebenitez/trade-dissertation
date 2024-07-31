# Requirements:
# PPML estimator
# International and intra-trade data for dependent trade variable
# Export data as reported by destination country
# exporter-year, importer-year and country-pair fixed effects
# Calculate x-year intervals
# Filtered data for only 1995-2015 and S countries with at least one NS and one SS

# Saving aggregated results in CSV. Removing post processing: significance and latex table
import gme as gm
import pandas as pd
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
        rhs_var=['fta_wto'],   # Independent variable (RTA variable)
        fixed_effects=[['iso3num_d', 'year'], ['iso3num_o', 'year'], ['iso3num_o', 'iso3num_d']]  # Fixed effects
    )

    # Estimate the model and process results
    try:
        estimates = model.estimate()
        results = estimates['all']
        
        # Process and display summary
        summary = results.summary()
        coef_df = summary.tables[1]
        coef_df = pd.read_html(coef_df.as_html(), header=0, index_col=0)[0]
        
        # Extract only the RTA coefficient
        coef = coef_df.loc['fta_wto', 'coef']
        se = coef_df.loc['fta_wto', 'std err']
        nobs = results.nobs
        
        # Append to lists
        coef_list.append(coef)
        se_list.append(se)
        nobs_list.append(nobs)
        
        # Print diagnostics
        print(model.ppml_diagnostics)
    except Exception as e:
        print(f"An error occurred: {e}")

# Compute weighted averages for coefficients and standard errors
if coef_list:
    total_nobs = sum(nobs_list)
    weighted_avg_coef = sum(c * n for c, n in zip(coef_list, nobs_list)) / total_nobs
    weighted_avg_se = sum(se * n for se, n in zip(se_list, nobs_list)) / total_nobs
    
    # Create final results DataFrame
    final_results = pd.DataFrame({
        'Coefficient': [weighted_avg_coef],
        'Standard Error': [weighted_avg_se],
        'Observations': [total_nobs]
    })
    
    # Save results to CSV
    results_file_path = './data/estimations_results/EC2_gravity_benchmark_results.csv'
    final_results.to_csv(results_file_path, index=False)
    print(f"Estimation completed and results saved to {results_file_path}.")
else:
    print("No results to combine.")

###############################################################################
# Chunks with coefficient aggregations

# import gme as gm
# import pandas as pd
# import numpy as np
# import boto3
# from pathlib import Path
# from significance_stars import add_significance_stars

# # Initialize boto3 S3 client
# s3 = boto3.client('s3')

# # S3 bucket and file paths
# bucket_name = 'trade-dissertation-data'
# merged_data_file_key = 'merged_trade_gravity_NS_SS.csv'

# # Local path to save the downloaded file
# local_merged_data_file_path = '/tmp/merged_trade_gravity_NS_SS.csv'

# # Download file from S3
# s3.download_file(bucket_name, merged_data_file_key, local_merged_data_file_path)

# # Define chunk size
# chunk_size = 100000  # Adjust this value based on your memory capacity

# # Filter years
# interval_years = [1990, 1995, 2000, 2005, 2010, 2015]

# # Initialize lists to store coefficients, variances, and number of observations
# coefficients = []
# variances = []
# total_observations = 0

# # Process the data in chunks
# for chunk in pd.read_csv(local_merged_data_file_path, low_memory=False, chunksize=chunk_size):
#     # Convert relevant columns to string type for merging
#     chunk['iso3num_o'] = chunk['iso3num_o'].astype(str)
#     chunk['iso3num_d'] = chunk['iso3num_d'].astype(str)

#     # Filter data for 5-year intervals
#     chunk = chunk[chunk['year'].isin(interval_years)]

#     # Create fixed effects
#     chunk['exporter_time'] = chunk['iso3num_o'] + '_' + chunk['year'].astype(str)
#     chunk['importer_time'] = chunk['iso3num_d'] + '_' + chunk['year'].astype(str)
#     chunk['pair'] = chunk['iso3num_o'] + '_' + chunk['iso3num_d']

#     # Convert fixed effects to categorical
#     chunk['exporter_time'] = chunk['exporter_time'].astype('category')
#     chunk['importer_time'] = chunk['importer_time'].astype('category')
#     chunk['pair'] = chunk['pair'].astype('category')

#     # Handle NaN values in the merged data
#     chunk = chunk.dropna(subset=['trade_comb', 'fta_wto'])

#     # Create EstimationData object
#     est_data = gm.EstimationData(data_frame=chunk,
#                                  imp_var_name='iso3num_d',
#                                  exp_var_name='iso3num_o',
#                                  trade_var_name='trade_comb',
#                                  year_var_name='year')

#     # Define the gravity model
#     model = gm.EstimationModel(
#         estimation_data=est_data,
#         lhs_var='trade_comb',  # Dependent variable
#         rhs_var=['fta_wto'],   # Independent variable (RTA variable)
#         fixed_effects=[['iso3num_d', 'year'], ['iso3num_o', 'year'], ['iso3num_o', 'iso3num_d']]  # Fixed effects
#     )

#     # Estimate the model and process results
#     try:
#         estimates = model.estimate()
#         results = estimates['all']
        
#         # Process and display summary
#         summary = results.summary()
#         coef_df = summary.tables[1]
#         coef_df = pd.read_html(coef_df.as_html(), header=0, index_col=0)[0]
        
#         fta_wto_coef = coef_df.loc['fta_wto', 'coef']
#         fta_wto_se = coef_df.loc['fta_wto', 'std err']

#         coefficients.append(fta_wto_coef)
#         variances.append(fta_wto_se ** 2)
#         total_observations += results.nobs

#         # Print diagnostics
#         print(model.ppml_diagnostics)
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Aggregate coefficients and variances
# coefficients = np.array(coefficients)
# variances = np.array(variances)

# weights = 1 / variances
# aggregated_coef = np.sum(weights * coefficients) / np.sum(weights)
# aggregated_se = np.sqrt(1 / np.sum(weights))

# # Create final results DataFrame
# final_results = pd.DataFrame({
#     'coef': [aggregated_coef],
#     'std err': [aggregated_se],
#     'Significance': add_significance_stars([aggregated_coef / aggregated_se])
# })

# # Add the total number of observations
# observations_row = pd.DataFrame([['', '', '', total_observations, '', '', '']], columns=final_results.columns, index=['Observations'])
# final_results = pd.concat([final_results, observations_row])

# # Generate LaTeX table string
# latex_table = final_results.to_latex()

# # Save LaTeX table to a file in the ./tex folder
# tex_file_path = Path('./tex/tables/benchmark_results_table.tex')
# tex_file_path.write_text(latex_table)

# print("Estimation completed and results saved.")

##############################################################
# With Chunks

# import gme as gm
# import pandas as pd
# import numpy as np
# import boto3
# from pathlib import Path
# from significance_stars import add_significance_stars

# # Initialize boto3 S3 client
# s3 = boto3.client('s3')

# # S3 bucket and file paths
# bucket_name = 'trade-dissertation-data'
# merged_data_file_key = 'merged_trade_gravity_NS_SS.csv'

# # Local path to save the downloaded file
# local_merged_data_file_path = '/tmp/merged_trade_gravity_NS_SS.csv'

# # Download file from S3
# s3.download_file(bucket_name, merged_data_file_key, local_merged_data_file_path)

# # Define chunk size
# chunk_size = 100000  # Adjust this value based on your memory capacity

# # Filter years
# interval_years = [1990, 1995, 2000, 2005, 2010, 2015]

# # Initialize an empty DataFrame for combined results
# combined_results = []

# # Process the data in chunks
# for chunk in pd.read_csv(local_merged_data_file_path, low_memory=False, chunksize=chunk_size):
#     # Convert relevant columns to string type for merging
#     chunk['iso3num_o'] = chunk['iso3num_o'].astype(str)
#     chunk['iso3num_d'] = chunk['iso3num_d'].astype(str)

#     # Filter data for 5-year intervals
#     chunk = chunk[chunk['year'].isin(interval_years)]

#     # Create fixed effects
#     chunk['exporter_time'] = chunk['iso3num_o'] + '_' + chunk['year'].astype(str)
#     chunk['importer_time'] = chunk['iso3num_d'] + '_' + chunk['year'].astype(str)
#     chunk['pair'] = chunk['iso3num_o'] + '_' + chunk['iso3num_d']

#     # Convert fixed effects to categorical
#     chunk['exporter_time'] = chunk['exporter_time'].astype('category')
#     chunk['importer_time'] = chunk['importer_time'].astype('category')
#     chunk['pair'] = chunk['pair'].astype('category')

#     # Handle NaN values in the merged data
#     chunk = chunk.dropna(subset=['trade_comb', 'fta_wto'])

#     # Create EstimationData object
#     est_data = gm.EstimationData(data_frame=chunk,
#                                  imp_var_name='iso3num_d',
#                                  exp_var_name='iso3num_o',
#                                  trade_var_name='trade_comb',
#                                  year_var_name='year')

#     # Define the gravity model
#     model = gm.EstimationModel(
#         estimation_data=est_data,
#         lhs_var='trade_comb',  # Dependent variable
#         rhs_var=['fta_wto'],   # Independent variable (RTA variable)
#         fixed_effects=[['iso3num_d', 'year'], ['iso3num_o', 'year'], ['iso3num_o', 'iso3num_d']]  # Fixed effects
#     )

#     # Estimate the model and process results
#     try:
#         estimates = model.estimate()
#         results = estimates['all']
        
#         # Process and display summary
#         summary = results.summary()
#         coef_df = summary.tables[1]
#         coef_df = pd.read_html(coef_df.as_html(), header=0, index_col=0)[0]
        
#         # Add significance stars
#         coef_df['Significance'] = add_significance_stars(coef_df['P>|z|'])
#         coef_df['coef'] = coef_df.apply(lambda x: f"{x['coef']}{x['Significance']}", axis=1)
        
#         # Extract only the RTA coefficient
#         rta_df = coef_df.loc[['fta_wto']]
        
#         # Add the total number of observations
#         observations_row = pd.DataFrame([['', '', '', results.nobs, '', '', '']], columns=rta_df.columns, index=['Observations'])
#         rta_df = pd.concat([rta_df, observations_row])
        
#         # Append the results to the combined results list
#         combined_results.append(rta_df)
        
#         # Print diagnostics
#         print(model.ppml_diagnostics)
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Combine all chunk results into a single DataFrame
# combined_df = pd.concat(combined_results)

# # Generate LaTeX table string
# latex_table = combined_df.to_latex()

# # Save LaTeX table to a file in the ./tex folder
# tex_file_path = Path('./tex/tables/benchmark_results_table.tex')
# tex_file_path.write_text(latex_table)

# print("Estimation completed and results saved.")

########################################
# Without Chunks 

# import gme as gm
# import pandas as pd
# import numpy as np
# import boto3
# from pathlib import Path
# from significance_stars import add_significance_stars

# # Initialize boto3 S3 client
# s3 = boto3.client('s3')

# # S3 bucket and file paths
# bucket_name = 'trade-dissertation-data'
# merged_data_file_key = 'merged_trade_gravity_NS_SS.csv'

# # Local path to save the downloaded file
# local_merged_data_file_path = '/tmp/merged_trade_gravity_NS_SS.csv'

# # Download file from S3
# s3.download_file(bucket_name, merged_data_file_key, local_merged_data_file_path)

# # Read the data into pandas DataFrame
# merged_data = pd.read_csv(local_merged_data_file_path, low_memory=False)

# # Convert relevant columns to string type for merging
# merged_data['iso3num_o'] = merged_data['iso3num_o'].astype(str)
# merged_data['iso3num_d'] = merged_data['iso3num_d'].astype(str)

# # Filter data for 5-year intervals
# interval_years = [1990, 1995, 2000, 2005, 2010, 2015]
# merged_data = merged_data[merged_data['year'].isin(interval_years)]

# # Create fixed effects
# merged_data['exporter_time'] = merged_data['iso3num_o'] + '_' + merged_data['year'].astype(str)
# merged_data['importer_time'] = merged_data['iso3num_d'] + '_' + merged_data['year'].astype(str)
# merged_data['pair'] = merged_data['iso3num_o'] + '_' + merged_data['iso3num_d']

# # Convert fixed effects to categorical
# merged_data['exporter_time'] = merged_data['exporter_time'].astype('category')
# merged_data['importer_time'] = merged_data['importer_time'].astype('category')
# merged_data['pair'] = merged_data['pair'].astype('category')

# # Handle NaN values in the merged data
# merged_data = merged_data.dropna(subset=['trade_comb', 'fta_wto'])

# # Create EstimationData object
# est_data = gm.EstimationData(data_frame=merged_data,
#                              imp_var_name='iso3num_d',
#                              exp_var_name='iso3num_o',
#                              trade_var_name='trade_comb',
#                              year_var_name='year')

# # Define the gravity model
# model = gm.EstimationModel(
#     estimation_data=est_data,
#     lhs_var='trade_comb',  # Dependent variable
#     rhs_var=['fta_wto'],   # Independent variable (RTA variable)
#     fixed_effects=[['iso3num_d', 'year'], ['iso3num_o', 'year'], ['iso3num_o', 'iso3num_d']]  # Fixed effects
# )

# # Estimate the model and process results
# try:
#     estimates = model.estimate()
#     results = estimates['all']
    
#     # Process and display summary
#     summary = results.summary()
#     # print(summary)
#     coef_df = summary.tables[1]
#     coef_df = pd.read_html(coef_df.as_html(), header=0, index_col=0)[0]
    
#     # Debug print: Check the structure of coef_df
#     print("Coefficient DataFrame before adding significance:")
#     print(coef_df)
    
#     # Add significance stars
#     coef_df['Significance'] = add_significance_stars(coef_df['P>|z|'])
#     coef_df['coef'] = coef_df.apply(lambda x: f"{x['coef']}{x['Significance']}", axis=1)
    
#     # Debug print: Check the structure after adding significance
#     print("Coefficient DataFrame after adding significance:")
#     print(coef_df)
    
#     # Extract only the RTA coefficient
#     rta_df = coef_df.loc[['fta_wto']]
    
#     # Debug print: Check the structure of rta_df
#     print("RTA DataFrame before adding observations:")
#     print(rta_df)
    
#     # Add the total number of observations
#     observations_row = pd.DataFrame([['', '', '', results.nobs, '', '', '']], columns=rta_df.columns, index=['Observations'])
#     rta_df = pd.concat([rta_df, observations_row])
    
#     # Debug print: Check the structure after adding observations
#     print("RTA DataFrame after adding observations:")
#     print(rta_df)
    
#     # Generate LaTeX table string
#     latex_table = rta_df.to_latex()
    
#     # Save LaTeX table to a file in the ./tex folder
#     tex_file_path = Path('./tex/tables/benchmark_results_table.tex')
#     tex_file_path.write_text(latex_table)
    
#     # Print diagnostics
#     print(model.ppml_diagnostics)
# except Exception as e:
#     print(f"An error occurred: {e}")

###############################################################
# Without Merge

# import gme as gm
# import pandas as pd
# import numpy as np
# import boto3
# from pathlib import Path
# from significance_stars import add_significance_stars

# # Initialize boto3 S3 client
# s3 = boto3.client('s3')

# # S3 bucket and file paths
# bucket_name = 'trade-dissertation-data'
# trade_data_file_key = 'filtered_TPe_V202401.csv'
# gravity_data_file_key = 'filtered_Gravity_V202211.csv'
# country_key_file_key = 'TradeProd_Gravity_country_key.csv'

# # Local paths to save the downloaded files
# local_trade_data_file_path = '/tmp/filtered_TPe_V202401.csv'
# local_gravity_data_file_path = '/tmp/filtered_Gravity_V202211.csv'
# local_country_key_file_path = '/tmp/TradeProd_Gravity_country_key.csv'

# # Download files from S3
# s3.download_file(bucket_name, trade_data_file_key, local_trade_data_file_path)
# s3.download_file(bucket_name, gravity_data_file_key, local_gravity_data_file_path)
# s3.download_file(bucket_name, country_key_file_key, local_country_key_file_path)

# # Read the data into pandas DataFrames
# trade_data = pd.read_csv(local_trade_data_file_path, low_memory=False)
# gravity_data = pd.read_csv(local_gravity_data_file_path, low_memory=False)
# country_key = pd.read_csv(local_country_key_file_path, low_memory=False)

# # Convert relevant columns to string type for merging
# trade_data['iso3_tp_o'] = trade_data['iso3_tp_o'].astype(str)
# trade_data['iso3_tp_d'] = trade_data['iso3_tp_d'].astype(str)
# country_key['iso3_tp'] = country_key['iso3_tp'].astype(str)
# country_key['cnum'] = country_key['cnum'].astype(str)

# # Merge trade_data with country_key to get the numeric codes for origin
# trade_data = pd.merge(trade_data, country_key[['iso3_tp', 'cnum']], left_on='iso3_tp_o', right_on='iso3_tp', how='left')
# trade_data.rename(columns={'cnum': 'cnum_o'}, inplace=True)
# trade_data.drop(columns=['iso3_tp'], inplace=True)

# # Merge trade_data with country_key to get the numeric codes for destination
# trade_data = pd.merge(trade_data, country_key[['iso3_tp', 'cnum']], left_on='iso3_tp_d', right_on='iso3_tp', how='left')
# trade_data.rename(columns={'cnum': 'cnum_d'}, inplace=True)
# trade_data.drop(columns=['iso3_tp'], inplace=True)

# # Remove duplicate rows if any
# trade_data = trade_data.drop_duplicates()

# # Ensure the relevant columns are of type string for merging
# trade_data['cnum_o'] = trade_data['cnum_o'].astype(str)
# trade_data['cnum_d'] = trade_data['cnum_d'].astype(str)

# # Handle non-finite values in gravity_data
# gravity_data = gravity_data.dropna(subset=['iso3num_o', 'iso3num_d'])

# # Convert iso3num columns to strings without decimal points
# gravity_data['iso3num_o'] = gravity_data['iso3num_o'].astype(float).astype(int).astype(str)
# gravity_data['iso3num_d'] = gravity_data['iso3num_d'].astype(float).astype(int).astype(str)

# # Filter data for 5-year intervals
# interval_years = [1990, 1995, 2000, 2005, 2010, 2015]
# trade_data = trade_data[trade_data['year'].isin(interval_years)]
# gravity_data = gravity_data[gravity_data['year'].isin(interval_years)]

# # Merge trade_data with gravity_data using the numeric codes and year
# merged_data = pd.merge(trade_data, gravity_data, left_on=['cnum_o', 'cnum_d', 'year'], right_on=['iso3num_o', 'iso3num_d', 'year'])

# # Create fixed effects
# merged_data['exporter_time'] = merged_data['cnum_o'] + '_' + merged_data['year'].astype(str)
# merged_data['importer_time'] = merged_data['cnum_d'] + '_' + merged_data['year'].astype(str)
# merged_data['pair'] = merged_data['cnum_o'] + '_' + merged_data['cnum_d']

# # Convert fixed effects to categorical
# merged_data['exporter_time'] = merged_data['exporter_time'].astype('category')
# merged_data['importer_time'] = merged_data['importer_time'].astype('category')
# merged_data['pair'] = merged_data['pair'].astype('category')

# # Handle NaN values in the merged data
# merged_data = merged_data.dropna(subset=['trade_comb', 'fta_wto'])

# # Create EstimationData object
# est_data = gm.EstimationData(data_frame=merged_data,
#                              imp_var_name='cnum_d',
#                              exp_var_name='cnum_o',
#                              trade_var_name='trade_comb',
#                              year_var_name='year')

# # Define the gravity model
# model = gm.EstimationModel(
#     estimation_data=est_data,
#     lhs_var='trade_comb',  # Dependent variable
#     rhs_var=['fta_wto'],   # Independent variable (RTA variable)
#     fixed_effects=[['cnum_d', 'year'], ['cnum_o', 'year'], ['cnum_o', 'cnum_d']]  # Fixed effects
# )

# # Estimate the model and process results
# try:
#     estimates = model.estimate()
#     results = estimates['all']
    
#     # Process and display summary
#     summary = results.summary()
#     # print(summary)
#     coef_df = summary.tables[1]
#     coef_df = pd.read_html(coef_df.as_html(), header=0, index_col=0)[0]
    
#     # Debug print: Check the structure of coef_df
#     print("Coefficient DataFrame before adding significance:")
#     print(coef_df)
    
#     # Add significance stars
#     coef_df['Significance'] = add_significance_stars(coef_df['P>|z|'])
#     coef_df['coef'] = coef_df.apply(lambda x: f"{x['coef']}{x['Significance']}", axis=1)
    
#     # Debug print: Check the structure after adding significance
#     print("Coefficient DataFrame after adding significance:")
#     print(coef_df)
    
#     # Extract only the RTA coefficient
#     rta_df = coef_df.loc[['fta_wto']]
    
#     # Debug print: Check the structure of rta_df
#     print("RTA DataFrame before adding observations:")
#     print(rta_df)
    
#     # Add the total number of observations
#     observations_row = pd.DataFrame([['', '', '', results.nobs, '', '', '']], columns=rta_df.columns, index=['Observations'])
#     rta_df = pd.concat([rta_df, observations_row])
    
#     # Debug print: Check the structure after adding observations
#     print("RTA DataFrame after adding observations:")
#     print(rta_df)
    
#     # Generate LaTeX table string
#     latex_table = rta_df.to_latex()
    
#     # Save LaTeX table to a file in the ./tex folder
#     tex_file_path = Path('./tex/tables/benchmark_results_table.tex')
#     tex_file_path.write_text(latex_table)
    
#     # Print diagnostics
#     print(model.ppml_diagnostics)
# except Exception as e:
#     print(f"An error occurred: {e}")
