
# ==================================================
# NASSAU CANDY - MACHINE LEARNING MODEL DEVELOPMENT
# ==================================================

import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# STEP 1: LOAD DATASET

df = pd.read_csv("outputs/nassau_cleaned_audit.csv")

print("Dataset loaded successfully")
print("Dataset shape:", df.shape)


# STEP 2: CHECK TARGET VARIABLE

print("\nLEAD TIME SUMMARY")

print(df["Lead Time"].describe())


# STEP 3: VALIDATION GATE

# Keep False until your mentor confirms
# the correct date interpretation or provides
# a corrected dataset.

DATE_DATA_VALIDATED = False

if not DATE_DATA_VALIDATED:

    print("\nMODEL TRAINING PAUSED")

    print(
        "The calculated lead times are unusually long."
    )

    print(
        "Please confirm the date issue with your mentor."
    )

    print(
        "Do not report model performance as "
        "business-valid before validation."
    )

    raise SystemExit


# STEP 4: CHECK DATA QUALITY

df = df.dropna(
    subset=[
        "Lead Time",
        "Product Name",
        "Current Factory",
        "Region",
        "Ship Mode",
        "Division"
    ]
)

if (df["Lead Time"] < 0).any():

    raise ValueError(
        "Negative lead times found. "
        "Check the source dates."
    )


# STEP 5: SELECT FEATURES

features = [
    "Product Name",
    "Current Factory",
    "Region",
    "Ship Mode",
    "Division"
]

X = df[features]

y = df["Lead Time"]


# STEP 6: ENCODE CATEGORICAL DATA

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            features
        )
    ]
)


# STEP 7: SPLIT DATASET

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTRAINING RECORDS:", len(X_train))
print("TESTING RECORDS:", len(X_test))


# STEP 8: DEFINE THREE MODELS

models = {

    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=100,
        random_state=42
    )

}


# STEP 9: TRAIN AND EVALUATE MODELS

results = []

trained_models = {}

for name, algorithm in models.items():

    print("\nTraining:", name)

    pipeline = Pipeline(
        steps=[
            ("preprocessing", preprocessor),
            ("model", algorithm)
        ]
    )

    # Train model
    pipeline.fit(X_train, y_train)

    # Predict test data
    predictions = pipeline.predict(X_test)

    # Evaluation
    mae = mean_absolute_error(
        y_test, predictions
    )

    rmse = np.sqrt(
        mean_squared_error(y_test, predictions)
    )

    r2 = r2_score(
        y_test, predictions
    )

    results.append({

        "Model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2

    })

    trained_models[name] = pipeline

    print("MAE:", mae)
    print("RMSE:", rmse)
    print("R2:", r2)


# STEP 10: COMPARE MODELS

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="MAE"
)

print("\nMODEL COMPARISON")

print(results_df)


# STEP 11: SAVE RESULTS

os.makedirs("outputs", exist_ok=True)
os.makedirs("models", exist_ok=True)

results_df.to_csv(
    "outputs/model_metrics.csv",
    index=False
)


# STEP 12: SAVE BEST MODEL

best_model_name = results_df.iloc[0]["Model"]

best_model = trained_models[best_model_name]

joblib.dump(
    best_model,
    "models/best_lead_time_model.joblib"
)

print("\nBEST MODEL:", best_model_name)

print("Model and metrics saved successfully!")

print("\nMACHINE LEARNING COMPLETED!")
