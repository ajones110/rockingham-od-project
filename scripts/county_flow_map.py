import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# ---------------------------------------
# Load county flow data
# ---------------------------------------

flows = pd.read_csv(
    "outputs/od_matrices/top_county_destination_corridors.csv"
)

# Aggregate total trips by origin county
county_totals = (
    flows.groupby("origin_county")["trips"]
    .sum()
    .reset_index()
)

# ---------------------------------------
# Load county shapefile
# ---------------------------------------

counties = gpd.read_file(
    "data/shapefiles/counties/tl_2025_us_county.shp"
)

# Build matching county name
counties["origin_county"] = counties["NAME"] + " County"

# Keep NC only
counties = counties[counties["STATEFP"] == "37"]

# ---------------------------------------
# Join data
# ---------------------------------------

map_df = counties.merge(
    county_totals,
    on="origin_county",
    how="left"
)

map_df["trips"] = map_df["trips"].fillna(0)

# ---------------------------------------
# Plot
# ---------------------------------------

fig, ax = plt.subplots(figsize=(12, 10))

map_df.plot(
    column="trips",
    cmap="OrRd",
    linewidth=0.3,
    edgecolor="black",
    legend=True,
    ax=ax
)

ax.set_title(
    "Origins of Visits to Rockingham County Destinations",
    fontsize=16
)

ax.axis("off")

plt.tight_layout()

plt.savefig(
    "outputs/figures/county_flow_map.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nSaved:")
print("outputs/figures/county_flow_map.png")

