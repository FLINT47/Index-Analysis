import pandas as pd

# Load the datasets
nifty920_path = 'nifty920.csv'
updated_data_path = 'updated_data.csv'

nifty920_df = pd.read_csv(nifty920_path)
updated_data_df = pd.read_csv(updated_data_path)

# Checking the first few rows of each dataframe to understand their structure
print(nifty920_df.head(), updated_data_df.head())
# Merging the dataframes on the 'date' column
merged_df = pd.merge(nifty920_df, updated_data_df[['date', 'Daily Expected Movement']], on='date', how='left')

# Correcting the calculations for expected day high and low as per the new instructions
merged_df['Expected Day High'] = merged_df['open'] + ((merged_df['Daily Expected Movement'] / 100) * merged_df['open'])
merged_df['Expected Day Low'] = merged_df['open'] - ((merged_df['Daily Expected Movement'] / 100) * merged_df['open'])

# Saving the corrected dataframe to the same CSV file
output_file_path = 'move.csv'
merged_df.to_csv(output_file_path, index=False)

output_file_path
