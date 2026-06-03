import pandas as pd
import numpy as np
import json
import os

# =================================================
# 1. LOAD DATA
# =================================================
file_path = "data/raw/export_1/2026-03-02--data_01c4ac48-0309-1cae-0042-fa0708e04496_008_4_0.snappy.parquet"
df = pd.read_parquet(file_path)

print("\n--- DATA LOADED ---")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# =================================================
# 2. STEP 2: MISSING VISITOR_HOME_CBGS LOG
# =================================================
missing_home = df["VISITOR_HOME_CBGS"].isna().sum()
total = len(df)

print("\n--- DATA QUALITY LOG ---")
print("Missing VISITOR_HOME_CBGS:", missing_home)
print("Percent missing:", round(100 * missing_home / total, 2), "%")

excluded_visitors = df.loc[df["VISITOR_HOME_CBGS"].isna(), "VISIT_COUNTS"].sum()
total_visitors = df["VISIT_COUNTS"].sum()

print("Excluded visitors:", excluded_visitors)
print("Percent excluded (by volume):", round(100 * excluded_visitors / total_visitors, 2), "%")

# =================================================
# 3. STEP 3: NORMALIZATION
# =================================================
coverage_rate = 0.30
coverage_rate = float(coverage_rate)

df["observed_trips"] = pd.to_numeric(df["VISIT_COUNTS"], errors="coerce")
df = df.dropna(subset=["observed_trips"])

df["adjusted_trips"] = df["observed_trips"].astype(float) / coverage_rate

print("\n--- NORMALIZATION SUMMARY ---")
print("Observed total:", df["observed_trips"].sum())
print("Adjusted total:", df["adjusted_trips"].sum())

# =================================================
# 4. STEP 4: OD MATRIX BUILD
# =================================================
rows = []

for _, row in df.iterrows():
    try:
        home_dict = json.loads(row["VISITOR_HOME_CBGS"])
        poi = row["FOOTPRINT_ID"]

        for origin_cbg, count in home_dict.items():
            rows.append([origin_cbg, poi, count])

    except Exception:
        pass

od = pd.DataFrame(rows, columns=["origin_cbg", "poi", "visits"])
od_matrix = od.groupby(["origin_cbg", "poi"])["visits"].sum().reset_index()

# =================================================
# 5. EXPORTS
# =================================================
os.makedirs("outputs/od_matrices", exist_ok=True)

df.to_csv("outputs/od_matrices/normalized_trips.csv", index=False)
od_matrix.to_csv("outputs/od_matrices/od_matrix.csv", index=False)

print("\n--- EXPORT COMPLETE ---")
print("Normalized trips saved")
print("OD matrix saved")
print("OD rows:", len(od_matrix))

