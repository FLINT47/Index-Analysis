import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV file
file_path = 'banknifty.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataframe
print(data.head())

# Convert 'date' to datetime and extract the year
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data['year'] = data['date'].dt.year

# Calculate the daily candle length
data['candle_length'] = data['high'] - data['low']

# Group by year and calculate average, max, and min candle length
yearly_stats = data.groupby('year')['candle_length'].agg(['mean', 'max', 'min']).reset_index()

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(yearly_stats['year'], yearly_stats['mean'], marker='o', label='Average Candle Length')
plt.scatter(yearly_stats['year'], yearly_stats['max'], marker='x', color='red', label='Max Candle Length')
plt.scatter(yearly_stats['year'], yearly_stats['min'], marker='x', color='green', label='Min Candle Length')

for i, row in yearly_stats.iterrows():
    plt.text(row['year'], row['mean'], round(row['mean'], 2), ha='center', va='bottom')
    plt.text(row['year'], row['max'], round(row['max'], 2), ha='center', va='bottom')
    plt.text(row['year'], row['min'], round(row['min'], 2), ha='center', va='top')

plt.title('Average, Max, and Min Daily Candle Length by Year')
plt.xlabel('Year')
plt.ylabel('Candle Length in Points')
plt.legend()
plt.grid(True)
plt.show()

print(yearly_stats)
