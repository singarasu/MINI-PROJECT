"""
==============================================================================
ONLINE SHOPPING CUSTOMER ANALYSIS (ANALYSIS MODULE)
==============================================================================
Author: Singarasu S (Reg. No: 25127056)
Course: BSc Computer Science with Data Analytics
Project: Customer Purchase Behaviour Analysis (Mini-Project)

Description:
  Exploratory analysis script that can be run directly from within the
  analysis/ folder or from the project root.
==============================================================================
"""

import os
import sys

# Dynamically locate project root
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File paths
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "shopping_trends.csv")
CHARTS_DIR = os.path.join(PROJECT_ROOT, "assets", "analysis-charts")


def run_analysis():
    print(f"Loading data from: {DATA_PATH}")
    if not os.path.exists(DATA_PATH):
        print(f"[ERROR] Could not find data file at {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)

    print("\n===== DATASET OVERVIEW =====")
    print("Rows and Columns:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nFirst 5 Records:")
    print(df.head())

    # Ensure output directory exists
    os.makedirs(CHARTS_DIR, exist_ok=True)

    print("\n===== MISSING VALUES =====")
    print(df.isnull().sum())

    dupes = df.duplicated().sum()
    print("\nDuplicate Rows:", dupes)
    if dupes > 0:
        df = df.drop_duplicates()

    # Numeric conversions
    if "Purchase Amount (USD)" in df.columns:
        df["Purchase Amount (USD)"] = pd.to_numeric(df["Purchase Amount (USD)"], errors="coerce")
    if "Review Rating" in df.columns:
        df["Review Rating"] = pd.to_numeric(df["Review Rating"], errors="coerce")

    # Basic statistics
    print("\n===== BASIC STATISTICS =====")
    print(df.describe())

    if "Purchase Amount (USD)" in df.columns:
        total_sales = df["Purchase Amount (USD)"].sum()
        aov = df["Purchase Amount (USD)"].mean()
        print(f"\nTotal Purchase Amount: ${total_sales:,.2f}")
        print(f"Average Purchase Amount: ${aov:.2f}")

    # Chart 1: Category Orders
    if "Category" in df.columns:
        category_orders = df["Category"].value_counts()
        print("\n===== ORDERS BY CATEGORY =====")
        print(category_orders)

        plt.figure(figsize=(8, 5))
        category_orders.plot(kind="bar", color="#2b7bba")
        plt.title("Orders by Product Category")
        plt.xlabel("Product Category")
        plt.ylabel("Number of Orders")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(CHARTS_DIR, "orders_by_category.png"), dpi=150)
        plt.close()

    # Chart 2: Average Order Value by Category
    if "Category" in df.columns and "Purchase Amount (USD)" in df.columns:
        category_aov = df.groupby("Category")["Purchase Amount (USD)"].mean().sort_values(ascending=False)
        print("\n===== AVERAGE ORDER VALUE BY CATEGORY =====")
        print(category_aov)

        plt.figure(figsize=(8, 5))
        category_aov.plot(kind="bar", color="#2b7bba")
        plt.title("Average Order Value by Product Category")
        plt.xlabel("Product Category")
        plt.ylabel("Average Purchase Amount (USD)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(CHARTS_DIR, "average_order_value_by_category.png"), dpi=150)
        plt.close()

    # Chart 3: Payment Method Distribution
    if "Payment Method" in df.columns:
        payment_counts = df["Payment Method"].value_counts()
        print("\n===== PAYMENT METHOD =====")
        print(payment_counts)

        plt.figure(figsize=(7, 7))
        payment_counts.plot(kind="pie", autopct="%1.1f%%", startangle=90)
        plt.title("Payment Method Distribution")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig(os.path.join(CHARTS_DIR, "payment_method_distribution.png"), dpi=150)
        plt.close()

    # Chart 4: Top 10 Customers by Previous Purchases
    if "Customer ID" in df.columns and "Previous Purchases" in df.columns:
        top_customers = (
            df[["Customer ID", "Previous Purchases"]]
            .sort_values("Previous Purchases", ascending=False)
            .head(10)
            .set_index("Customer ID")["Previous Purchases"]
        )
        print("\n===== TOP 10 CUSTOMERS BY PREVIOUS PURCHASES =====")
        print(top_customers)

        plt.figure(figsize=(9, 5))
        top_customers.plot(kind="bar", color="#2b7bba")
        plt.title("Top 10 Customers by Previous Purchases")
        plt.xlabel("Customer ID")
        plt.ylabel("Previous Purchases")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(CHARTS_DIR, "top_10_customers.png"), dpi=150)
        plt.close()

    # Chart 5: Orders by Purchase Frequency
    if "Frequency of Purchases" in df.columns:
        freq_order = [
            "Weekly", "Fortnightly", "Bi-Weekly",
            "Monthly", "Every 3 Months", "Quarterly", "Annually"
        ]
        freq_counts = (
            df["Frequency of Purchases"]
            .value_counts()
            .reindex([f for f in freq_order if f in df["Frequency of Purchases"].unique()])
        )
        print("\n===== ORDERS BY PURCHASE FREQUENCY =====")
        print(freq_counts)

        plt.figure(figsize=(9, 5))
        freq_counts.plot(kind="line", marker="o", color="#2b7bba")
        plt.title("Orders by Purchase Frequency")
        plt.xlabel("Purchase Frequency")
        plt.ylabel("Number of Customers")
        plt.grid(True)
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig(os.path.join(CHARTS_DIR, "orders_by_purchase_frequency.png"), dpi=150)
        plt.close()

    print("\n===================================")
    print("ONLINE SHOPPING ANALYSIS COMPLETED")
    print("===================================")
    print(f"Charts saved to: {CHARTS_DIR}")


if __name__ == "__main__":
    run_analysis()
