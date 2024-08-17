import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File paths
files = {
    'North-North': './data/vis/north-north.csv',
    'North-South': './data/vis/north-south.csv',
    'South-South': './data/vis/south-south.csv'
}

# Colors for each trade relationship type
colors = {
    'North-North': 'blue',
    'North-South': 'green',
    'South-South': 'red'
}

# Iterate through the files and create a plot for each
for trade_type, file_path in files.items():
    # Load the CSV file
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
        color=colors[trade_type],  # Use the color associated with the trade type
        s=100,  # Dot size
        data=df
    )

    plt.axhline(y=0, color='gray', linestyle='--', linewidth=1)  # Add horizontal line at 0 significance
    plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)  # Add vertical line at 0 coefficient

    # Adjust y-axis to show significance levels
    plt.yticks([-1, 1, 2, 3], ['Not Significant', 'p < 0.10', 'p < 0.05', 'p < 0.01'])

    plt.title(f'{trade_type} PTA Heterogeneity Across Regions Extended')
    plt.xlabel('Coefficient Magnitude')
    plt.ylabel('Significance Level')
    plt.grid(True)

    # Save the plot as a JPEG file
    output_image_path = f'./data/vis/{trade_type}_trade_relationships_visualization.jpeg'
    plt.savefig(output_image_path, format='jpeg')
    plt.close()

    print(f"Visualization saved to {output_image_path}")

# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from matplotlib.backends.backend_pdf import PdfPages

# # File paths
# files = {
#     'North-North': './data/vis/north-north.csv',
#     'North-South': './data/vis/north-south.csv',
#     'South-South': './data/vis/south-south.csv'
# }

# # Colors for each trade relationship type
# colors = {
#     'North-North': 'blue',
#     'North-South': 'green',
#     'South-South': 'red'
# }

# # Create a PDF file to save the plots
# output_pdf_path = './data/vis/trade_relationships_visualizations.pdf'
# with PdfPages(output_pdf_path) as pdf:
#     for trade_type, file_path in files.items():
#         # Load the CSV file
#         df = pd.read_csv(file_path)

#         # Map the Significance levels: -1 for not significant, and keep the original values for significance levels
#         def map_significance(significance):
#             if significance == 0:
#                 return -1  # Not significant
#             else:
#                 return significance  # Keep original significance level (1, 2, 3)

#         # Apply the mapping
#         df['Significance_Mapped'] = df['Significance'].apply(map_significance)

#         # Plotting the scatter plot with mapped significance levels
#         plt.figure(figsize=(12, 8))

#         sns.scatterplot(
#             x='Estimate',
#             y='Significance_Mapped',
#             color=colors[trade_type],  # Use the color associated with the trade type
#             s=100,  # Dot size
#             data=df
#         )

#         plt.axhline(y=0, color='gray', linestyle='--', linewidth=1)  # Add horizontal line at 0 significance
#         plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)  # Add vertical line at 0 coefficient

#         # Adjust y-axis to show significance levels
#         plt.yticks([-1, 1, 2, 3], ['Not Significant', 'p < 0.10', 'p < 0.05', 'p < 0.01'])

#         plt.title(f'{trade_type} Trade Relationships: Coefficient Magnitude vs Significance')
#         plt.xlabel('Coefficient Magnitude')
#         plt.ylabel('Significance Level')
#         plt.grid(True)

#         # Save the plot to the PDF
#         pdf.savefig()
#         plt.close()

# print(f"Visualizations saved to {output_pdf_path}")

# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load the CSV file
# file_path = './data/vis/south-south.csv'
# df = pd.read_csv(file_path)

# # Map the Significance levels: -1 for not significant, and keep the original values for significance levels
# def map_significance(significance):
#     if significance == 0:
#         return -1  # Not significant
#     else:
#         return significance  # Keep original significance level (1, 2, 3)

# # Apply the mapping
# df['Significance_Mapped'] = df['Significance'].apply(map_significance)

# # Filter the DataFrame for the 'Intercontinental' region
# df_intercontinental = df[df['Region'] == 'Africa']

# # Plotting the scatter plot with mapped significance levels
# plt.figure(figsize=(10, 6))

# sns.scatterplot(
#     x='Estimate',
#     y='Significance_Mapped',
#     hue='Region',
#     data=df_intercontinental,
#     palette='colorblind',  # Use a colorblind-friendly palette
#     s=50  # Dot size
# )

# plt.axhline(y=0, color='gray', linestyle='--', linewidth=1)  # Add horizontal line at 0 significance
# plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)  # Add vertical line at 0 coefficient

# # Adjust y-axis to show significance levels
# plt.yticks([-1, 1, 2, 3], ['Not Significant', 'p < 0.10', 'p < 0.05', 'p < 0.01'])

# plt.title('South-South Trade Relationships: Coefficient Magnitude vs Significance')
# plt.xlabel('Coefficient Magnitude')
# plt.ylabel('Significance Level')
# plt.legend(title='Region')
# plt.grid(True)
# plt.show()
