#!/usr/bin/env python3
"""
DatabaseStudy — Chaos-Simulated Enterprise ERP Database Generator
=================================================================
Generates a fully randomized, non-deterministic 28-table enterprise ERP
database in SQLite. Every execution produces a unique dataset so no two
runs are identical and solutions cannot be hardcoded.

Usage:
    python generator.py              # Creates chaos_erp.db in current directory
    python generator.py --output my_erp.db
    python generator.py --csv        # Also exports every table to CSV

Author : Sujash Bharadwaj
License: MIT
"""

import argparse
import csv
import json
import os
import random
import sqlite3
import string
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Attempt to import Faker; provide a clear message if missing.
# ---------------------------------------------------------------------------
try:
    from faker import Faker
except ImportError:
    print("ERROR: The 'faker' library is required.")
    print("Install it with:  pip install faker")
    sys.exit(1)

fake = Faker()

# ---------------------------------------------------------------------------
# Constants & helpers
# ---------------------------------------------------------------------------

YEAR_START = 2018
YEAR_END = 2026

DIRTY_NULLS = [None, "NULL", "null", "None", "N/A", "NA", "0", "", "-", "#REF!", "undefined"]
DIRTY_BOOLS = ["1", "0", "true", "false", "Y", "N", "yes", "no", "TRUE", "FALSE", "null", "NULL"]
DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%Y-%m-%dT%H:%M:%SZ", "%d-%b-%Y"]

ACCOUNT_TYPES = ["Asset", "Liability", "Equity", "Revenue", "Expense"]
CURRENCIES = ["USD", "EUR", "GBP", "INR", "JPY", "CAD", "AUD"]
JOURNAL_STATUSES = ["POSTED", "posted", "DRAFT", "PENDING", "VOID", "Posted", "draft"]
SOURCE_SYSTEMS = ["SAP_MIG_2018", "NETSUITE_V2", "MANUAL_ENTRY", "LEGACY_ORACLE", "CSV_IMPORT_2019", "API_SYNC"]
RECON_FLAGS = ["Y", "N", "null", "None", "PENDING", "", "0", "1"]
PERIOD_STATUSES = ["CLOSED", "open", "OPEN", "closed", "1", "0", "true", "false"]
ORDER_STATUSES = ["FULFILLED", "cancelled", "Pending", "SHIPPED", "null", "PROCESSING", "RETURNED", "shipped"]
PAYMENT_STATUSES = ["PAID", "UNPAID", "PARTIAL", "DISPUTED", "paid", "null"]
DIRTY_PAID_DATES = ["0000-00-00", "N/A", "NULL", "null", "", "-", "NOT_PAID", "PENDING"]
PAYMENT_TERMS = ["Net 30", "NET30", "30_DAYS", "Net60", "Net 45", "PREPAID", "NULL", "null", "COD"]
APPROVAL_STATUSES = ["APPROVED", "Pending_Review", "REJECTED", "DRAFT", "approved", "PENDING"]
UOM_VALUES = ["PCS", "BOX", "KGS", "EA", "CASE", "null", "LBS", "PALLET", "EACH", "UNIT"]
MATCHING_STATUSES = ["3_WAY_MATCHED", "PRICE_MISMATCH", "QTY_MISMATCH", "PENDING", "UNMATCHED"]
MOVEMENT_TYPES = ["RECEIPT", "SHIPMENT", "TRANSFER", "ADJUSTMENT", "RETURN", "SCRAP"]
DELIVERY_STATUSES = ["IN_TRANSIT", "DELIVERED", "LOST", "FAILED_ATTEMPT", "in_transit", "RETURNED_TO_SENDER"]
CARRIER_SERVICES = ["EXPRESS", "GROUND", "OVERNIGHT", "STANDARD", "ECONOMY"]
SHIPMENT_EVENTS = ["DEPARTED_FACILITY", "GPS_PING", "CUSTOMS_HOLD", "ARRIVED_SORT_CENTER", "OUT_FOR_DELIVERY", "SCAN_ERROR"]
EMPLOYMENT_STATUSES = ["ACTIVE", "TERMINATED", "ON_LEAVE", "PROBATION", "active", "SUSPENDED"]
DEPT_CODES = ["FIN", "ENG", "OPS", "EXEC", "MKT", "HR", "LEGAL", "IT", "SALES", "R&D", "QA", "SUPPORT"]
SALARY_REASONS = ["PROMOTION", "ANNUAL_MERIT", "MARKET_ADJUSTMENT", "LATERAL_MOVE", "CORRECTION"]
TASK_CODES = ["BILLABLE_CLIENT", "INTERNAL_MEETING", "OVERTIME", "TRAINING", "PTO", "ADMIN", "PROJECT_X"]
RECON_RESOLUTION = ["RESOLVED", "UNRESOLVED", "MANUAL_OVERRIDE", "PENDING_REVIEW", "ESCALATED"]
TAX_CODES = ["VAT_STD", "GST_18", "GST_12", "GST_5", "STATE_CA", "STATE_NY", "VAT_REDUCED", "EXEMPT", "ZERO_RATED"]
PRODUCT_CATEGORIES = ["Electronics", "Raw Materials", "Finished Goods", "MRO Supplies", "Software Licenses", "Packaging", "Chemicals"]


def rand_date(start_year=YEAR_START, end_year=YEAR_END):
    """Return a random datetime between start_year and end_year."""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, max(delta, 1)))


def dirty_date(dt, force_dirty=False):
    """Format a datetime using a random format, occasionally returning epoch or dirty string."""
    if dt is None:
        return random.choice(DIRTY_NULLS)
    if force_dirty or random.random() < 0.08:
        # Return epoch milliseconds as string
        return str(int(dt.timestamp() * 1000))
    return dt.strftime(random.choice(DATE_FORMATS))


def maybe_dirty_null(value, probability=0.05):
    """With some probability, replace a value with a dirty null representation."""
    if random.random() < probability:
        return random.choice(DIRTY_NULLS)
    return value


def dirty_bool(probability_dirty=0.15):
    """Return a dirty boolean string."""
    if random.random() < probability_dirty:
        return random.choice(DIRTY_BOOLS)
    return random.choice(["1", "0"])


def mongo_oid():
    """Generate a fake 24-char hex MongoDB ObjectId."""
    return "".join(random.choices("0123456789abcdef", k=24))


def truncated_json(data):
    """Occasionally produce truncated / malformed JSON."""
    s = json.dumps(data)
    if random.random() < 0.06:
        # Truncate at a random point
        cut = random.randint(len(s) // 3, len(s) - 2)
        return s[:cut]
    return s


def noisy_phone():
    """Generate phone numbers in various dirty formats."""
    formats = [
        "+1 (555) {}-{}".format(random.randint(100, 999), random.randint(1000, 9999)),
        "555{:03d}{:04d}".format(random.randint(0, 999), random.randint(0, 9999)),
        "+44 20 {} {}".format(random.randint(1000, 9999), random.randint(1000, 9999)),
        "N/A",
        "",
        str(random.randint(1000000000, 9999999999)),
        "(555) {}-{}".format(random.randint(100, 999), random.randint(1000, 9999)),
    ]
    return random.choice(formats)


def noisy_country():
    """Return country in various inconsistent formats."""
    countries = [
        ("US", "USA", "United States", "US ", "us"),
        ("GB", "UK", "United Kingdom", "GBR"),
        ("IN", "IND", "India"),
        ("DE", "DEU", "Germany"),
        ("JP", "JPN", "Japan"),
        ("AU", "AUS", "Australia"),
    ]
    group = random.choice(countries)
    return random.choice(group)


# ---------------------------------------------------------------------------
# Table generation functions (one per table)
# ---------------------------------------------------------------------------

def gen_chart_of_accounts(cur, n=80):
    rows = []
    for i in range(1, n + 1):
        code_fmt = random.choice([
            f"{random.randint(1000,9999)}",
            f"{random.randint(1000,9999)}-{random.choice(['US','EU','IN'])}",
            f"{random.randint(1000,9999)}_LEGACY",
        ])
        rows.append((
            i,
            code_fmt,
            fake.bs().title(),
            random.choice(ACCOUNT_TYPES),
            maybe_dirty_null(random.choice(CURRENCIES), 0.03),
            dirty_bool(),
        ))
    cur.executemany("INSERT INTO chart_of_accounts VALUES (?,?,?,?,?,?)", rows)
    return n


def gen_fiscal_periods(cur):
    rows = []
    pid = 1
    for year in range(YEAR_START, YEAR_END + 1):
        for q in range(1, 5):
            month_start = (q - 1) * 3 + 1
            month_end = q * 3
            start = datetime(year, month_start, 1)
            end = datetime(year, month_end, 28)
            name_fmt = random.choice([
                f"{year}-Q{q}",
                f"FY{year}-P{q:02d}",
                f"Q{q}_{year}",
            ])
            rows.append((
                pid,
                name_fmt,
                dirty_date(start),
                dirty_date(end),
                random.choice(PERIOD_STATUSES),
            ))
            pid += 1
    cur.executemany("INSERT INTO fiscal_periods VALUES (?,?,?,?,?)", rows)
    return pid - 1


def gen_gl_journal_headers(cur, num_periods, n=2000):
    rows = []
    for i in range(1, n + 1):
        num_fmt = random.choice([
            f"JV-{random.randint(2018,2026)}-{i:05d}",
            f"JNL_{random.randint(18,26)}_{i:05d}",
            f"GL-{uuid.uuid4().hex[:8].upper()}-{i}",
        ])
        rows.append((
            i,
            num_fmt,
            random.randint(1, num_periods),
            dirty_date(rand_date()),
            random.choice(JOURNAL_STATUSES),
            random.choice(SOURCE_SYSTEMS),
            maybe_dirty_null(fake.name(), 0.08),
        ))
    cur.executemany("INSERT INTO gl_journal_headers VALUES (?,?,?,?,?,?,?)", rows)
    return n


def gen_gl_journal_lines(cur, num_journals, num_accounts, n=8000):
    rows = []
    for i in range(1, n + 1):
        journal_id = random.randint(1, num_journals)
        # Occasionally reference a non-existent account (orphan FK)
        if random.random() < 0.03:
            account_id = random.randint(num_accounts + 1, num_accounts + 500)
        else:
            account_id = random.randint(1, num_accounts)

        # Generate debit/credit — mostly balanced, but inject imbalances
        amount = round(random.uniform(10.0, 250000.0), 2)
        if random.random() < 0.5:
            debit = amount
            credit = 0.0
        else:
            debit = 0.0
            credit = amount

        # ~1.5% of lines: introduce floating-point truncation drift
        if random.random() < 0.015:
            if debit > 0:
                debit = round(debit + random.uniform(0.001, 14.52), 2)
            else:
                credit = round(credit - random.uniform(0.001, 0.99), 2)

        rows.append((
            i,
            journal_id,
            account_id,
            maybe_dirty_null(fake.sentence(nb_words=4), 0.1),
            maybe_dirty_null(debit, 0.02),
            maybe_dirty_null(credit, 0.02),
            random.choice(RECON_FLAGS),
        ))
    cur.executemany("INSERT INTO gl_journal_lines VALUES (?,?,?,?,?,?,?)", rows)
    return n


def gen_tax_rates_history(cur, n=60):
    rows = []
    for i in range(1, n + 1):
        eff_from = rand_date()
        # Overlapping windows: effective_to might be before effective_from
        eff_to = eff_from + timedelta(days=random.randint(-30, 730))
        rows.append((
            i,
            random.choice(TAX_CODES),
            round(random.uniform(0, 28.0), 2),
            dirty_date(eff_from),
            dirty_date(eff_to),
            maybe_dirty_null(fake.country(), 0.06),
        ))
    cur.executemany("INSERT INTO tax_rates_history VALUES (?,?,?,?,?,?)", rows)
    return n


def gen_bank_reconciliation_logs(cur, n=500):
    rows = []
    for i in range(1, n + 1):
        payload = {
            "transaction_id": f"TXN-{uuid.uuid4().hex[:12]}",
            "bank_ref": f"REF-{random.randint(100000, 999999)}",
            "api_status": random.choice(["SUCCESS", "TIMEOUT", "PARTIAL", 200, 500]),
            "timestamp": dirty_date(rand_date()),
            "amount": round(random.uniform(-50000, 500000), 2),
            "mongo_id": mongo_oid(),
        }
        rows.append((
            i,
            dirty_date(rand_date()),
            f"BANK-{random.randint(1000,9999)}",
            truncated_json(payload),
            maybe_dirty_null(round(random.uniform(-5000, 5000), 2), 0.12),
            random.choice(RECON_RESOLUTION),
        ))
    cur.executemany("INSERT INTO bank_reconciliation_logs VALUES (?,?,?,?,?,?)", rows)
    return n


def gen_customers(cur, n=400):
    rows = []
    used_emails = []
    for i in range(1, n + 1):
        email = fake.email()
        # Inject duplicate emails ~5%
        if used_emails and random.random() < 0.05:
            email = random.choice(used_emails)
        # Occasionally inject trailing spaces or uppercase
        if random.random() < 0.08:
            email = email.upper() + " "
        used_emails.append(email)

        legacy_num = random.choice([
            f"CUST-{random.randint(100, 99999):05d}",
            f"MIG_{random.randint(1000, 9999)}",
            f"C{i}",
        ])
        rows.append((
            i,
            legacy_num,
            fake.company(),
            maybe_dirty_null(email, 0.04),
            noisy_phone(),
            maybe_dirty_null(fake.address().replace("\n", ", "), 0.06),
            maybe_dirty_null(fake.bothify("??-########"), 0.1),
            dirty_date(rand_date()),
        ))
    cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?,?,?)", rows)
    return n


def gen_customer_branches(cur, num_customers, n=600):
    rows = []
    for i in range(1, n + 1):
        # ~4% orphan customer IDs
        if random.random() < 0.04:
            cust_id = random.randint(num_customers + 1, num_customers + 200)
        else:
            cust_id = random.randint(1, num_customers)
        rows.append((
            i,
            cust_id,
            maybe_dirty_null(fake.city() + " Branch", 0.05),
            maybe_dirty_null(fake.city(), 0.03),
            noisy_country(),
            dirty_bool(0.2),
        ))
    cur.executemany("INSERT INTO customer_branches VALUES (?,?,?,?,?,?)", rows)
    return n


def gen_sales_orders(cur, num_customers, num_branches, n=3000):
    rows = []
    for i in range(1, n + 1):
        order_num = random.choice([
            f"SO-{random.randint(2018,2026)}-{random.randint(1,9999):04d}",
            f"ORD#{random.randint(1000,99999)}",
            f"WEB-{uuid.uuid4().hex[:8]}",
        ])
        # Build a realistic checkout JSON payload
        num_items = random.randint(1, 5)
        cart_items = []
        for _ in range(num_items):
            item = {
                random.choice(["productId", "product_id", "id", "sku"]): random.randint(1, 500),
                "qty": random.randint(1, 20),
                "price": round(random.uniform(5.0, 2500.0), 2),
            }
            if random.random() < 0.3:
                item["coupon"] = fake.bothify("PROMO-####")
            cart_items.append(item)
        cart_json = {
            "items": cart_items,
            "checkout_ts": dirty_date(rand_date()),
            "session_token": uuid.uuid4().hex,
        }
        rows.append((
            i,
            order_num,
            random.randint(1, num_customers),
            maybe_dirty_null(random.randint(1, num_branches), 0.08),
            dirty_date(rand_date()),
            random.choice(ORDER_STATUSES),
            truncated_json(cart_json),
            maybe_dirty_null(mongo_oid(), 0.7),  # 30% have mongo OIDs
        ))
    cur.executemany("INSERT INTO sales_orders VALUES (?,?,?,?,?,?,?,?)", rows)
    return n


def gen_sales_order_items(cur, num_orders, num_products, n=9000):
    rows = []
    for i in range(1, n + 1):
        order_id = random.randint(1, num_orders)
        # ~3% orphan product IDs
        if random.random() < 0.03:
            product_id = random.randint(num_products + 1, num_products + 300)
        else:
            product_id = random.randint(1, num_products)
        rows.append((
            i,
            order_id,
            product_id,
            random.randint(1, 100),
            round(random.uniform(1.0, 5000.0), 2),
            maybe_dirty_null(round(random.uniform(0, 0.40), 2), 0.15),
            maybe_dirty_null(round(random.uniform(0, 0.28), 2), 0.1),
        ))
    cur.executemany("INSERT INTO sales_order_items VALUES (?,?,?,?,?,?,?)", rows)
    return n


def gen_invoices(cur, num_orders, n=2800):
    rows = []
    for i in range(1, n + 1):
        inv_num = f"INV-{random.randint(2018,2026)}-{i:06d}"
        inv_date = rand_date()
        due_date = inv_date + timedelta(days=random.choice([15, 30, 45, 60, 90]))
        # Paid date: dirty representations for unpaid
        if random.random() < 0.35:
            paid_date = random.choice(DIRTY_PAID_DATES)
        else:
            paid_date = dirty_date(inv_date + timedelta(days=random.randint(1, 120)))
        rows.append((
            i,
            inv_num,
            random.randint(1, num_orders),
            dirty_date(inv_date),
            dirty_date(due_date),
            paid_date,
            round(random.uniform(50.0, 500000.0), 2),
            random.choice(PAYMENT_STATUSES),
        ))
    cur.executemany("INSERT INTO invoices VALUES (?,?,?,?,?,?,?,?)", rows)
    return n


def gen_vendors(cur, n=200):
    rows = []
    for i in range(1, n + 1):
        legacy_code = random.choice([
            f"VEND-{random.randint(1000,9999)}",
            f"SUPP_{random.randint(10,999)}",
            f"V{i:04d}",
        ])
        rows.append((
            i,
            str(uuid.uuid4()),
            legacy_code,
            fake.company(),
            random.choice(PAYMENT_TERMS),
            maybe_dirty_null(round(random.uniform(1.0, 5.0), 1), 0.08),
            noisy_country(),
        ))
    cur.executemany("INSERT INTO vendors VALUES (?,?,?,?,?,?,?)", rows)
    return n


def gen_purchase_orders(cur, num_vendors, n=1500):
    rows = []
    for i in range(1, n + 1):
        po_num = random.choice([
            f"PO-{random.randint(2018,2026)}-{random.randint(1,9999):04d}",
            f"PURC#{random.randint(10000,99999)}",
        ])
        rows.append((
            i,
            po_num,
            random.randint(1, num_vendors),
            dirty_date(rand_date()),
            random.choice(APPROVAL_STATUSES),
            maybe_dirty_null(fake.name(), 0.12),
            random.choice(CURRENCIES),
        ))
    cur.executemany("INSERT INTO purchase_orders VALUES (?,?,?,?,?,?,?)", rows)
    return n


def gen_po_line_items(cur, num_pos, num_products, n=5000):
    rows = []
    for i in range(1, n + 1):
        rows.append((
            i,
            random.randint(1, num_pos),
            random.randint(1, num_products),
            random.randint(1, 5000),
            round(random.uniform(0.5, 10000.0), 2),
            random.choice(UOM_VALUES),
        ))
    cur.executemany("INSERT INTO po_line_items VALUES (?,?,?,?,?,?)", rows)
    return n


def gen_goods_received_notes(cur, num_pos, num_warehouses, n=1200):
    rows = []
    for i in range(1, n + 1):
        grn_num = f"GRN-{random.randint(10000,99999)}"
        rcvd_qty = random.randint(1, 2000)
        # Damaged quantity: sometimes exceeds received (bad data)
        dmg = 0
        if random.random() < 0.15:
            dmg = random.randint(0, rcvd_qty + 50)
        rows.append((
            i,
            grn_num,
            random.randint(1, num_pos),
            dirty_date(rand_date()),
            random.randint(1, num_warehouses),
            rcvd_qty,
            dmg,
            maybe_dirty_null(fake.sentence(), 0.3),
        ))
    cur.executemany("INSERT INTO goods_received_notes VALUES (?,?,?,?,?,?,?,?)", rows)
    return n


def gen_vendor_bills(cur, num_vendors, num_pos, n=1400):
    rows = []
    for i in range(1, n + 1):
        rows.append((
            i,
            random.randint(1, num_vendors),
            random.randint(1, num_pos),
            f"BILL-{uuid.uuid4().hex[:10].upper()}",
            dirty_date(rand_date()),
            round(random.uniform(100.0, 500000.0), 2),
            random.choice(MATCHING_STATUSES),
        ))
    cur.executemany("INSERT INTO vendor_bills VALUES (?,?,?,?,?,?,?)", rows)
    return n


def gen_warehouses(cur, n=12):
    rows = []
    for i in range(1, n + 1):
        code = random.choice([
            f"WH-{fake.city()[:4].upper()}",
            f"WH_{i:02d}_OLD",
            f"DC-{random.randint(100,999)}",
        ])
        rows.append((
            i,
            code,
            f"{fake.city()} Distribution Center",
            fake.city(),
            random.randint(5000, 500000),
            dirty_bool(0.2),
        ))
    cur.executemany("INSERT INTO warehouses VALUES (?,?,?,?,?,?)", rows)
    return n


def gen_products(cur, n=350):
    rows = []
    for i in range(1, n + 1):
        sku = random.choice([
            f"SKU-{i:05d}-{random.choice(string.ascii_uppercase)}",
            f"LEGACY_PRD_{i:04d}",
            f"P{i:05d}",
        ])
        specs = {
            "weight_kg": round(random.uniform(0.01, 500.0), 2),
            "color": fake.color_name(),
            "dimensions_cm": f"{random.randint(1,200)}x{random.randint(1,200)}x{random.randint(1,100)}",
        }
        if random.random() < 0.3:
            specs["hazmat_class"] = random.choice(["NONE", "CLASS_3", "CLASS_8", "ORM-D"])
        cost = round(random.uniform(0.5, 5000.0), 2)
        rows.append((
            i,
            sku,
            fake.catch_phrase(),
            random.choice(PRODUCT_CATEGORIES),
            truncated_json(specs),
            cost,
            round(cost * random.uniform(1.1, 3.5), 2),
            dirty_bool(0.12),
        ))
    cur.executemany("INSERT INTO products VALUES (?,?,?,?,?,?,?,?)", rows)
    return n


def gen_inventory_stock(cur, num_warehouses, num_products, n=1500):
    rows = []
    for i in range(1, n + 1):
        # ~5% negative stock from race conditions
        qty = random.randint(-50 if random.random() < 0.05 else 0, 10000)
        rows.append((
            i,
            random.randint(1, num_warehouses),
            random.randint(1, num_products),
            qty,
            random.randint(0, max(qty, 0)),
            maybe_dirty_null(dirty_date(rand_date(2024, 2026)), 0.1),
        ))
    cur.executemany("INSERT INTO inventory_stock VALUES (?,?,?,?,?,?)", rows)
    return n


def gen_stock_movements(cur, num_products, num_warehouses, n=4000):
    rows = []
    for i in range(1, n + 1):
        mv_type = random.choice(MOVEMENT_TYPES)
        from_wh = random.randint(1, num_warehouses)
        to_wh = random.randint(1, num_warehouses)
        # ~4% missing timestamps (system outage)
        ts = dirty_date(rand_date()) if random.random() > 0.04 else random.choice(DIRTY_NULLS)
        ref_doc = random.choice([
            f"SO-{random.randint(2018,2026)}-{random.randint(1,9999)}",
            f"PO-{random.randint(100,9999)}",
            f"AUDIT_ADJ",
            f"CYCLE_COUNT_{random.randint(1,500)}",
            None,
        ])
        rows.append((
            i,
            mv_type,
            random.randint(1, num_products),
            from_wh if mv_type != "RECEIPT" else None,
            to_wh,
            random.randint(-20 if random.random() < 0.02 else 1, 5000),
            ts,
            maybe_dirty_null(ref_doc, 0.08),
        ))
    cur.executemany("INSERT INTO stock_movements VALUES (?,?,?,?,?,?,?,?)", rows)
    return n


def gen_carriers(cur, n=10):
    carrier_names = ["FedEx", "DHL Express", "UPS", "Local Fleet", "USPS",
                     "Maersk Logistics", "BlueDart", "SF Express", "TNT", "Aramex"]
    rows = []
    for i in range(1, n + 1):
        rows.append((
            i,
            carrier_names[i - 1] if i <= len(carrier_names) else fake.company(),
            random.choice(CARRIER_SERVICES),
            maybe_dirty_null(f"https://track.example.com/?id={{tracking_number}}", 0.15),
        ))
    cur.executemany("INSERT INTO carriers VALUES (?,?,?,?)", rows)
    return n


def gen_shipments(cur, num_orders, num_carriers, n=2500):
    rows = []
    for i in range(1, n + 1):
        tracking = f"{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}{random.randint(100000000, 999999999)}"
        dispatch = rand_date()
        # Timezones stored inconsistently
        tz_suffixes = ["", "Z", "+00:00", "-05:00", "+05:30", " EST", " UTC", " IST"]
        dispatch_str = dispatch.strftime("%Y-%m-%d %H:%M:%S") + random.choice(tz_suffixes)
        estimate_str = (dispatch + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
        rows.append((
            i,
            tracking,
            random.randint(1, num_orders),
            random.randint(1, num_carriers),
            dispatch_str,
            maybe_dirty_null(estimate_str, 0.08),
            random.choice(DELIVERY_STATUSES),
        ))
    cur.executemany("INSERT INTO shipments VALUES (?,?,?,?,?,?,?)", rows)
    return n


def gen_shipment_events(cur, num_shipments, n=7000):
    rows = []
    for i in range(1, n + 1):
        telemetry = {
            "lat": round(random.uniform(-90, 90), 6),
            "lng": round(random.uniform(-180, 180), 6),
            "temp_c": round(random.uniform(-20, 45), 1),
            "battery_pct": random.randint(0, 100),
            "scanner_id": f"SCAN_{random.randint(1,200)}",
        }
        rows.append((
            i,
            random.randint(1, num_shipments),
            random.choice(SHIPMENT_EVENTS),
            dirty_date(rand_date()),
            maybe_dirty_null(f"LOC-{random.randint(100,999)}", 0.06),
            truncated_json(telemetry),
        ))
    cur.executemany("INSERT INTO shipment_events VALUES (?,?,?,?,?,?)", rows)
    return n


def gen_delivery_proofs(cur, num_shipments, n=1800):
    rows = []
    for i in range(1, n + 1):
        rows.append((
            i,
            random.randint(1, num_shipments),
            maybe_dirty_null(fake.name(), 0.1),
            dirty_date(rand_date()),
            maybe_dirty_null(fake.sentence(), 0.6),
        ))
    cur.executemany("INSERT INTO delivery_proofs VALUES (?,?,?,?,?)", rows)
    return n


def gen_departments(cur, n=None):
    dept_names = {
        "FIN": "Finance", "ENG": "Engineering", "OPS": "Operations",
        "EXEC": "Executive", "MKT": "Marketing", "HR": "Human Resources",
        "LEGAL": "Legal", "IT": "Information Technology", "SALES": "Sales",
        "R&D": "Research & Development", "QA": "Quality Assurance", "SUPPORT": "Customer Support",
    }
    rows = []
    for i, (code, name) in enumerate(dept_names.items(), 1):
        # Root departments have None parent; sub-departments reference a random parent
        parent = None if i <= 4 else random.randint(1, min(i - 1, 4))
        rows.append((i, code, name, parent))
    cur.executemany("INSERT INTO departments VALUES (?,?,?,?)", rows)
    return len(dept_names)


def gen_employees(cur, num_departments, n=500):
    rows = []
    for i in range(1, n + 1):
        badge = random.choice([
            f"EMP{i:04d}",
            f"B-{random.randint(1000,9999)}",
            f"LEGACY_{random.randint(1,999)}",
        ])
        # Manager: null for C-level, occasional cyclic references
        if i <= 5:
            manager = None
        elif random.random() < 0.02:
            manager = i  # Cyclic self-reference (bad data)
        else:
            manager = random.randint(1, max(i - 1, 1))

        hire_date = rand_date(2017, 2026)
        # Active employees: dirty null for termination_date
        if random.random() < 0.75:
            term_date = random.choice(DIRTY_NULLS)
        else:
            term_date = dirty_date(hire_date + timedelta(days=random.randint(90, 2500)))

        rows.append((
            i,
            badge,
            fake.first_name(),
            fake.last_name(),
            random.randint(1, num_departments),
            manager,
            dirty_date(hire_date),
            term_date,
            random.choice(EMPLOYMENT_STATUSES),
        ))
    cur.executemany("INSERT INTO employees VALUES (?,?,?,?,?,?,?,?,?)", rows)
    return n


def gen_salaries_history(cur, num_employees, n=1500):
    rows = []
    for i in range(1, n + 1):
        rows.append((
            i,
            random.randint(1, num_employees),
            dirty_date(rand_date()),
            round(random.uniform(25000, 350000), 2),
            random.choice(CURRENCIES[:3]),  # Mostly USD/EUR/GBP
            random.choice(SALARY_REASONS),
        ))
    cur.executemany("INSERT INTO salaries_history VALUES (?,?,?,?,?,?)", rows)
    return n


def gen_timesheets(cur, num_employees, n=6000):
    rows = []
    seen = set()
    for i in range(1, n + 1):
        emp_id = random.randint(1, num_employees)
        work_date = rand_date()
        # ~6% duplicate submissions (browser retry)
        if random.random() < 0.06 and seen:
            emp_id, work_date_str = random.choice(list(seen))
        else:
            work_date_str = dirty_date(work_date)
            seen.add((emp_id, work_date_str))

        # Hours: occasionally impossible values
        if random.random() < 0.04:
            hours = round(random.uniform(24.1, 36.0), 1)  # > 24 hours in a day
        elif random.random() < 0.02:
            hours = round(random.uniform(-8.0, -0.5), 1)  # Negative hours
        else:
            hours = round(random.uniform(0.5, 12.0), 1)

        rows.append((
            i,
            emp_id,
            work_date_str if isinstance(work_date_str, str) else dirty_date(work_date),
            hours,
            random.choice(TASK_CODES),
            dirty_date(rand_date()),
        ))
    cur.executemany("INSERT INTO timesheets VALUES (?,?,?,?,?,?)", rows)
    return n


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

def build_database(db_path: str, export_csv: bool = False):
    """Create the chaos ERP database from scratch."""

    if os.path.exists(db_path):
        os.remove(db_path)

    schema_path = Path(__file__).parent / "schema.sql"
    if not schema_path.exists():
        print(f"ERROR: schema.sql not found at {schema_path}")
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Execute DDL
    print("[1/28] Creating schema …")
    with open(schema_path, "r", encoding="utf-8") as f:
        cur.executescript(f.read())

    # Generate each table — order matters for FK references
    print("[2/28]  chart_of_accounts")
    n_accounts = gen_chart_of_accounts(cur)

    print("[3/28]  fiscal_periods")
    n_periods = gen_fiscal_periods(cur)

    print("[4/28]  gl_journal_headers")
    n_journals = gen_gl_journal_headers(cur, n_periods)

    print("[5/28]  gl_journal_lines")
    gen_gl_journal_lines(cur, n_journals, n_accounts)

    print("[6/28]  tax_rates_history")
    gen_tax_rates_history(cur)

    print("[7/28]  bank_reconciliation_logs")
    gen_bank_reconciliation_logs(cur)

    print("[8/28]  customers")
    n_customers = gen_customers(cur)

    print("[9/28]  customer_branches")
    n_branches = gen_customer_branches(cur, n_customers)

    print("[10/28] sales_orders")
    n_orders = gen_sales_orders(cur, n_customers, n_branches)

    print("[11/28] sales_order_items")
    n_products_temp = 350  # products not yet created, but items reference future product IDs
    gen_sales_order_items(cur, n_orders, n_products_temp)

    print("[12/28] invoices")
    gen_invoices(cur, n_orders)

    print("[13/28] vendors")
    n_vendors = gen_vendors(cur)

    print("[14/28] purchase_orders")
    n_pos = gen_purchase_orders(cur, n_vendors)

    print("[15/28] warehouses")
    n_warehouses = gen_warehouses(cur)

    print("[16/28] products")
    n_products = gen_products(cur)

    print("[17/28] po_line_items")
    gen_po_line_items(cur, n_pos, n_products)

    print("[18/28] goods_received_notes")
    gen_goods_received_notes(cur, n_pos, n_warehouses)

    print("[19/28] vendor_bills")
    gen_vendor_bills(cur, n_vendors, n_pos)

    print("[20/28] inventory_stock")
    gen_inventory_stock(cur, n_warehouses, n_products)

    print("[21/28] stock_movements")
    gen_stock_movements(cur, n_products, n_warehouses)

    print("[22/28] carriers")
    n_carriers = gen_carriers(cur)

    print("[23/28] shipments")
    n_shipments = gen_shipments(cur, n_orders, n_carriers)

    print("[24/28] shipment_events")
    gen_shipment_events(cur, n_shipments)

    print("[25/28] delivery_proofs")
    gen_delivery_proofs(cur, n_shipments)

    print("[26/28] departments")
    n_depts = gen_departments(cur)

    print("[27/28] employees")
    n_employees = gen_employees(cur, n_depts)

    print("[28/28] salaries_history")
    gen_salaries_history(cur, n_employees)

    # Bonus: timesheets (still part of 28-table count — replaces separate numbering)
    print("        timesheets")
    gen_timesheets(cur, n_employees)

    conn.commit()

    # Print summary
    print("\n" + "=" * 60)
    print("  DATABASE GENERATION COMPLETE")
    print("=" * 60)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cur.fetchall()]
    total_rows = 0
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM [{t}]")
        count = cur.fetchone()[0]
        total_rows += count
        print(f"  {t:35s} {count:>8,} rows")
    print("-" * 60)
    print(f"  {'TOTAL':35s} {total_rows:>8,} rows")
    print(f"\n  Output: {os.path.abspath(db_path)}")
    print(f"  Size:   {os.path.getsize(db_path) / (1024*1024):.2f} MB")
    print("=" * 60)

    # Optional CSV export
    if export_csv:
        csv_dir = Path(db_path).parent / "csv_export"
        csv_dir.mkdir(exist_ok=True)
        print(f"\nExporting tables to CSV in {csv_dir}/ …")
        for t in tables:
            cur.execute(f"SELECT * FROM [{t}]")
            rows = cur.fetchall()
            col_names = [desc[0] for desc in cur.description]
            csv_path = csv_dir / f"{t}.csv"
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(col_names)
                writer.writerows(rows)
            print(f"  [OK] {t}.csv ({len(rows):,} rows)")
        print("CSV export complete.")

    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DatabaseStudy — Generate a chaos-simulated enterprise ERP database.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Every run produces a unique, non-deterministic database.\nRepo: https://github.com/SujashBharadwaj/DatabaseStudy",
    )
    parser.add_argument(
        "--output", "-o",
        default="chaos_erp.db",
        help="Output SQLite database file path (default: chaos_erp.db)",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Also export all tables as CSV files alongside the database.",
    )
    args = parser.parse_args()

    build_database(args.output, export_csv=args.csv)
