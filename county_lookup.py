import pandas as pd

# Load top corridors
corridors = pd.read_csv(
    "outputs/od_matrices/top_corridors.csv"
)

# Convert origin to string
corridors["origin"] = corridors["origin"].astype(str)

# County FIPS extraction
corridors["county_fips"] = corridors["origin"].str[:5]

county_lookup = {
    "37157": "Rockingham County",
    "37081": "Guilford County",
    "37067": "Forsyth County",
    "37119": "Mecklenburg County",
    "37183": "Wake County",
    "37129": "New Hanover County",
    "37063": "Durham County",
    "37135": "Orange County",
    "37051": "Cumberland County",
    "37099": "Jackson County"
}

corridors["origin_county"] = (
    corridors["county_fips"]
    .map(county_lookup)
    .fillna("Other County")
)

print(corridors[
    ["origin_county", "destination", "trips"]
].head(20))

corridors.to_csv(
    "outputs/od_matrices/top_corridors_counties.csv",
    index=False
)

print("\nSaved: outputs/od_matrices/top_corridors_counties.csv")


