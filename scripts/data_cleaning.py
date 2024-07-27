# data_cleaning.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def check_and_clean_data(data, required_columns):
    """
    Check and clean the data.

    Parameters:
    data (pd.DataFrame): The raw data
    required_columns (list): List of required columns

    Returns:
    pd.DataFrame: The cleaned and scaled data
    """
    # Ensure necessary columns are present
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"Column {col} not found in the dataset")
    
    # Select relevant columns and drop rows with missing values
    data_subset = data[required_columns].dropna()

    # Convert columns to numeric types
    data_subset['tradeflow_comtrade_o'] = pd.to_numeric(data_subset['tradeflow_comtrade_o'])
    data_subset['gdp_o'] = pd.to_numeric(data_subset['gdp_o'])
    data_subset['gdp_d'] = pd.to_numeric(data_subset['gdp_d'])
    data_subset['dist'] = pd.to_numeric(data_subset['dist'])

    # Remove rows with invalid (NaN, inf) values in the independent variables
    data_subset = data_subset.replace([np.inf, -np.inf], np.nan).dropna()

    # Remove rows with zero or negative trade flows, GDP, or distance
    data_subset = data_subset[(data_subset['tradeflow_comtrade_o'] > 0) &
                              (data_subset['gdp_o'] > 0) &
                              (data_subset['gdp_d'] > 0) &
                              (data_subset['dist'] > 0)]

# I was having problems with my weights having NaN or infite values before scaling the data. ChatGPT gave me the following explanation:
# The issue was likely due to extreme values, zeros, or negative values in the dependent or independent variables, 
# which can cause numerical instability during model estimation. Scaling the data using StandardScaler normalized the values, 
# ensuring they fall within a similar range, thus improving the stability and convergence of the estimation algorithm. 
# This helps avoid overflow, underflow, and other numerical issues that can result in invalid weights or other computational errors.

    # Scale the data
    scaler = StandardScaler()
    data_subset[['gdp_o', 'gdp_d', 'dist']] = scaler.fit_transform(data_subset[['gdp_o', 'gdp_d', 'dist']])
    
    return data_subset
