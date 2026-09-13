# Challenge 02 — Data Scientist

These challenges focus on feature engineering, data preparation, and extracting structured information from messy enterprise data for modeling and analysis pipelines.

---

## Challenge 2.1 — Feature Extraction from JSON Blobs

The `sales_orders.cart_raw_json` column stores raw checkout payloads as JSON strings (some truncated or malformed).

**Task**: Parse the JSON and extract:
- Total number of items per order.
- Whether a coupon code was applied.
- The total cart value (sum of `qty * price` for each item).

Handle truncated JSON gracefully (flag those rows instead of crashing).

---

## Challenge 2.2 — Date Normalization Pipeline

Multiple tables use inconsistent date formats in the same column: `YYYY-MM-DD`, `DD/MM/YYYY`, `MM-DD-YYYY`, ISO 8601 with timezone, and raw epoch milliseconds.

**Task**: Using the `shipments` table, write a query or Python script that normalizes `dispatch_date` into a consistent `YYYY-MM-DD` format. Strip timezone suffixes like `EST`, `UTC`, `IST`, `+05:30`, `Z`.

---

## Challenge 2.3 — Extracting Product Specifications from Nested JSON

The `products.specifications_json` column stores nested JSON attributes (weight, color, dimensions, optional hazmat class). Some entries are truncated.

**Task**: Extract `weight_kg`, `color`, and `hazmat_class` (default `'NONE'` if absent) into a clean tabular format suitable for ML feature input.

---

## Challenge 2.4 — Identifying Anomalous Timesheets

The `timesheets` table contains:
- Entries logging > 24 hours in a single day.
- Negative hours.
- Duplicate submissions for the same employee on the same date.

**Task**: Build a flagging pipeline that identifies all anomalous timesheet entries and categorizes each anomaly type (`OVER_24H`, `NEGATIVE`, `DUPLICATE`).

---

## Challenge 2.5 — Churn Prediction Feature Table

Using `customers`, `sales_orders`, and `invoices`:

**Task**: Build a feature table at the customer level with:
- `total_orders`: Count of orders.
- `total_revenue`: Sum of invoice amounts.
- `avg_days_to_pay`: Average days between `invoice_date` and `paid_date` (excluding dirty nulls).
- `has_disputed_invoice`: Binary flag.
- `days_since_last_order`: Days since most recent order relative to 2026-09-01.

Handle all dirty date representations and null variants.

---

## Challenge 2.6 — GPS Telemetry Outlier Detection

The `shipment_events.telemetry_raw_json` column stores GPS pings with latitude, longitude, temperature, and battery data.

**Task**: Parse the telemetry JSON and identify events where:
- Latitude/longitude is outside valid ranges (lat: -90 to 90, lng: -180 to 180).
- Temperature readings are extreme (< -40°C or > 60°C).
- Battery percentage is negative or above 100.

---

## Challenge 2.7 — Vendor Risk Scoring

Using `vendors`, `purchase_orders`, `vendor_bills`, and `goods_received_notes`:

**Task**: Create a vendor risk score combining:
- Frequency of `QTY_MISMATCH` or `PRICE_MISMATCH` in `vendor_bills.matching_status`.
- Ratio of `damaged_quantity` to `received_quantity` in GRN records.
- Missing or dirty vendor rating values.

Rank vendors from highest to lowest risk.
