import pandas as pd

od = pd.read_csv(
    "outputs/od_matrices/od_matrix_with_counties.csv",
    low_memory=False
)

county_totals = (
    od.groupby("origin_county")["trips"]
    .sum()
    .reset_index()
    .sort_values("trips", ascending=False)
)

print(county_totals.head(20))

county_totals.to_csv(
    "outputs/od_matrices/top_origin_counties.csv",
    index=False
)
