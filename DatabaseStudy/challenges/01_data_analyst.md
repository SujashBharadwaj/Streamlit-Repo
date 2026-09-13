# Challenge 01 — Data Analyst

These challenges test core data cleaning, joining, and aggregation skills using SQL.
Every time `generator.py` is run, the data is different — you cannot memorize answers.

---

## Challenge 1.1 — Handling Dirty Nulls

The `invoices` table stores unpaid dates using inconsistent representations:
`NULL`, `'NULL'`, `'null'`, `'N/A'`, `'0000-00-00'`, `''`, `'-'`, `'NOT_PAID'`, `'PENDING'`.

**Task**: Write a query that returns all truly unpaid invoices (where `paid_date` is logically missing or invalid), along with their `invoice_number`, `invoice_date`, and `total_amount`.

---

## Challenge 1.2 — Revenue by Fiscal Quarter

Using `sales_orders`, `sales_order_items`, and `fiscal_periods`:

**Task**: Calculate total revenue per fiscal quarter. You must handle:
- `order_date` stored in mixed date formats (ISO, DD/MM/YYYY, MM-DD-YYYY, epoch ms).
- Null / dirty null values in `unit_price` and `discount_rate`.

---

## Challenge 1.3 — Customer Deduplication

The `customers` table contains duplicate emails (some with trailing spaces, some uppercased).

**Task**: Identify all duplicate customer groups by normalized email and return `customer_id`, `company_name`, and `contact_email` for each duplicate set.

---

## Challenge 1.4 — Joining Across Dirty Foreign Keys

The `customer_branches` table has orphan `customer_id` values referencing customers that no longer exist.

**Task**: Write a query that lists all branches whose parent customer does not exist in the `customers` table.

---

## Challenge 1.5 — Standardizing Country Codes

The `customer_branches.country_code` column contains values like `'US'`, `'USA'`, `'United States'`, `'us'`, `'null'`.

**Task**: Write a query that groups branch counts by standardized country, mapping all variants to a single canonical country name.

---

## Challenge 1.6 — Top 10 Products by Order Volume

Using `sales_order_items` and `products`:

**Task**: Find the top 10 products by total quantity ordered. Handle orphan `product_id` values that don't exist in the `products` table (label them as "Unknown Product").

---

## Challenge 1.7 — Employee Headcount Over Time

Using `employees`:

**Task**: For each year from 2018 to 2026, calculate the number of active employees (hired on or before year-end, not terminated before year-end). You must handle `termination_date` stored as `'NULL'`, `'N/A'`, `''`, and actual dates in mixed formats.
