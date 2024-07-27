import pandas as pd

file_path = './data/processed_data/filtered_gravity_data.csv'
data = pd.read_csv(file_path, low_memory=False)

print(data.columns)