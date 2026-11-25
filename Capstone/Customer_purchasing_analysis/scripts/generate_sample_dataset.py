"""
scripts/generate_sample_dataset.py
Generates a realistic 10,000 session clickstream and purchase dataset
matching the exact schema expected by the Customer Purchasing Analysis system.
"""

import os
import random
import datetime
from pathlib import Path

def generate_dataset(output_path: Path, num_sessions: int = 10000):
    random.seed(42)
    categories = ["Electronics", "Apparel", "Home & Living", "Books", "Beauty & Care", "Sports"]
    devices = ["desktop", "mobile", "tablet"]
    device_weights = [0.55, 0.38, 0.07]
    sources = ["organic", "direct", "cpc", "referral", "social"]
    source_weights = [0.35, 0.25, 0.20, 0.12, 0.08]
    pages = ["Home", "Product_List", "Product_Detail", "Search", "Cart", "Checkout", "Order_Confirmation"]
    
    start_date = datetime.datetime(2026, 1, 1, 8, 0, 0)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        # Header
        f.write(
            "session_id,customer_id,event_timestamp,event_type,page_name,"
            "product_category,product_price,quantity,cart_value,purchase_amount,"
            "session_page_number,time_on_page_seconds,device_category,traffic_source,"
            "customer_lifetime_value,previous_purchase_count,historical_average_order_value,"
            "customer_tenure_days,discount_percent,session_converted,is_conversion_event\n"
        )
        
        num_customers = num_sessions // 3
        customer_profiles = {}
        for c in range(1, num_customers + 1):
            cid = f"CUST_{c:05d}"
            tenure = random.randint(10, 720)
            prev_orders = random.choices([0, 1, 2, 3, 5, 8, 15], weights=[0.4, 0.2, 0.15, 0.1, 0.08, 0.05, 0.02])[0]
            haov = round(random.uniform(25.0, 320.0), 2) if prev_orders > 0 else 0.0
            clv = round(prev_orders * haov, 2)
            customer_profiles[cid] = (tenure, prev_orders, haov, clv)
            
        for s in range(1, num_sessions + 1):
            sid = f"SESS_{s:06d}"
            cid = f"CUST_{random.randint(1, num_customers):05d}"
            tenure, prev_orders, haov, clv = customer_profiles[cid]
            device = random.choices(devices, weights=device_weights)[0]
            source = random.choices(sources, weights=source_weights)[0]
            
            # Session timestamp
            time_offset = datetime.timedelta(
                days=random.randint(0, 90),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )
            session_time = start_date + time_offset
            
            # Will this session convert? (~18% conversion rate)
            will_convert = random.random() < 0.18
            num_pages = random.randint(3, 10) if will_convert else random.randint(1, 6)
            
            cat = random.choice(categories)
            price = round(random.uniform(15.0, 280.0), 2)
            cart_val = 0.0
            
            for page_num in range(1, num_pages + 1):
                event_time = session_time + datetime.timedelta(seconds=(page_num - 1) * random.randint(20, 150))
                time_str = event_time.strftime("%Y-%m-%d %H:%M:%S")
                time_on_page = random.randint(15, 240)
                discount = random.choice([0, 0, 5, 10, 15, 20])
                
                is_last = (page_num == num_pages)
                
                if page_num == 1:
                    page = "Home"
                    ev_type = "page_view"
                    qty = 0
                    p_amt = 0.0
                    is_conv = 0
                elif page_num == 2:
                    page = "Product_List"
                    ev_type = "page_view"
                    qty = 0
                    p_amt = 0.0
                    is_conv = 0
                elif page_num == 3:
                    page = "Product_Detail"
                    ev_type = "product_view"
                    qty = 0
                    p_amt = 0.0
                    is_conv = 0
                elif will_convert and is_last:
                    page = "Order_Confirmation"
                    ev_type = "purchase"
                    qty = random.randint(1, 3)
                    p_amt = round(price * qty * (1 - discount / 100), 2)
                    cart_val = p_amt
                    is_conv = 1
                elif will_convert and page_num == num_pages - 1:
                    page = "Checkout"
                    ev_type = "checkout"
                    qty = 1
                    p_amt = 0.0
                    cart_val = round(price * (1 - discount / 100), 2)
                    is_conv = 0
                elif will_convert and page_num == num_pages - 2:
                    page = "Cart"
                    ev_type = "add_to_cart"
                    qty = 1
                    p_amt = 0.0
                    cart_val = round(price, 2)
                    is_conv = 0
                else:
                    page = random.choice(["Search", "Product_Detail", "Product_List"])
                    ev_type = "page_view" if page != "Product_Detail" else "product_view"
                    qty = 0
                    p_amt = 0.0
                    is_conv = 0
                
                converted_flag = 1 if will_convert else 0
                
                f.write(
                    f"{sid},{cid},{time_str},{ev_type},{page},"
                    f"{cat},{price},{qty},{cart_val},{p_amt},"
                    f"{page_num},{time_on_page},{device},{source},"
                    f"{clv},{prev_orders},{haov},{tenure},{discount},"
                    f"{converted_flag},{is_conv}\n"
                )

if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "dataset" / "customer_clickstream_purchase_dataset.csv"
    print(f"Generating dataset at: {out}...")
    generate_dataset(out, num_sessions=10000)
    print(f"Done! File size: {out.stat().st_size / 1024 / 1024:.2f} MB")

