import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('midcpnifty.csv')

# Adding a 'year' column for grouping

data['date'] = pd.to_datetime(data['date'], errors='coerce')
# Modifying the code to group and display data on a monthly basis

data['year_month'] = data['date'].dt.strftime('%Y-%m')
# Grouping by this new year_month label

data['High From Open'] = data['high'] - data['open']
data['Low Below Close'] = data['close'] - data['low']

monthly_avg = data.groupby('year_month').agg({'High From Open': 'mean', 'Low Below Close': 'mean'}).reset_index()
# Plotting with year-month labels
# Plotting the data with the month-year format
plt.figure(figsize=(15, 6))

# Plotting High From Open
plt.subplot(1, 2, 1)
plt.bar(monthly_avg['year_month'], monthly_avg['High From Open'], color='blue')
plt.xticks(rotation=45)
for i, row in monthly_avg.iterrows():
    plt.text(row['year_month'], row['High From Open'], f'{row["High From Open"]:.2f}', ha='center', va='bottom')
plt.xlabel('Month-Year')
plt.ylabel('Average High From Open (points)')
plt.title('Monthly Average Points Nifty Goes High From Open')

# Plotting Low Below Close
plt.subplot(1, 2, 2)
plt.bar(monthly_avg['year_month'], monthly_avg['Low Below Close'], color='green')
plt.xticks(rotation=45)
for i, row in monthly_avg.iterrows():
    plt.text(row['year_month'], row['Low Below Close'], f'{row["Low Below Close"]:.2f}', ha='center', va='bottom')
plt.xlabel('Month-Year')
plt.ylabel('Average Low Below Close (points)')
plt.title('Monthly Average Points Nifty Goes Low Below Close')

plt.tight_layout()
plt.show()
