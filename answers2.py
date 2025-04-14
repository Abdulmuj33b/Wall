# Import libraries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(Dataset.csv):
    """Load dataset from the given file path."""
    if not os.path.exists(Dataset.csv):
        raise FileNotFoundError(f"Dataset file '{Dataset.csv}' not found.")
    return pd.read_csv(Dataset.csv)

def clean_data(df):
    """Clean the dataset."""
    # Check for missing values
    print("Missing values:\n", df.isnull().sum())

    # Drop duplicates
    df = df.drop_duplicates()

    # Convert 'Date' to datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Validate 'total' = quantity * price
    df['calculated_total'] = df['quantity'] * df['price']
    mismatch = df[df['calculated_total'] != df['total']]
    if not mismatch.empty:
        print(f"\nFound {len(mismatch)} mismatched rows in 'total'. Overwriting with calculated values.")
    df['total'] = np.where(df['calculated_total'] != df['total'], df['calculated_total'], df['total'])
    df.drop('calculated_total', axis=1, inplace=True)

    return df

def analyze_data(df):
    """Perform exploratory data analysis."""
    # Summary statistics
    print("\nSummary Statistics:\n", df.describe())

    # Total revenue
    total_revenue = df['total'].sum()
    print(f"\nTotal Revenue: ${total_revenue:,.2f}")

    # Top 10 products by revenue
    product_revenue = df.groupby('product')['total'].sum().sort_values(ascending=False)
    print("\nTop Products by Revenue:\n", product_revenue.head(10))

    # Top customers
    top_customers = df.groupby('customerID')['total'].sum().sort_values(ascending=False).head(5)
    print("\nTop Customers:\n", top_customers)

    return product_revenue

def visualize_data(df, product_revenue):
    """Create visualizations."""
    # Monthly sales trend
    df['YearMonth'] = df['Date'].dt.to_period('M')
    monthly_sales = df.groupby('YearMonth')['total'].sum()

    plt.figure(figsize=(14, 8))

    # Plot 1: Line plot of Monthly Sales
    plt.subplot(2, 2, 1)
    sns.lineplot(x=monthly_sales.index.astype(str), y=monthly_sales.values, marker='o')
    plt.title('Monthly Sales Trend')
    plt.xticks(rotation=45)
    plt.xlabel('Month')
    plt.ylabel('Revenue ($)')

    # Plot 2: Bar chart of Top Products
    plt.subplot(2, 2, 2)
    product_revenue.head(5).plot(kind='bar', color='skyblue')
    plt.title('Top 5 Products by Revenue')
    plt.ylabel('Revenue ($)')
    plt.xlabel('Product')

    # Plot 3: Histogram using Seaborn of Price Distribution
    plt.subplot(2, 2, 3)
    sns.histplot(df['price'], bins=20, kde=True, color='purple')
    plt.title('Price Distribution')
    plt.xlabel('Price')

    # Plot 4: Scatter plot for Quantity vs. Revenue
    plt.subplot(2, 2, 4)
    sns.scatterplot(x='quantity', y='total', data=df)
    plt.title('Quantity vs. Total Revenue')
    plt.xlabel('Quantity')
    plt.ylabel('Total Revenue ($)')

    plt.tight_layout()
    plt.show()

# Main script
if __name__ == "__main__":
    FILE_PATH = 'Dataset.csv'

    # Load the dataset
    df = load_data(FILE_PATH)

    # Clean the dataset
    df = clean_data(df)

    # Analyze the dataset
    product_revenue = analyze_data(df)

    # Visualize the dataset
    visualize_data(df, product_revenue)
