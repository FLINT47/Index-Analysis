from pandas.tseries.offsets import BDay
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Load the CSV file
file_path = 'midcpnifty.csv'
data = pd.read_csv(file_path)

# Convert 'date' to datetime, extract year and month
data['date'] = pd.to_datetime(data['date'])
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month

# Calculate the daily candle length
data['candle_length'] = data['high'] - data['low']

# Filter the data from January 24, 2022, onwards
data_from_2022 = data[data['date'] >= '2022-01-24']

# Adjust for market holidays
def adjust_for_holiday(date):
    if date in data_from_2022['date'].values:
        return date
    else:
        return date - BDay(1)

# Generate expiry days
expiry_wednesdays = pd.date_range(start='2022-01-24', end='2023-08-17', freq='W-WED')
expiry_mondays = pd.date_range(start='2023-08-21', end=data['date'].max(), freq='W-MON')
expiry_days = expiry_wednesdays.union(expiry_mondays).map(adjust_for_holiday)

# Filter the dataset for expiry days
expiry_day_data = data_from_2022[data_from_2022['date'].isin(expiry_days)]

# Group by year and month
grouped_data = expiry_day_data.groupby(['year', 'month'])

# Calculate average candle length for each month
monthly_avg_candle_length = grouped_data['candle_length'].mean()

# Calculate the number of expiry days each month when the market remained within the average candle length
within_avg_expiry = grouped_data.apply(lambda x: (x['candle_length'] <= monthly_avg_candle_length[x.name]).sum())

# Calculate the total number of expiry days per month
total_expiry_days_per_month = grouped_data.size()

# Calculate the probability for each month
probabilities_expiry = within_avg_expiry / total_expiry_days_per_month

date_index = pd.to_datetime(probabilities_expiry.index.map(lambda x: f"{x[0]}-{x[1]}"))
probabilities_expiry.index = date_index

# Plotting the probabilities for expiry days as a line graph
plt.figure(figsize=(15, 8))
plt.plot(probabilities_expiry.index, probabilities_expiry.values, marker='o', linestyle='-')
for month, prob in probabilities_expiry.items():
    plt.text(month, prob, f'{prob:.2f}', ha='center', va='bottom')
plt.title('Monthly Probability of Market Remaining Within Average Length on Expiry Days')
plt.xlabel('Month and Year')
plt.ylabel('Probability')

# Formatting the x-axis to show month and year
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=45)

plt.grid(True)
plt.show()