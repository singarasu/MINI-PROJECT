# Online Shopping Customer Analysis

An end-to-end customer purchase behaviour analysis project: one dataset, three ways to visualize it (HTML/JS dashboard, Python/Streamlit dashboard, static chart script), plus an academic project report.

**Author:** Singarasu S · Reg. No: 25127056 · BSc Computer Science with Data Analytics  
**Course:** Data Analysis using R & Tableau (25BKDC301)

---

## Project Structure

```text
MINI-PROJECT/
├── data/
│   └── shopping_trends.csv           # shared dataset (3,900 records, 19 attributes)
│
├── analysis/
│   └── analysis.py                   # exploratory analysis / report-generation script
│
├── analysis.py                       # root analysis pipeline script (EDA, KPIs, charts)
│
├── dashboard/                        # Option 1: HTML/JS interactive dashboard
│   ├── index.html                    # responsive markup, styling, Chart.js logic
│   └── data.js                       # embedded JSON dataset
│
├── python-dashboard/                 # Option 2 & 3: Python dashboards
│   ├── app.py                        # interactive Streamlit dashboard
│   ├── generate_static_charts.py     # static PNG chart generator (matplotlib/seaborn)
│   └── requirements.txt
│
├── docs/
│   └── Online_Shopping_Customer_Analysis_Dashboard.docx   # written academic report
│
├── assets/
│   ├── screenshots/                  # chart exports from the academic report (chart-1 to chart-5)
│   └── analysis-charts/              # output folder for generated charts
│
├── requirements.txt                  # Python dependencies
└── README.md
```

---

## Dataset Overview

`data/shopping_trends.csv` contains 3,900 customer purchase records across 19 attributes:
- **Demographics:** Age, Gender, Location
- **Order Details:** Item Purchased, Category, Purchase Amount (USD), Size, Color, Season
- **Customer Behaviour:** Review Rating, Subscription Status, Payment Method, Shipping Type, Discount Applied, Promo Code Used, Previous Purchases, Preferred Payment Method, Frequency of Purchases

### Key Highlights
- **Total Orders Analyzed:** 3,900
- **Average Order Value (USD):** $59.76
- **Top Product Categories:** Clothing (1,737), Accessories (1,240), Footwear (599), Outerwear (324)
- **Top Payment Methods:** Credit Card, Venmo, Cash, PayPal, Debit Card, Bank Transfer
- **Subscription Rate:** ~27% active subscribers

---

## How to Run

### 1. Run Python Analysis & Generate Charts
Run the main Python analysis script from the root directory:
```bash
python analysis.py
```
Options:
- `python analysis.py` — Runs full exploratory data analysis, prints summary KPIs to console, and saves charts to `assets/analysis-charts/`.
- `python analysis.py --all` — Generates both full exploratory charts and report screenshots (`chart-1.png` to `chart-5.png`).
- `python analysis.py --report-charts` — Generates only the 5 academic report charts into `assets/screenshots/`.
- `python analysis.py --show` — Opens interactive matplotlib windows.

Or run from the `analysis/` folder:
```bash
python analysis/analysis.py
```

### 2. Static PNG Chart Generator
Generate high-resolution static PNG charts:
```bash
python python-dashboard/generate_static_charts.py
```
Saves 7 charts directly to `assets/analysis-charts/`.

### 3. Interactive Web Dashboard (Streamlit)
Launch the interactive Streamlit dashboard with real-time filtering and KPI metrics:
```bash
pip install -r requirements.txt
streamlit run python-dashboard/app.py
```
Open `http://localhost:8501` in your browser.

### 4. Browser-based Static Dashboard (HTML/JS)
Open `dashboard/index.html` directly in any web browser to explore the interactive Chart.js dashboard with filtering by category, season, gender, payment method, and subscription status.

---

## Generated Visualizations

| Chart File | Description |
| :--- | :--- |
| `01_orders_by_category.png` | Order volume distribution by product category |
| `02_avg_value_by_category.png` | Average purchase spend across categories |
| `03_payment_methods.png` | Distribution of payment methods used |
| `04_orders_by_season.png` | Seasonal ordering trends |
| `05_rating_distribution.png` | Customer review rating distribution |
| `06_subscription_status.png` | Breakdown of subscriber vs non-subscriber |
| `07_age_distribution.png` | Customer age spread and density |
| `chart-1.png` to `chart-5.png` | Academic report charts (Payment methods, Top customers, Category spend, Monthly trends, Category orders) |

---

## Technical Stack
- **Languages & Frameworks:** Python 3, JavaScript (Chart.js), HTML5/CSS3
- **Data Analysis & Processing:** Pandas, NumPy
- **Data Visualization:** Matplotlib, Seaborn, Plotly Express
- **Web App Dashboard:** Streamlit
