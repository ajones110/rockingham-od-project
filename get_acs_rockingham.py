from census import Census
import pandas as pd

# You must get a free API key:
# https://api.census.gov/data/key_signup.html

API_KEY = "7bdcb91b7c66d6d274c637bf5454bfd1b323361a"
c = Census(API_KEY)

# Rockingham County FIPS:
state_fips = "37"
county_fips = "157"

# ACS 5-year population variable
data = c.acs5.get(
    ("B01003_001E", "B19013_001E"),
    {
        "for": "block group:*",
        "in": f"state:{state_fips} county:{county_fips}"
    }
)

df = pd.DataFrame(data)

df = df.rename(columns={
    "B01003_001E": "population",
    "B19013_001E": "median_income"
})

print(df.head())

df.to_csv("outputs/rockingham_acs.csv", index=False)
print("Saved ACS data")
