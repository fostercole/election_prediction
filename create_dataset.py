
# df = pd.read_csv('1976-2020-president_only_dem_rep.csv')

# # Step 2: Extract the unique combinations of "year" and "state"
# unique_combinations = df[['year', 'state']].drop_duplicates().reset_index(drop=True)

# # Step 3: Create a new column combining "year" and "state"
# unique_combinations['year_state'] = unique_combinations.apply(lambda row: f"{row['year']}, {row['state']}", axis=1)

# # Filter the DataFrame to keep only rows with "party_simplified" as "DEMOCRAT" or "REPUBLICAN"
# df = df[df['party_simplified'].isin(['DEMOCRAT', 'REPUBLICAN'])]

# # Group the data by "year" and "state" to calculate the total votes for "DEMOCRAT" and "REPUBLICAN"
# grouped = df.groupby(['year', 'state', 'party_simplified'])['candidatevotes'].sum().unstack(fill_value=0)
# grouped['total_votes'] = grouped['DEMOCRAT'] + grouped['REPUBLICAN']

# # Calculate the percentage of votes for each candidate
# grouped['percent_votes_democrat'] = grouped['DEMOCRAT'] / grouped['total_votes']
# grouped['percent_votes_republican'] = grouped['REPUBLICAN'] / grouped['total_votes']

# # Reset the index to turn the grouped DataFrame back into a regular DataFrame
# grouped = grouped.reset_index()

# # Merge the election_data DataFrame with the grouped DataFrame on "year" and "state"
# merged_data = pd.merge(unique_combinations, grouped, on=['year', 'state'], how='left')

# # Rename the column 'percent_votes_democrat' to 'pct_voted_democrat'
# merged_data = merged_data.rename(columns={'percent_votes_democrat': 'proportion_democrat_president'})

# # Drop the unnecessary columns from the merge
# merged_data = merged_data.drop(columns=['DEMOCRAT', 'REPUBLICAN', 'total_votes', 'percent_votes_republican'])

# election_data = merged_data

import pandas as pd

# # Function to clean and convert numeric strings with commas to floats
# def clean_and_convert(column):
#     return column.astype(str).str.replace(',', '').astype(float)

# # Step 1: Read the CSV files into pandas DataFrames
# election_data = pd.read_csv('updated_election_data_with_cycles.csv')
# census_data = pd.read_csv('us_census.csv')

# # Step 2: Prepare the census data
# # Extract relevant columns
# census_data = census_data[['Year', 'Name', 'Resident Population', 'Percent Change in Resident Population', 'Resident Population Density', 'Resident Population Density Rank']]

# # Clean and convert numeric columns
# census_data['Resident Population'] = clean_and_convert(census_data['Resident Population'])
# census_data['Percent Change in Resident Population'] = clean_and_convert(census_data['Percent Change in Resident Population'])
# census_data['Resident Population Density'] = clean_and_convert(census_data['Resident Population Density'])
# census_data['Resident Population Density Rank'] = clean_and_convert(census_data['Resident Population Density Rank'])

# # Rename columns for clarity
# census_data.columns = ['census_year', 'state', 'resident_population', 'percent_change_resident_population', 'resident_population_density', 'resident_population_density_rank']

# # Step 3: Determine the relevant census year for each election year
# def get_previous_census_year(election_year):
#     return (election_year - 1) // 10 * 10  # Get the previous decade

# election_data['census_year'] = election_data['year'].apply(get_previous_census_year)

# # Step 4: Ensure state names are in the same format
# election_data['state'] = election_data['state'].str.upper()
# census_data['state'] = census_data['state'].str.upper()

# # Merge the census data with the election data based on state and census_year
# merged_data = pd.merge(election_data, census_data, how='left', left_on=['state', 'census_year'], right_on=['state', 'census_year'])


# Step 1: Read the CSV files into pandas DataFrames
merged_data = pd.read_csv('updated_election_data_with_cycles.csv')
president_data = pd.read_csv('1976-2020-president_only_dem_rep.csv')

# Step 2: Prepare the president data
# Extract relevant columns and ensure state names are in the same format
president_data = president_data[['year', 'state', 'party_simplified', 'candidate']]
president_data['state'] = president_data['state'].str.upper()

# Step 3: Separate the Republican and Democratic candidates
republican_candidates = president_data[president_data['party_simplified'] == 'REPUBLICAN'][['year', 'state', 'candidate']]
democratic_candidates = president_data[president_data['party_simplified'] == 'DEMOCRAT'][['year', 'state', 'candidate']]

# Rename columns for clarity
republican_candidates = republican_candidates.rename(columns={'candidate': 'republican_candidate'})
democratic_candidates = democratic_candidates.rename(columns={'candidate': 'democratic_candidate'})

# Step 4: Merge the candidates with the merged data
merged_data = pd.merge(merged_data, republican_candidates, how='left', on=['year', 'state'])
merged_data = pd.merge(merged_data, democratic_candidates, how='left', on=['year', 'state'])

# # Step 5: Save the resulting DataFrame to a new CSV file
# merged_data.to_csv('updated_election_data_with_cycles.csv', index=False)

# print("The file 'final_election_data_with_candidates.csv' has been saved.")

#COMBINES POLLING DATASETS
file_path1 = 'presidential_poll_averages_2020.csv'
df1 = pd.read_csv(file_path1)

# Load the second CSV file into a DataFrame
file_path2 = 'pres_pollaverages_1968-2016.csv'
df2 = pd.read_csv(file_path2)

# Combine the two DataFrames
combined_df = pd.concat([df1, df2])

# Save the combined DataFrame to a new CSV file
output_file_path = 'all_poll_averages.csv'
combined_df.to_csv(output_file_path, index=False)

# ONLY KEEP POLL CLOSEST TO ELECTION DATE, GET RID OF NAMES
# WITH CONVENTIONS

file_path = 'all_poll_averages.csv'
df = pd.read_csv(file_path)
df['modeldate'] = pd.to_datetime(df['modeldate'])
df = df[~df['candidate_name'].str.contains("convention", case=False, na=False)]
df = df.sort_values(by=['cycle', 'state', 'candidate_name', 'modeldate'])
latest_polls_df = df.groupby(['cycle', 'state', 'candidate_name']).tail(1)
output_file_path = 'latest_polls.csv'
latest_polls_df.to_csv(output_file_path, index=False)

# BRING DATA FROM LATEST POLLS INTO FULL DATASET

# NORMALIZE LATEST POLLS DATASET
election_data_path = 'updated_election_data_with_cycles.csv'
latest_polls_path = 'latest_polls.csv'

polls_df = pd.read_csv(latest_polls_path)

suffixes = {"Jr", "Jr.", "Sr", "Sr.", "II", "III", "IV", "V"}

# Function to extract first and last names only, ignoring suffixes
def extract_first_last(name):
    if pd.isna(name):
        return ""
    # Remove commas and split by spaces
    parts = name.replace(",", "").split()
    # Filter out suffixes
    parts = [part for part in parts if part not in suffixes]
    if len(parts) >= 2:
        first_name = parts[0]  # The first name part
        last_name = parts[-1]  # The last name part
        return f"{first_name} {last_name}".upper()
    return name.upper()

# Normalize the candidate names in the DataFrame
polls_df['candidate_name_normalized'] = polls_df['candidate_name'].apply(extract_first_last)

# Save the normalized DataFrame to a new CSV file
polls_output_path = 'latest_polls_normalized.csv'
polls_df.to_csv(polls_output_path, index=False)

# NORMALIZE UPDATED ELECTION DATASET

# Load the updated election data CSV file into a DataFrame
election_data_path = 'updated_election_data_with_cycles.csv'
election_df = pd.read_csv(election_data_path)

# List of common suffixes to ignore
suffixes = {"Jr", "Jr.", "Sr", "Sr.", "II", "III", "IV", "V"}

# Function to extract first and last names only, ignoring suffixes
def extract_first_last_election(name):
    if pd.isna(name):
        return ""
    # Remove commas and split by spaces
    parts = name.replace(",", "").split()
    # Move last name to the end
    parts = parts[1:] + [parts[0]]
    # Filter out suffixes
    parts = [part for part in parts if part not in suffixes]
    if len(parts) >= 2:
        first_name = parts[0]  # The first name part
        last_name = parts[-1]  # The last name part
        return f"{first_name} {last_name}".upper()
    return name.upper()

# Normalize the candidate names in the DataFrame
election_df['democratic_candidate_normalized'] = election_df['democratic_candidate'].apply(extract_first_last_election)
election_df['republican_candidate_normalized'] = election_df['republican_candidate'].apply(extract_first_last_election)

# Save the normalized DataFrame to a new CSV file
election_output_path = 'normalized_election_data.csv'
election_df.to_csv(election_output_path, index=False)

# ADD POLLING DATA TO MAIN DATASET

# Load the normalized CSV files into DataFrames
election_data_path = 'normalized_election_data.csv'
latest_polls_path = 'latest_polls_normalized.csv'

election_df = pd.read_csv(election_data_path)
polls_df = pd.read_csv(latest_polls_path)

# Convert state names in the polls_df to uppercase to match the format in election_df
polls_df['state'] = polls_df['state'].str.upper()

# Merge the DataFrames based on 'year'/'cycle', 'state', and normalized candidate names for Democrats
merged_df = pd.merge(
    election_df, 
    polls_df[['cycle', 'state', 'candidate_name_normalized', 'pct_estimate']], 
    left_on=['year', 'state', 'democratic_candidate_normalized'], 
    right_on=['cycle', 'state', 'candidate_name_normalized'], 
    how='left'
)

# Rename the 'pct_estimate' column to 'pct_dem_in_polls'
merged_df.rename(columns={'pct_estimate': 'pct_dem_in_polls'}, inplace=True)

# Drop unnecessary columns from the merge
merged_df.drop(columns=['cycle', 'candidate_name_normalized'], inplace=True)


# Step 2: Drop rows where the 'pct_dem_in_polls' column has NaN values
df = merged_df.dropna(subset=['pct_dem_in_polls'])

# Step 3: Convert the "Name" column values to uppercase
if 'Name' in df.columns:
    df['Name'] = df['Name'].str.upper()

# Step 4: Save the updated DataFrame back to a CSV file
df.to_csv('election_data_with_polls.csv', index=False)


import pandas as pd

# Load the CSV file
# import pandas as pd

# Load the CSV file

# Save the updated DataFrame to a new CSV file
# output_file_path = 'NEW.csv'  # Replace with the desired output file path
# df.to_csv(output_file_path, index=False)

df['pct_dem_in_polls'] = df['pct_dem_in_polls'] / 100
# Create the new columns and initialize them with the current pct_dem_in_polls
df['dem_prop_4_years_prior'] = df['pct_dem_in_polls']
df['dem_prop_8_years_prior'] = df['pct_dem_in_polls']
df['dem_prop_12_years_prior'] = df['pct_dem_in_polls']

# Function to get the prior year data
def get_prior_year_data(row, years_prior):
    prior_year = row['year'] - years_prior
    prior_data = df[(df['state'] == row['state']) & (df['year'] == prior_year)]
    if not prior_data.empty:
        return prior_data['proportion_democrat_president'].values[0]
    return row['pct_dem_in_polls']

# Apply the function to create the new columns
df['dem_prop_4_years_prior'] = df.apply(lambda row: get_prior_year_data(row, 4), axis=1)
df['dem_prop_8_years_prior'] = df.apply(lambda row: get_prior_year_data(row, 8), axis=1)
df['dem_prop_12_years_prior'] = df.apply(lambda row: get_prior_year_data(row, 12), axis=1)

# Save the updated DataFrame to a new CSV file
output_file_path = 'election_data_with_polls.csv'  # Replace with the desired output file path
df.to_csv(output_file_path, index=False)



file_path = 'election_data_with_polls.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Define the columns to be deleted
columns_to_delete = ['last_cycle_1', 'last_cycle_2', 'last_cycle_3']

# Drop the specified columns
df.drop(columns=columns_to_delete, inplace=True)

# Save the updated DataFrame to a new CSV file
output_file_path = 'election_data_with_polls.csv'  # Replace with the desired output file path
df.to_csv(output_file_path, index=False)

# Drop the 'year_state' column
df.drop(columns=['year_state'], inplace=True)

# Save the updated DataFrame to a new CSV file
output_file_path = 'MAIN.csv'  # Replace with the desired output file path
df.to_csv(output_file_path, index=False)