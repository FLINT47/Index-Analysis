import pandas as pd
import matplotlib.pyplot as plt
from pandas.tseries.offsets import BDay
import numpy as np

file_path = 'midcpnifty.csv'
data = pd.read_csv(file_path)

# Convert 'date' to datetime and extract the year
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data['year'] = data['date'].dt.year

# Calculate the daily candle length
data['candle_length'] = data['high'] - data['low']

# Adjust the filtering of the data to start from January 24, 2022.
data_from_2022 = data[data['date'] >= pd.to_datetime("2022-01-24")]
# Modifying the function to handle date calculations more robustly

# Modifying the function to handle date calculations more robustly

def adjust_for_expiry_and_holidays(date):
    # Expiry day is Wednesday till August 17, 2023, and then Monday afterwards
    if date <= pd.to_datetime("2023-08-17"):
        expiry_day = 'W-WED'
    else:
        expiry_day = 'W-MON'

    # Generate the expiry date for the week
    expiry_date = pd.date_range(start=date, periods=1, freq=expiry_day)[0]

    # Adjust for market holidays
    while expiry_date not in data_from_2022['date'].values:
        expiry_date -= BDay(1)
        # Additional check to prevent infinite loop or invalid date calculations
        if expiry_date < data_from_2022['date'].min():
            return None

    return expiry_date

# Apply the function to each date in the range individually
adjusted_expiry_dates = [adjust_for_expiry_and_holidays(date) for date in all_potential_expiry_dates]
# Filter out None values which may have occurred due to invalid date calculations
adjusted_expiry_dates = [date for date in adjusted_expiry_dates if date is not None]

# Filter the dataset for adjusted expiry days
expiry_day_data = data_from_2022[data_from_2022['date'].isin(adjusted_expiry_dates)]

# Continuing with the rest of the analysis
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
plt.title('Probability of Market Remaining Within Average Length on Expiry Days (2022 Onwards)')
plt.xlabel('Year')
plt.ylabel('Probability')
plt.grid(True)
plt.show()

# Returning the probabilities
probabilities_expiry
