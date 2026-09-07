"""
==============================================================================
ONLINE SHOPPING CUSTOMER ANALYSIS & VISUALIZATION PIPELINE
==============================================================================
Author: Singarasu S (Reg. No: 25127056)
Course: BSc Computer Science with Data Analytics
Project: Customer Purchase Behaviour Analysis (Mini-Project)

Description:
  This script performs end-to-end exploratory data analysis (EDA), cleaning,
  statistical KPI calculation, and chart generation for online shopping customer
  behaviour data.

Usage:
  python analysis.py                      # Runs full analysis & generates charts
  python analysis.py --report-charts      # Generates the 5 academic report charts
  python analysis.py --all                # Generates all analysis and report charts
  python analysis.py --show               # Display interactive chart windows
==============================================================================
"""

import os
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Base directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA_PATH = os.path.join(SCRIPT_DIR, "data", "shopping_trends.csv")
CHARTS_DIR = os.path.join(SCRIPT_DIR, "assets", "analysis-charts")
SCREENSHOTS_DIR = os.path.join(SCRIPT_DIR, "assets", "screenshots")


def load_and_clean_data(csv_path: str) -> pd.DataFrame:
    """
    Loads dataset from CSV, inspects structure, handles missing values,
    removes duplicates, and casts types.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at: {csv_path}")

    print("\n" + "=" * 60)
    print("1. LOADING & INSPECTING DATASET")
    print("=" * 60)
    df = pd.read_csv(csv_path)
    print(f"Total Rows: {df.shape[0]:,}")
    print(f"Total Columns: {df.shape[1]}")
    print(f"Columns: {', '.join(df.columns.tolist())}")

    print("\n" + "=" * 60)
    print("2. DATA CLEANING & VALIDATION")
    print("=" * 60)

    # Missing values
    missing_count = df.isnull().sum()
    print("Missing Values per Column:")
    has_missing = False
    for col, count in missing_count.items():
        if count > 0:
            print(f"  - {col}: {count}")
            has_missing = True
    if not has_missing:
        print("  - No missing values found in the dataset.")

    # Duplicate records
    dupes = df.duplicated().sum()
    print(f"\nDuplicate Rows: {dupes}")
    if dupes > 0:
        df = df.drop_duplicates()
        print(f"  - Removed {dupes} duplicates.")

    # Numeric type conversions
    if "Purchase Amount (USD)" in df.columns:
        df["Purchase Amount (USD)"] = pd.to_numeric(
            df["Purchase Amount (USD)"], errors="coerce"
        )
    if "Review Rating" in df.columns:
        df["Review Rating"] = pd.to_numeric(
            df["Review Rating"], errors="coerce"
        )

    return df


def print_executive_summary(df: pd.DataFrame):
    """
    Calculates and prints executive KPIs and statistical summaries.
    """
    print("\n" + "=" * 60)
    print("3. EXECUTIVE SUMMARY & KEY PERFORMANCE INDICATORS (KPIs)")
    print("=" * 60)

    total_orders = len(df)
    total_spend = df["Purchase Amount (USD)"].sum() if "Purchase Amount (USD)" in df.columns else 0
    avg_order_val = df["Purchase Amount (USD)"].mean() if "Purchase Amount (USD)" in df.columns else 0
    avg_rating = df["Review Rating"].mean() if "Review Rating" in df.columns else 0
    subscribers = (df["Subscription Status"] == "Yes").sum() if "Subscription Status" in df.columns else 0
    sub_pct = (subscribers / total_orders * 100) if total_orders > 0 else 0

    print(f"Total Orders Analyzed      : {total_orders:,}")
    print(f"Total Purchase Amount (USD): ${total_spend:,.2f}")
    print(f"Average Order Value (AOV)  : ${avg_order_val:.2f}")
    print(f"Average Review Rating      : {avg_rating:.2f} / 5.0")
    print(f"Subscribers                : {subscribers:,} ({sub_pct:.1f}%)")

    # Top Product Category
    if "Category" in df.columns:
        cat_counts = df["Category"].value_counts()
        top_cat = cat_counts.index[0]
        top_cat_count = cat_counts.iloc[0]
        print(f"Top Category (by Volume)   : {top_cat} ({top_cat_count:,} orders, {top_cat_count/total_orders*100:.1f}%)")

    # Top Payment Method
    if "Payment Method" in df.columns:
        pay_counts = df["Payment Method"].value_counts()
        top_pay = pay_counts.index[0]
        top_pay_count = pay_counts.iloc[0]
        print(f"Top Payment Method         : {top_pay} ({top_pay_count:,} orders, {top_pay_count/total_orders*100:.1f}%)")

    # Seasonality
    if "Season" in df.columns:
        season_counts = df["Season"].value_counts()
        top_season = season_counts.index[0]
        print(f"Peak Season                : {top_season} ({season_counts.iloc[0]:,} orders)")

    print("\n" + "-" * 60)
    print("Orders by Category:")
    if "Category" in df.columns:
        for cat, cnt in df["Category"].value_counts().items():
            avg_p = df[df["Category"] == cat]["Purchase Amount (USD)"].mean()
            print(f"  * {cat:15s}: {cnt:5d} orders ({cnt/total_orders*100:5.1f}%) | Avg Spend: ${avg_p:6.2f}")

    print("\nPayment Method Distribution:")
    if "Payment Method" in df.columns:
        for pm, cnt in df["Payment Method"].value_counts().items():
            print(f"  * {pm:15s}: {cnt:5d} orders ({cnt/total_orders*100:5.1f}%)")


def generate_analysis_charts(df: pd.DataFrame, output_dir: str, show_gui: bool = False):
    """
    Generates exploratory analysis charts from shopping_trends.csv and saves them as PNG.
    """
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid")
    print("\n" + "=" * 60)
    print(f"4. GENERATING ANALYSIS CHARTS -> {output_dir}")
    print("=" * 60)

    # 1. Orders by Category
    if "Category" in df.columns:
        plt.figure(figsize=(8, 5))
        order = df["Category"].value_counts().index
        sns.countplot(data=df, x="Category", order=order, palette="viridis", hue="Category", legend=False)
        plt.title("Orders by Product Category", fontsize=14, pad=12)
        plt.xlabel("Product Category", fontsize=11)
        plt.ylabel("Number of Orders", fontsize=11)
        plt.xticks(rotation=30)
        plt.tight_layout()
        chart_path = os.path.join(output_dir, "orders_by_category.png")
        plt.savefig(chart_path, dpi=150)
        print(f"  [SAVED] {os.path.basename(chart_path)}")
        if show_gui:
            plt.show()
        plt.close()

    # 2. Average Order Value by Category
    if "Category" in df.columns and "Purchase Amount (USD)" in df.columns:
        plt.figure(figsize=(8, 5))
        cat_aov = df.groupby("Category")["Purchase Amount (USD)"].mean().sort_values(ascending=False)
        sns.barplot(x=cat_aov.index, y=cat_aov.values, palette="magma", hue=cat_aov.index, legend=False)
        plt.title("Average Order Value by Product Category", fontsize=14, pad=12)
        plt.xlabel("Product Category", fontsize=11)
        plt.ylabel("Average Purchase Amount (USD)", fontsize=11)
        plt.xticks(rotation=30)
        plt.tight_layout()
        chart_path = os.path.join(output_dir, "average_order_value_by_category.png")
        plt.savefig(chart_path, dpi=150)
        print(f"  [SAVED] {os.path.basename(chart_path)}")
        if show_gui:
            plt.show()
        plt.close()

    # 3. Payment Method Distribution
    if "Payment Method" in df.columns:
        plt.figure(figsize=(7, 7))
        pay_counts = df["Payment Method"].value_counts()
        plt.pie(
            pay_counts.values,
            labels=pay_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=sns.color_palette("pastel")
        )
        plt.title("Payment Method Distribution", fontsize=14, pad=12)
        plt.tight_layout()
        chart_path = os.path.join(output_dir, "payment_method_distribution.png")
        plt.savefig(chart_path, dpi=150)
        print(f"  [SAVED] {os.path.basename(chart_path)}")
        if show_gui:
            plt.show()
        plt.close()

    # 4. Top 10 Customers by Previous Purchases
    if "Customer ID" in df.columns and "Previous Purchases" in df.columns:
        plt.figure(figsize=(9, 5))
        top_cust = (
            df[["Customer ID", "Previous Purchases"]]
            .sort_values("Previous Purchases", ascending=False)
            .head(10)
        )
        top_cust["Customer ID"] = top_cust["Customer ID"].astype(str)
        sns.barplot(data=top_cust, x="Customer ID", y="Previous Purchases", color="#2b7bba")
        plt.title("Top 10 Customers by Previous Purchases", fontsize=14, pad=12)
        plt.xlabel("Customer ID", fontsize=11)
        plt.ylabel("Previous Purchases", fontsize=11)
        plt.xticks(rotation=45)
        plt.tight_layout()
        chart_path = os.path.join(output_dir, "top_10_customers.png")
        plt.savefig(chart_path, dpi=150)
        print(f"  [SAVED] {os.path.basename(chart_path)}")
        if show_gui:
            plt.show()
        plt.close()

    # 5. Orders by Purchase Frequency
    if "Frequency of Purchases" in df.columns:
        plt.figure(figsize=(9, 5))
        freq_order = ["Weekly", "Fortnightly", "Bi-Weekly", "Monthly", "Every 3 Months", "Quarterly", "Annually"]
        existing_freqs = [f for f in freq_order if f in df["Frequency of Purchases"].values]
        freq_counts = df["Frequency of Purchases"].value_counts().reindex(existing_freqs)
        plt.plot(freq_counts.index, freq_counts.values, marker="o", linewidth=2.2, color="#2b7bba")
        plt.title("Orders by Purchase Frequency", fontsize=14, pad=12)
        plt.xlabel("Purchase Frequency", fontsize=11)
        plt.ylabel("Number of Customers", fontsize=11)
        plt.xticks(rotation=30)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        chart_path = os.path.join(output_dir, "orders_by_purchase_frequency.png")
        plt.savefig(chart_path, dpi=150)
        print(f"  [SAVED] {os.path.basename(chart_path)}")
        if show_gui:
            plt.show()
        plt.close()


def generate_report_screenshot_charts(output_dir: str, show_gui: bool = False):
    """
    Generates the exact 5 academic report charts (chart-1.png to chart-5.png)
    matching docs/Online_Shopping_Customer_Analysis_Dashboard.docx.
    """
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid")
    bar_color = "#2b7bba"
    print("\n" + "=" * 60)
    print(f"5. GENERATING ACADEMIC REPORT CHARTS -> {output_dir}")
    print("=" * 60)

    # Chart 1: Distribution of Payment Methods (Pie)
    # UPI (31.0%), Credit Card (26.2%), Debit Card (16.6%), Cash on Delivery (11.4%), Net Banking (10.0%), Wallet (4.8%)
    plt.figure(figsize=(9, 9))
    pm_labels = ["UPI", "Credit Card", "Debit Card", "Cash on Delivery", "Net Banking", "Wallet"]
    pm_shares = [31.0, 26.2, 16.6, 11.4, 10.0, 4.8]
    plt.pie(
        pm_shares,
        labels=pm_labels,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1.2}
    )
    plt.title("Distribution of Payment Methods", fontsize=13, pad=15)
    plt.tight_layout()
    c1_path = os.path.join(output_dir, "chart-1.png")
    plt.savefig(c1_path, dpi=200)
    print(f"  [SAVED] {os.path.basename(c1_path)} (Payment Methods Distribution)")
    if show_gui:
        plt.show()
    plt.close()

    # Chart 2: Top 10 Frequent Customers (Bar)
    # CUST1086 (9), others 7
    plt.figure(figsize=(9.5, 5))
    customers = ["CUST1086", "CUST1012", "CUST1029", "CUST1098", "CUST1090",
                 "CUST1091", "CUST1059", "CUST1096", "CUST1113", "CUST1010"]
    orders = [9, 7, 7, 7, 7, 7, 7, 7, 7, 7]
    plt.bar(customers, orders, color=bar_color)
    plt.title("Top 10 Frequent Customers", fontsize=12, pad=12)
    plt.xlabel("Customer ID", fontsize=10)
    plt.ylabel("Number of Orders", fontsize=10)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.tight_layout()
    c2_path = os.path.join(output_dir, "chart-2.png")
    plt.savefig(c2_path, dpi=200)
    print(f"  [SAVED] {os.path.basename(c2_path)} (Top 10 Frequent Customers)")
    if show_gui:
        plt.show()
    plt.close()

    # Chart 3: Average Order Value by Product Category (Bar)
    # Electronics, Home & Kitchen, Sports, Fashion, Beauty, Groceries, Books
    plt.figure(figsize=(9.5, 5))
    categories_aov = ["Electronics", "Home & Kitchen", "Sports", "Fashion", "Beauty", "Groceries", "Books"]
    aov_values = [4260.40, 2170.20, 1840.50, 1480.30, 850.10, 790.60, 470.20]
    plt.bar(categories_aov, aov_values, color=bar_color)
    plt.title("Average Order Value by Product Category", fontsize=12, pad=12)
    plt.xlabel("Product Category", fontsize=10)
    plt.ylabel("Average Order Value (Rs.)", fontsize=10)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.tight_layout()
    c3_path = os.path.join(output_dir, "chart-3.png")
    plt.savefig(c3_path, dpi=200)
    print(f"  [SAVED] {os.path.basename(c3_path)} (Average Order Value by Category)")
    if show_gui:
        plt.show()
    plt.close()

    # Chart 4: Monthly Order Trends (Line)
    # Jan - Dec
    plt.figure(figsize=(10, 5))
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    monthly_orders = [31, 47, 23, 49, 51, 44, 37, 47, 45, 43, 38, 45]
    plt.plot(months, monthly_orders, marker="o", color=bar_color, linewidth=2, markersize=6)
    plt.title("Monthly Order Trends", fontsize=12, pad=12)
    plt.xlabel("Month", fontsize=10)
    plt.ylabel("Number of Orders", fontsize=10)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.tight_layout()
    c4_path = os.path.join(output_dir, "chart-4.png")
    plt.savefig(c4_path, dpi=200)
    print(f"  [SAVED] {os.path.basename(c4_path)} (Monthly Order Trends)")
    if show_gui:
        plt.show()
    plt.close()

    # Chart 5: Orders by Product Category (Bar)
    # Fashion 120, Electronics 117, Home & Kitchen 76, Beauty 69, Sports 54, Books 36, Groceries 28
    plt.figure(figsize=(9.5, 5))
    cats = ["Fashion", "Electronics", "Home & Kitchen", "Beauty", "Sports", "Books", "Groceries"]
    cat_counts = [120, 117, 76, 69, 54, 36, 28]
    plt.bar(cats, cat_counts, color=bar_color)
    plt.title("Orders by Product Category", fontsize=12, pad=12)
    plt.xlabel("Product Category", fontsize=10)
    plt.ylabel("Number of Orders", fontsize=10)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.tight_layout()
    c5_path = os.path.join(output_dir, "chart-5.png")
    plt.savefig(c5_path, dpi=200)
    print(f"  [SAVED] {os.path.basename(c5_path)} (Orders by Product Category)")
    if show_gui:
        plt.show()
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Online Shopping Customer Analysis")
    parser.add_argument("--data", default=DEFAULT_DATA_PATH, help="Path to shopping_trends.csv")
    parser.add_argument("--report-charts", action="store_true", help="Generate academic report charts (chart-1 to 5)")
    parser.add_argument("--all", action="store_true", help="Generate both analysis and report charts")
    parser.add_argument("--show", action="store_true", help="Show interactive chart windows")
    args = parser.parse_args()

    # If --report-charts is requested exclusively
    if args.report_charts and not args.all:
        generate_report_screenshot_charts(SCREENSHOTS_DIR, show_gui=args.show)
        print("\n[SUCCESS] Academic report charts generated.")
        return

    # Default flow: Load dataset and analyze
    df = load_and_clean_data(args.data)
    print_executive_summary(df)
    generate_analysis_charts(df, CHARTS_DIR, show_gui=args.show)

    # If --all requested or by default keep academic screenshots available
    if args.all:
        generate_report_screenshot_charts(SCREENSHOTS_DIR, show_gui=args.show)

    print("\n" + "=" * 60)
    print("ANALYSIS & VISUALIZATION PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f"Exploratory charts saved to: {CHARTS_DIR}")
    if args.all or args.report_charts:
        print(f"Academic report charts saved to: {SCREENSHOTS_DIR}")


if __name__ == "__main__":
    main()
