# Modify the code to account for expiry day changes starting from January 11, 2021

import pandas as pd
import matplotlib.pyplot as plt
from pandas.tseries.offsets import BDay
import numpy as np

# Load the CSV file
file_path = 'finnifty.csv'
data = pd.read_csv(file_path)

# Convert 'date' to datetime and extract the year
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data['year'] = data['date'].dt.year

# Calculate the daily candle length
data['candle_length'] = data['high'] - data['low']

# Filter the data from January 11, 2021 onwards
data_from_2021 = data[data['date'] >= pd.to_datetime("2021-01-11")]

# Function to adjust for expiry days and market holidays
def adjust_for_expiry_and_holidays(date):
    # Expiry day is Thursday till October 14, 2021, and then Tuesday thereafter
    if date <= pd.to_datetime("2021-10-14"):
        expiry_day = 'W-THU'
    else:
        expiry_day = 'W-TUE'

    # Generate the expiry date for the week
    expiry_date = pd.date_range(start=date, periods=1, freq=expiry_day)[0]

    # Adjust for market holidays
    while expiry_date not in data_from_2021['date'].values:
        expiry_date -= BDay(1)

    return expiry_date

# Generate all potential expiry dates from January 11, 2021 onwards
start_date = pd.to_datetime("2021-01-11")
end_date = data['date'].max()
all_potential_expiry_dates = pd.date_range(start=start_date, end=end_date, freq='W')

# Adjust for market holidays and changes in expiry days
adjusted_expiry_dates = all_potential_expiry_dates.map(adjust_for_expiry_and_holidays)

# Filter the dataset for adjusted expiry days
expiry_day_data = data_from_2021[data_from_2021['date'].isin(adjusted_expiry_dates)]

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
plt.title('Probability of Market Remaining Within Average Length on Expiry Days (2021 Onwards)')
plt.xlabel('Year')
plt.ylabel('Probability')
plt.grid(True)
plt.show()



# Function to calculate required increase for target probabilities
def calculate_required_increase_expiry(target_probability, year, expiry_data, yearly_avg):
    candle_lengths = expiry_data[expiry_data['year'] == year]['candle_length'].sort_values().values
    index = int(np.ceil(len(candle_lengths) * target_probability) - 1)
    index = min(max(index, 0), len(candle_lengths) - 1)
    required_candle_length = candle_lengths[index]
    current_avg_length = yearly_avg[year]
    return max(required_candle_length - current_avg_length, 0)

# Calculate required increases for each probability target
required_increase_expiry = {}
for target_probability in [0.70, 0.80, 0.90, 0.98]:
    required_increase_expiry[target_probability] = {}
    for year in yearly_avg_candle_length_expiry.index:
        increase = calculate_required_increase_expiry(target_probability, year, expiry_day_data, yearly_avg_candle_length_expiry)
        required_increase_expiry[target_probability][year] = increase

# Convert to dataframes for easier plotting
df_increase_expiry = {prob: pd.DataFrame(list(increase.items()), columns=['Year', f'Increase for {int(prob * 100)}%']) for prob, increase in required_increase_expiry.items()}

# Plotting the required increases for expiry days
plt.figure(figsize=(12, 6))
for prob, df in df_increase_expiry.items():
    plt.plot(df['Year'], df.iloc[:, 1], label=f'Increase for {int(prob * 100)}%', marker='o')
    # Adding numbers to the plot
    for i, row in df.iterrows():
        plt.text(row['Year'], row.iloc[1], f'{row.iloc[1]:.2f}', ha='center', va='bottom')
plt.title('Required Increase in Average Candle Length for Target Probabilities on Expiry Days')
plt.xlabel('Year')
plt.ylabel('Required Increase in Points')
plt.legend()
plt.grid(True)
plt.show()
