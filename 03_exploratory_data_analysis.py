
# ==========================================
# NASSAU CANDY - EXPLORATORY DATA ANALYSIS
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# STEP 1: Load cleaned dataset

df = pd.read_csv("outputs/nassau_cleaned_audit.csv")

# STEP 2: Convert date column

df["Order Date"] = pd.to_datetime(
    df["Order Date"], errors="coerce"
)

# STEP 3: Create output folder

os.makedirs("outputs/eda", exist_ok=True)

# STEP 4: Set graph style

sns.set_theme(style="whitegrid")

print("EDA STARTED")
print("Dataset shape:", df.shape)


# ==========================================
# GRAPH 1: SALES BY PRODUCT
# ==========================================

sales_product = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n1. SALES BY PRODUCT")
print(sales_product)

plt.figure(figsize=(12, 7))
sales_product.plot(kind="bar")

plt.title("Total Sales by Product")
plt.xlabel("Product Name")
plt.ylabel("Total Sales")
plt.xticks(rotation=75, ha="right")
plt.tight_layout()

plt.savefig("outputs/eda/01_sales_by_product.png")
plt.show()
plt.close()


# ==========================================
# GRAPH 2: PROFIT BY PRODUCT
# ==========================================

profit_product = (
    df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\n2. PROFIT BY PRODUCT")
print(profit_product)

plt.figure(figsize=(12, 7))
profit_product.plot(kind="bar")

plt.title("Total Gross Profit by Product")
plt.xlabel("Product Name")
plt.ylabel("Gross Profit")
plt.xticks(rotation=75, ha="right")
plt.tight_layout()

plt.savefig("outputs/eda/02_profit_by_product.png")
plt.show()
plt.close()


# ==========================================
# GRAPH 3: SALES BY REGION
# ==========================================

sales_region = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n3. SALES BY REGION")
print(sales_region)

plt.figure(figsize=(9, 5))
sales_region.plot(kind="bar")

plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("outputs/eda/03_sales_by_region.png")
plt.show()
plt.close()


# ==========================================
# GRAPH 4: SHIPPING METHODS
# ==========================================

ship_count = df["Ship Mode"].value_counts()

print("\n4. SHIPPING METHOD COUNT")
print(ship_count)

plt.figure(figsize=(9, 5))

sns.countplot(
    data=df,
    x="Ship Mode",
    order=ship_count.index
)

plt.title("Orders by Shipping Method")
plt.xlabel("Shipping Method")
plt.ylabel("Number of Records")
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig("outputs/eda/04_shipping_methods.png")
plt.show()
plt.close()


# ==========================================
# GRAPH 5: MONTHLY SALES TREND
# ==========================================

df["Order Month"] = (
    df["Order Date"].dt.to_period("M").astype(str)
)

monthly_sales = (
    df.groupby("Order Month")["Sales"]
    .sum()
    .sort_index()
)

print("\n5. MONTHLY SALES")
print(monthly_sales)

plt.figure(figsize=(13, 5))
monthly_sales.plot(kind="line", marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Order Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=60)
plt.tight_layout()

plt.savefig("outputs/eda/05_monthly_sales.png")
plt.show()
plt.close()


# ==========================================
# GRAPH 6: SALES VS PROFIT
# ==========================================

plt.figure(figsize=(9, 6))

sns.scatterplot(
    data=df,
    x="Sales",
    y="Gross Profit",
    hue="Division"
)

plt.title("Sales vs Gross Profit")
plt.xlabel("Sales")
plt.ylabel("Gross Profit")
plt.tight_layout()

plt.savefig("outputs/eda/06_sales_vs_profit.png")
plt.show()
plt.close()


# ==========================================
# FINAL BUSINESS SUMMARY
# ==========================================

print("\n========== BUSINESS SUMMARY ==========")

print("Total Sales:", df["Sales"].sum())

print("Total Gross Profit:",
      df["Gross Profit"].sum())

print("Total Units:", df["Units"].sum())

print("\nHighest Sales Product:")
print(sales_product.head(1))

print("\nHighest Profit Product:")
print(profit_product.head(1))

print("\nHighest Sales Region:")
print(sales_region.head(1))

print("\nEDA COMPLETED SUCCESSFULLY!")

print("Charts saved inside outputs/eda/")
