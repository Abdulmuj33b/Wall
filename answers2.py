# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset ( using 'Dataset.csv')
df = pd.read_csv('Dataset.csv')  # file path 

# Data Cleaning
# ---------------
# Check for missing values
print("Missing values:\n", df.isnull().sum())

# Drop duplicates
df = df.drop_duplicates()

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Validate 'total' = quantity * price
df['calculated_total'] = df['quantity'] * df['price']
df['total'] = np.where(df['calculated_total'] != df['total'], df['calculated_total'], df['total'])
df.drop('calculated_total', axis=1, inplace=True)

# Data Exploration
# ---------------
# Summary statistics
print("\nSummary Statistics:\n", df.describe())

# Total revenue
total_revenue = df['total'].sum()
print(f"\nTotal Revenue: ${total_revenue:,.2f}")

# Top 10 products by revenue
product_revenue = df.groupby('product')['total'].sum().sort_values(ascending=False)
print("\nTop Products by Revenue:\n", product_revenue.head(10))

# Monthly sales trend
df['month'] = df['Date'].dt.month_name()
monthly_sales = df.groupby('month')['total'].sum().reindex(pd.date_range('2023-01', '2023-12', freq='M').month_name())

# Data Visualization
# ---------------
plt.figure(figsize=(14, 8))

# Plot 1: Line plot of Monthly Sales
plt.subplot(2, 2, 1)
sns.lineplot(x=monthly_sales.index, y=monthly_sales.values, marker='o')
plt.title('Monthly Sales Trend')
plt.xticks(rotation=45)

# Plot 2: Bar chart of Top Products
plt.subplot(2, 2, 2)
product_revenue.head(5).plot(kind='bar', color='skyblue')
plt.title('Top 5 Products by Revenue')
plt.ylabel('Revenue ($)')

# Plot 3: Histogram using Seabound of Price Distribution
plt.subplot(2, 2, 3)
sns.histplot(df['price'], bins=20, kde=True)
plt.title('Price Distribution')

# Plot 4: Scatter plot for Quantity vs. Revenue
plt.subplot(2, 2, 4)
sns.scatterplot(x='quantity', y='total', data=df)
plt.title('Quantity vs. Total Revenue')

plt.tight_layout()
plt.show()

# Customer Analysis
# ---------------
# Top customers
top_customers = df.groupby('customerID')['total'].sum().sort_values(ascending=False).head(5)
print("\nTop Customers:\n", top_customers)
