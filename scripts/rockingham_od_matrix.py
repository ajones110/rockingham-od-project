import polars as pl
import json

# ==========================================
# INPUT FILES
# ==========================================

files = [
    "2026-03-02--data_01c4ac48-0309-1cae-0042-fa0708e04496_008_4_0.snappy.parquet",
    "2026-03-09--data_01c4ac48-0309-1cae-0042-fa0708e04496_208_0_0.snappy.parquet",
    "2026-03-16--data_01c4ac48-0309-1cae-0042-fa0708e04496_008_2_0.snappy.parquet"
]

output_rows = []

# ==========================================
# PROCESS FILES
# ==========================================

for file in files:

    print(f"\nLoading {file}...")

    df = pl.read_parquet(file)

    print("Filtering Rockingham County POIs...")

    rockingham_df = df.filter(
        pl.col("POI_CBG").cast(pl.Utf8).str.starts_with("37157")
    )

    print(f"Rows after filtering: {rockingham_df.height}")

    print("Building OD trips...")

    for row in rockingham_df.iter_rows(named=True):

        destination = str(row["POI_CBG"])

        visitor_data = row.get("VISITOR_HOME_CBGS")

        if visitor_data is None:
            continue

        try:
            visitor_dict = json.loads(visitor_data)

            for origin, trips in visitor_dict.items():

                output_rows.append({
                    "origin_cbg": str(origin),
                    "destination_cbg": destination,
                    "trips": int(trips)
                })

        except Exception:
            continue

# ==========================================
# CREATE FINAL OD MATRIX
# ==========================================

print("\nCreating OD matrix...")

od_df = pl.DataFrame(output_rows)

od_matrix = (
    od_df
    .group_by(["origin_cbg", "destination_cbg"])
    .agg(pl.col("trips").sum())
)

# ==========================================
# SAVE OUTPUT
# ==========================================

output_file = "rockingham_od_matrix.csv"

od_matrix.write_csv(output_file)

print(f"\nSaved to {output_file}")
print("Done!")

