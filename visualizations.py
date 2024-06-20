import pandas as pd
import matplotlib.pyplot as plt

# Load the consolidated data
file_path = './data/Export_Data_Summary.csv'
data = pd.read_csv(file_path)

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

# Plot and save Unique Products Exported
plot_data(data, 'Unique Products Exported', 'Unique Products Exported', 'Unique Products Exported by Year for Each Country', 'Unique_Products_Exported')

# Plot and save Total Value of Exports
plot_data(data, 'Total Value of Exports (PrimaryValue)', 'Total Value of Exports (PrimaryValue)', 'Total Value of Exports by Year for Each Country', 'Total_Value_of_Exports')

# Plot and save Total Net Weight of Exports
plot_data(data, 'Total Net Weight of Exports (NetWgt)', 'Total Net Weight of Exports (NetWgt)', 'Total Net Weight of Exports by Year for Each Country', 'Total_Net_Weight_of_Exports')
