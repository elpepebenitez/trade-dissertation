import pandas as pd
import matplotlib.pyplot as plt

# Load the final CSV file
df = pd.read_csv('./output_data/country_agreements_classified_summary.csv')

# Aggregate data by region
region_agg = df.groupby('Region').agg({
    'North-North': lambda x: (x > 0).sum(),
    'North-South': lambda x: (x > 0).sum(),
    'South-South': lambda x: (x > 0).sum()
}).reset_index()

# Aggregate data by income level
income_agg = df.groupby('Income group').agg({
    'North-North': lambda x: (x > 0).sum(),
    'North-South': lambda x: (x > 0).sum(),
    'South-South': lambda x: (x > 0).sum()
}).reset_index()

# Calculate proportions for regions
region_agg['Total'] = region_agg['North-North'] + region_agg['North-South'] + region_agg['South-South']
region_agg['North-North (%)'] = (region_agg['North-North'] / region_agg['Total']) * 100
region_agg['North-South (%)'] = (region_agg['North-South'] / region_agg['Total']) * 100
region_agg['South-South (%)'] = (region_agg['South-South'] / region_agg['Total']) * 100

# Calculate proportions for income levels
income_agg['Total'] = income_agg['North-North'] + income_agg['North-South'] + income_agg['South-South']
income_agg['North-North (%)'] = (income_agg['North-North'] / income_agg['Total']) * 100
income_agg['North-South (%)'] = (income_agg['North-South'] / income_agg['Total']) * 100
income_agg['South-South (%)'] = (income_agg['South-South'] / income_agg['Total']) * 100

# Plotting the data for regions
fig, ax = plt.subplots(1, 2, figsize=(15, 7))

region_agg.plot(kind='bar', x='Region', y=['North-North', 'North-South', 'South-South'], stacked=True, ax=ax[0])
ax[0].set_title('Total Unique Countries by Region')
ax[0].set_ylabel('Number of Unique Countries')

region_agg.plot(kind='bar', x='Region', y=['North-North (%)', 'North-South (%)', 'South-South (%)'], stacked=True, ax=ax[1])
ax[1].set_title('Proportion of Agreements by Region')
ax[1].set_ylabel('Percentage of Agreements')

plt.tight_layout()
plt.show()

# Plotting the data for income levels
fig, ax = plt.subplots(1, 2, figsize=(15, 7))

income_agg.plot(kind='bar', x='Income group', y=['North-North', 'North-South', 'South-South'], stacked=True, ax=ax[0])
ax[0].set_title('Total Unique Countries by Income Group')
ax[0].set_ylabel('Number of Unique Countries')

income_agg.plot(kind='bar', x='Income group', y=['North-North (%)', 'North-South (%)', 'South-South (%)'], stacked=True, ax=ax[1])
ax[1].set_title('Proportion of Agreements by Income Group')
ax[1].set_ylabel('Percentage of Agreements')

plt.tight_layout()
plt.show()