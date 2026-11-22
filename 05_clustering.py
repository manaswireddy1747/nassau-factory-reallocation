
# ==================================================
# NASSAU CANDY - PRODUCT PERFORMANCE CLUSTERING
# ==================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# STEP 1: LOAD DATASET

df = pd.read_csv("outputs/nassau_cleaned_audit.csv")

print("Dataset loaded:", df.shape)


# STEP 2: GROUP DATA BY PRODUCT

product_data = df.groupby("Product Name").agg(

    Total_Sales=("Sales", "sum"),

    Total_Profit=("Gross Profit", "sum"),

    Total_Units=("Units", "sum"),

    Record_Count=("Row ID", "count")

).reset_index()


print("\nPRODUCT PERFORMANCE SUMMARY")

print(product_data)


# STEP 3: SELECT NUMERICAL FEATURES

features = [
    "Total_Sales",
    "Total_Profit",
    "Total_Units",
    "Record_Count"
]

X = product_data[features]


# STEP 4: SCALE THE DATA

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# STEP 5: FIND THE BEST NUMBER OF CLUSTERS

scores = {}

maximum_k = min(5, len(product_data) - 1)

for k in range(2, maximum_k + 1):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X_scaled)

    if len(set(labels)) > 1:

        score = silhouette_score(
            X_scaled,
            labels
        )

        scores[k] = score

        print(
            "Clusters:", k,
            "Silhouette Score:", score
        )


if not scores:

    raise ValueError(
        "Unable to calculate valid clusters."
    )


# STEP 6: SELECT BEST K

best_k = max(scores, key=scores.get)

print("\nBest number of clusters:", best_k)


# STEP 7: TRAIN FINAL K-MEANS MODEL

kmeans = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init=10
)

product_data["Cluster"] = kmeans.fit_predict(
    X_scaled
)


# STEP 8: DISPLAY CLUSTER RESULTS

print("\nPRODUCT CLUSTER RESULTS")

print(
    product_data.sort_values(
        "Cluster"
    )
)


# STEP 9: UNDERSTAND EACH CLUSTER

cluster_summary = product_data.groupby(
    "Cluster"
)[features].mean()

print("\nCLUSTER SUMMARY")

print(cluster_summary)


# STEP 10: SAVE RESULTS

os.makedirs("outputs/clustering", exist_ok=True)

product_data.to_csv(
    "outputs/clustering/product_clusters.csv",
    index=False
)


# STEP 11: CREATE CLUSTER GRAPH

plt.figure(figsize=(11, 7))

sns.scatterplot(
    data=product_data,
    x="Total_Sales",
    y="Total_Profit",
    hue="Cluster",
    palette="viridis",
    s=120
)

for _, row in product_data.iterrows():

    plt.annotate(
        row["Product Name"],
        (
            row["Total_Sales"],
            row["Total_Profit"]
        ),
        fontsize=7
    )


plt.title("Nassau Candy Product Performance Clusters")

plt.xlabel("Total Sales")

plt.ylabel("Total Gross Profit")

plt.tight_layout()

plt.savefig(
    "outputs/clustering/product_clusters.png"
)

plt.show()

plt.close()


# STEP 12: FINAL RESULT

print("\nCLUSTERING COMPLETED!")

print("Best K:", best_k)

print(
    "Results saved in outputs/clustering/"
)
