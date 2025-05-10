# ==============================
# Hope Foundation Dashboard
# QQ 2025 - ECON project
# ==============================

# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

import plotly.io as pio # set up plotly template
pio.templates.default = "plotly_dark"  # apply dark theme to all plotly charts

# Set page configuration
st.set_page_config(page_title="Hope Foundation Dashboard", layout="wide")
# ====================
# Add dark theme
# ====================
st.markdown(
    """
    <style>
    body {
        background-color: #0E1117;
        color: #FFFFFF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stApp {
        background-color: #0E1117;
    }
    h1, h2, h3 {
        color: #3399FF;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5em 1em;
        font-size: 1em;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Load data
df = pd.read_csv("cleaned_hope_data.csv")
# Clean Pt State values
df["Pt State"] = df["Pt State"].astype(str).str.upper().str.strip()
df["Pt State"] = df["Pt State"].replace("NONE", "UNKNOWN")

# Title
st.title("Hope Foundation Patient Assistance Dashboard")

# Main KPIs
total_requests = len(df)
total_amount = pd.to_numeric(df["Amount"], errors='coerce').sum()
unique_patients = df["Patient ID#"].nunique()

# Display KPIs
st.metric(label="Total Grant Requests", value=total_requests)
st.metric(label="Total Amount Granted ($)", value=f"${total_amount:,.2f}")
st.metric(label="Unique Patients", value=unique_patients)

# Sidebar filters
st.sidebar.header("Filter Options")
state_filter = st.sidebar.multiselect(
    "Select States",
    options=df["Pt State"].dropna().unique(),
    default=df["Pt State"].dropna().unique()
)
year_filter = st.sidebar.multiselect(
    "Select Years",
    options=df["App Year"].dropna().unique(),
    default=df["App Year"].dropna().unique()
)

# Apply filters
filtered_df = df[
    (df["Pt State"].isin(state_filter)) & 
    (df["App Year"].isin(year_filter))
]

# Show filtered data table
st.subheader("Filtered Data Table")
st.dataframe(filtered_df)

# Plot 1: Amount by State
st.subheader("Total Grant Amount by State")
amount_by_state = filtered_df.groupby("Pt State")["Amount"].sum().reset_index()
fig1 = px.bar(amount_by_state, x="Pt State", y="Amount", title="Total Amount by State")
st.plotly_chart(fig1)

# Plot 2: Amount by Year
st.subheader("Total Grant Amount by Application Year")
amount_by_year = filtered_df.groupby("App Year")["Amount"].sum().reset_index()
fig2 = px.line(amount_by_year, x="App Year", y="Amount", title="Total Amount by Year")
st.plotly_chart(fig2)
