import geopandas as gpd
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import haversine_distances

# =====================================================
# LOAD ROCKINGHAM BLOCK GROUPS
# =====================================================
bg = gpd.read_file(
    "data/shapefiles/places/data/shapefiles/block_groups/tl_2025_37_bg.shp"
)

bg = bg[bg["COUNTYFP"] == "157"].copy()

print("Rockingham CBGs:", len(bg))

# =====================================================
# CREATE ACS JOIN KEY
# =====================================================
bg["tract"] = bg["TRACTCE"]
bg["block group"] = bg["BLKGRPCE"]

# =====================================================
# LOAD ACS DATA
# =====================================================
acs = pd.read_csv("outputs/rockingham_acs.csv")

print("ACS rows:", len(acs))

# Make types match
acs["tract"] = acs["tract"].astype(str).str.zfill(6)
acs["block group"] = acs["block group"].astype(str)

# =====================================================
# JOIN ACS TO CBGS
# =====================================================
bg = bg.merge(
    acs,
    on=["tract", "block group"],
    how="left"
)

print("Population missing:", bg["population"].isna().sum())

# =====================================================
# CLEAN DATA
# =====================================================
bg["population"] = bg["population"].fillna(1)

# Fix Census missing-income code
bg["median_income"] = bg["median_income"].replace(-666666666, np.nan)

# =====================================================
# CENTROIDS
# =====================================================
bg = bg.to_crs(3857)
bg["centroid"] = bg.geometry.centroid

centroids = gpd.GeoDataFrame(
    bg[["GEOID", "population"]],
    geometry=bg["centroid"],
    crs=3857
)

centroids_ll = centroids.to_crs(4326)

coords = np.array([
    [geom.y, geom.x]
    for geom in centroids_ll.geometry
])

coords_rad = np.radians(coords)

# =====================================================
# DISTANCE MATRIX
# =====================================================
dist_matrix = haversine_distances(coords_rad) * 6371

# =====================================================
# POPULATION-WEIGHTED GRAVITY MODEL
# =====================================================
P = bg["population"].values

beta = 1.5
eps = 0.1

OD = np.zeros((len(bg), len(bg)))

for i in range(len(bg)):
    for j in range(len(bg)):
        if i != j:
            OD[i, j] = (
                P[i] * P[j]
            ) / ((dist_matrix[i, j] + eps) ** beta)

OD = OD / OD.sum() * 10000

# =====================================================
# BUILD OD TABLE
# =====================================================
geoids = bg["GEOID"].values

od = pd.DataFrame(OD)
od["origin"] = geoids

od = od.melt(
    id_vars="origin",
    var_name="dest_index",
    value_name="trips"
)

od["destination"] = od["dest_index"].astype(int).map(
    lambda x: geoids[x]
)

od = od[od["origin"] != od["destination"]]

# =====================================================
# SAVE
# =====================================================
od.to_csv(
    "outputs/rockingham_od_population_weighted.csv",
    index=False
)

print("DONE")
print("Rows:", len(od))
