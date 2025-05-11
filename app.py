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
#Handle 'MISSING' and 'NAN' values
df["Pt State"] = df["Pt State"].replace(["MISSING", "NAN"], "UNKNOWN")
#Replace 'MISSING' and "NAN' in other columns with pd.NA
df.replace("MISSING", pd.NA, inplace=True)
df.replace("NAN", pd.NA, inplace=True)
# Fill missing 'Amount' values with the column's mean
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df = df[df['Amount'].notna()]
df['Amount'] = df['Amount'].astype(float)
# Fill missing 'Pt State' values with the mode
df['Pt State'].fillna(df['Pt State'].mode()[0], inplace=True)
# Save the cleaned data to new CSV file
df.to_csv('cleaned_hope_data_final.csv', index=False)

# Title
st.title("Hope Foundation Patient Assistance Dashboard")

# Main KPIs
total_requests = len(df)
total_amount = df['Amount'].sum()
unique_patients = df["Patient ID#"].nunique()

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

# Show filtered data
t.st.subheader("Filtered Data Table")
st.dataframe(filtered_df)

# Step 1: Total Support by State and Gender
st.subheader("Total Support by State and Gender")
support_by_demo = filtered_df.groupby(["Pt State", "Gender"])["Amount"].sum().reset_index()
fig_demo = px.bar(
    support_by_demo,
    x="Pt State",
    y="Amount",
    color="Gender",
    title="Total Support by State and Gender"
)
st.plotly_chart(fig_demo)

# Step 2: Applications Ready for Review
st.subheader("Applications Ready for Review")
ready_apps = filtered_df[filtered_df["Application Signed?"] == "Yes"]
st.write(f"Total Ready Applications: {len(ready_apps)}")
st.dataframe(ready_apps)

# Step 3: Patients Who Did Not Use Full Grant Amount
st.subheader("Patients Who Did Not Use Full Grant Amount")
not_used_full = filtered_df[filtered_df["Remaining Balance"] > 0]
st.write(f"Total Patients with Unused Grant Funds: {len(not_used_full)}")
st.dataframe(not_used_full)

# Step 4: Impact Summary for Past 12 Months
st.subheader("Impact Summary for the Past 12 Months")
filtered_df["Grant Req Date"] = pd.to_datetime(filtered_df["Grant Req Date"], errors='coerce')
recent_12_months = filtered_df[filtered_df["Grant Req Date"] >= (pd.Timestamp.now() - pd.DateOffset(months=12))]
recent_12_months["Amount"] = pd.to_numeric(recent_12_months["Amount"], errors='coerce')
total_requests = len(recent_12_months)
total_amount = recent_12_months["Amount"].sum()
unique_patients = recent_12_months["Patient ID#"].nunique()
avg_grant = total_amount / unique_patients if unique_patients > 0 else 0
st.write(f"Total Requests in Past 12 Months: {total_requests}")
st.write(f"Total Amount Granted: ${total_amount:,.2f}")
st.write(f"Total Unique Patients: {unique_patients}")
st.write(f"Average Grant per Patient: ${avg_grant:,.2f}")

# Step 5: Time to Support Analysis
st.subheader("Time to Support Analysis")
filtered_df["Grant Req Date"] = pd.to_datetime(filtered_df["Grant Req Date"], errors='coerce')
filtered_df["Payment Submitted?"] = pd.to_datetime(filtered_df["Payment Submitted?"], errors='coerce')
support_df = filtered_df.dropna(subset=["Grant Req Date", "Payment Submitted?"])
support_df["Days to Support"] = (support_df["Payment Submitted?"] - support_df["Grant Req Date"]).dt.days
support_df = support_df[support_df["Days to Support"] >= 0]
total_requests = len(support_df)
avg_days = support_df["Days to Support"].mean()
min_days = support_df["Days to Support"].min()
max_days = support_df["Days to Support"].max()
st.write(f"Total Records with Payment Date: {total_requests}")
st.write(f"Average Time to Support: {avg_days:.2f} days")
st.write(f"Fastest Time to Support: {min_days} days")
st.write(f"Slowest Time to Support: {max_days} days")
fig_time = px.histogram(
    support_df,
    x="Days to Support",
    nbins=30,
    title="Distribution of Time to Support (Days)"
)
st.plotly_chart(fig_time)

# Step 6: Additional Impact Visualizations
st.subheader("Total Grant Amount by State")
amount_by_state = filtered_df.groupby("Pt State")["Amount"].sum().reset_index()
fig1 = px.bar(amount_by_state, x="Pt State", y="Amount", title="Total Amount by State")
st.plotly_chart(fig1)

st.subheader("Total Grant Amount by Application Year")
amount_by_year = filtered_df.groupby("App Year")["Amount"].sum().reset_index()
fig2 = px.line(amount_by_year, x="App Year", y="Amount", title="Total Amount by Year")
st.plotly_chart(fig2)

