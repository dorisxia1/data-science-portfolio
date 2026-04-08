# Pre-processing scripts documentation

This folder contains Python scripts used for data processing, cleaning, and analysis in the project. Below is a description of each script and its functionality.

---

## `synthetic_medicare_data_builder.py`
**Purpose**:  
Generates synthetic Medicare data for multiple years (2021-2024) based on the 2020 dataset. The script applies random adjustments to prevalence and mortality counts to simulate future data.

**Key Outputs**:  
- `circlePackingData_withSyntheticYears.csv`: A CSV file containing the original and synthetic data for 2020-2024.

---

## `preprocess_environmental_data.py`
**Purpose**:  
Processes and merges various environmental and health-related datasets, including dementia data, air quality data, weather data, and CDC health measures. The script calculates rates, reshapes data, and combines them into a unified dataset.

**Key Outputs**:  
- `EnvironmentalViewData.csv`: A cleaned and combined dataset in long format for visualization and analysis.

---

## `FPIS_map_meta.py`
**Purpose**:  
Generates a mapping of FIPS codes to state and county names using external data sources. This mapping is essential for linking datasets by geographic identifiers.

**Key Outputs**:  
- `fips_states_counties_codebook.csv`: A CSV file containing FIPS codes, state abbreviations, state names, and county names.

---

## `dementia_mismatch_index.py`
**Purpose**:  
Calculates a mismatch index for dementia prevalence by comparing observed prevalence rates with expected rates predicted using a linear regression model. The model uses stroke, diabetes, and cognitive disability rates as predictors.

**Key Outputs**:  
- `dementia_mismatch_index.csv`: A CSV file containing the mismatch index and related metrics for each county.

---

## `data_cleaning.ipynb`
**Purpose**:  
A Jupyter Notebook for cleaning and preparing raw data for analysis. It includes steps for filtering, reshaping, and exporting cleaned datasets.

**Key Outputs**:  
- `circlePackingData.csv`: A cleaned dataset for visualization.
- `fips_states_codebook.csv`: A simplified FIPS codebook.

---

### Notes
- Ensure all required input files are present in the appropriate directories before running the scripts.
- Outputs are saved in the `public/data/cleaned` directory unless specified otherwise.
- For additional details, refer to the comments within each script.