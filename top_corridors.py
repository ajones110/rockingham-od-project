od = pd.DataFrame(rows, columns=["origin_cbg", "destination_poi", "trips"])

# Rename for clarity (clean reporting names)
od = od.rename(columns={
    "origin_cbg": "origin",
    "destination_poi": "destination"
})import pandas as pd
import json

df = pd.read_parquet(
    "data/raw/export_1/2026-03-02--data_01c4ac48-0309-1cae-0042-fa0708e04496_008_4_0.snappy.parquet"
)

rows = []

for _, row in df.iterrows():
    try:
        home_dict = json.loads(row["VISITOR_HOME_CBGS"])
        poi = row["PERSISTENT_ID_STORE"]

        for origin, count in home_dict.items():
            rows.append([origin, poi, count])

    except Exception:
        pass

od = pd.DataFrame(rows, columns=["origin_cbg", "destination_poi", "trips"])

# --- TOP CORRIDORS ---
top_corridors = (
    od.groupby(["origin_cbg", "destination_poi"])["trips"]
    .sum()
    .reset_index()
    .sort_values("trips", ascending=False)
)

print("\n--- TOP 20 CORRIDORS ---")
print(top_corridors.head(20))

top_corridors.head(50).to_csv(
    "outputs/od_matrices/top_corridors.csv",
    index=False
)

print("\nSaved: outputs/od_matrices/top_corridors.csv")

