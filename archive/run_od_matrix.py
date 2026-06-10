import geopandas as gpd
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import haversine_distances

# =========================================================
# 1. LOAD RAW BLOCK GROUPS (IMPORTANT: use raw shapefile)
# =========================================================
bg = gpd.read_file(
    "data/shapefiles/places/data/shapefiles/block_groups/tl_2025_37_bg.shp"
)

print("Total NC CBGs:", len(bg))

# =========================================================
# 2. FILTER TO ROCKINGHAM COUNTY FIRST (CRITICAL FIX)
# =========================================================
bg = bg[bg["COUNTYFP"] == "157"].copy()

print("Rockingham CBGs:", len(bg))

# =========================================================
# 3. PROJECT FOR SPATIAL OPERATIONS
# =========================================================
bg = bg.to_crs(3857)

# =========================================================
# 4. CREATE CENTROIDS
# =========================================================
bg["centroid"] = bg.geometry.centroid

# Convert to lat/lon for distance calculation
bg_ll = bg.to_crs(4326)
coords = np.array([(p.x, p.y) for p in bg_ll["centroid"]])
coords_rad = np.radians(coords)

# =========================================================
# 5. DISTANCE MATRIX (HAVERSINE)
# =========================================================
dist_matrix = haversine_distances(coords_rad) * 6371  # km

# =========================================================
# 6. GRAVITY MODEL (BASELINE OD)
# =========================================================
n = len(bg)

# Placeholder "mass" (upgrade later with population)
P = np.ones(n)

beta = 1.5
eps = 0.1

OD = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        if i != j:
            OD[i, j] = (P[i] * P[j]) / ((dist_matrix[i, j] + eps) ** beta)

# Normalize to realistic total trips
OD = OD / OD.sum() * 10000

# =========================================================
# 7. BUILD OD TABLE
# =========================================================
geoids = bg["GEOID"].values

od_df = pd.DataFrame(OD)
od_df["origin"] = geoids

od_df = od_df.melt(
    id_vars="origin",
    var_name="dest_index",
    value_name="trips"
)

od_df["destination"] = od_df["dest_index"].astype(int).map(lambda x: geoids[x])

od_df = od_df[["origin", "destination", "trips"]]
od_df = od_df[od_df["origin"] != od_df["destination"]]

# =========================================================
# 8. SAVE OUTPUT
# =========================================================
od_df.to_csv("outputs/rockingham_od_matrix.csv", index=False)

print("DONE — OD matrix created")
print("Rows:", len(od_df))
