
# ============================================================
# NASSAU CANDY DISTRIBUTOR
# FACTORY REALLOCATION & SHIPPING OPTIMIZATION DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import os


# ------------------------------------------------------------
# STEP 1: PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="Nassau Candy Optimization",
    page_icon="🍬",
    layout="wide"
)


# ------------------------------------------------------------
# STEP 2: LOAD DATA
# ------------------------------------------------------------

DATA_FILE = "outputs/nassau_cleaned_audit.csv"

SCENARIO_FILE = (
    "outputs/factory_optimization/"
    "candidate_factory_scenarios.csv"
)


@st.cache_data
def load_data():

    data = pd.read_csv(DATA_FILE)

    scenarios = pd.read_csv(SCENARIO_FILE)

    return data, scenarios


if not os.path.exists(DATA_FILE):

    st.error(f"Dataset not found: {DATA_FILE}")
    st.stop()


if not os.path.exists(SCENARIO_FILE):

    st.error(f"Factory scenario file not found: {SCENARIO_FILE}")
    st.stop()


df, scenarios = load_data()


# ------------------------------------------------------------
# STEP 3: DASHBOARD TITLE
# ------------------------------------------------------------

st.title("🍬 Nassau Candy Distributor")

st.subheader(
    "Factory Reallocation & Shipping Optimization System"
)

st.caption(
    "Interactive business analytics and factory scenario simulator"
)

st.divider()


# ------------------------------------------------------------
# STEP 4: SIDEBAR FILTERS
# ------------------------------------------------------------

st.sidebar.header("Dashboard Filters")

products = sorted(
    df["Product Name"].dropna().unique()
)

regions = sorted(
    df["Region"].dropna().unique()
)

ship_modes = sorted(
    df["Ship Mode"].dropna().unique()
)


selected_product = st.sidebar.selectbox(
    "Select Product",
    products
)

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + regions
)

selected_ship_mode = st.sidebar.selectbox(
    "Select Shipping Method",
    ["All"] + ship_modes
)


# ------------------------------------------------------------
# STEP 5: FILTER DATA
# ------------------------------------------------------------

filtered_df = df[
    df["Product Name"] == selected_product
].copy()


if selected_region != "All":

    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]


if selected_ship_mode != "All":

    filtered_df = filtered_df[
        filtered_df["Ship Mode"] == selected_ship_mode
    ]


# ------------------------------------------------------------
# STEP 6: BUSINESS KPI SECTION
# ------------------------------------------------------------

st.header("Business Overview")

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Sales",
    f"${filtered_df['Sales'].sum():,.2f}"
)

col2.metric(
    "Gross Profit",
    f"${filtered_df['Gross Profit'].sum():,.2f}"
)

col3.metric(
    "Total Units",
    f"{filtered_df['Units'].sum():,.0f}"
)

col4.metric(
    "Order Records",
    f"{len(filtered_df):,}"
)


st.divider()


# ------------------------------------------------------------
# STEP 7: FACTORY OPTIMIZATION SIMULATOR
# ------------------------------------------------------------

st.header("1. Factory Optimization Simulator")

st.write(
    "Compare the current factory with the alternative "
    "factory assignments available for the selected product."
)


product_scenarios = scenarios[
    scenarios["Product"] == selected_product
].copy()


st.subheader("Factory Comparison")

display_columns = [

    "Candidate_Factory",

    "Assignment_Type",

    "Historical_Sales",

    "Historical_Gross_Profit",

    "Historical_Units",

    "Recommendation_Status"

]


st.dataframe(

    product_scenarios[display_columns],

    use_container_width=True,

    hide_index=True

)


st.info(
    "Historical sales and gross profit are repeated "
    "product-level figures. They are not predicted "
    "financial outcomes for each factory."
)


st.divider()


# ------------------------------------------------------------
# STEP 8: WHAT-IF SCENARIO ANALYSIS
# ------------------------------------------------------------

st.header("2. What-If Scenario Analysis")


current_factory = product_scenarios[
    product_scenarios["Assignment_Type"] == "Current"
]["Candidate_Factory"].iloc[0]


alternative_factories = product_scenarios[
    product_scenarios["Assignment_Type"] == "Alternative"
]["Candidate_Factory"].tolist()


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Current Factory",
        current_factory
    )


with col2:

    proposed_factory = st.selectbox(
        "Choose Alternative Factory",
        alternative_factories
    )


st.write("Selected reassignment scenario:")

st.write(
    f"**{current_factory} → {proposed_factory}**"
)


st.warning(
    "What-if comparison is currently a candidate scenario only. "
    "Validated lead-time predictions and financial impacts "
    "are not available yet."
)


st.divider()


# ------------------------------------------------------------
# STEP 9: RECOMMENDATION DASHBOARD
# ------------------------------------------------------------

st.header("3. Recommendation Dashboard")


top_n = st.slider(
    "Number of candidate factories to display",
    min_value=1,
    max_value=4,
    value=3
)


st.caption(
    "Candidates are displayed for investigation, "
    "not ranked by proven business benefit."
)


candidate_list = product_scenarios[
    product_scenarios["Assignment_Type"] == "Alternative"
].copy()


candidate_list = candidate_list.sort_values(
    "Candidate_Factory"
).head(top_n)


st.dataframe(

    candidate_list[[
        "Product",
        "Current_Factory",
        "Candidate_Factory",
        "Recommendation_Status"
    ]],

    use_container_width=True,

    hide_index=True

)


st.info(
    "A genuine top-N recommendation ranking requires "
    "validated lead-time predictions, operational risk data "
    "and factory-specific financial information."
)


st.divider()


# ------------------------------------------------------------
# STEP 10: SPEED VS PROFIT PRIORITY
# ------------------------------------------------------------

st.header("4. Optimization Priority")


speed_priority = st.slider(
    "Priority towards shipping speed (%)",
    min_value=0,
    max_value=100,
    value=50
)


profit_priority = 100 - speed_priority


col1, col2 = st.columns(2)


col1.metric(
    "Speed Priority",
    f"{speed_priority}%"
)


col2.metric(
    "Profit Priority",
    f"{profit_priority}%"
)


st.caption(
    "This is a preference setting for the future ranking engine. "
    "It does not calculate a recommendation score yet."
)


st.divider()


# ------------------------------------------------------------
# STEP 11: RISK AND IMPACT PANEL
# ------------------------------------------------------------

st.header("5. Risk & Impact Panel")


st.warning(
    "DATA QUALITY WARNING: Calculated shipping lead times "
    "range from 904 to 1,642 days. Date interpretation "
    "must be confirmed before model predictions are trusted."
)


st.warning(
    "ALTERNATIVE FACTORY WARNING: Historical records show "
    "only one mapped current factory per product. "
    "Alternative-factory effects have not been validated."
)


st.warning(
    "FINANCIAL WARNING: Historical gross profit is available, "
    "but factory-specific production and transportation costs "
    "are missing. Incremental profit cannot be calculated."
)


st.info(
    "CAPACITY WARNING: Factory production capacity, "
    "inventory and operational constraints are not available."
)


st.divider()


# ------------------------------------------------------------
# STEP 12: REGIONAL SALES ANALYSIS
# ------------------------------------------------------------

st.header("6. Regional Sales Analysis")


regional_sales = (

    filtered_df.groupby("Region")["Sales"]

    .sum()

    .sort_values(ascending=False)

)


st.bar_chart(regional_sales)


# ------------------------------------------------------------
# STEP 13: FINAL STATUS
# ------------------------------------------------------------

st.divider()

st.success(
    "Nassau Candy Interactive Dashboard Loaded Successfully!"
)


st.caption(
    "Academic internship prototype | "
    "Predictions and reassignment benefits require validation."
)
