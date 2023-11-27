import pandas as pd


# Repeating the process with the newly uploaded files

# Loading the new datasets
new_move_csv_path = 'move.csv'
new_nifty50_csv_path = 'nifty50.csv'

new_move_df = pd.read_csv(new_move_csv_path)
new_nifty50_df = pd.read_csv(new_nifty50_csv_path)

# Standardizing the 'date' column format in both dataframes
new_nifty50_df['date'] = pd.to_datetime(new_nifty50_df['date']).dt.date
new_move_df['date'] = pd.to_datetime(new_move_df['date']).dt.date

# Merging the dataframes on the 'date' column for comparison
new_comparison_df = pd.merge(new_nifty50_df, new_move_df[['date', 'Expected Day High', 'Expected Day Low']], on='date', how='inner')

# Calculating the probability for high and low
new_high_within_expected = (new_comparison_df['high'] <= new_comparison_df['Expected Day High']).mean()
new_low_within_expected = (new_comparison_df['low'] >= new_comparison_df['Expected Day Low']).mean()

print(new_high_within_expected, new_low_within_expected)



# Function to find the required adjustment for expected high and low to achieve the target probability
def find_adjustment_for_probability(df, target_probability, high=True):
    # Initial adjustment
    adjustment = 0
    step = 10  # Initial step size for adjustment, can be fine-tuned

    # Loop to adjust until the target probability is reached or exceeded
    while True:
        if high:
            adjusted_high = df['Expected Day High'] + adjustment
            probability = (df['high'] <= adjusted_high).mean()
        else:
            adjusted_low = df['Expected Day Low'] - adjustment
            probability = (df['low'] >= adjusted_low).mean()

        # Check if the probability meets or exceeds the target
        if probability >= target_probability:
            return adjustment
        
        # Increase the adjustment
        adjustment += step

# Finding the required adjustments
adjustment_high = find_adjustment_for_probability(new_comparison_df, 0.99, high=True)
adjustment_low = find_adjustment_for_probability(new_comparison_df, 0.99, high=False)

print(adjustment_high, adjustment_low)
