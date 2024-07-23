# Counting South countries without agreements, only with SS, and with both SS and NS
import pandas as pd
import matplotlib.pyplot as plt

# Load the output file
df = pd.read_csv('./output_data/ptas_per_country_summary/ptas_per_country_and_classifications.csv')

# Filter the data for South countries
south_countries = df[df['dahi'].isin(['ES', 'S'])]

# Categorize the South countries
south_no_agreements = south_countries[
    (south_countries['North-North'] == 0) &
    (south_countries['North-South'] == 0) &
    (south_countries['South-South'] == 0)
]

south_only_south_south = south_countries[
    (south_countries['South-South'] > 0) &
    (south_countries['North-North'] == 0) &
    (south_countries['North-South'] == 0)
]

south_only_north_south = south_countries[
    (south_countries['South-South'] == 0) &
    (south_countries['North-North'] == 0) &
    (south_countries['North-South'] > 0)
]

south_south_and_north_south = south_countries[
    (south_countries['South-South'] > 0) &
    (south_countries['North-South'] > 0) &
    (south_countries['North-North'] == 0)
]

# Count the regions for each category
regions_no_agreements = south_no_agreements['Region'].value_counts()
regions_only_south_south = south_only_south_south['Region'].value_counts()
regions_only_north_south = south_only_north_south['Region'].value_counts()
regions_south_and_north_south = south_south_and_north_south['Region'].value_counts()

# Define a consistent color map for regions
region_colors = {
    'East Asia & Pacific': '#ff9999',
    'Europe & Central Asia': '#66b3ff',
    'Latin America & Caribbean': '#99ff99',
    'Middle East & North Africa': '#ffcc99',
    'South Asia': '#c2c2f0',
    'Sub-Saharan Africa': '#ffb3e6',
    'North America': '#c4e17f'  # Adding North America
}

# Get colors for each pie chart based on the defined color map for regions
colors_no_agreements_region = [region_colors[region] for region in regions_no_agreements.index]
colors_only_south_south_region = [region_colors[region] for region in regions_only_south_south.index]
colors_only_north_south_region = [region_colors[region] for region in regions_only_north_south.index]
colors_south_and_north_south_region = [region_colors[region] for region in regions_south_and_north_south.index]

# Plotting the data for regions
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Pie chart for South countries with no agreements
axes[0, 0].pie(regions_no_agreements, labels=regions_no_agreements.index, autopct='%1.1f%%', colors=colors_no_agreements_region)
axes[0, 0].set_title('Regions of South Countries with No Agreements')

# Pie chart for South countries with only South-South agreements
axes[0, 1].pie(regions_only_south_south, labels=regions_only_south_south.index, autopct='%1.1f%%', colors=colors_only_south_south_region)
axes[0, 1].set_title('Regions of South Countries with Only South-South Agreements')

# Pie chart for South countries with only North-South agreements
axes[1, 0].pie(regions_only_north_south, labels=regions_only_north_south.index, autopct='%1.1f%%', colors=colors_only_north_south_region)
axes[1, 0].set_title('Regions of South Countries with Only North-South Agreements')

# Pie chart for South countries with South-South and North-South agreements
axes[1, 1].pie(regions_south_and_north_south, labels=regions_south_and_north_south.index, autopct='%1.1f%%', colors=colors_south_and_north_south_region)
axes[1, 1].set_title('Regions of South Countries with South-South and North-South Agreements')

plt.tight_layout()
plt.savefig('./output_data/visualizations/regions_pie_charts.pdf')
plt.show()

# Count the income levels for each category
income_no_agreements = south_no_agreements['Income group'].value_counts()
income_only_south_south = south_only_south_south['Income group'].value_counts()
income_only_north_south = south_only_north_south['Income group'].value_counts()
income_south_and_north_south = south_south_and_north_south['Income group'].value_counts()

# Define a consistent color map for income levels
income_colors = {
    'Low income': '#ff9999',
    'Lower middle income': '#66b3ff',
    'Upper middle income': '#99ff99',
    'High income': '#ffcc99'
}

# Get colors for each pie chart based on the defined color map for income levels
colors_no_agreements_income = [income_colors[income] for income in income_no_agreements.index]
colors_only_south_south_income = [income_colors[income] for income in income_only_south_south.index]
colors_only_north_south_income = [income_colors[income] for income in income_only_north_south.index]
colors_south_and_north_south_income = [income_colors[income] for income in income_south_and_north_south.index]

# Plotting the data for income levels
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Pie chart for South countries with no agreements
axes[0, 0].pie(income_no_agreements, labels=income_no_agreements.index, autopct='%1.1f%%', colors=colors_no_agreements_income)
axes[0, 0].set_title('Income Levels of South Countries with No Agreements')

# Pie chart for South countries with only South-South agreements
axes[0, 1].pie(income_only_south_south, labels=income_only_south_south.index, autopct='%1.1f%%', colors=colors_only_south_south_income)
axes[0, 1].set_title('Income Levels of South Countries with Only South-South Agreements')

# Pie chart for South countries with only North-South agreements
axes[1, 0].pie(income_only_north_south, labels=income_only_north_south.index, autopct='%1.1f%%', colors=colors_only_north_south_income)
axes[1, 0].set_title('Income Levels of South Countries with Only North-South Agreements')

# Pie chart for South countries with South-South and North-South agreements
axes[1, 1].pie(income_south_and_north_south, labels=income_south_and_north_south.index, autopct='%1.1f%%', colors=colors_south_and_north_south_income)
axes[1, 1].set_title('Income Levels of South Countries with South-South and North-South Agreements')

plt.tight_layout()
plt.savefig('./output_data/visualizations/incomes_pie_charts.pdf')
plt.show()