import pandas as pd

# Load the CSV file
dementia_file = 'public/data/raw/NORC_Dementia_DataHub_County_2020.csv'
dementa_df_raw = pd.read_csv(dementia_file)

# Subset the data based on the conditions
dementia_df_clean = dementa_df_raw[
    dementa_df_raw['INSURANCE'].isna() &  # Insurance is missing (all insurance categories)
    dementa_df_raw['FIPS_COUNTY'].notna() &  # FIPS_COUNTY is not missing
    dementa_df_raw['DEMENTIACAT'].isna() &  # DEMENTIACAT is missing (all dementia categories)
    dementa_df_raw.loc[:, 'AGECAT2':'SEXCAT'].isna().all(axis=1)  # AGECAT2 thru SEXCAT are missing (excludes demographic subsets)
]
# Drop the 'Insurance' column and columns from 'AGECAT2' to 'SEXCAT'
dementia_df_clean = dementia_df_clean.drop(columns=['INSURANCE', 'DEMENTIACAT', 'atc'] + list(dementia_df_clean.loc[:, 'AGECAT2':'SEXCAT'].columns))

# Ensure FIPS_STATE is length 2 and FIPS_COUNTY is length 3 with leading zeros
dementia_df_clean['FIPS_STATE'] = dementia_df_clean['FIPS_STATE'].apply(lambda x: f"{int(x):02d}")
dementia_df_clean['FIPS_COUNTY'] = dementia_df_clean['FIPS_COUNTY'].apply(lambda x: f"{int(x):03d}")

# Load the US FIPS County Codes data
fips_file = 'public/data/cleaned/fips_states_counties_codebook.csv'
fips_df = pd.read_csv(fips_file)
fips_df['FIPS_STATE'] = fips_df['FIPS_STATE'].apply(lambda x: f"{int(x):02d}")
fips_df['FIPS_COUNTY'] = fips_df['FIPS_COUNTY'].apply(lambda x: f"{int(x):03d}")
fips_df['FIPS_CODE'] = fips_df['FIPS_CODE'].apply(lambda x: f"{int(x):05d}")

# Merge the dementia data with the FIPS County Codes data (inner join to only keep mappable rows)
dementia_df_merged = pd.merge(
    fips_df,
    dementia_df_clean,
    how='inner',
    left_on=['FIPS_STATE', 'FIPS_COUNTY'],
    right_on=['FIPS_STATE', 'FIPS_COUNTY']
)

# Calculate rates
dementia_df_merged['prev_rate'] = dementia_df_merged['prev_cnt'] / dementia_df_merged['bene_cnt'] * 100
dementia_df_merged['inc_rate'] = dementia_df_merged['inc_cnt'] / dementia_df_merged['bene_cnt'] * 100
dementia_df_merged['mort_rate'] = dementia_df_merged['mort_cnt'] / dementia_df_merged['prev_cnt'] * 100

# Remove records where division by zero or missing values occur
dementia_df_merged = dementia_df_merged.replace([float('inf'), -float('inf')], float('nan'))
dementia_df_merged = dementia_df_merged.dropna()

# Sort the merged data by FIPS_CODE
dementia_df_merged = dementia_df_merged.sort_values(by='FIPS_CODE')

# Reshape the dataset to long format
columns_to_keep = ['STATE_ABBR', 'STATE', 'COUNTY_NAME', 'FIPS_STATE', 'FIPS_COUNTY', 'FIPS_CODE', 'prev_rate', 'inc_rate', 'mort_rate']
dementia_df_merged = dementia_df_merged[columns_to_keep]
dementia_df_merged['Category'] = "Dementia"
dementia_df_merged = pd.melt(
    dementia_df_merged,
    id_vars=['STATE_ABBR','STATE', 'COUNTY_NAME', 'FIPS_STATE', 'FIPS_COUNTY', 'FIPS_CODE','Category'],
    value_vars=['prev_rate', 'inc_rate', 'mort_rate'],
    var_name='Measure',
    value_name='Value'
)

# Map the Measure field to descriptive names
measure_mapping = {
    'prev_rate': 'Prevalence rate',
    'inc_rate': 'Incidence rate',
    'mort_rate': 'Mortality rate'
}
dementia_df_merged['Measure'] = dementia_df_merged['Measure'].map(measure_mapping)

################
### AQI DATA ###
################

# Load the AQI data
aqi_data = pd.read_csv("./public/data/raw/annual_aqi_by_county_2020.csv")

# Remove trailing whitespace from the County column in AQI data
aqi_data["County"] = aqi_data["County"].str.strip()

# Manual changes to the AQI data
aqi_data = aqi_data[~aqi_data["State"].isin(["Country Of Mexico", "Puerto Rico", "Virgin Islands"])]
aqi_data["State"] = aqi_data["State"].replace("District Of Columbia", "District of Columbia")
aqi_data.loc[(aqi_data["State"] == "Illinois") & (aqi_data["County"] == "Saint Clair"),"County"] = "St. Clair"
aqi_data.loc[(aqi_data["State"] == "Virginia") & (aqi_data["County"] == "Charles"),"County"] = "Charles City"
aqi_data["County"] = aqi_data["County"].replace({
    "Baltimore (City)": "Baltimore",
    "Saint Louis": "St. Louis",
    "Saint Charles": "St. Charles",
    "Sainte Genevieve": "Ste. Genevieve",
    "St. Louis City": "St. Louis",
    "Dona Ana": "Doña Ana",
    "Bristol City": "Bristol",
    "Hampton City": "Hampton",
    "Hopewell City": "Hopewell",
    "Lynchburg City": "Lynchburg",
    "Norfolk City": "Norfolk",
    "Richmond City": "Richmond",
    "Salem City": "Salem",
    "Suffolk City": "Suffolk",
    "Virginia Beach City": "Virginia Beach",
    "Winchester City": "Winchester"
})

# Merge the datasets on State and County
aqi_df_merged = pd.merge(
    fips_df,
    aqi_data,
    right_on=["State", "County"],
    left_on=["STATE", "COUNTY_NAME"],
    how="inner"
)

# Calculate "Rate of detectable <pollutant>"
pollutants = ["Ozone", "PM2.5"]
for pollutant in pollutants:
    aqi_df_merged[f"Rate of detectable {pollutant}"] = aqi_df_merged[f"Days {pollutant}"] / aqi_df_merged["Days with AQI"]  * 100

# Reshape the dataset to long format
columns_to_keep = ['STATE_ABBR', 'STATE', 'COUNTY_NAME', 'FIPS_STATE', 'FIPS_COUNTY', 'FIPS_CODE', 
                   'Median AQI', 
                   'Rate of detectable Ozone','Rate of detectable PM2.5']
aqi_df_merged = aqi_df_merged[columns_to_keep]
aqi_df_merged['Category'] = "Physical Environment Risk Factors"
aqi_df_merged = pd.melt(
    aqi_df_merged,
    id_vars=['STATE_ABBR', 'STATE', 'COUNTY_NAME', 'FIPS_STATE', 'FIPS_COUNTY', 'FIPS_CODE','Category'],
    value_vars=['Median AQI', 'Rate of detectable Ozone', 'Rate of detectable PM2.5'],
    var_name='Measure',
    value_name='Value'
)
# Map the Measure field to descriptive names
measure_mapping = {
    'Median AQI': "Median air quality index (AQI) score",
    'Rate of detectable Ozone': '% of days with detectable Ozone',
    'Rate of detectable PM2.5': '% of days with detectable PM2.5'
}
aqi_df_merged['Measure'] = aqi_df_merged['Measure'].map(measure_mapping)

# Combine dementia_df_merged and aqi_df_merged into a single DataFrame
combined_df = pd.concat([dementia_df_merged, aqi_df_merged], ignore_index=True)


####################
### Weather Data ###
####################
# Load temperature data
temperature_data = pd.read_csv("./public/data/raw/US_County_Temperatures.csv")
temperature_data = pd.melt(
    temperature_data,
    id_vars=['ID'],
    value_vars=['2020 Mean','1901-2000 Mean'],
    var_name='Measure',
    value_name='Value'
)
measure_mapping = {
    '2020 Mean': 'Annual mean temperature (°F in 2020)', 
    '1901-2000 Mean': 'Historical mean temperature (°F in 1901-2000)'
}
temperature_data['Measure'] = temperature_data['Measure'].map(measure_mapping)
# Lead precipitation data
precipitation_data = pd.read_csv("./public/data/raw/US_County_Precipitation.csv")
precipitation_data = pd.melt(
    precipitation_data,
    id_vars=['ID'],
    value_vars=['2020 Mean','1901-2000 Mean'],
    var_name='Measure',
    value_name='Value'
)
measure_mapping = {
    '2020 Mean': 'Annual mean precipitation (inches in 2020)', 
    '1901-2000 Mean': 'Historical mean precipitation (inches in 1901-2000)'
}
precipitation_data['Measure'] = precipitation_data['Measure'].map(measure_mapping)
weather_df = pd.concat([temperature_data, precipitation_data], ignore_index=True)

# Extract STATE_ABBR and FIPS_COUNTY from the ID column
weather_df['STATE_ABBR'] = weather_df['ID'].str[:2]
weather_df['FIPS_COUNTY'] = weather_df['ID'].str[-3:]

# Merge the datasets on State and County
weather_df_merged = pd.merge(
    fips_df,
    weather_df,
    right_on=["STATE_ABBR", "FIPS_COUNTY"],
    left_on=["STATE_ABBR", "FIPS_COUNTY"],
    how="inner"
)
weather_df_merged = weather_df_merged.drop(columns=['ID'])
weather_df_merged['Category'] = "Physical Environment Risk Factors"


combined_df = pd.concat([combined_df, weather_df_merged], ignore_index=True)





################
### CDC DATA ###
################

# Load the CDC data
cdc_data = pd.read_csv("./public/data/raw/PLACES__Local_Data_for_Better_Health__County_Data_2024_release_20250307.csv", low_memory=False)
columns_to_keep = ['LocationID', 'Measure', 'Data_Value', 'Data_Value_Type']
cdc_data = cdc_data[columns_to_keep]
# subset to Data_Value_Type = 'Age-adjusted prevalence'
cdc_data = cdc_data[cdc_data['Data_Value_Type'] == 'Age-adjusted prevalence']
# subset measures
measures_to_keep = ['No leisure-time physical activity among adults',
                    'Short sleep duration among adults',
                    'Lack of reliable transportation in the past 12 months among adults',
                    'Food insecurity in the past 12 months among adults',
                    'Housing insecurity in the past 12 months among adults',
                    'Utility services shut-off threat in the past 12 months among adults',
                    'Lack of social and emotional support among adults',
                    'Feeling socially isolated among adults']
cdc_data = cdc_data[cdc_data['Measure'].isin(measures_to_keep)]
measure_mapping = {
    'No leisure-time physical activity among adults': 'Physical inactivity (prevalence %)',
                    'Short sleep duration among adults': 'Sleep deprivation (prevalence %)',
                    'Lack of reliable transportation in the past 12 months among adults': 'Limited transportation access (prevalence %)',
                    'Food insecurity in the past 12 months among adults': 'Food insecurity (prevalence %)',
                    'Housing insecurity in the past 12 months among adults': 'Housing insecurity (prevalence %)',
                    'Utility services shut-off threat in the past 12 months among adults': 'Utility insecurity (prevalence %)',
                    'Lack of social and emotional support among adults': 'Social support insecurity (prevalence %)',
                    'Feeling socially isolated among adults': 'Social isolation (prevalence %)'
}
cdc_data['Measure'] = cdc_data['Measure'].map(measure_mapping)
# Category
cdc_data['Category'] = 'Social Environment Risk Factors'
cdc_data.loc[cdc_data['Measure'].isin(['Physical inactivity (prevalence %)', 'Sleep deprivation (prevalence %)', 'Limited transportation access (prevalence %)']), 'Category'] = 'Physical Environment Risk Factors'
# LocationID as 5 length with leading zeros
cdc_data['LocationID'] = cdc_data['LocationID'].apply(lambda x: f"{int(x):05d}")
#merge with fips
cdc_df_merged = pd.merge(
    fips_df,
    cdc_data,
    right_on=["LocationID"],
    left_on=["FIPS_CODE"],
    how="inner"
)
# drop LocationID and Data_Value_Type
cdc_df_merged = cdc_df_merged.drop(columns=['LocationID', 'Data_Value_Type'])
# rename Data_Value to Value
cdc_df_merged = cdc_df_merged.rename(columns={'Data_Value': 'Value'})

# append cdc_df_merged to combined_df
combined_df = pd.concat([combined_df, cdc_df_merged], ignore_index=True)


################
### FINALIZE ###
################

# Save the long dataset to a CSV file
combined_df.to_csv('public/data/cleaned/EnvironmentalViewData.csv', index=False)