import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import matplotlib.pyplot as plt

# -----------------------------
# Load place OD
# -----------------------------

od = pd.read_csv(
    "outputs/rockingham_place_od.csv"
)

# Remove internal trips
od = od[
    od["origin_place"] != od["destination_place"]
]

# -----------------------------
# Load place polygons
# -----------------------------

places = gpd.read_file(
    "data/shapefiles/places/tl_2025_37_place.shp"
)

# Keep only places used in OD matrix
used_places = set(od["origin_place"]) | set(od["destination_place"])

places = places[
    places["NAME"].isin(used_places)
].copy()

# Project
places = places.to_crs(3857)

# Centroids
places["centroid"] = places.geometry.centroid

# Lookup
lookup = {
    row["NAME"]: row["centroid"]
    for _, row in places.iterrows()
}

# -----------------------------
# Create flow lines
# -----------------------------

lines = []

for _, row in od.iterrows():

    o = row["origin_place"]
    d = row["destination_place"]

    if o not in lookup or d not in lookup:
        continue

    line = LineString([
        lookup[o],
        lookup[d]
    ])

    lines.append({
        "origin": o,
        "destination": d,
        "trips": row["trips"],
        "geometry": line
    })

flows = gpd.GeoDataFrame(
    lines,
    crs=places.crs
)

# Keep strongest flows
flows = flows.nlargest(20, "trips")

# -----------------------------
# Plot
# -----------------------------

fig, ax = plt.subplots(
    figsize=(10,10)
)

places.boundary.plot(
    ax=ax,
    linewidth=1
)

flows.plot(
    ax=ax,
    linewidth=flows["trips"]/75,
    alpha=0.7
)

for _, row in places.iterrows():

    x = row["centroid"].x
    y = row["centroid"].y

    ax.annotate(
        row["NAME"],
        (x,y),
        fontsize=8
    )

ax.set_title(
    "Rockingham County Place-to-Place OD Flows"
)

plt.tight_layout()

plt.savefig(
    "outputs/figures/place_flow_map.png",
    dpi=300
)

print(
    "Saved outputs/figures/place_flow_map.png"
)
