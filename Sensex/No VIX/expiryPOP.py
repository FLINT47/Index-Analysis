import pandas as pd
import matplotlib.pyplot as plt
from pandas.tseries.offsets import BDay
import numpy as np

# Load the CSV file
file_path = 'sensex.csv'
data = pd.read_csv(file_path)

# Convert 'date' to datetime
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month

# Calculate the daily candle length
data['candle_length'] = data['high'] - data['low']

# Filter the data from May 15, 2023 onwards
data_from_2023 = data[data['date'] >= pd.to_datetime("2023-05-15")]

# Function to adjust for market holidays
def adjust_for_holiday(date):
    if date in data_from_2023['date'].values:
        return date
    else:
        return date - BDay(1)

# Generate all Fridays as potential expiry dates from May 15, 2023 onwards
start_date = pd.to_datetime("2023-05-15")
end_date = data['date'].max()
fridays = pd.date_range(start=start_date, end=end_date, freq='W-FRI')
expiry_days = fridays.map(adjust_for_holiday)

# Filter the dataset for adjusted expiry days
expiry_day_data = data_from_2023[data_from_2023['date'].isin(expiry_days)]

# Group by year and month, and calculate average candle length for expiry days
year_month_avg_candle_length_expiry = expiry_day_data.groupby(['year', 'month'])['candle_length'].mean()

# Calculate the number of expiry days each month when the market remained within the average candle length
within_avg_expiry = expiry_day_data.groupby(['year', 'month']).apply(lambda x: (x['candle_length'] <= year_month_avg_candle_length_expiry[x.name]).sum())

# Calculate the total number of expiry days per month
total_expiry_days = expiry_day_data.groupby(['year', 'month']).size()

# Calculate the probability for each month (expiry days)
probabilities_expiry = within_avg_expiry / total_expiry_days
# Assuming 'probabilities_expiry' is calculated as per your previous code

# Plotting the probabilities for expiry days month-wise
plt.figure(figsize=(12, 6))
# Create a string representation of the year-month index
year_month_str = probabilities_expiry.index.map(lambda x: f"{x[0]}-{x[1]:02d}")
plt.plot(year_month_str, probabilities_expiry.values, marker='o', linestyle='-')
for i, (index, prob) in enumerate(probabilities_expiry.items()):
    plt.text(year_month_str[i], prob, f'{prob:.2f}', ha='center', va='bottom')
plt.xticks(rotation=45)
plt.title('Probability of Market Remaining Within Average Length on Expiry Days (Month-wise for 2023)')
plt.xlabel('Year-Month')
plt.ylabel('Probability')
plt.grid(True)
plt.show()


print(probabilities_expiry)
