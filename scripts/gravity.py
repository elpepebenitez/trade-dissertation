import pandas as pd
import numpy as np
import gegravity as geg

# Load data
file_path = './data/raw_data/cepii/Gravity_csv_V202211/Gravity_V202211.csv'
df_gravity = pd.read_csv(file_path, low_memory=False)
df_treaties = pd.read_csv('./pre_analisis/input_data/pta/desta_list_of_treaties_02_02_dyads.csv')
df_country_codes = pd.read_csv('./pre_analisis/output_data/country_agreements_classified_summary.csv')

# Replace non-finite values in 'numeric_code' column and convert to integer
df_country_codes['numeric_code'] = pd.to_numeric(df_country_codes['numeric_code'], errors='coerce')
df_country_codes.dropna(subset=['numeric_code'], inplace=True)
df_country_codes['numeric_code'] = df_country_codes['numeric_code'].astype(int)

# Drop duplicates to ensure unique mapping
df_country_codes.drop_duplicates(subset='numeric_code', inplace=True)

# Create a mapping between numeric codes and 3-letter codes
numeric_to_code = df_country_codes.set_index('numeric_code')['Code'].to_dict()

# Manually add missing country codes to the mapping
manual_mapping = {
    732: 'ESH',  # Western Sahara
    500: 'FLK',  # Falkland Islands
    900: 'XKX',  # Kosovo (or another unrecognized entity, XKX is often used)
    184: 'COK',  # Cook Islands
    570: 'NIU'   # Niue
}
numeric_to_code.update(manual_mapping)

# Map numeric codes to 3-letter codes in the treaty dataset
df_treaties['country_id_o'] = df_treaties['iso1'].map(numeric_to_code)
df_treaties['country_id_d'] = df_treaties['iso2'].map(numeric_to_code)

# Ensure there are no missing mappings
assert df_treaties['country_id_o'].notna().all(), "Missing mapping for country_id_o"
assert df_treaties['country_id_d'].notna().all(), "Missing mapping for country_id_d"

# Rename columns for clarity
df_treaties.rename(columns={'entryforceyear': 'pta_year'}, inplace=True)

# Merge the datasets on country pairs and year
df_merged = pd.merge(df_gravity, df_treaties[['country_id_o', 'country_id_d', 'pta_year']], on=['country_id_o', 'country_id_d'], how='left')

# Create the PTA and Event Time variables
df_merged['PTA'] = (~df_merged['pta_year'].isna()).astype(int)  # PTA is 1 if pta_year is not NaN
df_merged['event_time'] = df_merged['year'] - df_merged['pta_year']

# Filter the data for years between 1990 and 2018 and within the event window (-10 to +10 years)
df_filtered = df_merged[(df_merged['year'] >= 1990) & (df_merged['year'] <= 2018)]
df_filtered = df_filtered[(df_filtered['event_time'] >= -10) & (df_filtered['event_time'] <= 10)]
df_filtered = df_filtered[df_filtered['country_id_o'] != df_filtered['country_id_d']]
df_filtered.replace([np.inf, -np.inf], np.nan, inplace=True)
df_filtered.dropna(subset=['tradeflow_baci', 'gdp_o', 'gdp_d', 'dist'], inplace=True)

# Log-transform and add constant
df_filtered['log_gdp_o'] = np.log(df_filtered['gdp_o'].replace(0, np.nan))
df_filtered['log_gdp_d'] = np.log(df_filtered['gdp_d'].replace(0, np.nan))
df_filtered['log_distance'] = np.log(df_filtered['dist'].replace(0, np.nan))

# Adding fixed effects
df_filtered['exporter_time'] = df_filtered.groupby(['country_id_o', 'year']).ngroup()
df_filtered['importer_time'] = df_filtered.groupby(['country_id_d', 'year']).ngroup()

# Adding additional control variables
controls = ['comlang_off', 'contig', 'col_dep_ever', 'pop_o', 'pop_d']
df_filtered[controls] = df_filtered[controls].fillna(0)  # Fill NaNs for dummy variables with 0

# Classify countries by income
north_countries = {'AUS', 'AUT', 'BEL', 'CAN', 'DNK', 'FIN', 'FRA', 'DEU', 'GRC', 'ISL', 'ISR', 'ITA', 'JPN', 'LUX', 'NLD', 'NZL', 'NOR', 'PRT', 'ESP', 'SWE', 'CHE', 'GBR', 'USA'}

# Create PTA type dummies
df_filtered['north_o'] = df_filtered['country_id_o'].isin(north_countries).astype(int)
df_filtered['north_d'] = df_filtered['country_id_d'].isin(north_countries).astype(int)

df_filtered['NN_PTA'] = df_filtered['PTA'] * df_filtered['north_o'] * df_filtered['north_d']
df_filtered['NS_PTA'] = df_filtered['PTA'] * ((df_filtered['north_o'] + df_filtered['north_d']) == 1)
df_filtered['SS_PTA'] = df_filtered['PTA'] * ((df_filtered['north_o'] == 0) & (df_filtered['north_d'] == 0))

# Filter for countries that have signed both NS and SS agreements
countries_ns = set(df_filtered[df_filtered['NS_PTA'] == 1]['country_id_o'].unique()) | set(df_filtered[df_filtered['NS_PTA'] == 1]['country_id_d'].unique())
countries_ss = set(df_filtered[df_filtered['SS_PTA'] == 1]['country_id_o'].unique()) | set(df_filtered[df_filtered['SS_PTA'] == 1]['country_id_d'].unique())
common_countries = countries_ns & countries_ss

df_filtered = df_filtered[(df_filtered['country_id_o'].isin(common_countries)) | (df_filtered['country_id_d'].isin(common_countries))]

# Separate datasets for NS and SS agreements
df_ns = df_filtered[df_filtered['NS_PTA'] == 1]
df_ss = df_filtered[df_filtered['SS_PTA'] == 1]

# Create event time dummies and drop one to avoid perfect multicollinearity for NS dataset
for i in range(-10, 11):
    if i != 0:  # Dropping event_time_0 as the reference category
        df_ns.loc[:, f'event_time_{i}'] = (df_ns['event_time'] == i).astype(int)

# PPML estimation for NS dataset using gegravity
X_ns = df_ns[['log_gdp_o', 'log_gdp_d', 'log_distance', 'exporter_time', 'importer_time'] + controls + [f'event_time_{i}' for i in range(-10, 11) if i != 0]]
y_ns = df_ns['tradeflow_baci']
model_ns = geg.ppml(y_ns, X_ns)

# Create event time dummies and drop one to avoid perfect multicollinearity for SS dataset
for i in range(-10, 11):
    if i != 0:  # Dropping event_time_0 as the reference category
        df_ss.loc[:, f'event_time_{i}'] = (df_ss['event_time'] == i).astype(int)

# PPML estimation for SS dataset using gegravity
X_ss = df_ss[['log_gdp_o', 'log_gdp_d', 'log_distance', 'exporter_time', 'importer_time'] + controls + [f'event_time_{i}' for i in range(-10, 11) if i != 0]]
y_ss = df_ss['tradeflow_baci']
model_ss = geg.ppml(y_ss, X_ss)

# Display model summaries
print("North-South PTA Model Summary:")
print(model_ns.summary())

print("South-South PTA Model Summary:")
print(model_ss.summary())

# Visualization with Statistical Significance for NS model
import matplotlib.pyplot as plt

# Extract coefficients and confidence intervals for event time dummies for NS model
event_time_coefs_ns = {i: model_ns.params[f'event_time_{i}'] for i in range(-10, 11) if i != 0}
event_time_cis_ns = {i: model_ns.conf_int().loc[f'event_time_{i}'] for i in range(-10, 11) if i != 0}
pvalues_ns = {i: model_ns.pvalues[f'event_time_{i}'] for i in range(-10, 11) if i != 0}

# Create a DataFrame for plotting for NS model
event_time_df_ns = pd.DataFrame({
    'event_time': list(event_time_coefs_ns.keys()),
    'coef': list(event_time_coefs_ns.values()),
    'ci_lower': [event_time_cis_ns[i][0] for i in range(-10, 11) if i != 0],
    'ci_upper': [event_time_cis_ns[i][1] for i in range(-10, 11) if i != 0],
    'pvalue': list(pvalues_ns.values())
}).sort_values('event_time')

event_time_df_ns['significance'] = event_time_df_ns['pvalue'].apply(significance_stars)

# Plot the event study results for NS model
plt.figure(figsize=(12, 8))
plt.plot(event_time_df_ns['event_time'], event_time_df_ns['coef'], marker='o', linestyle='-', color='b')
plt.fill_between(event_time_df_ns['event_time'], event_time_df_ns['ci_lower'], event_time_df_ns['ci_upper'], color='b', alpha=0.2)
plt.axhline(0, color='gray', linestyle='--')

# Add markers for statistical significance for NS model
for i, row in event_time_df_ns.iterrows():
    plt.text(row['event_time'], row['coef'], row['significance'], color='red', fontsize=12, ha='center')

plt.xlabel('Event Time (Years)')
plt.ylabel('Coefficient')
plt.title('Event Study: Impact of North-South PTA on Trade Flows')
plt.grid(True)
plt.show()
# plt.tight_layout()
# plt.savefig(f'./analisis/gravity/NS.pdf')
# plt.close()

# Visualization with Statistical Significance for SS model

# Extract coefficients and confidence intervals for event time dummies for SS model
event_time_coefs_ss = {i: model_ss.params[f'event_time_{i}'] for i in range(-10, 11) if i != 0}
event_time_cis_ss = {i: model_ss.conf_int().loc[f'event_time_{i}'] for i in range(-10, 11) if i != 0}
pvalues_ss = {i: model_ss.pvalues[f'event_time_{i}'] for i in range(-10, 11) if i != 0}

# Create a DataFrame for plotting for SS model
event_time_df_ss = pd.DataFrame({
    'event_time': list(event_time_coefs_ss.keys()),
    'coef': list(event_time_coefs_ss.values()),
    'ci_lower': [event_time_cis_ss[i][0] for i in range(-10, 11) if i != 0],
    'ci_upper': [event_time_cis_ss[i][1] for i in range(-10, 11) if i != 0],
    'pvalue': list(pvalues_ss.values())
}).sort_values('event_time')

event_time_df_ss['significance'] = event_time_df_ss['pvalue'].apply(significance_stars)

# Plot the event study results for SS model
plt.figure(figsize=(12, 8))
plt.plot(event_time_df_ss['event_time'], event_time_df_ss['coef'], marker='o', linestyle='-', color='b')
plt.fill_between(event_time_df_ss['event_time'], event_time_df_ss['ci_lower'], event_time_df_ss['ci_upper'], color='b', alpha=0.2)
plt.axhline(0, color='gray', linestyle='--')

# Add markers for statistical significance for SS model
for i, row in event_time_df_ss.iterrows():
    plt.text(row['event_time'], row['coef'], row['significance'], color='red', fontsize=12, ha='center')

plt.xlabel('Event Time (Years)')
plt.ylabel('Coefficient')
plt.title('Event Study: Impact of South-South PTA on Trade Flows')
plt.grid(True)
plt.show()
# plt.tight_layout()
# plt.savefig(f'./analisis/gravity/SS.pdf')
# plt.close()