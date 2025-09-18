import streamlit as st
import pandas as pd
import os

# ----------------------
# Load Dataset
# ----------------------
st.title("OLA Ride Insights Dashboard")
st.markdown("Interactive analytics on OLA Rides using Streamlit + Power BI")

# Attempt to load CSV from local directory
csv_file = "Cleaned_OLA_Dataset.csv"
cwd = os.getcwd()
csv_path = os.path.join(cwd, csv_file)

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.success(f"CSV loaded from {csv_path}")
else:
    st.warning(f"File not found at {csv_path}. Please upload the CSV.")
    uploaded_file = st.file_uploader("Upload Cleaned_OLA_Dataset.csv", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("CSV loaded successfully!")
    else:
        st.stop()  # Stop app if no CSV available

# ----------------------
# Sidebar Filters
# ----------------------
st.sidebar.header("Filters")

# Date filter
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])  # remove rows where Date could not be parsed
min_date, max_date = df["Date"].min(), df["Date"].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Vehicle type filter
vehicle = st.sidebar.selectbox("Vehicle Type", ["All"] + list(df["Vehicle_Type"].unique()))

# Booking status filter
status = st.sidebar.selectbox("Booking Status", ["All"] + list(df["Booking_Status"].unique()))

# Payment method filter
payment = st.sidebar.selectbox("Payment Method", ["All"] + list(df["Payment_Method"].unique()))

# Apply filters
filtered_df = df.copy()
if date_range:
    filtered_df = filtered_df[(filtered_df["Date"] >= pd.to_datetime(date_range[0])) &
                              (filtered_df["Date"] <= pd.to_datetime(date_range[1]))]
if vehicle != "All":
    filtered_df = filtered_df[filtered_df["Vehicle_Type"] == vehicle]
if status != "All":
    filtered_df = filtered_df[filtered_df["Booking_Status"] == status]
if payment != "All":
    filtered_df = filtered_df[filtered_df["Payment_Method"] == payment]

# ----------------------
# KPI Cards
# ----------------------
st.subheader("Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Rides", len(filtered_df))
col2.metric("Total Revenue", round(filtered_df["Booking_Value"].sum(), 2))
col3.metric("Avg Ride Distance", round(filtered_df["Ride_Distance"].mean(), 2))
col4.metric("Avg Rating", round(filtered_df["Customer_Rating"].mean(), 2))
cancellation_rate = (filtered_df[filtered_df["Booking_Status"] != "Success"].shape[0] / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
col5.metric("Cancellation Rate", f"{cancellation_rate:.1f}%")

# ----------------------
# Charts
# ----------------------
st.subheader("Rides Over Time")
rides_per_day = filtered_df.groupby(filtered_df["Date"].dt.date).size()
st.line_chart(rides_per_day)

st.subheader("Top 5 Vehicle Types by Avg Distance")
top_vehicles = filtered_df.groupby("Vehicle_Type")["Ride_Distance"].mean().nlargest(5)
st.bar_chart(top_vehicles)

st.subheader("Payment Method Share")
payment_share = filtered_df["Payment_Method"].value_counts()
st.bar_chart(payment_share)

st.subheader("Booking Status Breakdown")
status_share = filtered_df["Booking_Status"].value_counts()
st.bar_chart(status_share)

# ----------------------
# Data Table
# ----------------------
st.subheader("Filtered Data Table")
st.dataframe(filtered_df.head(50))

# ----------------------
# Embed Power BI
# ----------------------
st.subheader("Power BI Dashboard")
st.markdown(
    """<iframe title="PowerBI Report" width="100%" height="600"
    src="YOUR_POWERBI_LINK" frameborder="0" allowFullScreen="true"></iframe>""",
    unsafe_allow_html=True
)
