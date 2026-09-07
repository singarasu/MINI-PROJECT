"""
==============================================================================
Online Shopping Customer Analysis — Interactive Streamlit Dashboard
==============================================================================
Run with:
  streamlit run python-dashboard/app.py
  (or inside python-dashboard/ directory: streamlit run app.py)
==============================================================================
"""

import os
import pandas as pd
import plotly.express as px
import streamlit as st

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "shopping_trends.csv")

# Fallback check
if not os.path.exists(DATA_PATH):
    # Try local data directory if run inside different layout
    DATA_PATH = os.path.join(CURRENT_DIR, "data", "shopping_trends.csv")

# ---------- Page setup ----------
st.set_page_config(
    page_title="Online Shopping Customer Analysis",
    page_icon="🛍️",
    layout="wide",
)


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


df = load_data(DATA_PATH)

st.title("🛍️ Online Shopping Customer Analysis")
st.caption(f"{len(df):,} customer orders · {df.shape[1]} attributes · Author: Sellammal S (Reg. No: 25127055)")

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")

categories = sorted(df["Category"].unique())
selected_categories = st.sidebar.multiselect(
    "Category", categories, default=categories
)

seasons = sorted(df["Season"].unique())
selected_seasons = st.sidebar.multiselect("Season", seasons, default=seasons)

age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
age_range = st.sidebar.slider("Age range", age_min, age_max, (age_min, age_max))

filtered = df[
    df["Category"].isin(selected_categories)
    & df["Season"].isin(selected_seasons)
    & df["Age"].between(age_range[0], age_range[1])
]

st.sidebar.markdown(f"**{len(filtered):,}** orders match your filters")

# ---------- KPI row ----------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Orders", f"{len(filtered):,}")
col2.metric("Avg Order Value", f"${filtered['Purchase Amount (USD)'].mean():,.2f}")
col3.metric("Avg Rating", f"{filtered['Review Rating'].mean():.2f} / 5")
subscriber_pct = (filtered["Subscription Status"] == "Yes").mean() * 100
col4.metric("Subscribers", f"{subscriber_pct:.1f}%")

st.divider()

# ---------- Row 1: Category volume + avg value ----------
c1, c2 = st.columns(2)

with c1:
    cat_counts = filtered["Category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Orders"]
    fig = px.bar(
        cat_counts, x="Category", y="Orders",
        title="Orders by Category", color="Category",
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    cat_avg = (
        filtered.groupby("Category")["Purchase Amount (USD)"]
        .mean()
        .round(2)
        .reset_index()
        .sort_values("Purchase Amount (USD)", ascending=False)
    )
    fig = px.bar(
        cat_avg, x="Category", y="Purchase Amount (USD)",
        title="Average Order Value by Category", color="Category",
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ---------- Row 2: Payment method + Season ----------
c3, c4 = st.columns(2)

with c3:
    pay_counts = filtered["Payment Method"].value_counts().reset_index()
    pay_counts.columns = ["Payment Method", "Orders"]
    fig = px.pie(
        pay_counts, names="Payment Method", values="Orders",
        title="Payment Method Distribution", hole=0.4,
    )
    st.plotly_chart(fig, use_container_width=True)

with c4:
    season_counts = filtered["Season"].value_counts().reset_index()
    season_counts.columns = ["Season", "Orders"]
    fig = px.bar(
        season_counts, x="Season", y="Orders",
        title="Orders by Season", color="Season",
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ---------- Row 3: Rating distribution + Subscription ----------
c5, c6 = st.columns(2)

with c5:
    fig = px.histogram(
        filtered, x="Review Rating", nbins=20,
        title="Review Rating Distribution",
    )
    st.plotly_chart(fig, use_container_width=True)

with c6:
    sub_counts = filtered["Subscription Status"].value_counts().reset_index()
    sub_counts.columns = ["Subscription Status", "Customers"]
    fig = px.pie(
        sub_counts, names="Subscription Status", values="Customers",
        title="Subscriber vs Non-Subscriber", hole=0.4,
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------- Row 4: Age distribution ----------
fig = px.histogram(
    filtered, x="Age", nbins=30, marginal="box",
    title="Customer Age Distribution",
)
st.plotly_chart(fig, use_container_width=True)

# ---------- Raw data (optional) ----------
with st.expander("View filtered raw data"):
    st.dataframe(filtered, use_container_width=True)
