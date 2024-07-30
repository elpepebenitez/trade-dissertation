# Requirements:
# PPML estimator
# International and intra-trade data for dependent trade variable
# Export data as reported by destination country
# exporter-year, importer-year and country-pair fixed effects

import gme as gm
import pandas as pd
import numpy as np
from pathlib import Path
from significance_stars import add_significance_stars

trade_data_file_path = "./data/raw_data/cepii/TPe_V202401.csv"
gravity_data_file_path = "./data/raw_data/cepii/Gravity_csv_V202211/Gravity_V202211.csv"
# trade_data_file_path = "./data/processed_data/TPe_V202401_sample.csv"
# gravity_data_file_path = "./data/processed_data/Gravity_V202211_sample.csv"
country_key_file_path = "data/raw_data/cepii/TradeProd_Gravity_country_key.csv"

trade_data = pd.read_csv(trade_data_file_path, low_memory=False)
gravity_data = pd.read_csv(gravity_data_file_path, low_memory=False)
country_key = pd.read_csv(country_key_file_path, low_memory=False)

# Convert relevant columns to string type for merging
trade_data['iso3_tp_o'] = trade_data['iso3_tp_o'].astype(str)
trade_data['iso3_tp_d'] = trade_data['iso3_tp_d'].astype(str)
country_key['iso3_tp'] = country_key['iso3_tp'].astype(str)
country_key['cnum'] = country_key['cnum'].astype(str)

# Merge trade_data with country_key to get the numeric codes for origin
trade_data = pd.merge(trade_data, country_key[['iso3_tp', 'cnum']], left_on='iso3_tp_o', right_on='iso3_tp', how='left')
trade_data.rename(columns={'cnum': 'cnum_o'}, inplace=True)
trade_data.drop(columns=['iso3_tp'], inplace=True)

# Merge trade_data with country_key to get the numeric codes for destination
trade_data = pd.merge(trade_data, country_key[['iso3_tp', 'cnum']], left_on='iso3_tp_d', right_on='iso3_tp', how='left')
trade_data.rename(columns={'cnum': 'cnum_d'}, inplace=True)
trade_data.drop(columns=['iso3_tp'], inplace=True)

# Remove duplicate rows if any
trade_data = trade_data.drop_duplicates()

# Ensure the relevant columns are of type string for merging
trade_data['cnum_o'] = trade_data['cnum_o'].astype(str)
trade_data['cnum_d'] = trade_data['cnum_d'].astype(str)

# Handle non-finite values in gravity_data
gravity_data = gravity_data.dropna(subset=['iso3num_o', 'iso3num_d'])

# Convert iso3num columns to strings without decimal points
gravity_data['iso3num_o'] = gravity_data['iso3num_o'].astype(float).astype(int).astype(str)
gravity_data['iso3num_d'] = gravity_data['iso3num_d'].astype(float).astype(int).astype(str)

# Merge trade_data with gravity_data using the numeric codes and year
merged_data = pd.merge(trade_data, gravity_data, left_on=['cnum_o', 'cnum_d', 'year'], right_on=['iso3num_o', 'iso3num_d', 'year'])

# Create fixed effects
merged_data['exporter_time'] = merged_data['cnum_o'] + '_' + merged_data['year'].astype(str)
merged_data['importer_time'] = merged_data['cnum_d'] + '_' + merged_data['year'].astype(str)
merged_data['pair'] = merged_data['cnum_o'] + '_' + merged_data['cnum_d']

# Convert fixed effects to categorical
merged_data['exporter_time'] = merged_data['exporter_time'].astype('category')
merged_data['importer_time'] = merged_data['importer_time'].astype('category')
merged_data['pair'] = merged_data['pair'].astype('category')

# Handle NaN values in the merged data
merged_data = merged_data.dropna(subset=['trade_comb', 'fta_wto'])

# Create EstimationData object
est_data = gm.EstimationData(data_frame=merged_data,
                             imp_var_name='cnum_d',
                             exp_var_name='cnum_o',
                             trade_var_name='trade_comb',
                             year_var_name='year')

# Define the gravity model
model = gm.EstimationModel(
    estimation_data=est_data,
    lhs_var='trade_comb',  # Dependent variable
    rhs_var=['fta_wto'],   # Independent variable (RTA variable)
    fixed_effects=[['cnum_d', 'year'], ['cnum_o', 'year'], ['cnum_o', 'cnum_d']]  # Fixed effects
)

# Estimate the model and process results
try:
    estimates = model.estimate()
    results = estimates['all']
    
    # Process and display summary
    summary = results.summary()
    # print(summary)
    coef_df = summary.tables[1]
    coef_df = pd.read_html(coef_df.as_html(), header=0, index_col=0)[0]
    
    # Debug print: Check the structure of coef_df
    print("Coefficient DataFrame before adding significance:")
    print(coef_df)
    
    # Add significance stars
    coef_df['Significance'] = add_significance_stars(coef_df['P>|z|'])
    coef_df['coef'] = coef_df.apply(lambda x: f"{x['coef']}{x['Significance']}", axis=1)
    
    # Debug print: Check the structure after adding significance
    print("Coefficient DataFrame after adding significance:")
    print(coef_df)
    
    # Extract only the RTA coefficient
    rta_df = coef_df.loc[['fta_wto']]
    
    # Debug print: Check the structure of rta_df
    print("RTA DataFrame before adding observations:")
    print(rta_df)
    
    # Add the total number of observations
    observations_row = pd.DataFrame([['', '', '', results.nobs, '', '', '']], columns=rta_df.columns, index=['Observations'])
    rta_df = pd.concat([rta_df, observations_row])
    
    # Debug print: Check the structure after adding observations
    print("RTA DataFrame after adding observations:")
    print(rta_df)
    
    # Generate LaTeX table string
    latex_table = rta_df.to_latex()
    
    # Save LaTeX table to a file in the ./tex folder
    tex_file_path = Path('./tex/tables/benchmark_results_table.tex')
    tex_file_path.write_text(latex_table)
    
    # Print diagnostics
    print(model.ppml_diagnostics)
except Exception as e:
    print(f"An error occurred: {e}")