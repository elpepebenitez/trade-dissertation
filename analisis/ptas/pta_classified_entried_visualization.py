import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('./input_data/pta/desta_list_of_treaties_02_02.csv')
classified_df = pd.read_csv('./output_data/classified_membership.csv')

# Merge the datasets on the 'base_treaty' column
merged_df = pd.merge(data, classified_df[['base_treaty', 'classification']], on='base_treaty', how='left')

# Filter out rows where 'year' is missing
merged_df = merged_df.dropna(subset=['year'])

# Convert 'year' to integer
merged_df['year'] = merged_df['year'].astype(int)

# Define a function to plot the data for a specific classification and save as PDF
def plot_classification(classification):
    subset = merged_df[merged_df['classification'] == classification]
    entry_type_counts = subset.groupby(['year', 'entry_type']).size().reset_index(name='count')

    plt.figure(figsize=(14, 8))
    sns.barplot(data=entry_type_counts, x='year', y='count', hue='entry_type')

    plt.title(f'Number of Agreements per Year by Entry Type ({classification})')
    plt.xlabel('Year')
    plt.ylabel('Number of Agreements')
    plt.xticks(rotation=90)
    plt.legend(title='Entry Type')

    plt.tight_layout()
    plt.savefig(f'./output_data/visualizations/agreements_per_year_{classification}.pdf')
    plt.close()

# Plot for all classifications and save as PDF
for classification in ['North-North', 'North-South', 'South-South']:
    plot_classification(classification)