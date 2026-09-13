# Challenge 03 — Analytics Engineer

These challenges target data modeling, reconciliation, deduplication, and building reliable analytical layers on top of chaotic source data.

---

## Challenge 3.1 — General Ledger Trial Balance Reconciliation

The `gl_journal_lines` table contains debit and credit amounts. In a properly balanced ledger, total debits should equal total credits per journal.

**Task**: Identify all journals (by `journal_id`) where `SUM(debit_amount) != SUM(credit_amount)`. Report the journal number, post date, and the imbalance amount. Handle null and dirty-null debit/credit values.

---

## Challenge 3.2 — Deduplicating Retry Events

The `timesheets` table has duplicate submissions from browser retry logic (same `employee_id` + `work_date` appearing multiple times).

**Task**: Write a deduplication query that keeps only the most recent submission (by `submitted_at`) for each employee-date pair, and returns the count of removed duplicates per employee.

---

## Challenge 3.3 — Three-Way Purchase Order Matching

Enterprise procurement uses three-way matching: PO → GRN → Vendor Bill.

**Task**: Using `purchase_orders`, `goods_received_notes`, and `vendor_bills`, identify:
1. POs with no corresponding GRN (goods never received).
2. POs with GRN but no vendor bill (received but never invoiced).
3. POs where the vendor bill `matching_status` indicates a mismatch.

---

## Challenge 3.4 — Building a Clean Dimension Table from Dirty Sources

The `customers` table has dirty emails, mixed-format phone numbers, and inconsistent `country_code` values across branches.

**Task**: Build a clean `dim_customers` output containing:
- `customer_id`
- `company_name`
- `normalized_email` (lowercase, trimmed)
- `primary_country` (standardized from branches)
- `total_branches`
- `is_duplicate` (flag for customers sharing the same normalized email)

---

## Challenge 3.5 — Inventory Discrepancy Report

Compare `inventory_stock.quantity_on_hand` against the net of `stock_movements`:
- `RECEIPT` and `TRANSFER` (to) add stock.
- `SHIPMENT`, `TRANSFER` (from), `ADJUSTMENT`, and `SCRAP` remove stock.

**Task**: For each product-warehouse pair, calculate the expected stock from movements and compare it to the reported `quantity_on_hand`. Flag discrepancies.

---

## Challenge 3.6 — Fiscal Period Revenue Rollup with Schema Drift

The `fiscal_periods` table has mixed date formats and inconsistent `is_closed` flags (`'CLOSED'`, `'open'`, `'1'`, `'0'`).

**Task**: Build a revenue rollup by fiscal period by joining `sales_orders` to `fiscal_periods`. You must normalize both `order_date` and `start_date`/`end_date` to compare them. Only include periods marked as closed (handling all representations).

---

## Challenge 3.7 — Slowly Changing Tax Rate Lookup

The `tax_rates_history` table has overlapping effective date windows.

**Task**: For a given `invoice_date`, determine the correct applicable tax rate for each tax code. Handle overlapping ranges by selecting the most recently created entry. Flag invoices where no valid tax rate window exists.
