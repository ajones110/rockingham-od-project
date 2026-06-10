import pandas as pd

print("\n--- LOADING PLACE OD ---")

# --------------------------------------------------
# 1. Load OD with place assignments
# --------------------------------------------------
od = pd.read_csv("rockingham_place_od_gis.csv")

print("Raw OD shape:", od.shape)

# --------------------------------------------------
# 2. Basic cleaning: ensure strings
# --------------------------------------------------
od["home_place"] = od["home_place"].astype(str)
od["poi_place"] = od["poi_place"].astype(str)

# --------------------------------------------------
# 3. Identify missing mappings
# --------------------------------------------------
od["home_mapped"] = od["home_place"].notna() & (od["home_place"] != "nan")
od["poi_mapped"] = od["poi_place"].notna() & (od["poi_place"] != "nan")

print("\n--- MAPPING SUMMARY ---")
print("Missing home_place:", (~od["home_mapped"]).sum())
print("Missing poi_place:", (~od["poi_mapped"]).sum())

# --------------------------------------------------
# 4. Classify flows
# --------------------------------------------------

def classify_flow(row):
    if row["home_mapped"] and row["poi_mapped"]:
        return "internal"
    elif not row["home_mapped"] and row["poi_mapped"]:
        return "external_to_rockingham"
    elif row["home_mapped"] and not row["poi_mapped"]:
        return "external_from_rockingham"
    else:
        return "external_unknown"

od["flow_type"] = od.apply(classify_flow, axis=1)

# --------------------------------------------------
# 5. Split datasets
# --------------------------------------------------
internal_od = od[od["flow_type"] == "internal"]
external_in = od[od["flow_type"] == "external_to_rockingham"]
external_out = od[od["flow_type"] == "external_from_rockingham"]

print("\n--- FLOW BREAKDOWN ---")
print("Internal flows:", internal_od.shape)
print("External IN flows:", external_in.shape)
print("External OUT flows:", external_out.shape)

# --------------------------------------------------
# 6. Aggregate internal flows (core analysis dataset)
# --------------------------------------------------
internal_place_od = (
    internal_od.groupby(["home_place", "poi_place"])["visits"]
    .sum()
    .reset_index()
    .sort_values("visits", ascending=False)
)

# --------------------------------------------------
# 7. Normalize flows (share-based metric)
# --------------------------------------------------
internal_place_od["flow_share"] = (
    internal_place_od["visits"] /
    internal_place_od.groupby("home_place")["visits"].transform("sum")
)

# --------------------------------------------------
# 8. Save outputs
# --------------------------------------------------
internal_place_od.to_csv("rockingham_internal_place_od.csv", index=False)
external_in.to_csv("rockingham_external_inflows.csv", index=False)
external_out.to_csv("rockingham_external_outflows.csv", index=False)

print("\n✔ Saved:")
print("- rockingham_internal_place_od.csv")
print("- rockingham_external_inflows.csv")
print("- rockingham_external_outflows.csv")

# --------------------------------------------------
# 9. Quick insights
# --------------------------------------------------
print("\n--- TOP INTERNAL CORRIDORS ---")
print(internal_place_od.head(10))

print("\n--- FLOW TYPE SHARE ---")
print(od["flow_type"].value_counts(normalize=True))
