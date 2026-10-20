# Customer Engagement & Product Utilization Analytics for Retention Strategy

## Project Overview
This project analyzes banking customer engagement, product utilization, and financial behavior to identify patterns associated with customer churn.

The goal is to help banking stakeholders understand customer retention patterns and develop data-driven engagement strategies.

## Objectives
- Analyze customer engagement and its relationship with churn.
- Evaluate churn patterns across different product counts.
- Identify high-balance customers who are not actively engaged.
- Develop a Relationship Strength Index (RSI).
- Build an interactive Streamlit dashboard for customer analysis.

## Dataset
The dataset contains 10,000 customer records and 14 original columns, including:
- Credit Score
- Geography
- Gender
- Age
- Tenure
- Balance
- Number of Products
- Credit Card Ownership
- Active Membership
- Estimated Salary
- Customer Churn Status

Additional features were created during analysis to support customer segmentation and engagement analysis.

## Tools and Technologies
- Python
- Pandas
- Matplotlib
- Seaborn
- Jupyter Notebook
- Streamlit

## Key Findings

### 1. Customer Engagement and Churn
- Inactive customers had a churn rate of 26.85%.
- Active customers had a churn rate of 14.27%.
- The difference was 12.58 percentage points.

### 2. Product Utilization
- Customers with one product had a churn rate of 27.71%.
- Customers with two products had a churn rate of 7.58%.
- Customers with three or four products had higher churn rates, but these groups were much smaller. Therefore, the results should be interpreted cautiously.

### 3. High-Balance Customers
- High-balance customers had a churn rate of 23.68%.
- Other customers had a churn rate of 19.27%.
- Approximately 49.88% of high-balance customers were inactive.

### 4. Relationship Strength Index
The project uses a custom exploratory Relationship Strength Index based on customer activity and product usage.

- Average RSI for retained customers: 47.03
- Average RSI for churned customers: 36.48

This is an exploratory index developed for this project, not a validated industry-standard metric.

### 5. Credit Card Ownership
Retention rates were similar for customers with and without a credit card.

## Interactive Dashboard
The Streamlit dashboard allows users to explore:
- Engagement and churn patterns
- Product utilization and churn
- High-balance, disengaged customers
- Relationship Strength Index
- Customer segments and retention insights

Filters are available for geography, engagement, product count, balance, and estimated salary.

## Project Structure
- `customer_engagement_analysis.ipynb` — Data analysis and visualizations
- `app.py` — Streamlit dashboard
- `European_Bank(2).csv` — Dataset
- `project 3 documentation.docx` — Project documentation
- `outputs/` — Charts and KPI summary

## How to Run the Dashboard

1. Download or clone this repository.
2. Install the required packages:

   `pip install pandas matplotlib seaborn streamlit`

3. Ensure the dataset is available at the path expected by `app.py`.
4. Run the dashboard:

   `python -m streamlit run app.py`

5. Open the local URL displayed in the terminal.

## Methodology
The project uses data validation, exploratory data analysis, feature engineering, customer segmentation, and descriptive comparisons to study churn patterns.

The findings show associations in the dataset and do not establish that engagement or product usage directly causes churn.

## Conclusion
The analysis highlights differences in churn across engagement levels and product counts. These findings can support further investigation and help inform customer retention strategies.

## Author
Abhishek Vishwakarma
## Live Dashboard

Explore the interactive dashboard here:

[Launch Customer Engagement & Retention Analytics Dashboard](https://customer-engagement-retention-analytics-4esx9t3ydthrjcevykbbm5.streamlit.app/)

## GitHub Repository

Explore the complete project, including the Python code, Jupyter Notebook, dataset, and visualizations:

[View Project on GitHub](https://github.com/abhishek-vishwakarma29/customer-engagement-retention-analytics)
