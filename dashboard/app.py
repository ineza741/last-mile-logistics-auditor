"""
Last Mile Logistics Auditor - Streamlit Dashboard
==================================================
Professional delivery performance dashboard for Veridi Logistics.

Run with: streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# ==================================================
# PATH CONFIGURATION
# ==================================================
# Safe path that works both locally and on Streamlit Cloud

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "outputs" / "cleaned_delivery_data.csv"

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Last Mile Logistics Auditor",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    """Load and prepare the cleaned delivery data."""
    # Read the CSV file using safe path
    df = pd.read_csv(DATA_PATH)
    
    # Convert date columns back to datetime
    date_columns = [
        'order_purchase_timestamp',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df

# Load the data
df = load_data()

# ==================================================
# SIDEBAR FILTERS
# ==================================================

st.sidebar.header("🔍 Filters")

# Filter 1: Customer State
# Get all unique states and add "All" option
all_states = ['All'] + sorted(df['customer_state'].dropna().unique().tolist())
selected_state = st.sidebar.selectbox("Select Customer State", all_states)

# Filter 2: Product Category
# Get all unique categories and add "All" option
all_categories = ['All'] + sorted(df['product_category_name_english'].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select Product Category", all_categories)

# Apply filters to create filtered dataframe
filtered_df = df.copy()

# Filter by state if a specific state is selected
if selected_state != 'All':
    filtered_df = filtered_df[filtered_df['customer_state'] == selected_state]

# Filter by category if a specific category is selected
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['product_category_name_english'] == selected_category]

# ==================================================
# MAIN TITLE
# ==================================================

st.title("🚚 Last Mile Logistics Auditor")
st.markdown("**Delivery Performance & Customer Satisfaction Analysis**")
st.markdown("---")

# ==================================================
# TOP KPI CARDS
# ==================================================

# Calculate KPIs from filtered data
total_orders = filtered_df['order_id'].nunique()
late_orders = filtered_df[filtered_df['delivery_status'].isin(['Late', 'Super Late'])]['order_id'].nunique()
super_late_orders = filtered_df[filtered_df['delivery_status'] == 'Super Late']['order_id'].nunique()
avg_review = filtered_df['review_score'].mean()

# Calculate percentages
late_pct = (late_orders / total_orders * 100) if total_orders > 0 else 0
super_late_pct = (super_late_orders / total_orders * 100) if total_orders > 0 else 0

# Display KPI cards in 4 columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Delivered Orders", f"{total_orders:,}")

with col2:
    st.metric("Late Delivery %", f"{late_pct:.1f}%")

with col3:
    st.metric("Average Review Score", f"{avg_review:.2f}")

with col4:
    st.metric("Super Late %", f"{super_late_pct:.1f}%")

st.markdown("---")

# ==================================================
# CHART 1: GEOGRAPHIC DELIVERY PERFORMANCE
# ==================================================

st.subheader("📊 Chart 1: Geographic Delivery Performance")
st.markdown("**Question:** Which states have the worst delivery?")

# Calculate delivery metrics by state
state_delivery = filtered_df.groupby('customer_state').agg(
    total_orders=('order_id', 'count'),
    late_orders=('delivery_status', lambda x: x.isin(['Late', 'Super Late']).sum()),
    avg_review=('review_score', 'mean')
).reset_index()

# Force columns to numeric for safe calculation
state_delivery["late_orders"] = pd.to_numeric(state_delivery["late_orders"], errors="coerce").fillna(0)
state_delivery["total_orders"] = pd.to_numeric(state_delivery["total_orders"], errors="coerce").fillna(0)

# Calculate late percentage safely
state_delivery["late_percentage"] = np.where(
    state_delivery["total_orders"] > 0,
    (state_delivery["late_orders"] / state_delivery["total_orders"]) * 100,
    0
).round(2)

# Sort by late percentage descending
state_delivery = state_delivery.sort_values('late_percentage', ascending=False)

# Create bar chart
fig1 = px.bar(
    state_delivery,
    x='customer_state',
    y='late_percentage',
    title='Late Delivery Percentage by State',
    labels={'customer_state': 'State', 'late_percentage': 'Late %'},
    color='late_percentage',
    color_continuous_scale='Reds'
)
fig1.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig1, use_container_width=True)

# ==================================================
# CHART 2: DELIVERY STATUS VS CUSTOMER REVIEW
# ==================================================

st.subheader("📊 Chart 2: Delivery Status vs Customer Review")
st.markdown("**Question:** Do delays reduce customer satisfaction?")

# Calculate average review by delivery status
review_by_status = filtered_df.groupby('delivery_status').agg(
    avg_review=('review_score', 'mean'),
    count=('order_id', 'count')
).reset_index()

# Sort by delivery severity
status_order = ['On Time', 'Late', 'Super Late']
review_by_status['delivery_status'] = pd.Categorical(
    review_by_status['delivery_status'],
    categories=status_order,
    ordered=True
)
review_by_status = review_by_status.sort_values('delivery_status')

# Create bar chart
fig2 = px.bar(
    review_by_status,
    x='delivery_status',
    y='avg_review',
    title='Impact of Delivery Delay on Customer Reviews',
    labels={'delivery_status': 'Delivery Status', 'avg_review': 'Average Review Score'},
    color='delivery_status',
    color_discrete_map={'On Time': 'green', 'Late': 'orange', 'Super Late': 'red'}
)
fig2.update_layout(yaxis_range=[0, 5])
st.plotly_chart(fig2, use_container_width=True)

# ==================================================
# CHART 3: DELAY DAYS VS REVIEW SCORE
# ==================================================

st.subheader("📊 Chart 3: Delivery Delay vs Customer Sentiment")

# Create scatter plot
fig3 = px.scatter(
    filtered_df,
    x='delay_days',
    y='review_score',
    color='delivery_status',
    title='Delivery Delay vs Customer Sentiment',
    labels={'delay_days': 'Delay Days', 'review_score': 'Review Score'},
    color_discrete_map={'On Time': 'green', 'Late': 'orange', 'Super Late': 'red'},
    opacity=0.5
)
st.plotly_chart(fig3, use_container_width=True)

# ==================================================
# CHART 4: PRODUCT CATEGORY ANALYSIS
# ==================================================

st.subheader("📊 Chart 4: Product Category Analysis")
st.markdown("**Question:** Which product categories have delivery problems?")

# Calculate delivery metrics by product category
category_delivery = filtered_df.groupby('product_category_name_english').agg(
    total_orders=('order_id', 'count'),
    late_orders=('delivery_status', lambda x: x.isin(['Late', 'Super Late']).sum()),
    avg_review=('review_score', 'mean')
).reset_index()

# Force columns to numeric for safe calculation
category_delivery["late_orders"] = pd.to_numeric(category_delivery["late_orders"], errors="coerce").fillna(0)
category_delivery["total_orders"] = pd.to_numeric(category_delivery["total_orders"], errors="coerce").fillna(0)

# Calculate late percentage safely
category_delivery["late_percentage"] = np.where(
    category_delivery["total_orders"] > 0,
    (category_delivery["late_orders"] / category_delivery["total_orders"]) * 100,
    0
).round(2)

# Filter categories with at least 50 orders for meaningful analysis
category_delivery = category_delivery[category_delivery['total_orders'] >= 50]

# Sort by late percentage and take top 10
category_delivery = category_delivery.sort_values('late_percentage', ascending=False).head(10)

# Create bar chart
fig4 = px.bar(
    category_delivery,
    x='product_category_name_english',
    y='late_percentage',
    title='Top 10 Categories by Late Delivery Percentage',
    labels={'product_category_name_english': 'Category', 'late_percentage': 'Late %'},
    color='late_percentage',
    color_continuous_scale='Reds'
)
fig4.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig4, use_container_width=True)

# ==================================================
# CANDIDATE CHOICE FEATURE: STATE RISK SCORE
# ==================================================

st.subheader("🎯 Candidate Choice Feature: State Risk Score")
st.markdown("---")

# Create explanation box
st.info("""
**Risk Score Formula:** `risk_score = late_percentage * (5 - average_review_score)`

**Why this matters:** Risk Score combines operational delay and customer dissatisfaction. 
A high score means the region should be prioritized for logistics improvement.
""")

# Calculate risk score for each state
risk_analysis = filtered_df.groupby('customer_state').agg(
    total_orders=('order_id', 'count'),
    late_orders=('delivery_status', lambda x: x.isin(['Late', 'Super Late']).sum()),
    avg_review=('review_score', 'mean')
).reset_index()

# Force columns to numeric for safe calculation
risk_analysis["late_orders"] = pd.to_numeric(risk_analysis["late_orders"], errors="coerce").fillna(0)
risk_analysis["total_orders"] = pd.to_numeric(risk_analysis["total_orders"], errors="coerce").fillna(0)
risk_analysis["avg_review"] = pd.to_numeric(risk_analysis["avg_review"], errors="coerce").fillna(0)

# Calculate late percentage safely
risk_analysis["late_percentage"] = np.where(
    risk_analysis["total_orders"] > 0,
    (risk_analysis["late_orders"] / risk_analysis["total_orders"]) * 100,
    0
).round(2)

# Calculate risk score safely
risk_analysis["risk_score"] = (
    risk_analysis["late_percentage"] * (5 - risk_analysis["avg_review"])
).round(2)

# Sort by risk score descending
risk_analysis = risk_analysis.sort_values('risk_score', ascending=False)

# Create display table with selected columns
risk_table = risk_analysis[['customer_state', 'late_percentage', 'avg_review', 'risk_score']].copy()
risk_table.columns = ['State', 'Late %', 'Avg Review Score', 'Risk Score']

# Display the table
st.dataframe(risk_table, use_container_width=True, hide_index=True)

# ==================================================
# EXECUTIVE INSIGHT SECTION
# ==================================================

st.subheader("📋 Executive Insight")
st.markdown("---")

# Calculate dynamic insights from the data

# Worst performing state
worst_state = state_delivery.iloc[0]['customer_state']
worst_state_late_pct = state_delivery.iloc[0]['late_percentage']

# Best performing state
best_state = state_delivery.iloc[-1]['customer_state']
best_state_late_pct = state_delivery.iloc[-1]['late_percentage']

# Review score difference between On Time and Late
on_time_review = filtered_df[filtered_df['delivery_status'] == 'On Time']['review_score'].mean()
late_review = filtered_df[filtered_df['delivery_status'] == 'Late']['review_score'].mean()
review_difference = on_time_review - late_review

# Display business summary
st.markdown("### Business Summary for Veridi Logistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Worst Performing State",
        f"{worst_state}",
        f"{worst_state_late_pct:.1f}% late"
    )

with col2:
    st.metric(
        "Best Performing State",
        f"{best_state}",
        f"{best_state_late_pct:.1f}% late"
    )

with col3:
    st.metric(
        "Review Score Impact",
        f"{review_difference:.2f}",
        "On Time vs Late"
    )

st.markdown("---")

# Recommendation
st.markdown("### Recommendation")
st.write(f"""
Based on the analysis, here are the key findings:

1. **Worst State:** {worst_state} has the highest late delivery rate at {worst_state_late_pct:.1f}%
2. **Review Impact:** Late deliveries reduce review scores by {review_difference:.2f} points on average
3. **Priority Action:** Focus logistics improvements on {worst_state} to reduce delays and improve customer satisfaction

The Risk Score analysis shows that states with both high delay rates AND low review scores 
should be prioritized for immediate intervention.
""")

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")
st.markdown("*Last Mile Logistics Auditor - Built with Streamlit*")
