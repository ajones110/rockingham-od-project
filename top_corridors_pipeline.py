import pandas as pd
import json
import matplotlib.pyplot as plt
import os

# ----------------------------
# 1. LOAD DATA
# ----------------------------
df = pd.read_parquet(
    "data/raw/export_1/2026-03-02--data_01c4ac48-0309-1cae-0042-fa0708e04496_008_4_0.snappy.parquet"
)

print("\n--- DATA LOADED ---")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ----------------------------
# 2. BUILD OD MATRIX
# ----------------------------
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

# ----------------------------
# 3. RENAME COLUMNS
# ----------------------------
od = od.rename(columns={
    "origin_cbg": "origin",
    "destination_poi": "destination"
})

# ----------------------------
# 4. COUNTY MAPPING
# ----------------------------
county_fips_map = {
    "37001": "Alamance",
    "37051": "Cumberland",
    "37063": "Durham",
    "37081": "Guilford",
    "37099": "Gaston",
    "37119": "Mecklenburg",
    "37147": "New Hanover",
    "37183": "Wake",
    "37199": "Yadkin",
    "37057": "Davidson",
    "37067": "Forsyth"
}

od["origin_county_fips"] = od["origin"].astype(str).str[:5]
od["origin_county"] = od["origin_county_fips"].map(county_fips_map).fillna("Other NC")

# ----------------------------
# 5. TOP CORRIDORS
# ----------------------------
top_corridors = (
    od.groupby(["origin", "destination"])["trips"]
    .sum()
    .reset_index()
    .sort_values("trips", ascending=False)
)

print("\n--- TOP 20 CORRIDORS ---")
print(top_corridors.head(20))

# ----------------------------
# 6. EXPORT RESULTS
# ----------------------------
os.makedirs("outputs/od_matrices", exist_ok=True)
os.makedirs("outputs/figures", exist_ok=True)

top_corridors.to_csv(
    "outputs/od_matrices/top_corridors.csv",
    index=False
)

print("\nSaved: outputs/od_matrices/top_corridors.csv")

# ----------------------------
# 7. TOP 10 PLOT
# ----------------------------
top10 = top_corridors.head(10).copy()

labels = top10["origin"] + " → " + top10["destination"]

plt.figure(figsize=(10, 6))
plt.bar(labels, top10["trips"])
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 Travel Corridors (CBG → POI)")
plt.ylabel("Trips")

plt.tight_layout()
plt.savefig("outputs/figures/top_10_corridors.png", dpi=300)
plt.show()

print("\nSaved: outputs/figures/top_10_corridors.png")

# ----------------------------
# 8. SUMMARY
# ----------------------------
print("\n--- SUMMARY ---")
print("Total OD pairs:", len(od))
print("Unique origins:", od["origin"].nunique())
print("Unique destinations:", od["destination"].nunique())

