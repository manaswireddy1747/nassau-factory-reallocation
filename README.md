
# Nassau Candy Distributor

## Factory Reallocation & Shipping Optimization Recommendation System

### Project Overview

This project develops an analytical system to study
product-to-factory assignments and shipping performance
for Nassau Candy Distributor.

The system uses Python, Pandas, Machine Learning,
K-Means Clustering and Streamlit.

### Objectives

- Analyze product and regional sales.
- Study shipping lead times.
- Compare five factory assignment scenarios.
- Explore factory reassignment opportunities.
- Develop an interactive dashboard.

### Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Streamlit
- GitHub

### Project Structure

- data/
- outputs/
- models/
- 03_exploratory_data_analysis.py
- 04_machine_learning.py
- 05_clustering.py
- 06_factory_optimization.py
- app.py
- requirements.txt

### Installation

Create a virtual environment:

python3 -m venv .venv

Activate it:

source .venv/bin/activate

Install packages:

pip install -r requirements.txt

### Run the Dashboard

streamlit run app.py

### Data Limitations

The supplied dataset contains unusual calculated
shipping lead times that require date validation.

Alternative factory outcomes are not established
by historical observations.

Factory capacity, transportation costs and
incremental profit data are unavailable.

Therefore, reassignment scenarios are exploratory
and should not be treated as validated business
recommendations.

### Author

## Author

**Gade Lakshmi Naga Sai Manaswi**

Data Analyst Intern Project – Nassau Candy Distributor

B.E. Computer Science and Engineering