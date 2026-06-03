import pandas as pd
import numpy as np
import os

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_parquet(
    "data/raw/export_1/2026-03-02--data_01c4ac48-0309-1cae-0042-fa0708e04496_008_4_0.snappy.parquet"
)

# -----------------------------
# NORMALIZATION
# -----------------------------
coverage_rate = 0.30
coverage_rate = float(coverage_rate)

df["observed_trips"] = pd.to_numeric(df["VISIT_COUNTS"], errors="coerce")
df = df.dropna(subset=["observed_trips"])

df["adjusted_trips"] = df["observed_trips"].astype(float) / coverage_rate

# -----------------------------
# PRINT SUMMARY
# -----------------------------
print("\n--- NORMALIZATION RESULTS ---")
print("Coverage rate:", coverage_rate)
print("Total observed:", df["observed_trips"].sum())
print("Total adjusted:", df["adjusted_trips"].sum())

# -----------------------------
# EXPORT RESULTS
# -----------------------------
os.makedirs("outputs/od_matrices", exist_ok=True)

df.to_csv("outputs/od_matrices/normalized_trips.csv", index=False)

print("\nSaved: outputs/od_matrices/normalized_trips.csv")

