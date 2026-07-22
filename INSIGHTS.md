# Retail Sales Visualization — Insights Summary

Dataset: 80,590 synthetic orders across 4 regions and 5 categories (2024–2025).

## Key Insights

1. **Electronics dominates revenue** — it generates the highest total revenue of
   any category, roughly double the next closest category, driven by a higher
   average order value rather than order count.
2. **Strong seasonality** — revenue spikes every November–December (holiday
   shopping) across all regions, and dips in February. Weekend days also
   consistently outperform weekdays.
3. **North region leads** — North contributes the largest share of total
   revenue, followed by West; South is the smallest contributor, suggesting an
   opportunity for targeted regional marketing.
4. **Customer satisfaction is solid but not uniform** — ratings cluster around
   4.0–4.3 on average, with a long tail of low-rated orders (1–2 stars) worth
   investigating for service or quality issues.
5. **Ad spend has a positive but noisy relationship with revenue** — higher ad
   spend per order generally associates with higher revenue, but Electronics
   shows the steepest and most consistent return, while Beauty shows a flatter,
   more scattered relationship — implying ad efficiency varies a lot by category.

## Chart-to-Insight Mapping

| Chart | File | Insight it supports |
|---|---|---|
| Bar chart | `01_bar_revenue_by_category.png` | Category revenue ranking |
| Line chart | `02_line_monthly_revenue_trend.png` | Seasonality & regional trend comparison |
| Pie chart | `03_pie_revenue_share_by_region.png` | Regional revenue share |
| Histogram | `04_histogram_customer_ratings.png` | Rating distribution & satisfaction spread |
| Scatter plot | `05_scatter_adspend_vs_revenue.png` | Ad spend efficiency by category |
| Interactive dashboard | `06_interactive_dashboard.html` | All of the above, explorable in one view |

---

## Bonus: Building this as a Power BI / Tableau Dashboard

The same `sales_data.csv` can be loaded directly into either tool to build a
live, filterable dashboard:

### Power BI
1. **Get Data → Text/CSV** → load `sales_data.csv`.
2. In **Power Query Editor**, set correct types (`date` → Date, `revenue`/`ad_spend` → Decimal Number) and create a `Month` column (`Date.StartOfMonth`).
3. Build visuals on the canvas:
   - **Clustered bar chart**: `category` on axis, `sum(revenue)` on values.
   - **Line chart**: `Month` on axis, `sum(revenue)` on values, `region` as legend.
   - **Pie/donut chart**: `region` as legend, `sum(revenue)` as values.
   - **Histogram**: use a **Column chart** on a binned `customer_rating` field (Power BI can auto-bin numeric columns).
   - **Scatter chart**: `ad_spend` (X), `revenue` (Y), `category` as legend/color, with a play axis on `Month` if desired.
4. Add **slicers** for `region`, `category`, and a date range slicer for interactivity.
5. Arrange visuals on one page and publish to the Power BI Service to share as a live dashboard.

### Tableau
1. **Connect → Text File** → `sales_data.csv`.
2. Drag `Category` to Columns and `SUM(Revenue)` to Rows for the bar chart.
3. Create a new sheet: `Month(Date)` to Columns, `SUM(Revenue)` to Rows, `Region` to Color, for the line chart.
4. Create a pie chart: switch Marks type to **Pie**, `Region` to Color/Angle with `SUM(Revenue)`.
5. Create a histogram: right-click `Customer Rating` → **Create → Bins**, then drag the binned field to Columns and `CNT(Orders)` to Rows.
6. Create a scatter plot: `Ad Spend` to Columns, `Revenue` to Rows, `Category` to Color.
7. Combine all sheets into a **Dashboard**, add filter actions (click a region on the pie chart to filter the other charts), and publish to Tableau Public/Server.

Both tools turn this static chart set into a fully interactive, filterable
dashboard that a business user can explore without touching code.
