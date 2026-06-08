import pandas as pd
import json
from pathlib import Path

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

FILE_PATH = "data/raw/export_1/2026-03-02--data_01c4ac48-0309-1cae-0042-fa0708e04496_008_4_0.snappy.parquet"

df = pd.read_parquet(FILE_PATH)

print("\n--- DATA LOADED ---")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# --------------------------------------------------
# DATA QUALITY CHECK
# --------------------------------------------------

missing = df["VISITOR_HOME_CBGS"].isna().sum()

print("\n--- DATA QUALITY LOG ---")
print("Missing VISITOR_HOME_CBGS:", missing)
print("Percent missing:", round(missing / len(df) * 100, 2), "%")

# --------------------------------------------------
# BUILD OD MATRIX
# --------------------------------------------------

records = []

for _, row in df.iterrows():

    if pd.isna(row["VISITOR_HOME_CBGS"]):
        continue

    try:
        cbg_dict = json.loads(row["VISITOR_HOME_CBGS"])
    except Exception:
        continue

    destination_id = row["PERSISTENT_ID"]
    destination_name = row["LOCATION_NAME"]

    for origin, trips in cbg_dict.items():

        records.append({
            "origin": str(origin),
            "destination_id": str(destination_id),
            "destination_name": str(destination_name),
            "trips": float(trips)
        })

od = pd.DataFrame(records)

print("\n--- TRIP SUMMARY ---")
print("Estimated trips:", round(od["trips"].sum()))

# --------------------------------------------------
# EXPORT
# --------------------------------------------------

Path("outputs/od_matrices").mkdir(parents=True, exist_ok=True)

od.to_csv(
    "outputs/od_matrices/od_matrix.csv",
    index=False
)

print("\n--- EXPORT COMPLETE ---")
print("OD matrix saved")
print("OD rows:", len(od))
