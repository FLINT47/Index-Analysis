import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV file
file_path = 'midcpnifty.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataframe
print(data.head())

# Convert 'date' to datetime and extract the year
data['date'] = pd.to_datetime(data['date'], errors='coerce')
# Adjusting the data to show monthly statistics instead of yearly
data['candle_length'] = data['high'] - data['low']
# Extracting the month from the date
data['year_month'] = data['date'].dt.strftime('%Y-%m')
# Grouping by this new year_month label

monthly_stats = data.groupby('year_month')['candle_length'].agg(['mean', 'max', 'min']).reset_index()
# Plotting with year-month labels

plt.figure(figsize=(12, 6))
plt.plot(monthly_stats['year_month'], monthly_stats['mean'], marker='o', label='Average Candle Length')
plt.scatter(monthly_stats['year_month'], monthly_stats['max'], marker='x', color='red', label='Max Candle Length')
plt.scatter(monthly_stats['year_month'], monthly_stats['min'], marker='x', color='green', label='Min Candle Length')

for i, row in monthly_stats.iterrows():
    plt.text(row['year_month'], row['mean'], round(row['mean'], 2), ha='center', va='bottom')
    plt.text(row['year_month'], row['max'], round(row['max'], 2), ha='center', va='bottom')
    plt.text(row['year_month'], row['min'], round(row['min'], 2), ha='center', va='top')

plt.title('Average, Max, and Min Monthly Candle Length (Year-Month)')
plt.xlabel('Year-Month')
plt.ylabel('Candle Length in Points')
plt.xticks(rotation=45)  # Rotate labels for better readability
plt.legend()
plt.grid(True)
plt.show()

