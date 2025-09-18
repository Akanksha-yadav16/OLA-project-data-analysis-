# ================================
# Exploratory Data Analysis (EDA) - OLA RIDE INSIGHTS
# ================================

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
df = pd.read_csv("Cleaned_OLA_Dataset.csv")

# ================================
# 1. Dataset Overview
# ================================
print("\n--- Dataset Info ---")
print(df.info())

print("\n--- Summary Statistics ---")
print(df.describe(include="all").transpose())

print("\n--- Missing Values ---")
print(df.isnull().sum())

# ================================
# 2. Ride Trends
# ================================
# Convert Date to datetime safely
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Ride volume over time
rides_per_day = df.groupby(df["Date"].dt.date).size()
plt.figure(figsize=(12,5))
rides_per_day.plot(kind="line", marker="o", color="purple")
plt.title("Ride Volume Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Rides")
plt.grid(True)
plt.show()

# Weekday vs Weekend
plt.figure(figsize=(6,4))
sns.countplot(data=df, x="Is_Weekend", palette="Set2")
plt.title("Weekday vs Weekend Rides")
plt.xticks([0,1], ["Weekday","Weekend"])
plt.show()

# Peak vs Off-Peak
plt.figure(figsize=(6,4))
sns.countplot(data=df, x="Peak_Hours", palette="coolwarm")
plt.title("Peak vs Off-Peak Rides")
plt.show()

# ================================
# 3. Booking Status Analysis
# ================================
plt.figure(figsize=(8,5))
sns.countplot(data=df, x="Booking_Status", order=df["Booking_Status"].value_counts().index, palette="viridis")
plt.title("Booking Status Distribution")
plt.xticks(rotation=30)
plt.show()

# Cancellations by customer vs driver
cancel_reasons = df[["Canceled_Rides_by_Customer","Canceled_Rides_by_Driver"]] \
                   .replace("Not Available", pd.NA).dropna(how="all")
print("\n--- Sample Cancellation Reasons ---")
print(cancel_reasons.head())

# ================================
# 4. Customer Behavior
# ================================
# Top customers by ride count
top_customers = df["Customer_ID"].value_counts().head(5)
print("\n--- Top 5 Customers by Ride Count ---")
print(top_customers)

# Payment method preferences
plt.figure(figsize=(7,5))
sns.countplot(data=df, x="Payment_Method", order=df["Payment_Method"].value_counts().index, palette="pastel")
plt.title("Payment Method Preferences")
plt.xticks(rotation=30)
plt.show()

# ================================
# 5. Vehicle Insights
# ================================
plt.figure(figsize=(10,5))
sns.countplot(data=df, x="Vehicle_Type", order=df["Vehicle_Type"].value_counts().index, palette="Set2")
plt.title("Vehicle Type Popularity")
plt.xticks(rotation=30)
plt.show()

# Average ride distance per vehicle
avg_distance_vehicle = df.groupby("Vehicle_Type")["Ride_Distance"].mean().sort_values(ascending=False)
print("\n--- Average Ride Distance per Vehicle Type ---")
print(avg_distance_vehicle)

# ================================
# 6. Financial Insights
# ================================
# Revenue by payment method
revenue_payment = df.groupby("Payment_Method")["Booking_Value"].sum().sort_values(ascending=False)
print("\n--- Revenue by Payment Method ---")
print(revenue_payment)

# Revenue by day of week
revenue_day = df.groupby("Day_Of_Week")["Booking_Value"].sum().sort_values(ascending=False)
print("\n--- Revenue by Day of Week ---")
print(revenue_day)

# ================================
# 7. Ratings Analysis
# ================================
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
sns.histplot(df["Driver_Ratings"], bins=20, kde=True, color="blue")
plt.title("Driver Ratings Distribution")

plt.subplot(1,2,2)
sns.histplot(df["Customer_Rating"], bins=20, kde=True, color="green")
plt.title("Customer Ratings Distribution")

plt.tight_layout()
plt.show()

# Average customer rating per vehicle type
avg_rating_vehicle = df.groupby("Vehicle_Type")["Customer_Rating"].mean().sort_values(ascending=False)
print("\n--- Average Customer Rating per Vehicle Type ---")
print(avg_rating_vehicle)

# ================================
# 8. Outlier Detection
# ================================
# Success rides with 0 distance
outliers = df[(df["Ride_Distance"]==0) & (df["Booking_Status"]=="Success")]
print("\n--- Suspicious Successful Rides with 0 Distance ---")
print(outliers.head())

# High booking values
print("\n--- Top 5 Highest Booking Values ---")
print(df.nlargest(5, "Booking_Value")[["Booking_ID","Booking_Value","Vehicle_Type","Ride_Distance"]])

# ================================
# 9. Correlation Analysis
# ================================
plt.figure(figsize=(10,6))
sns.heatmap(df[["Booking_Value","Ride_Distance","Driver_Ratings","Customer_Rating","Ride_Duration"]].corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()
