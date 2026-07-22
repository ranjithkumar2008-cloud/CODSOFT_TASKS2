"""
generate_data.py
Creates a realistic synthetic retail sales dataset used to demonstrate
all the visualizations in visualize.py.
"""
import numpy as np
import pandas as pd

np.random.seed(42)

# ---- Date range: 2 years of daily sales ----
dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")

regions = ["North", "South", "East", "West"]
categories = ["Electronics", "Apparel", "Home & Kitchen", "Beauty", "Sports"]

rows = []
for date in dates:
    # seasonal effect: higher sales in Nov-Dec, lower in Feb
    month = date.month
    seasonal_factor = 1.0
    if month in (11, 12):
        seasonal_factor = 1.6
    elif month == 2:
        seasonal_factor = 0.75
    elif month in (6, 7):
        seasonal_factor = 1.15

    # weekend boost
    weekend_factor = 1.3 if date.weekday() >= 5 else 1.0

    for region in regions:
        # regional baseline differences
        region_base = {"North": 1.1, "South": 0.9, "East": 1.0, "West": 1.05}[region]

        for category in categories:
            cat_base = {
                "Electronics": 320, "Apparel": 150, "Home & Kitchen": 210,
                "Beauty": 95, "Sports": 130
            }[category]

            n_orders = max(0, int(np.random.poisson(
                cat_base / 40 * seasonal_factor * weekend_factor * region_base
            )))
            if n_orders == 0:
                continue

            unit_price = {
                "Electronics": np.random.normal(250, 60),
                "Apparel": np.random.normal(45, 15),
                "Home & Kitchen": np.random.normal(70, 20),
                "Beauty": np.random.normal(30, 10),
                "Sports": np.random.normal(55, 18),
            }[category]
            unit_price = max(5, unit_price)

            for _ in range(n_orders):
                qty = np.random.randint(1, 5)
                price = max(5, np.random.normal(unit_price, unit_price * 0.1))
                discount = np.random.choice([0, 0.05, 0.10, 0.15, 0.20],
                                             p=[0.5, 0.2, 0.15, 0.1, 0.05])
                revenue = qty * price * (1 - discount)
                rating = np.clip(np.random.normal(4.1, 0.6), 1, 5)

                rows.append({
                    "date": date,
                    "region": region,
                    "category": category,
                    "quantity": qty,
                    "unit_price": round(price, 2),
                    "discount": discount,
                    "revenue": round(revenue, 2),
                    "customer_rating": round(rating, 1),
                    "ad_spend": round(max(0, np.random.normal(revenue * 0.08, 5)), 2),
                })

df = pd.DataFrame(rows)
df.to_csv("/home/claude/viz_project/sales_data.csv", index=False)
print(f"Generated {len(df):,} rows -> sales_data.csv")
print(df.head())
