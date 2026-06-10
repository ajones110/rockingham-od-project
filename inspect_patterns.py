import pandas as pd

df = pd.read_csv(
    "/Users/pandeyadmin/Downloads/weekly-patterns-plus-sample.csv"
)

print(df.columns.tolist())

print("\nFIRST visitor_home_cbgs RECORD:\n")
print(df["visitor_home_cbgs"].iloc[0])
