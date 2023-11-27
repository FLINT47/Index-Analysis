from pandas.tseries.offsets import BDay
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load the CSV file
file_path = 'nifty50.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataframe
data.head()

# Convert 'date' to datetime and extract the year
data['date'] = pd.to_datetime(data['date'])
data['year'] = data['date'].dt.year

# Calculate the daily candle length
data['candle_length'] = data['high'] - data['low']

# Group by year and calculate average, max, and min candle length
yearly_stats = data.groupby('year')['candle_length'].agg(['mean', 'max', 'min']).reset_index()

# Filter the data from 2019 onwards
data_from_2019 = data[data['date'].dt.year >= 2019]

# Function to adjust for market holidays (if Thursday is a holiday, use Wednesday)
def adjust_for_holiday(date):
    # If the market was open on the date, return the date
    if date in data_from_2019['date'].values:
        return date
    # Else return the previous business day
    else:
        return date - BDay(1)

# Generate all Thursdays from 2019 onwards
thursdays = pd.date_range(start='2019-01-01', end=data['date'].max(), freq='W-THU')

# Adjust for market holidays
expiry_days = thursdays.map(adjust_for_holiday)

# Filter the dataset for expiry days
expiry_day_data = data_from_2019[data_from_2019['date'].isin(expiry_days)]

print(expiry_day_data.head())

# Group by year and calculate average candle length for expiry days
yearly_avg_candle_length_expiry = expiry_day_data.groupby('year')['candle_length'].mean()

# Calculate the number of expiry days each year when the market remained within the average candle length
within_avg_expiry = expiry_day_data.groupby('year').apply(lambda x: (x['candle_length'] <= yearly_avg_candle_length_expiry[x.name]).sum())

# Calculate the total number of expiry days per year
total_expiry_days = expiry_day_data['year'].value_counts().sort_index()

# Calculate the probability for each year (expiry days)
probabilities_expiry = within_avg_expiry / total_expiry_days


# Plotting the probabilities for expiry days
plt.figure(figsize=(12, 6))
plt.plot(probabilities_expiry.index, probabilities_expiry.values, marker='o', linestyle='-')
for year, prob in probabilities_expiry.items():
    plt.text(year, prob, f'{prob:.2f}', ha='center', va='bottom')
plt.title('Probability of Market Remaining Within Average Length on Expiry Days (2019 Onwards)')
plt.xlabel('Year')
plt.ylabel('Probability')
plt.grid(True)
plt.show()

print(probabilities_expiry)







