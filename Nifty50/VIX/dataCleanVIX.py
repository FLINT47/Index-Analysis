import pandas as pd

# Load the data
file_path = 'path_to_your_file.csv'  # Replace with your file path
data = pd.read_csv('nifty.csv')

# Convert 'date' column to datetime
data['date'] = pd.to_datetime(data['date'])

# Filter for entries at 9:20
data_at_920 = data[data['date'].dt.time == pd.to_datetime('09:20:00').time()]

# Save the filtered data to a new CSV file
data_at_920.to_csv('nifty920.csv', index=False)
