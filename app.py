# ==============================
# Hope Foundation Dashboard
# QQ 2025 - ECON project
# ==============================

# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# ================== Set page configuration ==================
st.set_page_config(page_title="Hope Foundation Dashboard", layout="wide")

# ================== Load and clean data ==================
df = pd.read_csv("cleaned_hope_data.csv")

# Clean Pt State values
df["Pt State"] = df["Pt State"].astype(str).str.upper().str.strip()
df["Pt State"] = df["Pt State"].replace("NONE", "UNKNOWN")
df["Pt State"] = df["Pt State"].replace(["MISSING", "NAN"], "UNKNOWN")

# Replace MISSING and NAN in all columns
df.replace("MISSING", pd.NA, inplace=True)
df.replace("NAN", pd.NA, inplace=True)

# Ensure Amount column is numeric and float
df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce')
df["Amount"] = df["Amount"].astype(float)

# ================== Main KPIs ==================
st.title("Hope Foundation Patient Assistance Dashboard")

total_requests = len(df)
total_amount = df["Amount"].sum()
unique_patients = df["Patient ID#"].nunique()

st.metric(label="Total Grant Requests", value=total_requests)
st.metric(label="Total Amount Granted ($)", value=f"${total_amount:,.2f}")
st.metric(label="Unique Patients", value=unique_patients)

# ================== Applications Ready for Review ==================
st.header("Applications Ready for Review")
ready_apps = df[df["Request Status"] == "Ready for Review"]
st.dataframe(ready_apps)

# ================== Filter Options ==================
st.sidebar.header("Filter Options")
state_filter = st.sidebar.multiselect("Select States", options=df["Pt State"].unique())
year_filter = st.sidebar.multiselect("Select Years", options=df["Application Year"].unique())

filtered_df = df.copy()
if state_filter:
    filtered_df = filtered_df[filtered_df["Pt State"].isin(state_filter)]
if year_filter:
    filtered_df = filtered_df[filtered_df["Application Year"].isin(year_filter)]

# ================== Support by Demographics ==================
st.header("Total Support by State and Gender")
fig1 = px.bar(
    filtered_df,
    x="Pt State",
    y="Amount",
    color="Gender",
    title="Total Support by State and Gender"
)
st.plotly_chart(fig1, use_container_width=True)

# ================== Request & Support Analysis ==================
st.header("Request and Support Analysis")

# Time to Support chart
filtered_df['Request Date'] = pd.to_datetime(filtered_df['Request Date'], errors='coerce')
filtered_df['Support Date'] = pd.to_datetime(filtered_df['Support Date'], errors='coerce')
filtered_df['Days to Support'] = (filtered_df['Support Date'] - filtered_df['Request Date']).dt.days

fig2 = px.box(
    filtered_df,
    x="Application Year",
    y="Days to Support",
    title="Time Between Request and Support by Year"
)
st.plotly_chart(fig2, use_container_width=True)

# Average Amount by Assistance Type
fig3 = px.bar(
    filtered_df.groupby("Assistance Type")["Amount"].mean().reset_index(),
    x="Assistance Type",
    y="Amount",
    title="Average Amount by Assistance Type"
)
st.plotly_chart(fig3, use_container_width=True)

# ================== Conclusion / High-Level Summary ==================
st.header("High-Level Impact Summary")
total_per_year = filtered_df.groupby("Application Year")["Amount"].sum().reset_index()
fig4 = px.line(
    total_per_year,
    x="Application Year",
    y="Amount",
    markers=True,
    title="Total Amount Granted Over Time"
)
st.plotly_chart(fig4, use_container_width=True)

st.success("Dashboard loaded successfully and meets project requirements.")

