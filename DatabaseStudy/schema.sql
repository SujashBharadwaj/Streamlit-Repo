-- DatabaseStudy: Enterprise Chaos ERP Schema (28 Tables)
-- Note: Foreign key constraints are intentionally unenforced/relaxed in several tables
-- to replicate real-world legacy enterprise schema drift, partial migrations, and dirty data.

-- ============================================================================
-- 1. FINANCE & GENERAL LEDGER MODULE (6 Tables)
-- ============================================================================

CREATE TABLE IF NOT EXISTS chart_of_accounts (
    account_id INTEGER PRIMARY KEY,
    account_code TEXT NOT NULL,         -- e.g. "1010", "1010-US", "1010_LEGACY"
    account_name TEXT NOT NULL,
    account_type TEXT NOT NULL,         -- Asset, Liability, Equity, Revenue, Expense
    currency TEXT DEFAULT 'USD',
    is_active TEXT                      -- Dirty booleans: '1', '0', 'true', 'Y', 'NULL'
);

CREATE TABLE IF NOT EXISTS fiscal_periods (
    period_id INTEGER PRIMARY KEY,
    period_name TEXT NOT NULL,          -- e.g. "2018-Q1", "FY2019-P04"
    start_date TEXT NOT NULL,           -- Mixed format: ISO or DD/MM/YYYY or Epoch
    end_date TEXT NOT NULL,
    is_closed TEXT                      -- 'CLOSED', 'open', '1', '0'
);

CREATE TABLE IF NOT EXISTS gl_journal_headers (
    journal_id INTEGER PRIMARY KEY,
    journal_number TEXT UNIQUE,         -- "JV-2018-0001", "JNL_18_99"
    period_id INTEGER,
    post_date TEXT,                     -- Mixed date formats
    status TEXT,                        -- 'POSTED', 'posted', 'DRAFT', 'PENDING', 'VOID'
    source_system TEXT,                 -- 'SAP_MIG_2018', 'NETSUITE_V2', 'MANUAL_ENTRY'
    created_by TEXT
);

CREATE TABLE IF NOT EXISTS gl_journal_lines (
    line_id INTEGER PRIMARY KEY,
    journal_id INTEGER,
    account_id INTEGER,                 -- Some orphan IDs referencing deleted accounts
    line_description TEXT,
    debit_amount REAL,                  -- Mixed floating point and nulls
    credit_amount REAL,
    reconciled_flag TEXT                -- 'Y', 'N', 'null', 'None', 'PENDING'
);

CREATE TABLE IF NOT EXISTS tax_rates_history (
    tax_id INTEGER PRIMARY KEY,
    tax_code TEXT NOT NULL,             -- 'VAT_STD', 'GST_18', 'STATE_CA'
    rate_percent REAL,
    effective_from TEXT,                -- Overlapping date ranges (classic enterprise drift)
    effective_to TEXT,
    jurisdiction TEXT
);

CREATE TABLE IF NOT EXISTS bank_reconciliation_logs (
    recon_id INTEGER PRIMARY KEY,
    statement_date TEXT,
    bank_account_code TEXT,
    raw_api_payload TEXT,               -- Unparsed JSON blob from Plaid / Swift API
    discrepancy_amount REAL,
    resolution_status TEXT              -- 'RESOLVED', 'UNRESOLVED', 'MANUAL_OVERRIDE'
);

-- ============================================================================
-- 2. SALES & CUSTOMER MANAGEMENT MODULE (5 Tables)
-- ============================================================================

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    legacy_customer_num TEXT,           -- "CUST-00921", "MIG_8812"
    company_name TEXT NOT NULL,
    contact_email TEXT,                 -- Contains dirty emails, spaces, duplicate addresses
    phone_number TEXT,                  -- Mixed "+1 (555)...", "5551234567", "N/A"
    billing_address TEXT,
    tax_identifier TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS customer_branches (
    branch_id INTEGER PRIMARY KEY,
    customer_id INTEGER,                -- Some orphans from soft-deleted customers
    branch_name TEXT,
    city TEXT,
    country_code TEXT,                  -- 'US', 'USA', 'United States', 'null'
    is_headquarters TEXT
);

CREATE TABLE IF NOT EXISTS sales_orders (
    order_id INTEGER PRIMARY KEY,
    order_number TEXT,                  -- "SO-2019-1092", "ORD#9981"
    customer_id INTEGER,
    branch_id INTEGER,
    order_date TEXT,                    -- Mixed formats (timestamps, DD/MM/YYYY)
    order_status TEXT,                  -- 'FULFILLED', 'cancelled', 'Pending', 'SHIPPED', 'null'
    cart_raw_json TEXT,                 -- Raw checkout JSON containing nested items & coupon tokens
    mongo_oid TEXT                      -- Simulation of dual-write to Mongo: "64f1a2b3c9..."
);

CREATE TABLE IF NOT EXISTS sales_order_items (
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,                 -- Some orphans pointing to deprecated product IDs
    quantity INTEGER,
    unit_price REAL,                    -- Price snapshot at time of order
    discount_rate REAL,
    tax_rate REAL
);

CREATE TABLE IF NOT EXISTS invoices (
    invoice_id INTEGER PRIMARY KEY,
    invoice_number TEXT UNIQUE,
    order_id INTEGER,
    invoice_date TEXT,
    due_date TEXT,
    paid_date TEXT,                     -- Dirty representations: '0000-00-00', 'N/A', 'NULL', 'null', ''
    total_amount REAL,
    payment_status TEXT                 -- 'PAID', 'UNPAID', 'PARTIAL', 'DISPUTED'
);

-- ============================================================================
-- 3. PROCUREMENT & SUPPLY CHAIN MODULE (5 Tables)
-- ============================================================================

CREATE TABLE IF NOT EXISTS vendors (
    vendor_id INTEGER PRIMARY KEY,
    vendor_uuid TEXT,                   -- UUID v4 format
    legacy_vendor_code TEXT,            -- "VEND-8812", "SUPP_19"
    vendor_name TEXT NOT NULL,
    payment_terms TEXT,                 -- 'Net 30', 'NET30', '30_DAYS', 'Net60', 'NULL'
    rating REAL,
    country TEXT
);

CREATE TABLE IF NOT EXISTS purchase_orders (
    po_id INTEGER PRIMARY KEY,
    po_number TEXT,
    vendor_id INTEGER,
    po_date TEXT,
    approval_status TEXT,               -- 'APPROVED', 'Pending_Review', 'REJECTED', 'DRAFT'
    approved_by TEXT,
    currency TEXT
);

CREATE TABLE IF NOT EXISTS po_line_items (
    po_line_id INTEGER PRIMARY KEY,
    po_id INTEGER,
    product_id INTEGER,
    ordered_quantity INTEGER,
    unit_cost REAL,
    unit_of_measure TEXT                -- 'PCS', 'BOX', 'KGS', 'EA', 'CASE', 'null'
);

CREATE TABLE IF NOT EXISTS goods_received_notes (
    grn_id INTEGER PRIMARY KEY,
    grn_number TEXT,
    po_id INTEGER,
    received_date TEXT,
    warehouse_id INTEGER,
    received_quantity INTEGER,
    damaged_quantity INTEGER,
    inspector_notes TEXT
);

CREATE TABLE IF NOT EXISTS vendor_bills (
    bill_id INTEGER PRIMARY KEY,
    vendor_id INTEGER,
    po_id INTEGER,
    bill_reference TEXT,
    bill_date TEXT,
    amount_due REAL,
    matching_status TEXT                -- '3_WAY_MATCHED', 'PRICE_MISMATCH', 'QTY_MISMATCH', 'PENDING'
);

-- ============================================================================
-- 4. INVENTORY & WAREHOUSE OPERATIONS MODULE (4 Tables)
-- ============================================================================

CREATE TABLE IF NOT EXISTS warehouses (
    warehouse_id INTEGER PRIMARY KEY,
    warehouse_code TEXT,                -- "WH-EAST", "WH_01_OLD"
    warehouse_name TEXT,
    location_city TEXT,
    capacity_sqft INTEGER,
    is_temperature_controlled TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    sku TEXT UNIQUE,                    -- "SKU-9921-A", "LEGACY_PRD_44"
    product_name TEXT NOT NULL,
    category TEXT,
    specifications_json TEXT,           -- Unstructured JSON attributes (weight, color, dimensions)
    standard_cost REAL,
    list_price REAL,
    discontinued_flag TEXT              -- '0', '1', 'true', 'false', 'Y'
);

CREATE TABLE IF NOT EXISTS inventory_stock (
    stock_id INTEGER PRIMARY KEY,
    warehouse_id INTEGER,
    product_id INTEGER,
    quantity_on_hand INTEGER,           -- Contains negative numbers from system race conditions
    reserved_quantity INTEGER,
    last_counted_date TEXT
);

CREATE TABLE IF NOT EXISTS stock_movements (
    movement_id INTEGER PRIMARY KEY,
    movement_type TEXT,                 -- 'RECEIPT', 'SHIPMENT', 'TRANSFER', 'ADJUSTMENT'
    product_id INTEGER,
    from_warehouse_id INTEGER,
    to_warehouse_id INTEGER,
    quantity INTEGER,
    movement_timestamp TEXT,            -- Contains missing dates from system outages
    reference_document TEXT             -- "SO-2020-99", "PO-102", "AUDIT_ADJ"
);

-- ============================================================================
-- 5. LOGISTICS & FLEET SHIPPING MODULE (4 Tables)
-- ============================================================================

CREATE TABLE IF NOT EXISTS carriers (
    carrier_id INTEGER PRIMARY KEY,
    carrier_name TEXT NOT NULL,         -- "FedEx", "DHL Express", "Local Fleet"
    service_level TEXT,                 -- 'EXPRESS', 'GROUND', 'OVERNIGHT', 'STANDARD'
    tracking_url_template TEXT
);

CREATE TABLE IF NOT EXISTS shipments (
    shipment_id INTEGER PRIMARY KEY,
    tracking_number TEXT,
    order_id INTEGER,
    carrier_id INTEGER,
    dispatch_date TEXT,                 -- Mixed timezones (UTC vs EST vs ISO without offset)
    delivery_estimate TEXT,
    delivery_status TEXT                -- 'IN_TRANSIT', 'DELIVERED', 'LOST', 'FAILED_ATTEMPT'
);

CREATE TABLE IF NOT EXISTS shipment_events (
    event_id INTEGER PRIMARY KEY,
    shipment_id INTEGER,
    event_type TEXT,                    -- 'DEPARTED_FACILITY', 'GPS_PING', 'CUSTOMS_HOLD'
    event_timestamp TEXT,
    location_code TEXT,
    telemetry_raw_json TEXT             -- Raw sensor ping payload: {"lat": ..., "lng": ..., "temp_c": ...}
);

CREATE TABLE IF NOT EXISTS delivery_proofs (
    proof_id INTEGER PRIMARY KEY,
    shipment_id INTEGER,
    signed_by TEXT,
    signature_timestamp TEXT,
    exception_notes TEXT                -- Notes on damaged boxes, missed gates, etc.
);

-- ============================================================================
-- 6. HR & PAYROLL MODULE (4 Tables)
-- ============================================================================

CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY,
    department_code TEXT,               -- "FIN", "ENG", "OPS", "EXEC"
    department_name TEXT NOT NULL,
    parent_department_id INTEGER        -- Self-referential hierarchy with null roots
);

CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    legacy_badge_no TEXT,               -- "EMP001", "B-9921"
    first_name TEXT,
    last_name TEXT,
    department_id INTEGER,
    manager_id INTEGER,                 -- Null for C-level, but some cyclic references from bad data
    hire_date TEXT,                     -- Spanning 2017 to 2026
    termination_date TEXT,              -- Mixed null strings for active staff: 'NULL', 'N/A', ''
    employment_status TEXT              -- 'ACTIVE', 'TERMINATED', 'ON_LEAVE', 'PROBATION'
);

CREATE TABLE IF NOT EXISTS salaries_history (
    salary_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    effective_date TEXT,
    annual_salary REAL,
    currency TEXT,                      -- 'USD', 'EUR', 'GBP'
    change_reason TEXT                  -- 'PROMOTION', 'ANNUAL_MERIT', 'MARKET_ADJUSTMENT'
);

CREATE TABLE IF NOT EXISTS timesheets (
    timesheet_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    work_date TEXT,
    hours_logged REAL,                  -- Contains anomalies: 24.5 hrs/day, negative hours, duplicates
    task_code TEXT,                     -- "BILLABLE_CLIENT", "INTERNAL_MEETING", "OVERTIME"
    submitted_at TEXT                   -- Duplicate submissions due to browser retry logic
);
