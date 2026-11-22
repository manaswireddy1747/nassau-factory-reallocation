
# STEP 1: Import Pandas
import pandas as pd

# STEP 2: Load the dataset
df = pd.read_csv("data/Nassau Candy Distributor.csv")

# STEP 3: Display first 5 rows
print("\nFIRST FIVE ROWS")
print(df.head())

# STEP 4: Display dataset size
print("\nDATASET SHAPE")
print(df.shape)

# STEP 5: Display column names
print("\nCOLUMN NAMES")
print(df.columns.tolist())

# STEP 6: Display information
print("\nDATASET INFORMATION")
print(df.info())

# STEP 7: Check missing values
print("\nMISSING VALUES")
print(df.isnull().sum())

# STEP 8: Statistical summary
print("\nSTATISTICAL SUMMARY")
print(df.describe())

print("\nDATASET LOADED SUCCESSFULLY!")
