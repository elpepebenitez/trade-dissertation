import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file for PTA heterogeneity results
file_path = './data/vis/pta_het.csv'
df = pd.read_csv(file_path)

# Map the Significance levels: -1 for not significant, and keep the original values for significance levels
def map_significance(significance):
    if significance == 0:
        return -1  # Not significant
    else:
        return significance  # Keep original significance level (1, 2, 3)

# Apply the mapping
df['Significance_Mapped'] = df['Significance'].apply(map_significance)

# Plotting the scatter plot with mapped significance levels
plt.figure(figsize=(12, 8))

sns.scatterplot(
    x='Estimate',
    y='Significance_Mapped',
    color='blue',  # Use a single color for all data points
    s=100,  # Dot size
    data=df
)

plt.axhline(y=0, color='gray', linestyle='--', linewidth=1)  # Add horizontal line at 0 significance
plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)  # Add vertical line at 0 coefficient

# Adjust y-axis to show significance levels
plt.yticks([-1, 1, 2, 3], ['Not Significant', 'p < 0.10', 'p < 0.05', 'p < 0.01'])

plt.title('PTA Heterogeneity Across Regions')
plt.xlabel('Coefficient Magnitude')
plt.ylabel('Significance Level')
plt.grid(True)

# Save the plot as a JPEG file
output_image_path = './data/vis/pta_het_vis.jpeg'
plt.savefig(output_image_path, format='jpeg')
plt.close()

print(f"Visualization saved to {output_image_path}")
