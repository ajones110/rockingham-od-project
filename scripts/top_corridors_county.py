import pandas as pd

od = pd.read_csv(
    "outputs/od_matrices/od_matrix_with_counties.csv",
    low_memory=False
)

corridors = (
    od.groupby(
        [
            "origin_county",
            "destination_name"
        ]
    )["trips"]
    .sum()
    .reset_index()
)

corridors = corridors.sort_values(
    "trips",
    ascending=False
)

print("\nTop County → Destination Corridors\n")
print(corridors.head(50))

corridors.to_csv(
    "outputs/od_matrices/top_county_destination_corridors.csv",
    index=False
)

print(
    "\nSaved: outputs/od_matrices/top_county_destination_corridors.csv"
)
