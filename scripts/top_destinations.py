import pandas as pd

od = pd.read_csv(
    "outputs/od_matrices/od_matrix_with_counties.csv",
    low_memory=False
)

destinations = (
    od.groupby("destination_name")["trips"]
    .sum()
    .reset_index()
    .sort_values("trips", ascending=False)
)

print("\nTop Destinations\n")
print(destinations.head(50))

destinations.to_csv(
    "outputs/od_matrices/top_destinations.csv",
    index=False
)

print("\nSaved: outputs/od_matrices/top_destinations.csv")
