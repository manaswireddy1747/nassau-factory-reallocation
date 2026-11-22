import json
from pathlib import Path
import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "Nassau Candy Distributor.csv"
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
required = ["Order Date","Ship Date","Ship Mode","Region","Product Name","Sales","Units","Gross Profit","Cost"]
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

# The source file uses dates such as 03-01-2024. Parse day-first, then audit.
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, errors="coerce")
df["lead_time_days"] = (df["Ship Date"] - df["Order Date"]).dt.days
bad = df["lead_time_days"].isna() | (df["lead_time_days"] < 0)
df = df.loc[~bad].copy()

# Important: this dataset's dates appear to produce unusually large durations.
# Do not silently delete them or treat them as real delivery lead times.
print("Lead-time audit (days):")
print(df["lead_time_days"].describe(percentiles=[.05,.25,.5,.75,.95]))
print("Rows with lead time > 60 days:", int((df["lead_time_days"] > 60).sum()))
print("Confirm date correctness with the project mentor before interpreting model results.")

with open(ROOT / "product_factory_mapping.json") as f:
    product_map = json.load(f)
df["Current Factory"] = df["Product Name"].map(lambda x: product_map.get(x, [None,None])[1])
df = df.dropna(subset=["Current Factory","lead_time_days"])

# Avoid using post-outcome fields such as Ship Date as model inputs.
features = ["Product Name","Current Factory","Region","Ship Mode","Division"]
target = "lead_time_days"
X = df[features].astype(str)
y = df[target]

cat_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])
pre = ColumnTransformer([("categorical", cat_pipe, features)])
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=250, random_state=42, min_samples_leaf=3),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42)
}
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scores = []
best_name, best_pipe, best_rmse = None, None, float("inf")
for name, estimator in models.items():
    pipe = Pipeline([("preprocess", pre), ("model", estimator)])
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    rmse = mean_squared_error(y_test, pred) ** 0.5
    mae = mean_absolute_error(y_test, pred)
    r2 = r2_score(y_test, pred)
    scores.append({"model":name,"MAE_days":mae,"RMSE_days":rmse,"R2":r2})
    if rmse < best_rmse:
        best_name, best_pipe, best_rmse = name, pipe, rmse

pd.DataFrame(scores).to_csv(ROOT / "outputs" / "model_metrics.csv", index=False)
joblib.dump({"pipeline":best_pipe,"features":features,"model_name":best_name},
            MODEL_DIR / "lead_time_model.joblib")
print(pd.DataFrame(scores).to_string(index=False))
print(f"Saved best model: {best_name}")
