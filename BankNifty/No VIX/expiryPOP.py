from pandas.tseries.offsets import BDay
import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV file
file_path = 'banknifty.csv'
data = pd.read_csv(file_path)

# Convert 'date' to datetime and extract the year
# data['date'] = pd.to_datetime(data['date'])
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data['year'] = data['date'].dt.year

# Calculate the daily candle length
data['candle_length'] = data['high'] - data['low']

# Group by year and calculate average, max, and min candle length
yearly_stats = data.groupby('year')['candle_length'].agg(['mean', 'max', 'min']).reset_index()

# Filter the data from 2019 onwards
data_from_2019 = data[data['date'].dt.year >= 2019]

# Function to adjust for market holidays and expiry day changes in 2023
def adjust_for_expiry_and_holidays(date):
    # Before September 2023, expiry day was Thursday
    if date < pd.to_datetime("2023-09-01"):
        expiry_day = 'W-THU'
    else:
        # In September 2023 onwards, expiry day is Wednesday except the last week
        if date.month != 12 and (date + pd.DateOffset(weeks=1)).month != date.month:
            expiry_day = 'W-THU'  # Last week of the month, expiry on Thursday
        else:
            expiry_day = 'W-WED'  # Other weeks, expiry on Wednesday

    # Generate the expiry date for the week
    expiry_date = pd.date_range(start=date, periods=1, freq=expiry_day)[0]

    # Adjust for market holidays
    while expiry_date not in data_from_2019['date'].values:
        expiry_date -= BDay(1)

    return expiry_date


# Generate all potential expiry dates from 2019 onwards
start_date = pd.to_datetime("2019-01-01")
end_date = data['date'].max()
all_potential_expiry_dates = pd.date_range(start=start_date, end=end_date, freq='W')

# Adjust for market holidays and changes in expiry days
adjusted_expiry_dates = all_potential_expiry_dates.map(adjust_for_expiry_and_holidays)

# Filter the dataset for adjusted expiry days
expiry_day_data = data_from_2019[data_from_2019['date'].isin(adjusted_expiry_dates)]

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

probabilities_expiry

