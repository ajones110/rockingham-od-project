import pandas as pd

od = pd.read_csv(
    "outputs/od_matrices/od_matrix_with_counties.csv",
    low_memory=False
)

county_flows = (
    od.groupby(
        [
            "origin_county",
            "destination_name"
        ]
    )["trips"]
    .sum()
    .reset_index()
)

county_flows = county_flows.sort_values(
    "trips",
    ascending=False
)

print("\nTop County-Destination Flows\n")
print(county_flows.head(25))

county_flows.to_csv(
    "outputs/od_matrices/county_destination_flows.csv",
    index=False
)

print(
    "\nSaved: outputs/od_matrices/county_destination_flows.csv"
)
