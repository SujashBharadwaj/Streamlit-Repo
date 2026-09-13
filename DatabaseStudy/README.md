# DatabaseStudy

**A Chaos-Simulated Enterprise ERP Database for Analytics & Data Engineering Practice**

DatabaseStudy generates a realistic, dirty, 28-table enterprise ERP database spanning 8 years of operational history. Every execution produces a completely unique, non-deterministic dataset — solutions cannot be hardcoded or memorized.

Built for Data Analysts, Data Scientists, Analytics Engineers, and Database Administrators who want to practice on data that actually resembles production enterprise systems.

---

## The Problem

Most academic SQL courses teach with sanitized, perfectly normalized tables containing 10 clean rows. In production enterprise systems:

- Invoice dates are stored as `'NULL'`, `'N/A'`, `'0000-00-00'`, `''`, and actual `NULL` — all in the same column.
- API payloads are dumped as raw JSON strings inside SQL `TEXT` columns.
- MongoDB ObjectIds sit alongside integer primary keys and UUID v4 strings.
- Legacy migrations leave orphan foreign keys, duplicate records from HTTP retries, and floating-point rounding drift in financial ledgers.
- Date columns contain `YYYY-MM-DD`, `DD/MM/YYYY`, `MM-DD-YYYY`, ISO 8601 with timezone offsets, and raw epoch milliseconds — all in the same field.

DatabaseStudy replicates all of this.

---

## Quick Start

### Requirements
- Python 3.9+
- `faker` library

### Generate the Database

```bash
# Clone the repository
git clone https://github.com/SujashBharadwaj/DatabaseStudy.git
cd DatabaseStudy

# Install dependencies
pip install -r requirements.txt

# Generate the chaos ERP database (SQLite)
python generator.py

# Generate with CSV export
python generator.py --csv

# Custom output path
python generator.py --output my_erp.db
```

Each run produces a **~5 MB SQLite database** with **~61,000 rows** across 28 tables.

### Download a Pre-Generated Database

If you do not want to run the generator, you can download a pre-generated `.db` file from the [Releases](https://github.com/SujashBharadwaj/DatabaseStudy/releases) page on GitHub.

Open it with any SQLite client:
```bash
# Using the SQLite CLI
sqlite3 chaos_erp.db

# List all tables
.tables

# Preview a table
SELECT * FROM invoices LIMIT 10;
```

Or load it in Python:
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("chaos_erp.db")
df = pd.read_sql("SELECT * FROM sales_orders LIMIT 5", conn)
print(df)
```

---

## Schema Overview (28 Tables, 6 Modules)

| Module | Tables | Description |
|---|---|---|
| **Finance & GL** | `chart_of_accounts`, `fiscal_periods`, `gl_journal_headers`, `gl_journal_lines`, `tax_rates_history`, `bank_reconciliation_logs` | General ledger with floating-point drift, overlapping tax windows, and embedded API JSON |
| **Sales & CRM** | `customers`, `customer_branches`, `sales_orders`, `sales_order_items`, `invoices` | Dirty emails, orphan branches, raw checkout JSON, mixed null paid dates |
| **Procurement** | `vendors`, `purchase_orders`, `po_line_items`, `goods_received_notes`, `vendor_bills` | UUID + MongoDB ID + integer ID mixing, three-way match mismatches |
| **Inventory** | `warehouses`, `products`, `inventory_stock`, `stock_movements` | Negative stock, JSON spec blobs, missing movement timestamps |
| **Logistics** | `carriers`, `shipments`, `shipment_events`, `delivery_proofs` | Timezone inconsistency, GPS telemetry JSON, tracking anomalies |
| **HR & Payroll** | `departments`, `employees`, `salaries_history`, `timesheets` | Cyclic manager refs, > 24h/day timesheets, duplicate retry submissions |

Full DDL is in [`schema.sql`](schema.sql).

---

## Injected Chaos & Anomalies

Every run randomly injects:

- **Dirty null representations**: `NULL`, `'NULL'`, `'null'`, `'None'`, `'N/A'`, `'NA'`, `'0'`, `''`, `'-'`, `'#REF!'`, `'undefined'`
- **Mixed date formats**: ISO, DD/MM/YYYY, MM-DD-YYYY, epoch milliseconds, ISO 8601 with/without timezone — in the same column
- **Embedded JSON blobs**: Raw API payloads, checkout carts, GPS telemetry, product specifications — some intentionally truncated or malformed
- **ID format collisions**: Integer PKs, UUID v4, 24-char hex MongoDB ObjectIds across the same entities
- **Orphan foreign keys**: Order items referencing deleted products, branches referencing deleted customers
- **Financial drift**: GL journal lines with floating-point cent truncation (trial balances off by $0.01–$14.52)
- **Duplicate records**: Timesheet double-submissions from browser retry logic
- **Impossible values**: Negative inventory stock, > 24 hour work days, damaged quantities exceeding received quantities
- **Cyclic references**: Employees managing themselves

---

## Challenge Suite

Role-specific challenge prompts are provided in the [`challenges/`](challenges/) directory:

| File | Target Role | Focus Areas |
|---|---|---|
| [`01_data_analyst.md`](challenges/01_data_analyst.md) | Data Analyst | Cleaning, joins, aggregation, null handling, deduplication |
| [`02_data_scientist.md`](challenges/02_data_scientist.md) | Data Scientist | JSON feature extraction, date normalization, anomaly detection, churn modeling |
| [`03_analytics_engineer.md`](challenges/03_analytics_engineer.md) | Analytics Engineer | GL reconciliation, three-way matching, dimension modeling, SCD tax lookups |
| [`04_dba_performance.md`](challenges/04_dba_performance.md) | Database Administrator | Orphan FK audit, constraint enforcement, indexing, cyclic ref detection, archival |

Each challenge is designed to be solved against any generated instance of the database. Since every run is different, the specific row counts, error distributions, and dirty values will vary.

---

## Non-Deterministic by Design

The generator uses **no fixed random seed**. Every execution produces a unique database with:
- Different row counts per anomaly category.
- Different dirty value placements.
- Different JSON payload structures and truncation points.
- Different orphan FK distributions.

This prevents students and candidates from sharing static answer keys.

---

## License

[MIT](LICENSE)

---

## Author

**Sujash Bharadwaj**
- GitHub: [@SujashBharadwaj](https://github.com/SujashBharadwaj)

Contributions, feedback, and issue reports are welcome.
