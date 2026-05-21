---
name: sql-recipes
description: Authoritative DuckDB SQL recipes for analytics work performed through the data agent's `duckdb` MCP tool. Use this skill whenever the user asks for window functions, top-N per group, cohort/retention, gap-and-island detection, running totals, percentiles, pivot/unpivot transforms, time bucketing, or direct querying of CSV/Parquet/JSON files. Trigger on phrases like "rank within", "rolling sum", "last value before", "sessionize", "top 3 per category", "monthly cohorts", "median by group", "read this CSV". Do NOT use for: schema design (DDL only), OLTP-style updates, vendor-specific dialects (PostgreSQL/MySQL/Snowflake — translate first), or pure ML feature pipelines that belong in Python.
agents: [data]
---

# SQL Recipes — DuckDB Analytics Patterns

DuckDB is an in-process analytical engine with first-class support for window functions, the `QUALIFY` clause, native `PIVOT`/`UNPIVOT`, and zero-copy reads of CSV, Parquet, and JSON files. This skill catalogues the patterns the `data` agent should reach for when answering analytical questions, with runnable examples that can be executed verbatim through the `duckdb` MCP tool.

---

## When to Apply

Apply this skill when the user asks for:

- Ranking, deduplication, or "latest record per key" lookups
- Running totals, moving averages, period-over-period deltas
- Top-N or bottom-N rows within groups
- Cohort, retention, churn, or funnel queries
- Gap-and-island detection (streaks, consecutive sessions, downtime windows)
- Time-series resampling, bucketing, or gap-filling
- Percentile, quantile, or distribution summaries
- Reshaping with `PIVOT` / `UNPIVOT`
- Reading external `.csv`, `.parquet`, or `.json` files directly without an `IMPORT` step

Skip this skill when the question is about schema design, transactional writes, or porting to another dialect.

---

## Methodology

Before writing SQL, the agent must answer three questions:

1. **Grain.** What does one row in the source represent? (event, daily snapshot, dimension row)
2. **Partition.** Which columns define "within a group" for the calculation?
3. **Order.** Which column establishes ordering inside the partition? (timestamp, id, version)

Once grain, partition, and order are explicit, the right window function follows mechanically.

Prefer `QUALIFY` over nested `SELECT` for filtering on window results. Prefer `USING SAMPLE` for exploratory work on large tables. Prefer `read_parquet` over CSV when both formats exist.

---

## Pattern 1 — Window Functions Catalogue

### ROW_NUMBER — deduplication and latest-per-key

```sql
SELECT
    user_id,
    event_time,
    event_type,
    ROW_NUMBER() OVER (
        PARTITION BY user_id
        ORDER BY event_time DESC
    ) AS rn
FROM events
QUALIFY rn = 1;
```

Use `ROW_NUMBER` when ties must be broken deterministically. Always include a tiebreaker column in `ORDER BY` (e.g. `event_time DESC, event_id DESC`).

### RANK and DENSE_RANK — leaderboards with ties

```sql
SELECT
    category,
    product,
    revenue,
    RANK()       OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS drnk
FROM sales;
```

`RANK` leaves gaps after ties (1, 2, 2, 4); `DENSE_RANK` does not (1, 2, 2, 3). Pick based on whether the user expects gap-preserving rankings.

### LAG and LEAD — period-over-period deltas

```sql
SELECT
    user_id,
    event_date,
    revenue,
    LAG(revenue, 1) OVER (PARTITION BY user_id ORDER BY event_date) AS prev_revenue,
    revenue - LAG(revenue, 1) OVER (PARTITION BY user_id ORDER BY event_date) AS delta
FROM daily_revenue;
```

Use `LAG(col, n, default)` to control offset and null-handling. `LEAD` is symmetric for forward-looking comparisons.

### SUM() OVER — running totals and moving averages

```sql
SELECT
    event_date,
    revenue,
    SUM(revenue) OVER (
        ORDER BY event_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total,
    AVG(revenue) OVER (
        ORDER BY event_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS ma_7d
FROM daily_revenue;
```

Always specify the frame clause explicitly. The default frame for `SUM/AVG` with `ORDER BY` is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, which behaves unexpectedly on duplicate ordering keys.

### FIRST_VALUE / LAST_VALUE / NTH_VALUE

```sql
SELECT
    session_id,
    page_url,
    FIRST_VALUE(page_url) OVER (
        PARTITION BY session_id
        ORDER BY visited_at
    ) AS landing_page,
    LAST_VALUE(page_url) OVER (
        PARTITION BY session_id
        ORDER BY visited_at
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS exit_page
FROM page_views;
```

`LAST_VALUE` requires the explicit `UNBOUNDED FOLLOWING` frame; otherwise it returns the current row.

---

## Pattern 2 — QUALIFY Clause

`QUALIFY` filters on window-function results without a nested subquery — a DuckDB and Snowflake extension.

```sql
-- Without QUALIFY (verbose)
SELECT *
FROM (
    SELECT
        user_id,
        order_id,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date DESC) AS rn
    FROM orders
) t
WHERE rn = 1;

-- With QUALIFY (preferred)
SELECT
    user_id,
    order_id,
    order_date
FROM orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date DESC) = 1;
```

Use `QUALIFY` for: latest-per-key, top-N per group, threshold filters on running totals. Combine with `WHERE` (row-level) and `HAVING` (group-level) — `QUALIFY` is evaluated last.

---

## Pattern 3 — Top-N per Group

```sql
SELECT
    category,
    product,
    revenue
FROM sales
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY category
    ORDER BY revenue DESC
) <= 3
ORDER BY category, revenue DESC;
```

For ties-included top-N, swap `ROW_NUMBER` for `RANK`. For percentile-based top-X%, use `NTILE(100)` and filter `<= 5`.

---

## Pattern 4 — PIVOT and UNPIVOT

DuckDB has native `PIVOT` syntax — no manual `CASE WHEN` pyramids.

### PIVOT — long to wide

```sql
PIVOT sales
ON quarter
USING SUM(revenue)
GROUP BY region;
```

Result columns: `region`, `Q1`, `Q2`, `Q3`, `Q4`.

### PIVOT with explicit value list

```sql
PIVOT sales
ON quarter IN ('Q1', 'Q2', 'Q3', 'Q4')
USING SUM(revenue) AS total, COUNT(*) AS n
GROUP BY region;
```

### UNPIVOT — wide to long

```sql
UNPIVOT monthly_revenue
ON jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec
INTO
    NAME month
    VALUE revenue;
```

Use `UNPIVOT` when the source has one column per period and downstream analysis needs a tall table.

---

## Pattern 5 — Cohort and Retention

### Monthly acquisition cohorts

```sql
WITH first_order AS (
    SELECT
        user_id,
        DATE_TRUNC('month', MIN(order_date)) AS cohort_month
    FROM orders
    GROUP BY user_id
),
activity AS (
    SELECT
        o.user_id,
        f.cohort_month,
        DATE_TRUNC('month', o.order_date) AS active_month,
        DATE_DIFF('month', f.cohort_month, DATE_TRUNC('month', o.order_date)) AS month_offset
    FROM orders o
    JOIN first_order f USING (user_id)
)
SELECT
    cohort_month,
    month_offset,
    COUNT(DISTINCT user_id) AS active_users
FROM activity
GROUP BY cohort_month, month_offset
ORDER BY cohort_month, month_offset;
```

### Retention as percentage of cohort

```sql
WITH cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT user_id) AS n0
    FROM activity
    WHERE month_offset = 0
    GROUP BY cohort_month
)
SELECT
    a.cohort_month,
    a.month_offset,
    a.active_users,
    ROUND(100.0 * a.active_users / c.n0, 1) AS retention_pct
FROM activity a
JOIN cohort_size c USING (cohort_month)
ORDER BY a.cohort_month, a.month_offset;
```

Pivot the final result for a classic triangular retention table.

---

## Pattern 6 — Gap and Island Detection

Detect consecutive runs (streaks, sessions, uptime windows) using the "row_number difference" trick.

```sql
WITH numbered AS (
    SELECT
        user_id,
        login_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn,
        login_date - INTERVAL (
            ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date)
        ) DAY AS grp
    FROM daily_logins
)
SELECT
    user_id,
    grp,
    MIN(login_date) AS streak_start,
    MAX(login_date) AS streak_end,
    COUNT(*)        AS streak_length
FROM numbered
GROUP BY user_id, grp
QUALIFY streak_length >= 3
ORDER BY user_id, streak_start;
```

For event-based sessionization (e.g. 30-minute inactivity gap), use a cumulative sum of "is new session" flags:

```sql
WITH flagged AS (
    SELECT
        user_id,
        event_time,
        CASE
            WHEN event_time - LAG(event_time) OVER (
                PARTITION BY user_id ORDER BY event_time
            ) > INTERVAL 30 MINUTE
            THEN 1 ELSE 0
        END AS new_session
    FROM events
)
SELECT
    user_id,
    event_time,
    SUM(new_session) OVER (
        PARTITION BY user_id ORDER BY event_time
    ) AS session_id
FROM flagged;
```

---

## Pattern 7 — Time Bucketing

```sql
SELECT
    DATE_TRUNC('hour', event_time) AS bucket,
    COUNT(*)                        AS events
FROM events
GROUP BY bucket
ORDER BY bucket;
```

For arbitrary intervals use `time_bucket`:

```sql
SELECT
    TIME_BUCKET(INTERVAL '15 minutes', event_time) AS bucket,
    COUNT(*)                                        AS events
FROM events
GROUP BY bucket
ORDER BY bucket;
```

Fill missing buckets with `generate_series`:

```sql
WITH grid AS (
    SELECT GENERATE_SERIES(
        '2026-01-01'::TIMESTAMP,
        '2026-01-31'::TIMESTAMP,
        INTERVAL 1 DAY
    ) AS day
),
counts AS (
    SELECT DATE_TRUNC('day', event_time) AS day, COUNT(*) AS n
    FROM events
    GROUP BY day
)
SELECT
    g.day,
    COALESCE(c.n, 0) AS events
FROM grid g
LEFT JOIN counts c USING (day)
ORDER BY g.day;
```

---

## Pattern 8 — Percentiles and Quantiles

```sql
SELECT
    category,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY price) AS median,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY price) AS p95,
    PERCENTILE_DISC(0.99) WITHIN GROUP (ORDER BY price) AS p99_disc
FROM products
GROUP BY category;
```

For large tables, prefer `APPROX_QUANTILE` (sub-linear, ~1% error):

```sql
SELECT
    APPROX_QUANTILE(response_ms, 0.50) AS p50,
    APPROX_QUANTILE(response_ms, 0.95) AS p95,
    APPROX_QUANTILE(response_ms, 0.99) AS p99
FROM request_log;
```

`PERCENTILE_CONT` interpolates between values; `PERCENTILE_DISC` picks an existing row. Report median + IQR for skewed distributions; report mean + stddev only when distribution is roughly symmetric.

---

## Pattern 9 — Reading External Files

DuckDB queries flat files directly — no `COPY` or `IMPORT` step needed.

### CSV

```sql
SELECT *
FROM 'data/sales_2026.csv'
LIMIT 10;

-- With explicit options
SELECT *
FROM read_csv(
    'data/sales_2026.csv',
    delim = ',',
    header = true,
    sample_size = -1
);
```

### Parquet

```sql
SELECT *
FROM 'data/events/*.parquet'
WHERE event_date >= '2026-01-01';

SELECT *
FROM read_parquet('s3://bucket/year=2026/month=*/*.parquet');
```

Parquet is preferred for repeat queries: predicate pushdown, column projection, and compression all apply.

### JSON

```sql
SELECT *
FROM read_json_auto('data/events.json');

-- Newline-delimited JSON
SELECT *
FROM read_ndjson_auto('data/events.ndjson');
```

### Glob and partition pruning

```sql
SELECT *
FROM read_parquet(
    'data/year=*/month=*/day=*/*.parquet',
    hive_partitioning = true
)
WHERE year = 2026 AND month = 5;
```

Hive-partitioned columns become queryable columns; DuckDB skips matching folders entirely.

---

## Output Template

Every SQL answer should arrive in this shape:

1. **Restate the question** in one sentence with grain, partition, and order made explicit.
2. **Quick schema check** — column names and types of the input(s).
3. **The query**, formatted with uppercase keywords and 4-space indent.
4. **One-line explanation** of every CTE.
5. **A sample of the output** (≤ 10 rows).
6. **Caveats** — null handling, tie-breaking, performance notes.

---

## Quality Checklist

Before returning a SQL answer, confirm:

- [ ] `ORDER BY` inside every window function includes a deterministic tiebreaker
- [ ] Every window frame is explicit (no implicit `RANGE` defaults)
- [ ] `QUALIFY` used instead of nested filter on window output
- [ ] No `SELECT *` in production-shape queries — column lists are explicit
- [ ] Date arithmetic uses `INTERVAL` literals, not magic numbers
- [ ] External file reads use `read_parquet` over `read_csv` when both exist
- [ ] Aggregations on skewed data report median + IQR, not mean + stddev
- [ ] `JOIN` keys verified to have expected cardinality (no accidental fan-out)

---

## Common Mistakes

**Forgetting the window frame.** `SUM(x) OVER (ORDER BY t)` defaults to `RANGE`, which can produce unexpected duplicates when `t` is non-unique. Always write `ROWS BETWEEN ...`.

**Using `RANK` when `ROW_NUMBER` is needed.** Deduplication requires exactly one row per key — `RANK` keeps ties.

**Filtering window output in `WHERE`.** Window functions are evaluated after `WHERE`, so filtering on `rn = 1` in `WHERE` fails. Use `QUALIFY` or wrap in a subquery.

**Casting wrong before `DATE_TRUNC`.** `DATE_TRUNC('month', '2026-05-20')` on a string errors silently in some clients. Cast to `TIMESTAMP` first.

**Pivoting without `IN (...)`.** Without an explicit value list, `PIVOT` scans the table twice — once to discover values, once to aggregate. Specify values when known.

**Trusting CSV auto-detection.** `read_csv_auto` samples the first ~20k rows; rare values later can mistype columns. For production, declare types or pass `sample_size = -1`.

**Calling `PERCENTILE_CONT` on huge tables.** It sorts the entire group. Use `APPROX_QUANTILE` when N > ~10M and 1% error is acceptable.

**Mixing `LEFT JOIN` with `WHERE` on the right side.** A `WHERE right.col = X` after a `LEFT JOIN` silently converts it to an `INNER JOIN`. Move the predicate into the `ON` clause.
