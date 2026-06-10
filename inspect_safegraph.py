import pandas as pd

df = pd.read_csv("weekly-patterns-plus-sample.csv")

print("Columns:")
print(df.columns)

print("\nFirst visitor_home_cbgs value:")
print(df["visitor_home_cbgs"].iloc[0])
