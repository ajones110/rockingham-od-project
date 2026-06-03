import pandas as pd

# load data
df = pd.read_parquet(
    "data/raw/export_1/2026-03-02--data_01c4ac48-0309-1cae-0042-fa0708e04496_008_4_0.snappy.parquet"
)

total_rows = len(df)

missing_mask = df["VISITOR_HOME_CBGS"].isna()

missing_rows = missing_mask.sum()
valid_rows = total_rows - missing_rows

# treat VISITOR_COUNTS as "trip volume"
total_trips = df["VISITOR_COUNTS"].sum()

excluded_trips = df.loc[missing_mask, "VISITOR_COUNTS"].sum()

included_trips = df.loc[~missing_mask, "VISITOR_COUNTS"].sum()

# percentages
pct_rows_missing = 100 * missing_rows / total_rows
pct_trips_excluded = 100 * excluded_trips / total_trips

report = f"""
=============================
VISITOR_HOME_CBGS MISSINGNESS REPORT
=============================

Total POI rows: {total_rows:,}

Missing VISITOR_HOME_CBGS rows: {missing_rows:,}
Valid rows: {valid_rows:,}
% rows missing: {pct_rows_missing:.2f}%

-----------------------------

Total VISITOR_COUNTS (trips): {total_trips:,}

Excluded trips (missing CBG): {excluded_trips:,}
Included trips: {included_trips:,}
% trips excluded: {pct_trips_excluded:.2f}%

=============================
"""

print(report)

with open("outputs/logs/missingness_report.txt", "w") as f:
    f.write(report)

