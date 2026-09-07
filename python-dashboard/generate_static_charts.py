"""
==============================================================================
Online Shopping Customer Analysis — Static Chart Generator
==============================================================================
Generates a comprehensive set of PNG charts from shopping_trends.csv
using pandas, matplotlib, and seaborn.
Saved into: assets/analysis-charts/
==============================================================================
"""

import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "shopping_trends.csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "assets", "analysis-charts")

sns.set_theme(style="whitegrid")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not os.path.exists(DATA_PATH):
        print(f"[ERROR] Data file not found: {DATA_PATH}")
        sys.exit(1)

    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df):,} records, {df.shape[1]} columns")

    # 1. Orders by category
    plt.figure(figsize=(8, 5))
    order = df["Category"].value_counts().index
    sns.countplot(data=df, x="Category", order=order, hue="Category",
                  palette="viridis", legend=False)
    plt.title("Orders by Category")
    plt.ylabel("Number of Orders")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "01_orders_by_category.png"), dpi=150)
    plt.close()

    # 2. Average order value by category
    plt.figure(figsize=(8, 5))
    avg_by_cat = (
        df.groupby("Category")["Purchase Amount (USD)"]
        .mean()
        .sort_values(ascending=False)
    )
    sns.barplot(x=avg_by_cat.index, y=avg_by_cat.values,
                hue=avg_by_cat.index, palette="magma", legend=False)
    plt.title("Average Order Value by Category")
    plt.ylabel("Average Purchase Amount (USD)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "02_avg_value_by_category.png"), dpi=150)
    plt.close()

    # 3. Payment method distribution
    plt.figure(figsize=(7, 7))
    pay_counts = df["Payment Method"].value_counts()
    plt.pie(pay_counts.values, labels=pay_counts.index, autopct="%1.1f%%",
            startangle=90, colors=sns.color_palette("pastel"))
    plt.title("Payment Method Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "03_payment_methods.png"), dpi=150)
    plt.close()

    # 4. Orders by season
    plt.figure(figsize=(7, 5))
    season_order = ["Spring", "Summer", "Fall", "Winter"]
    sns.countplot(data=df, x="Season", order=season_order, hue="Season",
                  palette="coolwarm", legend=False)
    plt.title("Orders by Season")
    plt.ylabel("Number of Orders")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "04_orders_by_season.png"), dpi=150)
    plt.close()

    # 5. Review rating distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df["Review Rating"], bins=20, kde=True, color="steelblue")
    plt.title("Review Rating Distribution")
    plt.xlabel("Review Rating")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "05_rating_distribution.png"), dpi=150)
    plt.close()

    # 6. Subscription status
    plt.figure(figsize=(6, 6))
    sub_counts = df["Subscription Status"].value_counts()
    plt.pie(sub_counts.values, labels=sub_counts.index, autopct="%1.1f%%",
            startangle=90, colors=["#4C72B0", "#DD8452"])
    plt.title("Subscriber vs Non-Subscriber")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "06_subscription_status.png"), dpi=150)
    plt.close()

    # 7. Age distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df["Age"], bins=30, kde=True, color="seagreen")
    plt.title("Customer Age Distribution")
    plt.xlabel("Age")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "07_age_distribution.png"), dpi=150)
    plt.close()

    print(f"Done. Charts saved to '{OUTPUT_DIR}/'")


if __name__ == "__main__":
    main()
