import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import drive
drive.mount('/content/drive')
# Load the dataset
file_path = '/content/drive/MyDrive/Untitled/Dataset.csv'  # Update with the actual file path
df = pd.read_csv(file_path)

# Data Cleaning
df.dropna(subset=["Product", "Total"], inplace=True)  # Removing rows with missing values
df["Total"] = df["Total"].astype(float)  # Ensure 'Total' is a numeric type
df["Date"] = pd.to_datetime(df["Date"])  # Convert Date column to datetime

# Summary statistics
print("Dataset Summary:\n", df.describe())
print("\nMissing Values:\n", df.isnull().sum())

# Exploratory Data Analysis (EDA)
plt.figure(figsize=(10, 5))
sns.histplot(df["Total"], bins=30, kde=True)
plt.title("Distribution of Total Sales")
plt.xlabel("Total Sales ($)")
plt.ylabel("Frequency")
plt.show()

# Sales Trends Over Time
plt.figure(figsize=(12, 6))
df.groupby(df["Date"].dt.month)["Total"].sum().plot(kind="line", marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales ($)")
plt.xticks(range(1, 13))
plt.show()

# Most Frequently Purchased Products
plt.figure(figsize=(10, 5))
df["Product"].value_counts().plot(kind="bar", color="skyblue")
plt.title("Most Purchased Products")
plt.xlabel("Product")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.show()

# Top Customers Based on Spending
top_customers = df.groupby("CustomerID")["Total"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 5))
top_customers.plot(kind="bar", color="salmon")
plt.title("Top 10 Customers by Total Spending")
plt.xlabel("Customer ID")
plt.ylabel("Total Amount Spent ($)")
plt.xticks(rotation=45)
plt.show()

# Correlation between Quantity and Total Sales
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="Quantity", y="Total")
plt.title("Quantity vs. Total Sales")
plt.xlabel("Quantity")
plt.ylabel("Total Sales ($)")
plt.show()

print("Analysis complete! Insights have been visualized.")
