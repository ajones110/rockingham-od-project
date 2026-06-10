import geopandas as gpd
import pandas as pd

# Load OD matrix
od = pd.read_csv(
    "outputs/rockingham_od_population_weighted.csv"
)

# Force IDs to strings
od["origin"] = od["origin"].astype(str)
od["destination"] = od["destination"].astype(str)

# Load place enrichment
places = gpd.read_file(
    "data/cbg_place_enriched.geojson"
)

# Force GEOID to string
places["GEOID"] = places["GEOID"].astype(str)

# Keep only needed columns
places = places[["GEOID", "place_name"]]

# Origin lookup
origin_lookup = places.rename(
    columns={
        "GEOID": "origin",
        "place_name": "origin_place"
    }
)

# Destination lookup
dest_lookup = places.rename(
    columns={
        "GEOID": "destination",
        "place_name": "destination_place"
    }
)

# Join origin names
od = od.merge(
    origin_lookup,
    on="origin",
    how="left"
)

# Join destination names
od = od.merge(
    dest_lookup,
    on="destination",
    how="left"
)

# Remove helper column
if "dest_index" in od.columns:
    od = od.drop(columns=["dest_index"])

# Save
od.to_csv(
    "outputs/rockingham_od_named.csv",
    index=False
)

print(od.head())
print("Saved named OD matrix")
