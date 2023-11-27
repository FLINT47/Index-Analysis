import pandas as pd


data = pd.read_csv('sensex.csv')

# Adding a 'year' column for grouping

data['date'] = pd.to_datetime(data['date'], errors='coerce')
data['year'] = data['date'].dt.year

# Calculating the average points Nifty goes high from open and low below close
data['High From Open'] = data['high'] - data['open']
data['Low Below Close'] = data['close'] - data['low']

# Grouping by year and calculating the average
yearly_avg = data.groupby('year').agg({'High From Open': 'mean', 'Low Below Close': 'mean'}).reset_index()

# Plotting the data
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

# Plotting High From Open
plt.subplot(1, 2, 1)
plt.bar(yearly_avg['year'], yearly_avg['High From Open'], color='blue')
for i, row in yearly_avg.iterrows():
    plt.text(row['year'], row['High From Open'], f'{row["High From Open"]:.2f}', ha='center', va='bottom')
plt.xlabel('Year')
plt.ylabel('Average High From Open (points)')
plt.title('Average Points Nifty Goes High From Open')

# Plotting Low Below Close
plt.subplot(1, 2, 2)
plt.bar(yearly_avg['year'], yearly_avg['Low Below Close'], color='green')
for i, row in yearly_avg.iterrows():
    plt.text(row['year'], row['Low Below Close'], f'{row["Low Below Close"]:.2f}', ha='center', va='bottom')
plt.xlabel('Year')
plt.ylabel('Average Low Below Close (points)')
plt.title('Average Points Nifty Goes Low Below Close')

plt.tight_layout()
plt.show()
