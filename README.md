# THIS IS BUSINESS

> **Turn your business data into meaningful insights.**

**THIS IS BUSINESS** is a complete, enterprise-grade business data analytics platform. It enables businesses to ingest sales datasets in CSV or Excel format, store normalized transactions in a relational SQL database, perform rigorous data cleaning and reconciliation, calculate core financial and customer metrics, generate longitudinal cohort retention heatmaps, derive automated business insights, and download publication-quality PDF and CSV reports.

---

## 🎨 Theme & UI Design

- **Primary**: Sky Blue (`#38BDF8`)
- **Secondary**: Royal Blue (`#2563EB`)
- **Background**: Pure White (`#FFFFFF`) / Light Blue (`#EAF6FF`)
- **Text**: Dark Navy (`#172B4D`)
- **Accent**: Soft Sky (`#7DD3FC`)
- **Dark Mode**: Dark Navy (`#0B132B`), Slate Cards (`#1E293B`), Light Text (`#F8FAFC`)
- **Languages**: Complete **English (EN)** & **हिंदी (HI)** localization across all views, metrics, charts, and explanations.

---

## 🏗️ Relational SQL Database Architecture

Built with **SQLAlchemy ORM** and version-controlled via **Alembic migrations**. The architecture is configured for **SQLite** during local development and is fully compatible with **PostgreSQL**.

### Relational Schema:
1. `users`: Authentication and account ownership (`id`, `name`, `email`, `password_hash`, `created_at`).
2. `datasets`: Metadata and raw file path isolation (`id`, `user_id`, `dataset_name`, `original_filename`, `file_format`, `uploaded_at`, `total_rows`, `total_columns`, `status`, `raw_file_path`, `data_quality_score`, `currency_symbol`, `monetary_type`).
3. `dataset_columns`: Detected and mapped schema attributes (`id`, `dataset_id`, `column_name`, `detected_type`, `mapped_type`).
4. `customers`: Isolated unique customer accounts per dataset (`id`, `dataset_id`, `customer_key`, `UniqueConstraint('dataset_id', 'customer_key')`).
5. `products`: Normalized product inventory items per dataset (`id`, `dataset_id`, `product_key`, `product_name`, `category`, `UniqueConstraint('dataset_id', 'product_key')`).
6. `orders`: Individual customer transactions (`id`, `dataset_id`, `customer_id`, `order_number`, `order_date`, `order_status`).
7. `order_items`: Line-item breakdown of transactions (`id`, `order_id`, `product_id`, `quantity`, `unit_price`, `line_amount`, `item_status`).
8. `analysis_results`: Serialized analytical outputs and snapshots (`id`, `dataset_id`, `analysis_type`, `result_data`, `generated_at`).
9. `reports`: Generated report history (`id`, `dataset_id`, `report_name`, `report_type`, `report_path`, `generated_at`).

*All relationships utilize cascading deletes (`ondelete="CASCADE"`) to maintain referential integrity without leaving orphan rows upon dataset deletion.*

---

## 📐 Mathematical & Business Calculation Rules

### 1. Revenue Integrity Rule
Before running analysis, the platform lets the user configure how the monetary column is interpreted:
* **Unit Price**: $\text{Line Revenue} = \text{Quantity} \times \text{Unit Price}$
* **Total Line Amount**: $\text{Line Revenue} = \text{Line Amount}$ *(strictly prevents double multiplication)*
* **Refunds & Cancellations**: Returns (invoices starting with `'C'` or negative quantities) are separated from gross sales:
  $$\text{Gross Sales} = \sum \text{Positive Line Amounts}$$
  $$\text{Refund Amount} = \sum |\text{Cancelled / Refunded Amounts}|$$
  $$\text{Net Revenue} = \text{Gross Sales} - \text{Refund Amount}$$
  $$\text{Net Units Sold} = \text{Gross Units} - \text{Returned Units}$$

### 2. Customer Identification Rule
* Missing customer IDs are **never** grouped together as a single customer (e.g. "Guest"). Each missing entry is assigned an isolated anonymous identifier to prevent artificial inflation of repeat rates.
* **Repeat Customer Definition**: Defined strictly as a customer with **at least two distinct completed orders** ($\ge 2$ valid invoices). It is never calculated by row count.

### 3. Cohort Retention Analysis
* Customers are grouped into cohorts by their first valid transaction month ($M_0$).
* For each subsequent month $M_n$, the retention rate is calculated:
  $$\text{Retention Rate} = \left(\frac{\text{Active Cohort Customers in Month } n}{\text{Cohort Size in Month 0}}\right) \times 100$$
* Month 0 is always $100.0\%$.

---

## 🚀 Key Features

1. **Animated Landing Page**: Exact bold heading **THIS IS BUSINESS**, subtitle, description, "Start Analyzing" CTA, and About Platform overview.
2. **Data Upload System**: Supports `.csv`, `.xlsx`, `.xls` with 10-row preview, missing values count, duplicate count, fuzzy column detection, and monetary configuration.
3. **Executive Dashboard**: 10 dynamic KPI cards, date range filtering (Last 30 Days, 90 Days, 6 Months, 1 Year, Custom), and "Explain My Data" drawer.
4. **Customer & Cohort Analysis**: Longitudinal cohort retention heatmap, monthly acquisition trends, order frequency distribution, and top 10 customers leaderboard.
5. **Product Intelligence**: Catalog search, sorting by revenue/units/price, lowest-selling products, category breakdown, and monthly product drilldown.
6. **Sales Analysis**: Monthly net revenue progression, dual-axis revenue vs orders chart, monthly units sold, and MoM velocity.
7. **Reports & Dataset History**:
   - Download Executive Vector PDF with charts and data quality breakdown.
   - Download Customer Analysis CSV.
   - Download Product Analysis CSV.
   - Download Monthly Sales CSV.
   - Download Cohort Retention CSV.
   - Reopen and delete stored datasets from SQL database.

---

## ⚡ Quick Start & Running Instructions

### Option 1: Unified Server (Recommended)
The backend serves both the FastAPI REST API and the compiled React production frontend on a single unified port:

```powershell
# Double-click start_app.bat or run:
python backend\main.py
```
Then navigate to: **`http://127.0.0.1:8000`**

### Option 2: Full Development Mode (Separate Servers)
1. **Start Backend**:
   ```powershell
   python backend\main.py
   ```
2. **Start Frontend (Vite Dev Server)**:
   ```powershell
   cd frontend
   npm run dev
   ```
   *Runs at `http://localhost:5173` with Hot Module Replacement (HMR).*

---

## 🧪 Automated Testing

Execute the comprehensive end-to-end verification suite:
```powershell
python backend\tests\test_comprehensive.py
```

This verifies:
1. SQL Database persistence, relations, and cascading deletes.
2. Revenue calculation rules (Unit Price vs Total Amount).
3. Customer identification and repeat customer rules ($\ge 2$ distinct orders).
4. Cohort retention heatmap calculation ($M_0 = 100\%$).
5. End-to-end sample retail dataset ingestion into SQL.
6. Vector PDF report generation and all 4 CSV exports.
