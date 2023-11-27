import pandas as pd
import numpy as np

# Load the data
file_path = 'path_to_your_file.csv'  # Replace with your file path
data = pd.read_csv('vix.csv')

# Calculate the square root of 365
sqrt_365 = np.sqrt(365)

# Calculate Daily Expected Movement and add it as a new column
data['Daily Expected Movement'] = (data['high'] / sqrt_365)

# Save the updated data to a new CSV file
data.to_csv('updated_data.csv', index=False)
