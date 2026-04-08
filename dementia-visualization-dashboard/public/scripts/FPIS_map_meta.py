import requests
import csv

# URL for counties data
counties_url = "https://cdn.jsdelivr.net/npm/us-atlas@3/counties-albers-10m.json"

# URL for FIPS state codes to state names mapping
state_fips_url = "https://raw.githubusercontent.com/kjhealy/fips-codes/master/state_fips_master.csv"

# Fetch counties data
response = requests.get(counties_url)
counties_data = response.json()

# Fetch state FIPS mapping
state_response = requests.get(state_fips_url)
state_fips_mapping = {}
state_abbr_fips_mapping = {}
for line in state_response.text.splitlines()[1:]:  # Skip header
    parts = line.split(",")
    fips_state = parts[3].zfill(2)  # Ensure FIPS_STATE is two digits
    state_name = parts[0]  # Use the state_name column
    state_abbr = parts[1]  # Use the state_abbr column
    state_fips_mapping[fips_state] = state_name
    state_abbr_fips_mapping[fips_state] = state_abbr
    

# Prepare CSV output
output_file = "public/data/cleaned/fips_states_counties_codebook.csv"
with open(output_file, mode="w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["STATE_ABBR","STATE", "COUNTY_NAME", "FIPS_STATE", "FIPS_COUNTY", "FIPS_CODE"])

    # Extract counties and write to CSV
    for county in counties_data["objects"]["counties"]["geometries"]:
        fips_code = county["id"]
        fips_state = fips_code[:2]  # Extract first two digits for FIPS_STATE
        fips_county = fips_code[2:]  # Extract last three digits for FIPS_COUNTY
        county_name = county["properties"]["name"]
        state_name = state_fips_mapping.get(fips_state, "Unknown")  # Match FIPS_STATE to state name
        state_abbr = state_abbr_fips_mapping.get(fips_state, "Unknown")

        writer.writerow([state_abbr, state_name, county_name, fips_state, fips_county, fips_code])

print(f"CSV file '{output_file}' has been created.")