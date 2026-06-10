import pandas as pd

INPUT = "march_2026_nc.parquet"
OUTPUT = "march_2026_nc_filtered.parquet"

print("Loading file...")

df = pd.read_parquet(INPUT)

print("Rows:", len(df))
print("Columns:", len(df.columns))

keep_cols = [
    "location_name",
    "poi_cbg",
    "latitude",
    "longitude",
    "visit_counts",
    "visitor_counts",
    "visitor_home_cbgs",
    "visitor_daytime_cbgs",
    "visits_by_day",
    "date_range_start",
    "date_range_end",
    "naics_code",
    "top_category",
    "sub_category",
    "city",
    "region"
]

existing = [c for c in keep_cols if c in df.columns]

df = df[existing]

print("Remaining columns:", len(df.columns))

df.to_parquet(
    OUTPUT,
    index=False
)

print("Saved:", OUTPUT)
print(df.head())
