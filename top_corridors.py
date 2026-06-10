import pandas as pd

# Load place OD matrix
od = pd.read_csv(
    "outputs/rockingham_place_od.csv"
)

# Remove internal trips
od = od[
    od["origin_place"] != od["destination_place"]
]

# Create undirected corridor names
od["corridor"] = od.apply(
    lambda row: " <-> ".join(
        sorted([
            row["origin_place"],
            row["destination_place"]
        ])
    ),
    axis=1
)

# Aggregate both directions
corridors = (
    od.groupby("corridor", as_index=False)
      .agg({"trips": "sum"})
      .sort_values(
          "trips",
          ascending=False
      )
)

print("\nTOP CORRIDORS\n")
print(corridors.head(20))

corridors.to_csv(
    "outputs/top_10_corridors.csv",
    index=False
)

print(
    "\nSaved outputs/top_10_corridors.csv"
)
