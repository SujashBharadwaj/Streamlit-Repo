"""
DatabaseStudy project preview component.
Displays head(5) sample rows from key chaotic tables, schema overview,
challenge prompts, and GitHub repository links.
"""
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st
from utils.helpers import sanitize_html


# Path to a generated sample database (relative to streamlit_portfolio/)
DB_PATH = Path(__file__).resolve().parent.parent.parent / "DatabaseStudy" / "chaos_erp.db"

# Schema overview data for the 6 modules
SCHEMA_MODULES = [
    ("Finance & GL", ["chart_of_accounts", "fiscal_periods", "gl_journal_headers",
                       "gl_journal_lines", "tax_rates_history", "bank_reconciliation_logs"],
     "General ledger with floating-point drift, overlapping tax windows, and embedded API JSON"),
    ("Sales & CRM", ["customers", "customer_branches", "sales_orders",
                      "sales_order_items", "invoices"],
     "Dirty emails, orphan branches, raw checkout JSON, mixed null paid dates"),
    ("Procurement", ["vendors", "purchase_orders", "po_line_items",
                      "goods_received_notes", "vendor_bills"],
     "UUID + MongoDB ID + integer ID mixing, three-way match mismatches"),
    ("Inventory", ["warehouses", "products", "inventory_stock", "stock_movements"],
     "Negative stock, JSON spec blobs, missing movement timestamps"),
    ("Logistics", ["carriers", "shipments", "shipment_events", "delivery_proofs"],
     "Timezone inconsistency, GPS telemetry JSON, tracking anomalies"),
    ("HR & Payroll", ["departments", "employees", "salaries_history", "timesheets"],
     "Cyclic manager refs, >24h/day timesheets, duplicate retry submissions"),
]

CHALLENGES = {
    "Data Analyst": [
        "Handling dirty null representations across multiple tables",
        "Revenue aggregation with mixed date formats",
        "Customer deduplication by normalized email",
        "Identifying orphan foreign key records",
        "Standardizing country code variants",
    ],
    "Data Scientist": [
        "Feature extraction from truncated JSON blobs",
        "Date normalization pipeline across mixed formats",
        "Anomalous timesheet detection (>24h, negatives, duplicates)",
        "Customer churn prediction feature table",
        "GPS telemetry outlier detection from sensor payloads",
    ],
    "Analytics Engineer": [
        "GL trial balance reconciliation with floating-point drift",
        "Deduplicating browser retry event submissions",
        "Three-way PO / GRN / Bill matching",
        "Building clean dimension tables from dirty sources",
        "Inventory discrepancy detection vs stock movements",
    ],
    "DBA": [
        "Orphan foreign key audit across 4+ tables",
        "Adding constraints after-the-fact with violation diagnostics",
        "Index optimization for common query patterns",
        "Cyclic self-referential manager chain detection",
        "Schema drift documentation and data type audit",
    ],
}


def render_db_study_preview(project):
    """Render the DatabaseStudy project detail page with head(5) previews and challenge tabs."""
    github_url = project.get("github_url", "")
    sample_tables = project.get("sample_tables", [])

    # ---- Action buttons ----
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        if github_url:
            st.link_button("GitHub Repository", github_url, use_container_width=True)
    with col2:
        st.link_button(
            "Download & Generate",
            github_url + "#quick-start" if github_url else "#",
            use_container_width=True,
        )

    # ---- Schema Overview ----
    st.markdown("#### Schema Overview — 28 Tables, 6 Modules")
    for module_name, tables, description in SCHEMA_MODULES:
        table_badges = " ".join(
            [f"<code>{t}</code>" for t in tables]
        )
        st.markdown(
            sanitize_html(f"""
            <div class="card" style="padding:12px 16px; margin-bottom:8px;">
              <div style="font-weight:700; font-size:1.05rem;">{module_name}
                <span style="color:#6B7280; font-weight:400; font-size:0.85rem;"> — {len(tables)} tables</span>
              </div>
              <div class="muted" style="margin:4px 0 6px 0; font-size:0.9rem;">{description}</div>
              <div>{table_badges}</div>
            </div>
            """),
            unsafe_allow_html=True,
        )

    # ---- Sample Data Previews (head 5) ----
    st.markdown("---")
    st.markdown("#### Sample Dirty Data Previews")

    if DB_PATH.exists():
        try:
            conn = sqlite3.connect(str(DB_PATH))
            for table_name in sample_tables:
                try:
                    df = pd.read_sql(f"SELECT * FROM [{table_name}] LIMIT 5", conn)
                    row_count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM [{table_name}]", conn)["cnt"][0]
                    st.markdown(
                        sanitize_html(f"""
                        <div style="margin-top:16px; margin-bottom:4px;">
                          <span style="font-weight:700; font-size:1rem;">{table_name}</span>
                          <span style="color:#6B7280; font-size:0.85rem;"> — {row_count:,} rows</span>
                        </div>
                        """),
                        unsafe_allow_html=True,
                    )
                    st.dataframe(df, use_container_width=True, hide_index=True)
                except Exception:
                    st.caption(f"Could not load `{table_name}`.")
            conn.close()
        except Exception:
            st.info("Sample database not found. Run `python generator.py` in the DatabaseStudy folder to generate one.")
    else:
        st.info(
            "No sample database available for preview. "
            "Clone the repository and run `python generator.py` to generate your own."
        )

    # ---- Challenge Suite ----
    st.markdown("---")
    st.markdown("#### Challenge Suite — 4 Roles, 28 Challenges")

    tabs = st.tabs(list(CHALLENGES.keys()))
    for tab, (role, challenges) in zip(tabs, CHALLENGES.items()):
        with tab:
            for j, challenge in enumerate(challenges, 1):
                st.markdown(f"**{j}.** {challenge}")
            st.markdown("")
            if github_url:
                st.link_button(
                    f"View Full {role} Challenges",
                    github_url + "/tree/main/challenges",
                    use_container_width=True,
                )

    # ---- Key Chaos Highlights ----
    st.markdown("---")
    st.markdown("#### Injected Chaos Highlights")
    chaos_items = [
        ("Dirty Nulls", "NULL, 'NULL', 'null', 'None', 'N/A', '0', '', '-', '#REF!', 'undefined'"),
        ("Mixed Dates", "YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY, ISO 8601 ± timezone, Epoch ms"),
        ("Embedded JSON", "Raw API payloads, checkout carts, GPS telemetry — some truncated"),
        ("ID Collisions", "Integer PKs alongside UUID v4 and 24-char MongoDB ObjectIds"),
        ("Financial Drift", "GL trial balances off by $0.01–$14.52 from floating-point truncation"),
        ("Impossible Values", "Negative inventory, >24h timesheets, damaged > received quantities"),
    ]
    cols = st.columns(2, gap="medium")
    for i, (label, detail) in enumerate(chaos_items):
        with cols[i % 2]:
            st.markdown(
                sanitize_html(f"""
                <div class="card" style="padding:10px 14px; margin-bottom:8px;">
                  <div style="font-weight:700; color:#F59E0B;">{label}</div>
                  <div class="muted" style="font-size:0.88rem;">{detail}</div>
                </div>
                """),
                unsafe_allow_html=True,
            )
