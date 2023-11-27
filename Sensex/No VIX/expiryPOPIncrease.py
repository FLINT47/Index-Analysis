import pandas as pd
import matplotlib.pyplot as plt
from pandas.tseries.offsets import BDay
import numpy as np

# Load the CSV file
data = pd.read_csv('sensex.csv')

# Convert 'date' to datetime
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data['year_month'] = data['date'].dt.to_period('M')
data['candle_length'] = data['high'] - data['low']

# Filter the data from May 15, 2023 onwards
data_from_2023 = data[data['date'] >= pd.to_datetime("2023-05-15")]

# Generate all Fridays as potential expiry dates from May 15, 2023 onwards
fridays = pd.date_range(start='2023-05-15', end='2024-05-14', freq='W-FRI')

# Adjust for market holidays: if a Friday is a holiday (not in data), use the previous business day
adjusted_fridays = [date - BDay(1) if date not in data_from_2023['date'].values else date for date in fridays]

# Filter the data for adjusted expiry days
expiry_day_data = data_from_2023[data_from_2023['date'].isin(adjusted_fridays)]

# Group by year_month and calculate average candle length for expiry days
month_avg_candle_length_expiry = expiry_day_data.groupby('year_month')['candle_length'].mean()

# Function to calculate required increase for target probabilities
def calculate_required_increase_expiry(target_probability, period, expiry_data, monthly_avg):
    candle_lengths = expiry_data[expiry_data['year_month'] == period]['candle_length'].sort_values().values
    index = int(np.ceil(len(candle_lengths) * target_probability) - 1)
    index = min(max(index, 0), len(candle_lengths) - 1)
    required_candle_length = candle_lengths[index]
    current_avg_length = monthly_avg[period]
    return max(required_candle_length - current_avg_length, 0)

# Calculate required increases for each target probability month-wise
required_increase_expiry = {target_probability: {} for target_probability in [0.70, 0.80, 0.90, 0.98]}
for target_probability in [0.70, 0.80, 0.90, 0.98]:
    for period in month_avg_candle_length_expiry.index:
        increase = calculate_required_increase_expiry(target_probability, period, expiry_day_data, month_avg_candle_length_expiry)
        required_increase_expiry[target_probability][period] = increase

# Plotting the probabilities for expiry days month-wise
plt.figure(figsize=(12, 6))
probabilities_expiry = expiry_day_data.groupby('year_month').apply(lambda x: (x['candle_length'] <= month_avg_candle_length_expiry[x.name]).sum()) / expiry_day_data['year_month'].value_counts()
plt.plot(probabilities_expiry.index.astype(str), probabilities_expiry.values, marker='o', linestyle='-')
for period, prob in probabilities_expiry.items():
    plt.text(period.strftime('%Y-%m'), prob, f'{prob:.2f}', ha='center', va='bottom')
plt.xticks(rotation=45)
plt.title('Probability of Market Remaining Within Average Length on Expiry Days (Month-wise for 2023-2024)')
plt.xlabel('Year-Month')
plt.ylabel('Probability')
plt.grid(True)
plt.show()

# Plotting the required increases for target probabilities month-wise
plt.figure(figsize=(12, 6))
for prob, increases in required_increase_expiry.items():
    months = [period.strftime('%Y-%m') for period in increases.keys()]
    values = list(increases.values())
    plt.plot(months, values, label=f'Increase for {int(prob * 100)}%', marker='o')
    for i, value in enumerate(values):
        plt.text(months[i], value, f'{value:.2f}', ha='center', va='bottom')
plt.xticks(rotation=45)
plt.title('Required Increase in Average Candle Length for Target Probabilities on Expiry Days')
plt.xlabel('Year-Month')
plt.ylabel('Required Increase in Points')
plt.legend()
plt.grid(True)
plt.show()
