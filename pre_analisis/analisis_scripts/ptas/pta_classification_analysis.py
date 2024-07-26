import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the classified membership dataset
classified_df = pd.read_csv('./output_data/classified_membership.csv')

# Count the number of agreements per year by classification
classified_counts = classified_df.groupby(['year', 'classification']).size().reset_index(name='count')

# Create the bar plot
plt.figure(figsize=(14, 8))
sns.barplot(data=classified_counts, x='year', y='count', hue='classification')

# Customize the plot
plt.title('Number of Agreements per Year by Classification')
plt.xlabel('Year')
plt.ylabel('Number of Agreements')
plt.xticks(rotation=90)
plt.legend(title='Classification')

# Show the plot
plt.tight_layout()
plt.show()