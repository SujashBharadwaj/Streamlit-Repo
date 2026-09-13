# Challenge 04 — Database Administrator (DBA)

These challenges focus on schema integrity, constraint enforcement, index optimization, orphan detection, and performance tuning on a database that has suffered years of enterprise neglect.

---

## Challenge 4.1 — Orphan Foreign Key Audit

Multiple tables have foreign keys that reference non-existent parent records due to partial migrations and soft deletes.

**Task**: Write queries to identify all orphan records in:
- `customer_branches` → `customers`
- `sales_order_items` → `products`
- `gl_journal_lines` → `chart_of_accounts`
- `employees` → `employees` (cyclic self-referencing `manager_id`)

Report the table, orphan count, and sample orphan IDs.

---

## Challenge 4.2 — Adding Proper Constraints After the Fact

The schema was created with intentionally relaxed constraints.

**Task**: Write `ALTER TABLE` / migration statements to:
1. Add `NOT NULL` constraints on critical columns (identify which ones are currently violating this).
2. Add `FOREIGN KEY` constraints with `ON DELETE SET NULL` where appropriate.
3. Add `CHECK` constraints on `timesheets.hours_logged` (must be 0–24) and `inventory_stock.quantity_on_hand` (must be >= 0).

First, write diagnostic queries to identify how many rows would violate each constraint, then provide the DDL.

---

## Challenge 4.3 — Index Optimization Analysis

Consider these common query patterns:
1. `SELECT * FROM sales_orders WHERE customer_id = ? AND order_date BETWEEN ? AND ?`
2. `SELECT * FROM gl_journal_lines WHERE journal_id = ? AND account_id = ?`
3. `SELECT * FROM shipment_events WHERE shipment_id = ? ORDER BY event_timestamp`
4. `SELECT * FROM timesheets WHERE employee_id = ? AND work_date = ?`

**Task**: Propose a set of indexes for optimal query performance. Justify your choices (composite index ordering, covering indexes). Write the `CREATE INDEX` statements.

---

## Challenge 4.4 — Detecting and Fixing Cyclic References

The `employees` table has `manager_id` as a self-referential foreign key. Some rows have cyclic references (employee A manages employee B who manages employee A, or an employee managing themselves).

**Task**: Write a recursive CTE that detects all cyclic manager chains. Propose a fix strategy.

---

## Challenge 4.5 — Schema Drift Documentation

The database has accumulated multiple naming conventions and data type inconsistencies:
- Boolean columns stored as `TEXT` with mixed representations.
- Date columns stored as `TEXT` with mixed formats.
- ID columns mixing `INTEGER`, `TEXT` (UUID), and `TEXT` (MongoDB ObjectId).

**Task**: Produce a schema audit report listing:
- Every column storing boolean-like data and the distinct values found.
- Every column storing date-like data and the distinct formats detected.
- Every column storing JSON strings and the average / max payload size.

---

## Challenge 4.6 — Data Retention and Archival Query

Management requests that all records older than 5 years (before 2021-01-01) be archived.

**Task**: Write queries to:
1. Count the records per table that fall within the archival window.
2. Identify cross-table dependencies (e.g., archiving a `sales_order` requires archiving its `sales_order_items`, `invoices`, and `shipments`).
3. Propose a safe archival execution order that respects referential dependencies.

---

## Challenge 4.7 — Negative Stock & Data Integrity Recovery

The `inventory_stock` table contains negative `quantity_on_hand` values from system race conditions.

**Task**:
1. Identify all product-warehouse pairs with negative stock.
2. Cross-reference with `stock_movements` to determine if the negative balance is explainable (e.g., shipment recorded before receipt).
3. Write corrective `UPDATE` statements to set minimum stock to 0 and log the corrections in a new `stock_corrections` audit table.
