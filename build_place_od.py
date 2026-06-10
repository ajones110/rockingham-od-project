import pandas as pd
import geopandas as gpd

# ------------------------------------
# Load OD matrix
# ------------------------------------

od = pd.read_csv(
    "outputs/rockingham_od_population_weighted.csv"
)

# Make GEOIDs strings
od["origin"] = od["origin"].astype(str)
od["destination"] = od["destination"].astype(str)

# ------------------------------------
# Load place lookup
# ------------------------------------

places = gpd.read_file(
    "outputs/rockingham_cbg_places.geojson"
)

places["GEOID"] = places["GEOID"].astype(str)

# Origin lookup
origin_lookup = dict(
    zip(
        places["GEOID"],
        places["place_name"]
    )
)

# Destination lookup
destination_lookup = origin_lookup

# ------------------------------------
# Add place names
# ------------------------------------

od["origin_place"] = od["origin"].map(origin_lookup)

od["destination_place"] = od["destination"].map(
    destination_lookup
)

# ------------------------------------
# Aggregate
# ------------------------------------

place_od = (
    od.groupby(
        ["origin_place", "destination_place"],
        as_index=False
    )["trips"]
    .sum()
)

place_od = place_od.sort_values(
    "trips",
    ascending=False
)

# ------------------------------------
# Save
# ------------------------------------

place_od.to_csv(
    "outputs/rockingham_place_od.csv",
    index=False
)

print(place_od.head(20))
print("\nSaved outputs/rockingham_place_od.csv")
