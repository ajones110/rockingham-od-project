import pandas as pd
import geopandas as gpd

print("\n--- LOADING DATA ---")

# --------------------------------------------------
# 1. Load CBG-level OD
# --------------------------------------------------
od = pd.read_csv("rockingham_cbg_od.csv")

od["home_cbg"] = od["home_cbg"].astype(str)
od["poi_cbg"] = od["poi_cbg"].astype(str)

print("OD shape:", od.shape)


# --------------------------------------------------
# 2. Load CBG → Place GIS mapping
# --------------------------------------------------
cbg_place = gpd.read_file("data/cbg_place_enriched.geojson")

print("\nCBG PLACE COLUMNS:")
print(cbg_place.columns)

# --------------------------------------------------
# 3. Identify join column safely
# --------------------------------------------------
# Try common names automatically
possible_keys = ["GEOID", "geoid", "cbg", "CBG", "census_block_group"]

join_key = None
for k in possible_keys:
    if k in cbg_place.columns:
        join_key = k
        break

if join_key is None:
    raise ValueError("No valid CBG ID column found in cbg_place_enriched.geojson")

print("\nUsing join key:", join_key)

cbg_place[join_key] = cbg_place[join_key].astype(str)


# --------------------------------------------------
# 4. Identify place column
# --------------------------------------------------
possible_place_cols = ["place_name", "NAME", "name", "town", "city"]

place_col = None
for c in possible_place_cols:
    if c in cbg_place.columns:
        place_col = c
        break

if place_col is None:
    raise ValueError("No place name column found in cbg_place_enriched.geojson")

print("Using place column:", place_col)


# --------------------------------------------------
# 5. Merge HOME side
# --------------------------------------------------
od = od.merge(
    cbg_place[[join_key, place_col]],
    left_on="home_cbg",
    right_on=join_key,
    how="left"
).rename(columns={place_col: "home_place"}).drop(columns=[join_key])


# --------------------------------------------------
# 6. Merge POI side
# --------------------------------------------------
od = od.merge(
    cbg_place[[join_key, place_col]],
    left_on="poi_cbg",
    right_on=join_key,
    how="left"
).rename(columns={place_col: "poi_place"}).drop(columns=[join_key])


print("\n--- AFTER JOIN ---")
print(od.head())


# --------------------------------------------------
# 7. Drop missing mappings (important clean step)
# --------------------------------------------------
od = od.dropna(subset=["home_place", "poi_place"])


# --------------------------------------------------
# 8. Aggregate to place-level OD
# --------------------------------------------------
place_od = (
    od.groupby(["home_place", "poi_place"])["visits"]
    .sum()
    .reset_index()
    .sort_values("visits", ascending=False)
)

print("\n--- TOP PLACE FLOWS ---")
print(place_od.head(15))


# --------------------------------------------------
# 9. Save outputs
# --------------------------------------------------
place_od.to_csv("rockingham_place_od_gis.csv", index=False)
print("\n✔ Saved: rockingham_place_od_gis.csv")


# Optional: matrix form (useful for heatmaps)
matrix = place_od.pivot(
    index="home_place",
    columns="poi_place",
    values="visits"
).fillna(0)

matrix.to_csv("rockingham_place_od_matrix.csv")
print("✔ Saved: rockingham_place_od_matrix.csv")


print("\n--- DONE ---")
