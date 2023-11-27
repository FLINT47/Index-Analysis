import pandas as pd
import matplotlib.pyplot as plt
from pandas.tseries.offsets import BDay
import numpy as np

# Assuming the data is already loaded into a DataFrame named 'data'
data = pd.read_csv('banknifty.csv')
# Convert 'date' to datetime
# data['date'] = pd.to_datetime(data['date'])
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data['year'] = data['date'].dt.year
data['candle_length'] = data['high'] - data['low']

# Filter the data from 2019 onwards
data_from_2019 = data[data['date'].dt.year >= 2019]

# Function to adjust for market holidays (if Thursday is a holiday, use Wednesday)
def adjust_for_expiry_and_holidays(date):
    # Check if the date is before or after the new rule implementation
    if date < pd.to_datetime("2023-09-01"):
        expiry_day = 'W-THU'  # Expiry day is Thursday
    else:
        # For dates in September 2023 onwards
        # Last week of the month, expiry on Thursday
        if date.month != 12 and (date + pd.DateOffset(weeks=1)).month != date.month:
            expiry_day = 'W-THU'
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
