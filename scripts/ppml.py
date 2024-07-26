import pandas as pd
import numpy as np
import gegravity as geg

# Load data
file_path = './data/raw_data/cepii/Gravity_csv_V202211/Gravity_V202211.csv'
df_gravity = pd.read_csv(file_path, low_memory=False)