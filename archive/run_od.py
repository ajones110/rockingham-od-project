import geopandas as gpd
import pandas as pd
import numpy as np

bg = gpd.read_file("data/cbg_place_enriched.geojson")

print(len(bg))
print(bg.head())
