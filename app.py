# ==============================
# Hope Foundation Dashboard
# QQ 2025 - ECON project
# ==============================

# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px


# Set page configuration
st.set_page_config(page_title="Hope Foundation Dashboard", layout="wide")


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
# =====================================
# Step 1: Applications Ready for Review (new page)
# =====================================
st.subheader("Applications Ready for Review")
# Filter the dataset to include only rows where 'Application Signed?' equals 'Yes'
ready_apps = filtered_df[filtered_df["Application Signed?"] == "Yes"]
# Display the total count of ready applications
st.write(f"Total Ready Applications: {len(ready_apps)}")
# Display the filtered dataset in a table format
st.dataframe(ready_apps)

# =====================================
# Step 2: Total Support by State and Gender
# =====================================
# Add a subheader for this section
st.subheader("Total Support by State and Gender")
# Group the data by Pt State and Patient Gender, and sum the Amount
support_by_demo = filtered_df.groupby(["Pt State", "Patient Gender"])["Amount"].sum().reset_index()
# Create a bar chart showing total support by demographic groups
fig_demo = px.bar(
    support_by_demo,
    x="Pt State",
    y="Amount",
    color="Patient Gender",
    title="Total Support by State and Gender"
)
# Display the chart
st.plotly_chart(fig_demo)

# ========================================
# Step 3: Applications Ready for Review Page
# ========================================
# Add a new section for applications that are ready for review
st.subheader("Applications Ready for Review")
# Filter the dataset to only include applications where the 'Signed?' field is 'Yes'
ready_apps = filtered_df[filtered_df["Signed?"] == "Yes"]
# Display the total number of ready applications
st.write(f"Total Ready Applications: {len(ready_apps)}")
# Display the list of ready applications in a table
st.dataframe(ready_apps)

# ========================================
# Step 4: Patients Who Did Not Use Full Grant Amount
# ========================================
# Add a subheader for this section
st.subheader("Patients Who Did Not Use Full Grant Amount")
# Filter records where the Remaining Balance column is greater than zero
not_used_full = filtered_df[filtered_df["Remaining Balance"] > 0]
# Show total number of patients with remaining balances
st.write(f"Total Patients with Unused Grant Funds: {len(not_used_full)}")
# Display the table of patients who did not fully use their grant
st.dataframe(not_used_full)

# ========================================
# Step 5: Impact Summary for Past 12 Months
# ========================================
# Add a subheader for this section
st.subheader("Impact Summary for the Past 12 Months")
# Convert 'Grant Req Date' column to datetime format
filtered_df["Grant Req Date"] = pd.to_datetime(filtered_df["Grant Req Date"], errors='coerce')
# Filter records where Grant Req Date is within the past 12 months
recent_12_months = filtered_df[filtered_df["Grant Req Date"] >= (pd.Timestamp.now() - pd.DateOffset(months=12))]
# Calculate summary metrics for the filtered data
total_requests = len(recent_12_months)
total_amount = recent_12_months["Amount"].sum()
unique_patients = recent_12_months["Patient ID#"].nunique()
avg_grant = total_amount / unique_patients if unique_patients > 0 else 0
# Display the calculated metrics
st.write(f"Total Requests in Past 12 Months: {total_requests}")
st.write(f"Total Amount Granted: ${total_amount:,.2f}")
st.write(f"Total Unique Patients: {unique_patients}")
st.write(f"Average Grant per Patient: ${avg_grant:,.2f}")




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
