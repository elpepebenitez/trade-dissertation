import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('./input_data/pta/desta_list_of_treaties_02_02.csv')

# Filter out rows where 'year' is missing
data = data.dropna(subset=['year'])

# Convert 'year' to integer
data['year'] = data['year'].astype(int)

# Count the number of agreements per year by entry_type
entry_type_counts = data.groupby(['year', 'entry_type']).size().reset_index(name='count')

# Create the bar plot
plt.figure(figsize=(14, 8))
sns.barplot(data=entry_type_counts, x='year', y='count', hue='entry_type')

# Customize the plot
plt.title('Number of Agreements per Year by Entry Type')
plt.xlabel('Year')
plt.ylabel('Number of Agreements')
plt.xticks(rotation=90)
plt.legend(title='Entry Type')

# Show the plot
plt.tight_layout()
plt.savefig(f'./output_data/visualizations/all_entries_agreements_per_year.pdf')
plt.close()