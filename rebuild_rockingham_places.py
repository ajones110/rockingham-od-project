import geopandas as gpd
import pandas as pd

# Load Rockingham CBGs
bg = gpd.read_file(
    "data/shapefiles/places/data/shapefiles/block_groups/tl_2025_37_bg.shp"
)

bg = bg[bg["COUNTYFP"] == "157"].copy()

print("Rockingham CBGs:", len(bg))

# Centroids
bg = bg.to_crs(3857)
bg["geometry"] = bg.geometry.centroid

# Places
places = gpd.read_file(
    "data/shapefiles/places/tl_2025_37_place.shp"
)

places = places[["NAME", "geometry"]]
places = places.rename(columns={"NAME": "place_name"})
places = places.to_crs(bg.crs)

# FIRST: inside municipality
inside = gpd.sjoin(
    bg,
    places,
    how="left",
    predicate="within"
)

print(
    "Inside matches:",
    inside["place_name"].notna().sum()
)

# SECOND: assign nearest ONLY where missing
missing_mask = inside["place_name"].isna()

nearest = gpd.sjoin_nearest(
    inside.loc[missing_mask, ["GEOID", "geometry"]],
    places,
    how="left",
    distance_col="distance_m"
)

# Create lookup
nearest_lookup = dict(
    zip(nearest["GEOID"], nearest["place_name"])
)

# Fill missing values
inside.loc[missing_mask, "place_name"] = (
    inside.loc[missing_mask, "GEOID"]
    .map(nearest_lookup)
)

print(
    "Missing after fill:",
    inside["place_name"].isna().sum()
)

print("\nPlace counts:")
print(
    inside["place_name"].value_counts()
)

# Save
inside[
    ["GEOID", "place_name", "geometry"]
].to_file(
    "outputs/rockingham_cbg_places.geojson",
    driver="GeoJSON"
)

print(
    "\nSaved outputs/rockingham_cbg_places.geojson"
)
