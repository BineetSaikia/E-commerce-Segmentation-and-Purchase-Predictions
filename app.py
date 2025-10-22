import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-commerce Customer Segmentation", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("segmented_customers.csv")

df = load_data()

st.title("🛒 E-commerce Customer Segmentation Dashboard")
st.markdown("""
Analyze customer behavior using RFM (Recency, Frequency, Monetary) metrics and visualize segment insights.
""")

# Sidebar filters
st.sidebar.header("Filters")
clusters = st.sidebar.multiselect(
    "Select Clusters",
    options=df["Cluster"].unique(),
    default=df["Cluster"].unique()
)
filtered_df = df[df["Cluster"].isin(clusters)]

# Layout
col1, col2 = st.columns(2)
with col1:
    st.subheader(" Cluster Summary")
    summary = filtered_df.groupby("Cluster").agg({
        "Recency": "mean",
        "Frequency": "mean",
        "Monetary": ["mean", "count"]
    }).round(2)
    st.dataframe(summary)

with col2:
    st.subheader("💰 Total Customers per Segment")
    cluster_counts = filtered_df["Cluster"].value_counts().reset_index()
    cluster_counts.columns = ["Cluster", "Count"]
    fig = px.pie(cluster_counts, names="Cluster", values="Count", title="Customer Distribution by Segment")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader(" Interactive RFM Scatter Plot")
x_axis = st.selectbox("Select X-axis", ["Recency", "Frequency", "Monetary"])
y_axis = st.selectbox("Select Y-axis", ["Recency", "Frequency", "Monetary"])

fig2 = px.scatter(
    filtered_df,
    x=x_axis,
    y=y_axis,
    color="Cluster",
    size="Monetary",
    hover_data=["Recency", "Frequency", "Monetary"],
    title=f"{x_axis} vs {y_axis} by Cluster"
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.subheader(" Key Insights")
st.markdown("""
- **Cluster 0:** High-frequency, high-value loyal customers → focus on retention  
- **Cluster 1:** Inactive users → target with win-back campaigns  
- **Cluster 2:** Medium spenders → upsell/cross-sell opportunities  
- **Cluster 3:** New customers → engage with onboarding offers  
""")

st.success("Dashboard Ready ")
