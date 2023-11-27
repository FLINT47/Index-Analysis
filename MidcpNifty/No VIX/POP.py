import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV file
file_path = 'midcpnifty.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataframe
print(data.head())

# Convert 'date' to datetime and extract the year
data['date'] = pd.to_datetime(data['date'], errors='coerce')

# Calculate the daily candle length
data['candle_length'] = data['high'] - data['low']

# Adjusting the data to show monthly statistics instead of yearly

# Extracting the month and year as a combined string for labeling
data['year_month'] = data['date'].dt.strftime('%Y-%m')

# Group by month-year and calculate average, max, and min candle length
monthly_stats = data.groupby('year_month')['candle_length'].agg(['mean', 'max', 'min']).reset_index()

# Calculate the number of days each month when the market remained within the average candle length
within_average_monthly = data.groupby('year_month').apply(lambda x: (x['candle_length'] <= monthly_stats[monthly_stats['year_month'] == x.name]['mean'].values[0]).sum())

# Calculate the total number of trading days per month
total_days_monthly = data['year_month'].value_counts().sort_index()

# Calculate the probability for each month
probabilities_monthly = within_average_monthly / total_days_monthly

# Plotting the monthly probabilities
plt.figure(figsize=(12, 6))
plt.plot(probabilities_monthly.index, probabilities_monthly.values, marker='o', linestyle='-')
for year_month, prob in probabilities_monthly.items():
    plt.text(year_month, prob, f'{prob:.2f}', ha='center', va='bottom')
plt.title('Probability of Market Remaining Within Average Daily Length Each Month')
plt.xlabel('Year-Month')
plt.ylabel('Probability')
plt.xticks(rotation=45) # Rotate labels for better readability
plt.grid(True)
plt.show()
