import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV file
file_path = 'banknifty.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataframe
print(data.head())

# Convert 'date' to datetime and extract the year
# data['date'] = pd.to_datetime(data['date'])
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data['year'] = data['date'].dt.year

# Calculate the daily candle length
data['candle_length'] = data['high'] - data['low']

# Group by year and calculate average, max, and min candle length
yearly_stats = data.groupby('year')['candle_length'].agg(['mean', 'max', 'min']).reset_index()
# Initialize dictionaries to hold the required increases for each target probability
required_increase_70 = {}
required_increase_80 = {}
required_increase_90 = {}
required_increase_98 = {}

# Function to calculate the required increase to achieve a certain probability
def calculate_required_increase(target_probability, year):
    # Sort the candle lengths for the year
    candle_lengths = data[data['year'] == year]['candle_length'].sort_values().values
    
    # Find the index that corresponds to the desired probability
    index = int(np.ceil(len(candle_lengths) * target_probability) - 1)
    index = min(max(index, 0), len(candle_lengths) - 1)

    # The required candle length for this probability
    required_candle_length = candle_lengths[index]
    
    # Current average candle length for the year
    current_avg_length = yearly_stats[yearly_stats['year'] == year]['mean'].values[0]
    
    # Calculate the required increase
    required_increase = required_candle_length - current_avg_length
    
    return max(required_increase, 0)  # Ensure the increase is not negative

# Calculate the required increases for each year and each target probability
for year in yearly_stats['year']:
    required_increase_70[year] = calculate_required_increase(0.70, year)
    required_increase_80[year] = calculate_required_increase(0.80, year)
    required_increase_90[year] = calculate_required_increase(0.90, year)
    required_increase_98[year] = calculate_required_increase(0.98, year)


# Convert to dataframes for easier plotting
df_increase_70 = pd.DataFrame(list(required_increase_70.items()), columns=['Year', 'Increase for 70%'])
df_increase_80 = pd.DataFrame(list(required_increase_80.items()), columns=['Year', 'Increase for 80%'])
df_increase_90 = pd.DataFrame(list(required_increase_90.items()), columns=['Year', 'Increase for 90%'])
df_increase_98 = pd.DataFrame(list(required_increase_98.items()), columns=['Year', 'Increase for 98%'])

# Plotting the results
plt.figure(figsize=(12, 6))
for df, label, color in [(df_increase_70, 'Increase for 70%', 'blue'), 
                         (df_increase_80, 'Increase for 80%', 'orange'), 
                         (df_increase_90, 'Increase for 90%', 'green'), 
                         (df_increase_98, 'Increase for 98%', 'purple')]:
    plt.plot(df['Year'], df.iloc[:, 1], label=label, marker='o', color=color)
    for i, row in df.iterrows():
        plt.text(row['Year'], row.iloc[1], f'{row.iloc[1]:.2f}', ha='center', va='bottom')

plt.title('Required Increase in Average Candle Length for Target Probabilities')
plt.xlabel('Year')
plt.ylabel('Required Increase in Points')
plt.legend()
plt.grid(True)
plt.show()

# Returning the dataframes for user reference
print(df_increase_70, df_increase_80, df_increase_90, df_increase_98)



