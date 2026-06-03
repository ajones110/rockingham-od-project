import pandas as pd
import json
import numpy as np

df = pd.read_parquet(
    "data/raw/export_1/2026-03-02--data_01c4ac48-0309-1cae-0042-fa0708e04496_008_4_0.snappy.parquet"
)

valid_rows = df[df["VISITOR_HOME_CBGS"].notna()].copy()

coverage_ratios = []

for _, row in valid_rows.iterrows():
    try:
        home_dict = json.loads(row["VISITOR_HOME_CBGS"])
        home_total = sum(home_dict.values())
        visitors = row["VISITOR_COUNTS"]

        if visitors > 0:
            coverage_ratios.append(home_total / visitors)

    except Exception:
        pass

print("\n--- MAIN RESULTS ---")
print("Number of POIs:", len(coverage_ratios))
print("Mean ratio:", np.mean(coverage_ratios))
print("Min ratio:", np.min(coverage_ratios))
print("Max ratio:", np.max(coverage_ratios))

print("\n--- EXTRA CHECK ---")
print("Std dev:", np.std(coverage_ratios))
print("Unique ratios:", len(set(round(x, 6) for x in coverage_ratios)))

mismatches = 0

for _, row in valid_rows.iterrows():
    try:
        home_dict = json.loads(row["VISITOR_HOME_CBGS"])
        home_total = sum(home_dict.values())
        visitors = row["VISITOR_COUNTS"]

        if visitors > 0 and home_total != visitors:
            mismatches += 1

    except Exception:
        pass

print("Mismatch rows:", mismatches)


