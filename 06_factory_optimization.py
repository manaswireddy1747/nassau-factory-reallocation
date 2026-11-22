
# =====================================================
# NASSAU CANDY - FACTORY REALLOCATION ANALYSIS
# STAGE 7
# =====================================================

import pandas as pd
import os

# STEP 1: LOAD CLEANED DATASET

df = pd.read_csv(
    "outputs/nassau_cleaned_audit.csv"
)

print("Dataset loaded successfully")
print("Total records:", len(df))


# STEP 2: DEFINE FIVE FACTORIES

factories = [

    "Lot's O' Nuts",

    "Wicked Choccy's",

    "Sugar Shack",

    "Secret Factory",

    "The Other Factory"

]


# STEP 3: CHECK REQUIRED COLUMNS

required_columns = [

    "Product Name",
    "Current Factory",
    "Sales",
    "Gross Profit",
    "Units",
    "Region"

]

for column in required_columns:

    if column not in df.columns:

        raise ValueError(
            f"Missing required column: {column}"
        )


# STEP 4: CHECK FACTORY MAPPING

print("\nFACTORY MAPPING CHECK")

print(
    df["Current Factory"].value_counts()
)

unmapped = df[
    df["Current Factory"].isna()
]

if len(unmapped) > 0:

    raise ValueError(
        "Some products have no factory mapping."
    )

unknown_factories = set(
    df["Current Factory"].unique()
) - set(factories)

if unknown_factories:

    raise ValueError(
        f"Unknown factories: {unknown_factories}"
    )


# STEP 5: CREATE PRODUCT SUMMARY

product_summary = df.groupby(
    "Product Name"
).agg(

    Current_Factory=(
        "Current Factory",
        "first"
    ),

    Factory_Count=(
        "Current Factory",
        "nunique"
    ),

    Total_Sales=(
        "Sales",
        "sum"
    ),

    Total_Profit=(
        "Gross Profit",
        "sum"
    ),

    Total_Units=(
        "Units",
        "sum"
    )

).reset_index()


# STEP 6: CHECK CONSISTENCY

if (product_summary["Factory_Count"] != 1).any():

    raise ValueError(
        "Some products have multiple current factories."
    )


# STEP 7: GENERATE FIVE SCENARIOS PER PRODUCT

scenarios = []

for _, product in product_summary.iterrows():

    for factory in factories:

        is_current = (
            factory == product["Current_Factory"]
        )

        scenarios.append({

            "Product": product["Product Name"],

            "Current_Factory": product["Current_Factory"],

            "Candidate_Factory": factory,

            "Assignment_Type": (
                "Current"
                if is_current
                else "Alternative"
            ),

            "Historical_Sales": product["Total_Sales"],

            "Historical_Gross_Profit": product["Total_Profit"],

            "Historical_Units": product["Total_Units"],

            "Lead_Time_Estimate": None,

            "Lead_Time_Reduction": None,

            "Risk_Impact": "Not validated",

            "Incremental_Profit_Impact": "Not available",

            "Recommendation_Status": (
                "Current assignment"
                if is_current
                else "Pending validation"
            )

        })


scenario_df = pd.DataFrame(scenarios)


# STEP 8: CREATE OUTPUT FOLDER

os.makedirs(
    "outputs/factory_optimization",
    exist_ok=True
)


# STEP 9: SAVE SCENARIO TABLE

scenario_df.to_csv(

    "outputs/factory_optimization/"
    "candidate_factory_scenarios.csv",

    index=False

)


# STEP 10: DISPLAY SUMMARY

print("\nFACTORY OPTIMIZATION SUMMARY")

print(
    "Unique products:",
    product_summary["Product Name"].nunique()
)

print(
    "Available factories:",
    len(factories)
)

print(
    "Total candidate scenarios:",
    len(scenario_df)
)

print(
    "Current assignments:",
    len(
        scenario_df[
            scenario_df["Assignment_Type"] == "Current"
        ]
    )
)

print(
    "Alternative scenarios:",
    len(
        scenario_df[
            scenario_df["Assignment_Type"] == "Alternative"
        ]
    )
)


# STEP 11: DISPLAY EXAMPLE PRODUCT

example_product = (
    "Wonka Bar - Triple Dazzle Caramel"
)

print("\nEXAMPLE FACTORY COMPARISON")

print(

    scenario_df[
        scenario_df["Product"] == example_product
    ].to_string(index=False)

)


print("\nFACTORY SCENARIO GENERATION COMPLETED!")

print(
    "Results saved in "
    "outputs/factory_optimization/"
)
