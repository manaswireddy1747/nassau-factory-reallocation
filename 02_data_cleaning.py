

import pandas as pd
import json
import os

# 1. Load dataset
df = pd.read_csv("data/Nassau Candy Distributor.csv")

print("Original dataset:", df.shape)

# 2. Check duplicates
print("Exact duplicates:", df.duplicated().sum())
print("Duplicate Row IDs:", df["Row ID"].duplicated().sum())

# 3. Check missing values
print("Missing values:", df.isnull().sum().sum())

# 4. Convert dates
df["Order Date"] = pd.to_datetime(
    df["Order Date"], dayfirst=True, errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"], dayfirst=True, errors="coerce"
)

# 5. Calculate lead time
df["Lead Time"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# 6. Audit lead time
print("\nLead time summary:")
print(df["Lead Time"].describe())

print("Above 60 days:", (df["Lead Time"] > 60).sum())
print("Negative lead times:", (df["Lead Time"] < 0).sum())

# 7. Load factory mapping
with open("product_factory_mapping.json", "r") as file:
    mapping = json.load(file)

df["Current Factory"] = df["Product Name"].map(
    lambda p: mapping.get(p, [None, None])[1]
)

print("\nUnmapped products:", df["Current Factory"].isna().sum())

# 8. Create output folder
os.makedirs("outputs", exist_ok=True)

# 9. Save audit dataset
df.to_csv(
    "outputs/nassau_cleaned_audit.csv",
    index=False
)

# 10. Final result
print("\nFinal dataset shape:", df.shape)
print("Cleaning and audit completed!")
