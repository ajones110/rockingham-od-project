import pandas as pd
import ast
import os

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

file_path = "data/raw/export_1/2026-03-02--data_01c4ac48-0309-1cae-0042-fa0708e04496_008_4_0.snappy.parquet"

df = pd.read_parquet(file_path)

print("\n--- DATA LOADED ---")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# --------------------------------------------------
# --------------------------------------------------

missing_home = df["VISITOR_HOME_CBGS"].isna().sum()

print("\n--- DATA QUALITY LOG ---")
print("Missing VISITOR_HOME_CBGS:", missing_home)
print(
    "Percent missing:",
    round(missing_home / len(df) * 100, 2),
    "%"
)

# --------------------------------------------------
# BUILD OD MATRIX
# --------------------------------------------------

import json

# --------------------------------------------------
# BUILD OD MATRIX
# --------------------------------------------------

od_rows = []

for _, row in df.iterrows():

    home_cbgs = row["VISITOR_HOME_CBGS"]

    if pd.isna(home_cbgs):
        continue

    try:

        cbg_dict = json.loads(home_cbgs)

        for origin, trips in cbg_dict.items():

            od_rows.append(
                {
                    "origin": str(origin),
                    "destination": str(row["PLACEKEY"]),
                    "trips": float(trips)
                }
            )

    except Exception:
        continue

od = pd.DataFrame(od_rows)

print("\n--- TRIP SUMMARY ---")
print("Estimated trips:", round(od["trips"].sum()))

for _, row in df.iterrows():

    home_cbgs = row.get("VISITOR_HOME_CBGS")

    if pd.isna(home_cbgs):
        continue

    try:
        cbg_dict = ast.literal_eval(home_cbgs)

        for origin, trips in cbg_dict.items():

            od_rows.append(
                {
                    "origin": str(origin),
                    "destination": str(row["PLACEKEY"]),
                    "trips": float(trips)
                }
            )

    except Exception:
        continue

od = pd.DataFrame(od_rows)

print("\n--- TRIP SUMMARY ---")
print("Estimated trips:", od["trips"].sum())

# --------------------------------------------------
# EXPORT
# --------------------------------------------------

os.makedirs(
    "outputs/od_matrices",
    exist_ok=True
)

od.to_csv(
    "outputs/od_matrices/od_matrix.csv",
    index=False
)

print("\n--- EXPORT COMPLETE ---")
print("OD matrix saved")
print("OD rows:", len(od))

