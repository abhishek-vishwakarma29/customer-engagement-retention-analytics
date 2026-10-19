import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Engagement & Retention Analytics",
    page_icon="🏦",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    data = pd.read_csv("European_Bank(2).csv")

    # Create engagement labels
    data["Engagement_Status"] = data["IsActiveMember"].map({
        1: "Active",
        0: "Inactive"
    })

    # Create churn labels
    data["Customer_Status"] = data["Exited"].map({
        0: "Retained",
        1: "Churned"
    })

    # Calculate the high-balance threshold
    balance_threshold = data["Balance"].quantile(0.75)

    # Identify high-balance customers
    data["High_Balance"] = data["Balance"] >= balance_threshold

    # Calculate relationship strength score
    max_products = data["NumOfProducts"].max()

    data["Engagement_Score"] = data["IsActiveMember"] * 100

    data["Product_Usage_Score"] = (
        data["NumOfProducts"] / max_products
    ) * 100

    data["Relationship_Strength_Index"] = (
        0.5 * data["Engagement_Score"]
        + 0.5 * data["Product_Usage_Score"]
    )

    return data


df = load_data()

# --------------------------------------------------
# DASHBOARD TITLE
# --------------------------------------------------

st.title("🏦 Customer Engagement & Retention Analytics")

st.markdown(
    """
    An interactive analytics dashboard for understanding customer
    engagement, banking product utilization, and churn patterns.

    **Objective:** Identify customer segments that may benefit from
    targeted retention strategies using data-driven insights.
    """
)

st.divider()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("🎛️ Dashboard Controls")

st.sidebar.markdown(
    """
    Filter the dataset to explore specific customer segments.

    **Available filters**
    - Geography
    - Engagement status
    - Number of products
    - Account balance
    - Estimated salary
    """
)

st.sidebar.divider()

st.sidebar.header("Customer Filters")

geographies = sorted(df["Geography"].dropna().unique())

selected_geographies = st.sidebar.multiselect(
    "Select Geography",
    options=geographies,
    default=geographies
)

engagement_options = ["Active", "Inactive"]

selected_engagement = st.sidebar.multiselect(
    "Engagement Status",
    options=engagement_options,
    default=engagement_options
)

product_options = sorted(df["NumOfProducts"].dropna().unique())

selected_products = st.sidebar.multiselect(
    "Number of Products",
    options=product_options,
    default=product_options
)

min_balance = float(df["Balance"].min())
max_balance = float(df["Balance"].max())

balance_range = st.sidebar.slider(
    "Balance Range",
    min_value=min_balance,
    max_value=max_balance,
    value=(min_balance, max_balance)
)

min_salary = float(df["EstimatedSalary"].min())
max_salary = float(df["EstimatedSalary"].max())

salary_range = st.sidebar.slider(
    "Estimated Salary Range",
    min_value=min_salary,
    max_value=max_salary,
    value=(min_salary, max_salary)
)

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df[
    (df["Geography"].isin(selected_geographies))
    & (df["Engagement_Status"].isin(selected_engagement))
    & (df["NumOfProducts"].isin(selected_products))
    & (df["Balance"].between(balance_range[0], balance_range[1]))
    & (
        df["EstimatedSalary"].between(
            salary_range[0], salary_range[1]
        )
    )
].copy()

# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

total_customers = len(filtered_df)

churn_rate = (
    filtered_df["Exited"].mean() * 100
    if total_customers > 0 else 0
)

retention_rate = 100 - churn_rate if total_customers > 0 else 0

active_customers = (
    filtered_df["IsActiveMember"].sum()
    if total_customers > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Churn Rate",
    f"{churn_rate:.2f}%"
)

col3.metric(
    "Retention Rate",
    f"{retention_rate:.2f}%"
)

col4.metric(
    "Active Customers",
    f"{active_customers:,}"
)

st.divider()

# --------------------------------------------------
# CUSTOMER DATA PREVIEW
# --------------------------------------------------

st.subheader("Customer Data Preview")

st.dataframe(
    filtered_df[
        [
            "CustomerId",
            "Geography",
            "Age",
            "Balance",
            "NumOfProducts",
            "Engagement_Status",
            "Customer_Status",
            "Relationship_Strength_Index"
        ]
    ],
    use_container_width=True
)

st.caption(
    "Use the filters in the sidebar to explore different customer segments."
)
# --------------------------------------------------
# ENGAGEMENT VS CHURN ANALYSIS
# --------------------------------------------------

st.divider()

st.header("1. Engagement vs. Churn Analysis")

if filtered_df.empty:
    st.warning("No customers match the selected filters.")

else:
    engagement_summary = (
        filtered_df.groupby("Engagement_Status")
        .agg(
            Total_Customers=("CustomerId", "count"),
            Churned_Customers=("Exited", "sum")
        )
        .reset_index()
    )

    engagement_summary["Churn_Rate"] = (
        engagement_summary["Churned_Customers"]
        / engagement_summary["Total_Customers"]
    ) * 100

    col1, col2 = st.columns(2)

    with col1:
        fig_engagement = px.bar(
            engagement_summary,
            x="Engagement_Status",
            y="Total_Customers",
            color="Engagement_Status",
            title="Customer Count by Engagement Status",
            labels={
                "Engagement_Status": "Engagement Status",
                "Total_Customers": "Number of Customers"
            },
            text_auto=True
        )

        st.plotly_chart(
            fig_engagement,
            use_container_width=True
        )

    with col2:
        fig_churn = px.bar(
            engagement_summary,
            x="Engagement_Status",
            y="Churn_Rate",
            color="Engagement_Status",
            title="Churn Rate by Engagement Status",
            labels={
                "Engagement_Status": "Engagement Status",
                "Churn_Rate": "Churn Rate (%)"
            },
            text_auto=".2f"
        )

        fig_churn.update_layout(
            yaxis_title="Churn Rate (%)"
        )

        st.plotly_chart(
            fig_churn,
            use_container_width=True
        )

    st.subheader("Engagement Analysis Summary")

    st.dataframe(
        engagement_summary.round(2),
        use_container_width=True,
        hide_index=True
    )
    # --------------------------------------------------
# PRODUCT UTILIZATION ANALYSIS
# --------------------------------------------------

st.divider()

st.header("2. Product Utilization Analysis")

if filtered_df.empty:
    st.warning("No customers match the selected filters.")

else:
    product_summary = (
        filtered_df.groupby("NumOfProducts")
        .agg(
            Total_Customers=("CustomerId", "count"),
            Churned_Customers=("Exited", "sum"),
            Retained_Customers=("Exited", lambda x: (x == 0).sum())
        )
        .reset_index()
    )

    product_summary["Churn_Rate"] = (
        product_summary["Churned_Customers"]
        / product_summary["Total_Customers"]
    ) * 100

    product_summary["Retention_Rate"] = (
        product_summary["Retained_Customers"]
        / product_summary["Total_Customers"]
    ) * 100

    col1, col2 = st.columns(2)

    with col1:
        fig_products = px.bar(
            product_summary,
            x="NumOfProducts",
            y="Total_Customers",
            title="Customer Distribution by Number of Products",
            labels={
                "NumOfProducts": "Number of Products",
                "Total_Customers": "Number of Customers"
            },
            text_auto=True
        )

        st.plotly_chart(
            fig_products,
            use_container_width=True
        )

    with col2:
        fig_product_churn = px.bar(
            product_summary,
            x="NumOfProducts",
            y="Churn_Rate",
            title="Churn Rate by Number of Products",
            labels={
                "NumOfProducts": "Number of Products",
                "Churn_Rate": "Churn Rate (%)"
            },
            text_auto=".2f"
        )

        fig_product_churn.update_layout(
            yaxis_title="Churn Rate (%)"
        )

        st.plotly_chart(
            fig_product_churn,
            use_container_width=True
        )

    st.subheader("Product Utilization Summary")

    st.dataframe(
        product_summary.round(2),
        use_container_width=True,
        hide_index=True
    )
    # --------------------------------------------------
# HIGH-VALUE DISENGAGED CUSTOMER DETECTOR
# --------------------------------------------------

st.divider()

st.header("3. High-Value Disengaged Customer Detector")

st.markdown(
    """
    Identify inactive customers with relatively high balances.
    These customers may be candidates for targeted retention campaigns.
    """
)

if filtered_df.empty:
    st.warning("No customers match the selected filters.")

else:
    # Calculate the 75th percentile within the filtered dataset
    balance_threshold = filtered_df["Balance"].quantile(0.75)

    # Identify high-balance, inactive customers
    high_value_disengaged = filtered_df[
        (filtered_df["Balance"] >= balance_threshold)
        & (filtered_df["IsActiveMember"] == 0)
    ].copy()

    total_high_value_disengaged = len(high_value_disengaged)

    churned_high_value = int(
        high_value_disengaged["Exited"].sum()
    )

    high_value_churn_rate = (
        high_value_disengaged["Exited"].mean() * 100
        if total_high_value_disengaged > 0
        else 0
    )

    # Display summary metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "High-Balance Inactive Customers",
        f"{total_high_value_disengaged:,}"
    )

    col2.metric(
        "Already Churned",
        f"{churned_high_value:,}"
    )

    col3.metric(
        "Churn Rate in This Group",
        f"{high_value_churn_rate:.2f}%"
    )

    st.caption(
        f"High-balance threshold for the current filters: "
        f"{balance_threshold:,.2f}"
    )

    # Display customer details
    st.subheader("High-Value Disengaged Customer List")

    customer_columns = [
        "CustomerId",
        "Geography",
        "Age",
        "Balance",
        "NumOfProducts",
        "EstimatedSalary",
        "Customer_Status"
    ]

    st.dataframe(
        high_value_disengaged[customer_columns].sort_values(
            "Balance",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    # Download the customer list
    csv_data = high_value_disengaged[customer_columns].to_csv(
        index=False
    )

    st.download_button(
        label="Download High-Value Customer List",
        data=csv_data,
        file_name="high_value_disengaged_customers.csv",
        mime="text/csv"
    )
    # --------------------------------------------------
# RELATIONSHIP STRENGTH ANALYSIS
# --------------------------------------------------

st.divider()

st.header("4. Relationship Strength Analysis")

st.markdown(
    """
    The Relationship Strength Index (RSI) is a custom score
    combining customer engagement and product usage.

    A higher score indicates a higher score under this project's
    chosen scoring method. It is not a validated measure of loyalty.
    """
)

if filtered_df.empty:
    st.warning("No customers match the selected filters.")

else:
    # Calculate average RSI
    average_rsi = filtered_df[
        "Relationship_Strength_Index"
    ].mean()

    # Calculate average RSI by customer status
    rsi_summary = (
        filtered_df.groupby("Customer_Status")
        .agg(
            Total_Customers=("CustomerId", "count"),
            Average_RSI=("Relationship_Strength_Index", "mean"),
            Median_RSI=("Relationship_Strength_Index", "median")
        )
        .reset_index()
    )

    # Display KPI
    st.metric(
        "Average Relationship Strength Index",
        f"{average_rsi:.2f} / 100"
    )

    # Compare RSI between retained and churned customers
    fig_rsi = px.box(
        filtered_df,
        x="Customer_Status",
        y="Relationship_Strength_Index",
        color="Customer_Status",
        title="Relationship Strength by Customer Status",
        labels={
            "Customer_Status": "Customer Status",
            "Relationship_Strength_Index": "Relationship Strength Index"
        }
    )

    st.plotly_chart(
        fig_rsi,
        use_container_width=True
    )

    # Average RSI comparison
    fig_rsi_average = px.bar(
        rsi_summary,
        x="Customer_Status",
        y="Average_RSI",
        color="Customer_Status",
        title="Average Relationship Strength by Customer Status",
        labels={
            "Customer_Status": "Customer Status",
            "Average_RSI": "Average RSI"
        },
        text_auto=".2f"
    )

    st.plotly_chart(
        fig_rsi_average,
        use_container_width=True
    )

    # Display summary
    st.subheader("Relationship Strength Summary")

    st.dataframe(
        rsi_summary.round(2),
        use_container_width=True,
        hide_index=True
    )
    # --------------------------------------------------
# EXECUTIVE INSIGHTS AND RETENTION RECOMMENDATIONS
# --------------------------------------------------

st.divider()

st.header("5. Executive Insights & Retention Recommendations")

if filtered_df.empty:
    st.warning("No customers match the selected filters.")

else:
    # Calculate customer engagement and churn statistics
    active_df = filtered_df[
        filtered_df["IsActiveMember"] == 1
    ]

    inactive_df = filtered_df[
        filtered_df["IsActiveMember"] == 0
    ]

    active_churn_rate = (
        active_df["Exited"].mean() * 100
        if not active_df.empty else 0
    )

    inactive_churn_rate = (
        inactive_df["Exited"].mean() * 100
        if not inactive_df.empty else 0
    )

    high_balance_inactive = filtered_df[
        (filtered_df["High_Balance"])
        & (filtered_df["IsActiveMember"] == 0)
        & (filtered_df["Exited"] == 0)
    ]

    # Executive summary
    st.subheader("Executive Summary")

    st.write(
        f"The selected customer segment contains "
        f"**{len(filtered_df):,} customers**, with a churn rate of "
        f"**{filtered_df['Exited'].mean() * 100:.2f}%**."
    )

    # Compare engagement groups
    st.subheader("Key Findings")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Active Customer Churn Rate",
            f"{active_churn_rate:.2f}%"
        )

    with col2:
        st.metric(
            "Inactive Customer Churn Rate",
            f"{inactive_churn_rate:.2f}%"
        )

    if not active_df.empty and not inactive_df.empty:
        if inactive_churn_rate > active_churn_rate:
            st.info(
                "Finding: In this filtered segment, inactive customers "
                "have a higher observed churn rate than active customers."
            )
        elif active_churn_rate > inactive_churn_rate:
            st.info(
                "Finding: In this filtered segment, active customers "
                "have a higher observed churn rate than inactive customers. "
                "Investigate the customer mix before drawing conclusions."
            )
        else:
            st.info(
                "Finding: Active and inactive customers have the same "
                "observed churn rate in this filtered segment."
            )

    st.write(
        f"**High-balance, inactive customers who have not churned:** "
        f"{len(high_balance_inactive):,}"
    )

    # Recommendations
    st.subheader("Recommended Retention Actions")

    st.markdown(
        """
        **1. Improve engagement**

        Consider targeted service reminders, relevant product education,
        and voluntary feedback surveys for inactive customers.

        **2. Review high-balance inactive customers**

        Prioritize appropriate, personalized outreach to eligible customers
        who have high balances but remain inactive. Use service history and
        customer preferences before deciding on an intervention.

        **3. Review product utilization**

        Examine whether customers with different product counts have
        different churn patterns. Offer additional products only where
        they meet genuine customer needs.

        **4. Monitor retention performance**

        Track churn rate, retention rate, engagement, and product usage
        over time to assess whether retention initiatives are effective.

        **5. Test before scaling**

        Pilot retention initiatives with a suitable comparison group.
        Measure results before expanding the program.
        """
    )

    st.caption(
        "These recommendations are based on descriptive analysis. "
        "They do not establish causation or predict individual churn."
    )
    # --------------------------------------------------
# DASHBOARD FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Customer Engagement & Retention Analytics | "
    "Data-driven customer retention analysis"
)

st.caption(
    "Note: This dashboard presents descriptive analysis. "
    "Observed associations do not establish causation, and "
    "the Relationship Strength Index is a custom project metric."
)