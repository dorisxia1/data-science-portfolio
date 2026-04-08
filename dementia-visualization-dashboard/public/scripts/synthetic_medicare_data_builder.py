import pandas as pd
import numpy as np

# Load your original 2020 dataset
df_2020 = pd.read_csv('../public/data/cleaned/circlePackingData.csv')  # Make sure your CSV is in the same folder
df_2020['YEAR'] = 2020  # Add YEAR column for 2020

# Function to generate aggressive synthetic data
def generate_next_year_data_aggressive(df_previous_year, year):
    df_next = df_previous_year.copy()
    df_next['YEAR'] = year
    # Increase prevalence counts by 5% to 15%
    df_next['prev_cnt'] = (df_next['prev_cnt'] * (1 + np.random.uniform(0.05, 0.15, size=len(df_next)))).round().astype(int)
    # Adjust mortality counts by -10% to +10%
    df_next['mort_cnt'] = (df_next['mort_cnt'] * (1 + np.random.uniform(-0.10, 0.10, size=len(df_next)))).round().astype(int)
    return df_next

# Generate synthetic data for 2021 to 2024
df_all_years = [df_2020]
current_df = df_2020
for year in range(2021, 2025):
    next_year_df = generate_next_year_data_aggressive(current_df, year)
    df_all_years.append(next_year_df)
    current_df = next_year_df

# Combine all years
df_final = pd.concat(df_all_years, ignore_index=True)

# Save to new CSV
df_final.to_csv('../public/data/cleaned/circlePackingData_withSyntheticYears.csv', index=False)

print("Synthetic data created and saved as 'circlePackingData_withSyntheticYears.csv'")
