# ===============================================
# OLA RIDE INSIGHTS - SQL QUERIES (Pandas Version)
# ===============================================

import pandas as pd

# Load cleaned dataset
df = pd.read_csv("Cleaned_OLA_Dataset.csv")

print("\n========== SQL QUERIES USING PANDAS ==========\n")

# 1. Retrieve all successful bookings
successful = df[df["Booking_Status"] == "Success"]
print("1. Successful Bookings:\n", successful.head(), "\n")

# 2. Find the average ride distance for each vehicle type
avg_distance = df.groupby("Vehicle_Type")["Ride_Distance"].mean()
print("2. Average Ride Distance per Vehicle Type:\n", avg_distance, "\n")

# 3. Get the total number of cancelled rides by customers
cancelled_customers = df[df["Booking_Status"] == "Canceled by Customer"].shape[0]
print("3. Total Cancelled Rides by Customers:", cancelled_customers, "\n")

# 4. List the top 5 customers who booked the highest number of rides
top_customers = df["Customer_ID"].value_counts().head(5)
print("4. Top 5 Customers by Number of Rides:\n", top_customers, "\n")

# 5. Get the number of rides cancelled by drivers due to personal & car-related issues
cancelled_drivers = df[df["Canceled_Rides_by_Driver"] == "Personal & Car related issue"].shape[0]
print("5. Rides Cancelled by Drivers (Personal/Car Issues):", cancelled_drivers, "\n")

# 6. Find max and min driver ratings for Prime Sedan bookings
prime_sedan_ratings = df[df["Vehicle_Type"] == "Prime Sedan"]["Driver_Ratings"]
max_rating, min_rating = prime_sedan_ratings.max(), prime_sedan_ratings.min()
print("6. Prime Sedan Ratings - Max:", max_rating, "Min:", min_rating, "\n")

# 7. Retrieve all rides where payment was made using UPI
upi_rides = df[df["Payment_Method"].str.lower() == "upi"]
print("7. Rides Paid with UPI:\n", upi_rides.head(), "\n")

# 8. Find the average customer rating per vehicle type
avg_cust_rating = df.groupby("Vehicle_Type")["Customer_Rating"].mean()
print("8. Average Customer Rating per Vehicle Type:\n", avg_cust_rating, "\n")

# 9. Calculate the total booking value of rides completed successfully
total_value = df[df["Booking_Status"] == "Success"]["Booking_Value"].sum()
print("9. Total Booking Value of Successful Rides:", total_value, "\n")

# 10. List all incomplete rides along with the reason
incomplete = df[df["Incomplete_Rides"].str.lower() == "yes"][["Booking_ID", "Incomplete_Rides_Reason"]]
print("10. Incomplete Rides with Reasons:\n", incomplete.head(), "\n")

