import pandas as pd

# Load the CSV file
file_path = './data/raw_data/cepii/Gravity_csv_V202211/Gravity_V202211.csv'
df = pd.read_csv(file_path, low_memory=False)

# Take a random sample of 2000 rows
sampled_df = df.sample(n=2000, random_state=42)

# Save the sample to a new CSV file
output_file_path = './data/processed_data/Gravity_V202211_sample.csv'
sampled_df.to_csv(output_file_path, index=False)

print(f'Sample saved to {output_file_path}')