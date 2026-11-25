"""
scripts/generate_report.py
Generates an Executive Analytics & Metrics Summary Report from the clickstream dataset.
Can be run directly via CLI:
    python ..\scripts\generate_report.py
"""

import sys
import datetime
from pathlib import Path
import csv

def generate_report():
    root = Path(__file__).resolve().parent.parent
    ds_file = root / "dataset" / "customer_clickstream_purchase_dataset.csv"
    
    if not ds_file.exists():
        print(f"[Error] Dataset not found at: {ds_file}")
        sys.exit(1)
        
    print("=" * 70)
    print("   CUSTOMER PURCHASING & CLICKSTREAM ANALYTICS EXECUTIVE REPORT")
    print("=" * 70)
    print(f"Generated on : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Dataset Path : {ds_file}")
    
    sessions = set()
    customers = set()
    converted_sessions = set()
    total_events = 0
    total_revenue = 0.0
    category_counts = {}
    device_counts = {}
    source_counts = {}
    event_counts = {}
    
    with open(ds_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_events += 1
            sid = row["session_id"]
            cid = row["customer_id"]
            sessions.add(sid)
            customers.add(cid)
            
            ev_type = row.get("event_type", "unknown")
            event_counts[ev_type] = event_counts.get(ev_type, 0) + 1
            
            cat = row.get("product_category", "unknown")
            category_counts[cat] = category_counts.get(cat, 0) + 1
            
            dev = row.get("device_category", "unknown")
            device_counts[dev] = device_counts.get(dev, 0) + 1
            
            src = row.get("traffic_source", "unknown")
            source_counts[src] = source_counts.get(src, 0) + 1
            
            if row.get("session_converted") == "1":
                converted_sessions.add(sid)
                
            p_amt = float(row.get("purchase_amount", 0) or 0)
            if p_amt > 0 and ev_type == "purchase":
                total_revenue += p_amt

    n_sessions = len(sessions)
    n_customers = len(customers)
    n_conv = len(converted_sessions)
    cr = (n_conv / n_sessions * 100) if n_sessions else 0
    aov = (total_revenue / n_conv) if n_conv else 0
    
    print("\n" + "-" * 70)
    print(" 1. EXECUTIVE KPI SUMMARY")
    print("-" * 70)
    print(f" - Total Clickstream Events    : {total_events:,}")
    print(f" - Unique Customer Sessions     : {n_sessions:,}")
    print(f" - Unique Customers             : {n_customers:,}")
    print(f" - Converted Sessions           : {n_conv:,}")
    print(f" - Overall Conversion Rate      : {cr:.2f}%")
    print(f" - Total Gross Revenue          : ${total_revenue:,.2f}")
    print(f" - Average Order Value (AOV)    : ${aov:.2f}")

    print("\n" + "-" * 70)
    print(" 2. EVENT TYPE BREAKDOWN")
    print("-" * 70)
    for ev, cnt in sorted(event_counts.items(), key=lambda x: x[1], reverse=True):
        print(f" - {ev:<25} : {cnt:>6,} ({cnt/total_events*100:5.1f}%)")

    print("\n" + "-" * 70)
    print(" 3. TRAFFIC SOURCE SHARE")
    print("-" * 70)
    for src, cnt in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
        print(f" - {src:<25} : {cnt:>6,} ({cnt/total_events*100:5.1f}%)")

    print("\n" + "-" * 70)
    print(" 4. DEVICE DISTRIBUTION")
    print("-" * 70)
    for dev, cnt in sorted(device_counts.items(), key=lambda x: x[1], reverse=True):
        print(f" - {dev:<25} : {cnt:>6,} ({cnt/total_events*100:5.1f}%)")

    print("\n" + "-" * 70)
    print(" 5. PRODUCT CATEGORY POPULARITY")
    print("-" * 70)
    for cat, cnt in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f" - {cat:<25} : {cnt:>6,} ({cnt/total_events*100:5.1f}%)")
        
    report_file = root / "Capstone_Analytics_Report.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# Capstone Project: Customer Purchasing Analysis Report\n\n")
        f.write(f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 1. Executive KPIs\n\n")
        f.write(f"| Metric | Value |\n|:---|:---|\n")
        f.write(f"| Total Events | {total_events:,} |\n")
        f.write(f"| Unique Sessions | {n_sessions:,} |\n")
        f.write(f"| Unique Customers | {n_customers:,} |\n")
        f.write(f"| Converted Sessions | {n_conv:,} |\n")
        f.write(f"| Conversion Rate | {cr:.2f}% |\n")
        f.write(f"| Total Revenue | ${total_revenue:,.2f} |\n")
        f.write(f"| Average Order Value (AOV) | ${aov:.2f} |\n\n")
        f.write("## 2. Machine Learning & Analytical Modules\n\n")
        f.write("- **Customer RFM Segmentation**: Evaluated via k-means silhouette ($k=2$ to $k=6$).\n")
        f.write("- **Leakage-Free Conversion Prediction**: Evaluated using Logistic Regression, Decision Tree, Random Forest, and XGBoost.\n")
        f.write("- **Revenue Estimation**: Expected monetary value forecasting with ARIMA/ETS models.\n")
        f.write("- **Funnel Analysis**: Drop-off rates across Browsing -> Add to Cart -> Checkout -> Purchase.\n")

    print("\n" + "=" * 70)
    print(f" Markdown Report Saved: {report_file}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    generate_report()
