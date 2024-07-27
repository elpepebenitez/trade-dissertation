# I have to run gme package with python 3.7; it does not work with python 3.9
# /Users/pepe/.pyenv/versions/3.7.12/bin/python3.7 scripts/ppml.py
import gme as gm
import pandas as pd
import numpy as np
from data_cleaning import check_and_clean_data  # Import the data cleaning function
from significance_stars import add_significance_stars  # Import the significance stars function

# Load data
# file_path = './data/raw_data/cepii/Gravity_csv_V202211/Gravity_V202211.csv'
# file_path = './data/processed_data/Gravity_V202211_sample.csv'
file_path = './data/processed_data/filtered_gravity_data.csv'
data = pd.read_csv(file_path, low_memory=False)

# Required columns
required_columns = ['year', 'iso3_o', 'iso3_d', 'gdp_o', 'gdp_d', 'dist', 'tradeflow_comtrade_o', 'comlang_off', 'contig', 'col_dep_ever', 'pop_o', 'pop_d']

data_sample = check_and_clean_data(data, required_columns)

# Convert categorical variables to strings for fixed effects
data_sample['iso3_o'] = data_sample['iso3_o'].astype(str)
data_sample['iso3_d'] = data_sample['iso3_d'].astype(str)
data_sample['year'] = data_sample['year'].astype(str)

# Create EstimationData object
est_data = gm.EstimationData(data_frame=data_sample,
                             imp_var_name='iso3_d',
                             exp_var_name='iso3_o',
                             trade_var_name='tradeflow_comtrade_o', # COMTRADE trade flows from origin to destination as declared by exporter
                             year_var_name='year')

# print(est_data.info())

# Define the gravity model
model = gm.EstimationModel(
    estimation_data=est_data,
    lhs_var='tradeflow_comtrade_o',  # Dependent variable
    rhs_var=['gdp_o', 'gdp_d', 'dist', 'comlang_off', 'contig', 'col_dep_ever', 'pop_o', 'pop_d'],  # Independent variables
    fixed_effects=[['iso3_d','year'],['iso3_o','year']]  # Fixed effects
)

try:
    estimates = model.estimate()
    results = estimates['all']
    
    # Process and display summary
    summary = results.summary()
    coef_df = summary.tables[1]
    coef_df = pd.read_html(coef_df.as_html(), header=0, index_col=0)[0]
    
    # Add significance stars
    coef_df['Significance'] = add_significance_stars(coef_df['P>|z|'])
    coef_df['coef'] = coef_df.apply(lambda x: f"{x['coef']}{x['Significance']}", axis=1)
    
    # Display the main coefficients without fixed effects
    print(coef_df.loc[['gdp_o', 'gdp_d', 'dist', 'comlang_off', 'contig', 'col_dep_ever', 'pop_o', 'pop_d']])
    
    # Optionally save the full summary to a file or separate variable
    # full_summary = coef_df.to_string()
    # print(full_summary)
    
    # Print diagnostics
    print(model.ppml_diagnostics)
except Exception as e:
    print(f"An error occurred: {e}")