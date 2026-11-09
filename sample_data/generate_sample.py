import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def generate_sample_dataset():
    random.seed(42)
    np.random.seed(42)

    products = [
        {"name": "Ultra Wireless Headphones", "category": "Electronics", "price": 89.99},
        {"name": "Ergonomic Mechanical Keyboard", "category": "Electronics", "price": 129.50},
        {"name": "Pro Gaming Mouse", "category": "Electronics", "price": 49.99},
        {"name": "4K Ultra HD Monitor 27\"", "category": "Electronics", "price": 299.00},
        {"name": "Smart Fitness Watch", "category": "Wearables", "price": 79.00},
        {"name": "USB-C Fast Charging Hub", "category": "Accessories", "price": 34.99},
        {"name": "Noise Cancelling Earbuds", "category": "Electronics", "price": 59.99},
        {"name": "Organic Cotton Hoodie", "category": "Apparel", "price": 45.00},
        {"name": "Slim Fit Denim Jeans", "category": "Apparel", "price": 55.00},
        {"name": "Stainless Steel Thermal Bottle", "category": "Home & Kitchen", "price": 24.50},
        {"name": "Aromatherapy Essential Diffuser", "category": "Home & Kitchen", "price": 32.00},
        {"name": "Leather Travel Backpack", "category": "Accessories", "price": 85.00},
        {"name": "Bamboo Desk Organizer", "category": "Office", "price": 19.99},
        {"name": "Portable Bluetooth Speaker", "category": "Electronics", "price": 39.99},
        {"name": "Memory Foam Ergonomic Pillow", "category": "Home & Kitchen", "price": 42.00}
    ]

    cities = ["New York", "San Francisco", "Austin", "Chicago", "Seattle", "Boston", "Denver", "Atlanta", "Miami", "Los Angeles"]
    payment_methods = ["Credit Card", "Debit Card", "PayPal", "Apple Pay", "UPI"]

    # Generate 350 unique customers
    customer_ids = [f"CUST-{1000 + i}" for i in range(350)]

    # Generate transactions from 2024-01-01 to 2024-12-31 (1 full year)
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    total_days = (end_date - start_date).days

    records = []
    order_id_counter = 5000

    # Create repeat customers (top 40% will have 3-10 orders, others 1-2 orders)
    customer_order_weights = {}
    for cid in customer_ids:
        # 35% repeat buyers with higher frequency
        if random.random() < 0.35:
            customer_order_weights[cid] = random.randint(3, 8)
        else:
            customer_order_weights[cid] = random.randint(1, 2)

    for cid, num_orders in customer_order_weights.items():
        city = random.choice(cities)
        # First order date for this customer
        first_day_offset = random.randint(0, total_days - 30)
        curr_date = start_date + timedelta(days=first_day_offset)

        for o in range(num_orders):
            order_id_counter += 1
            order_id = f"INV-{order_id_counter}"
            
            # Each order has 1 to 3 distinct items
            items_count = random.choices([1, 2, 3], weights=[0.65, 0.25, 0.10])[0]
            chosen_products = random.sample(products, items_count)
            pay_method = random.choice(payment_methods)

            # Date of subsequent orders is after the current date
            if o > 0:
                curr_date += timedelta(days=random.randint(5, 75))
                if curr_date > end_date:
                    curr_date = end_date - timedelta(days=random.randint(1, 15))

            for prod in chosen_products:
                qty = random.choices([1, 2, 3, 4], weights=[0.70, 0.20, 0.07, 0.03])[0]
                records.append({
                    "InvoiceNo": order_id,
                    "CustomerID": cid,
                    "OrderDate": curr_date.strftime("%Y-%m-%d"),
                    "Product": prod["name"],
                    "Category": prod["category"],
                    "Quantity": qty,
                    "UnitPrice": prod["price"],
                    "TotalAmount": round(qty * prod["price"], 2),
                    "PaymentMethod": pay_method,
                    "CustomerCity": city
                })

    df = pd.DataFrame(records)

    # Sort chronologically
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    df = df.sort_values("OrderDate").reset_index(drop=True)
    df["OrderDate"] = df["OrderDate"].dt.strftime("%Y-%m-%d")

    # Add a few benign edge cases for realistic data cleaning demonstration:
    # 3 duplicate rows
    duplicates = df.iloc[10:13].copy()
    df = pd.concat([df, duplicates], ignore_index=True)

    out_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(out_dir, "retail_sales_sample.csv")
    xlsx_path = os.path.join(out_dir, "retail_sales_sample.xlsx")

    df.to_csv(csv_path, index=False)
    df.to_excel(xlsx_path, index=False, engine="openpyxl")
    print(f"Generated sample dataset: {len(df)} rows across {df['CustomerID'].nunique()} customers and {df['InvoiceNo'].nunique()} orders.")
    print(f"Saved to:\n - {csv_path}\n - {xlsx_path}")

if __name__ == "__main__":
    generate_sample_dataset()
