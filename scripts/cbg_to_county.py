import pandas as pd

# Load OD matrix
od = pd.read_csv("outputs/od_matrices/od_matrix.csv")

# Read county gazetteer
counties = pd.read_csv(
    "data/crosswalks/2025_Gaz_counties_national.txt",
    sep="|",
    dtype={"GEOID": str}
)

# Keep only needed fields
counties = counties[["GEOID", "NAME", "USPS"]]

# Extract county FIPS from 12-digit CBG
od["origin"] = od["origin"].astype(str)
od["origin_county_fips"] = od["origin"].str[:5]

# Join county names
od = od.merge(
    counties,
    left_on="origin_county_fips",
    right_on="GEOID",
    how="left"
)

od.rename(
    columns={
        "NAME": "origin_county",
        "USPS": "origin_state"
    },
    inplace=True
)

print("\nCounty lookup complete.\n")
print(
    od[
        [
            "origin",
            "origin_county_fips",
            "origin_county",
            "origin_state"
        ]
    ].head()
)

od.to_csv(
    "outputs/od_matrices/od_matrix_with_counties.csv",
    index=False
)

print(
    "\nSaved: outputs/od_matrices/od_matrix_with_counties.csv"
)
