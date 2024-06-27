import pandas as pd
import matplotlib.pyplot as plt

# Load the consolidated data
file_path = './data/Export_Data_Summary.csv'
data = pd.read_csv(file_path)

# Add the new column
data['Total Value of Exports (PrimaryValue) / Unique Products Exported'] = (
    data['Total Value of Exports (PrimaryValue)'] / data['Unique Products Exported']
)

# Save the updated DataFrame to a new CSV file
updated_file_path = './data/Updated_Export_Data_Summary.csv'
data.to_csv(updated_file_path, index=False)

# Display the first few rows of the updated DataFrame
print("Updated DataFrame:")
print(data.head())
print(f"\nThe updated CSV file is saved as {updated_file_path}")

# Load the updated data
data = pd.read_csv(updated_file_path)

# Function to plot the data and save as PDF
def plot_data(df, y_column, y_label, title, filename):
    plt.figure(figsize=(12, 8))
    for country in df['Country'].unique():
        subset = df[df['Country'] == country]
        plt.plot(subset['Year'], subset[y_column], marker='o', label=country)
    
    plt.xlabel('Year')
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(f'./{filename}.pdf')
    plt.close()

# Plot and save the new column
plot_data(
    data,
    'Total Value of Exports (PrimaryValue) / Unique Products Exported',
    'Total Value of Exports / Unique Products Exported',
    'Total Value of Exports / Unique Products Exported by Year for Each Country',
    'Value_per_Product_Comparison'
)

print("The graph has been saved as 'Value_per_Product_Comparison.pdf'")
