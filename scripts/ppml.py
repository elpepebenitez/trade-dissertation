import gme as gm
import pandas as pd

# Load data
file_path = './data/raw_data/cepii/Gravity_csv_V202211/Gravity_V202211.csv'
data = pd.read_csv(file_path, low_memory=False)

# Subset of the data for testing
data_subset = data.sample(n=1000, random_state=1)

# Create EstimationData object
est_data = gm.EstimationData(data_frame=data_subset,
                                   imp_var_name='country_id_d',
                                   exp_var_name='country_id_o',
                                   trade_var_name='tradeflow_comtrade_o', # COMTRADE trade flows from origin to destination as declared by exporter
                                   year_var_name='year')

# print(est_data)

# Define the gravity model
model = gm.EstimationModel(
    estimation_data=est_data,
    lhs_var='tradeflow_comtrade_o',  # Dependent variable
    rhs_var=['gdp_o', 'gdp_d', 'dist', 'comlang_off', 'contig', 'col_dep_ever', 'pop_o', 'pop_d'],  # Independent variables
    fixed_effects=[['country_id_d','year'],['country_id_o','year']]  # Fixed effects
)

results = model.estimate()
print(results.summary())
# print(model.ppml_diagnostics)