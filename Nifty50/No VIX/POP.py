import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV file
file_path = 'nifty50.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataframe
print(data.head())

# Convert 'date' to datetime and extract the year
data['date'] = pd.to_datetime(data['date'])
data['year'] = data['date'].dt.year

# Calculate the daily candle length
data['candle_length'] = data['high'] - data['low']

# Group by year and calculate average, max, and min candle length
yearly_stats = data.groupby('year')['candle_length'].agg(['mean', 'max', 'min']).reset_index()


# Calculate the number of days each year when the market remained within the average candle length
within_average = data.groupby('year').apply(lambda x: (x['candle_length'] <= yearly_stats[yearly_stats['year'] == x.name]['mean'].values[0]).sum())

# Calculate the total number of trading days per year
total_days = data['year'].value_counts().sort_index()

# Calculate the probability for each year
probabilities = within_average / total_days

# Plotting the probabilities
plt.figure(figsize=(12, 6))
plt.plot(probabilities.index, probabilities.values, marker='o', linestyle='-')
for year, prob in probabilities.items():
    plt.text(year, prob, f'{prob:.2f}', ha='center', va='bottom')
plt.title('Probability of Market Remaining Within Average Daily Length Each Year')
plt.xlabel('Year')
plt.ylabel('Probability')
plt.grid(True)
plt.show()

print(probabilities)
