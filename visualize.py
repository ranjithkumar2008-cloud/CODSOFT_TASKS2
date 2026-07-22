"""
visualize.py
Generates a full suite of business-insight visualizations from sales_data.csv:
  1. Bar chart      - Revenue by category (Matplotlib)
  2. Line chart     - Monthly revenue trend by region (Matplotlib)
  3. Pie chart       - Revenue share by region (Matplotlib)
  4. Histogram       - Distribution of customer ratings (Seaborn)
  5. Scatter plot    - Ad spend vs revenue, colored by category (Seaborn)
  6. Interactive dashboard-style chart (Plotly) - bonus, saved as HTML

All charts are saved as PNG (300 dpi) / HTML into ./charts
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------------------------------------------------------------
# Setup
# ---------------------------------------------------------------
df = pd.read_csv("sales_data.csv", parse_dates=["date"])
df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

sns.set_theme(style="whitegrid", context="talk")
PALETTE = ["#2E5EAA", "#F2A541", "#4FB286", "#D65C6C", "#8D6BA8"]
sns.set_palette(PALETTE)

OUT = "charts"

def money_formatter(x, pos):
    if x >= 1_000_000:
        return f"${x/1_000_000:.1f}M"
    if x >= 1_000:
        return f"${x/1_000:.0f}K"
    return f"${x:.0f}"

# ---------------------------------------------------------------
# 1. BAR CHART — Total revenue by product category
# ---------------------------------------------------------------
cat_revenue = df.groupby("category")["revenue"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(cat_revenue.index, cat_revenue.values, color=PALETTE, edgecolor="white", linewidth=1.2)

for bar, val in zip(bars, cat_revenue.values):
    ax.text(bar.get_x() + bar.get_width()/2, val, money_formatter(val, None),
            ha="center", va="bottom", fontsize=11, fontweight="bold", color="#333")

ax.set_title("Total Revenue by Product Category (2024–2025)", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Category", fontsize=12)
ax.set_ylabel("Total Revenue", fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(money_formatter))
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT}/01_bar_revenue_by_category.png", dpi=300)
plt.close()
print("Saved: 01_bar_revenue_by_category.png")

# ---------------------------------------------------------------
# 2. LINE CHART — Monthly revenue trend by region
# ---------------------------------------------------------------
monthly = df.groupby(["month", "region"])["revenue"].sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 6.5))
for i, region in enumerate(sorted(monthly["region"].unique())):
    sub = monthly[monthly["region"] == region]
    ax.plot(sub["month"], sub["revenue"], marker="o", markersize=4,
            linewidth=2.2, label=region, color=PALETTE[i])

ax.set_title("Monthly Revenue Trend by Region", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Revenue", fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(money_formatter))
ax.legend(title="Region", frameon=True, loc="upper left")
ax.spines[["top", "right"]].set_visible(False)
fig.autofmt_xdate(rotation=30)
plt.tight_layout()
plt.savefig(f"{OUT}/02_line_monthly_revenue_trend.png", dpi=300)
plt.close()
print("Saved: 02_line_monthly_revenue_trend.png")

# ---------------------------------------------------------------
# 3. PIE CHART — Revenue share by region
# ---------------------------------------------------------------
region_revenue = df.groupby("region")["revenue"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    region_revenue.values,
    labels=region_revenue.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=PALETTE,
    explode=[0.06] + [0]*(len(region_revenue)-1),
    wedgeprops={"edgecolor": "white", "linewidth": 2},
    textprops={"fontsize": 13}
)
for at in autotexts:
    at.set_color("white")
    at.set_fontweight("bold")

ax.set_title("Revenue Share by Region", fontsize=16, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig(f"{OUT}/03_pie_revenue_share_by_region.png", dpi=300)
plt.close()
print("Saved: 03_pie_revenue_share_by_region.png")

# ---------------------------------------------------------------
# 4. HISTOGRAM — Distribution of customer ratings
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df["customer_rating"], bins=20, kde=True, color=PALETTE[0],
             edgecolor="white", ax=ax)
mean_rating = df["customer_rating"].mean()
ax.axvline(mean_rating, color=PALETTE[3], linestyle="--", linewidth=2,
           label=f"Mean = {mean_rating:.2f}")

ax.set_title("Distribution of Customer Ratings", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Customer Rating (1–5)", fontsize=12)
ax.set_ylabel("Number of Orders", fontsize=12)
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT}/04_histogram_customer_ratings.png", dpi=300)
plt.close()
print("Saved: 04_histogram_customer_ratings.png")

# ---------------------------------------------------------------
# 5. SCATTER PLOT — Ad spend vs revenue, colored by category
# ---------------------------------------------------------------
sample = df.sample(2000, random_state=1)  # sample for a readable scatter

fig, ax = plt.subplots(figsize=(11, 7))
sns.scatterplot(
    data=sample, x="ad_spend", y="revenue", hue="category",
    palette=PALETTE, alpha=0.6, s=45, edgecolor="none", ax=ax
)
ax.set_title("Ad Spend vs. Revenue by Category", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Ad Spend per Order ($)", fontsize=12)
ax.set_ylabel("Revenue per Order ($)", fontsize=12)
ax.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT}/05_scatter_adspend_vs_revenue.png", dpi=300)
plt.close()
print("Saved: 05_scatter_adspend_vs_revenue.png")

# ---------------------------------------------------------------
# 6. BONUS — Interactive Plotly dashboard (HTML)
# ---------------------------------------------------------------
monthly_cat = df.groupby(["month", "category"])["revenue"].sum().reset_index()
region_cat = df.groupby(["region", "category"])["revenue"].sum().reset_index()

dash = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Monthly Revenue by Category", "Revenue Share by Region",
        "Ad Spend vs Revenue (sample)", "Avg Rating by Category"
    ),
    specs=[[{"type": "scatter"}, {"type": "pie"}],
           [{"type": "scatter"}, {"type": "bar"}]]
)

# Panel 1: line
for i, cat in enumerate(categories := sorted(df["category"].unique())):
    sub = monthly_cat[monthly_cat["category"] == cat]
    dash.add_trace(go.Scatter(x=sub["month"], y=sub["revenue"], mode="lines+markers",
                               name=cat, legendgroup=cat,
                               line=dict(color=PALETTE[i % len(PALETTE)])),
                    row=1, col=1)

# Panel 2: pie
dash.add_trace(go.Pie(labels=region_revenue.index, values=region_revenue.values,
                       marker=dict(colors=PALETTE), hole=0.35, showlegend=False),
                row=1, col=2)

# Panel 3: scatter
for i, cat in enumerate(categories):
    sub = sample[sample["category"] == cat]
    dash.add_trace(go.Scatter(x=sub["ad_spend"], y=sub["revenue"], mode="markers",
                               name=cat, legendgroup=cat, showlegend=False,
                               marker=dict(color=PALETTE[i % len(PALETTE)], opacity=0.55, size=6)),
                    row=2, col=1)

# Panel 4: bar (avg rating)
avg_rating = df.groupby("category")["customer_rating"].mean().sort_values(ascending=False)
dash.add_trace(go.Bar(x=avg_rating.index, y=avg_rating.values,
                       marker_color=PALETTE, showlegend=False,
                       text=[f"{v:.2f}" for v in avg_rating.values], textposition="outside"),
                row=2, col=2)

dash.update_layout(
    title=dict(text="Retail Sales Performance Dashboard (2024–2025)", font=dict(size=22)),
    height=850, width=1200,
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.06, xanchor="center", x=0.25)
)
dash.update_yaxes(title_text="Revenue ($)", row=1, col=1)
dash.update_yaxes(title_text="Revenue ($)", row=2, col=1)
dash.update_xaxes(title_text="Ad Spend ($)", row=2, col=1)
dash.update_yaxes(title_text="Avg Rating", range=[0, 5], row=2, col=2)

dash.write_html(f"{OUT}/06_interactive_dashboard.html", include_plotlyjs="cdn")
print("Saved: 06_interactive_dashboard.html")

print("\nAll visualizations generated successfully in ./charts")
