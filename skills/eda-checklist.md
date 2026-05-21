---
name: eda-checklist
description: Systematic Exploratory Data Analysis checklist that the data agent must follow before answering any modeling, statistical, or reporting question on a new dataset. Use when the user asks (EN) "what's in this data?", "explore this CSV", "give me a summary", "find issues", "is this dataset clean?", or (FR) "analyse exploratoire", "EDA", "explore ce jeu de données", "résume ce dataset", "qu'y a-t-il dans ces données", "audit qualité données", or hands over a Parquet/CSV/JSON file without prior context. Covers shape & type audit, missingness patterns, distribution diagnostics, correlations, group comparisons, leakage detection, target imbalance, and feature engineering opportunities. Outputs a structured EDA report. Do NOT use for: production data quality monitoring (use Great Expectations / dbt tests), one-off ad-hoc queries on known data, or schema design.
agents: [data]
---

# EDA Checklist — Systematic Exploratory Data Analysis

Every new dataset should be put through the same disciplined pass before any modeling, statistical testing, or stakeholder-facing report. This skill prescribes the checklist the `data` agent must execute, the questions it must answer at each step, and the structured EDA report it must return. Visualizations are produced by handing off to the dev agent's `chartjs` or `plotly` skills.

---

## When to Apply

Apply this skill when the user:

- Provides a new file or table without prior context
- Asks "what's in this data?", "give me a summary", "explore this"
- Requests a data quality assessment before modeling
- Wants to know whether a dataset is suitable for a specific analysis
- Hands over a CSV / Parquet / JSON for ad-hoc investigation

Skip this skill when the dataset is already well-understood from prior conversation, when the user explicitly asks for a narrow query, or when the request is for production data quality monitoring (defer to Great Expectations / dbt tests).

---

## Methodology — The Nine Passes

EDA is performed in nine sequential passes. Each pass has a question, a method, and an exit condition. Do not skip ahead — later passes assume the artifacts from earlier passes exist.

### Pass 1 — Shape and Types Audit

**Question:** What is the grain, the size, and the type of every column?

**Method:**
1. Row and column count.
2. Memory footprint.
3. `dtype` of every column.
4. First 5 and last 5 rows printed.
5. Sample of 10 random rows (avoid the head/tail bias from sorted data).
6. Primary key candidate identified (column with N unique values where N = row count).

**Exit condition:** A schema table with `column, dtype, n_unique, n_null, example_value` for every column.

**DuckDB recipe:**

```sql
SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'my_table';

SELECT
    COUNT(*) AS n_rows,
    COUNT(DISTINCT id) AS n_unique_ids
FROM my_table;
```

### Pass 2 — Missingness Patterns

**Question:** Where is data missing, and is the missingness systematic?

**Method:**
1. Percentage of nulls per column.
2. Heatmap of missingness (rows × columns, black = missing).
3. Check correlations among missingness indicators — if `is_null(A)` correlates with `is_null(B)`, the missingness has structure (MAR or MNAR, not MCAR).
4. Cross-tabulate missingness against the target — biased missingness invalidates naive imputation.

**Exit condition:** Decision recorded for each column with missingness: drop / impute (mean/median/mode/model) / treat as separate category / flag and leave.

**DuckDB recipe:**

```sql
SELECT
    SUM(CASE WHEN col_a IS NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS pct_null_a,
    SUM(CASE WHEN col_b IS NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS pct_null_b,
    SUM(CASE WHEN col_a IS NULL AND col_b IS NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS pct_both_null
FROM my_table;
```

### Pass 3 — Distribution Checks (Univariate)

**Question:** For every numeric column — what is the shape, the spread, and where are the outliers?

**Method:**
1. Summary statistics: count, mean, median, std, min, p25, p75, max.
2. Skewness and kurtosis.
3. Modality check — histogram with 30-50 bins. Bimodality often hides a latent group.
4. Outlier check — IQR rule (`< Q1 - 1.5*IQR` or `> Q3 + 1.5*IQR`) AND z-score > 3 AND visual inspection.
5. For categorical: value counts, cardinality, presence of `NaN` / `None` / `''` / `'NULL'` as string literals.

**Exit condition:** Annotated distribution table noting skewness (e.g., "right-skewed, log-transform candidate"), outlier count, and any obvious bimodality.

**Visualization hand-off:** Defer to the dev agent's `chartjs` skill for histograms and box plots, or `plotly` for violin plots and faceted distributions.

**DuckDB recipe:**

```sql
SELECT
    COUNT(*) AS n,
    AVG(value) AS mean,
    MEDIAN(value) AS median,
    STDDEV(value) AS sd,
    MIN(value) AS min,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY value) AS p25,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY value) AS p75,
    MAX(value) AS max,
    SKEWNESS(value) AS skew,
    KURTOSIS(value) AS kurt
FROM my_table;
```

### Pass 4 — Pairwise Correlations

**Question:** Which pairs of features carry redundant information?

**Method:**
1. Pearson correlation matrix for continuous features.
2. Spearman matrix as well — captures monotonic non-linear relations Pearson misses.
3. Cramér's V matrix for categorical-categorical.
4. ANOVA F-stat or Kruskal-Wallis for categorical-vs-continuous.
5. Flag pairs with |r| > 0.9 as redundant candidates.

**Exit condition:** Correlation heatmap (Plotly), list of redundant pairs, decision for each (drop one / combine / leave).

**Visualization hand-off:** Use the dev agent's `plotly` skill for the heatmap — Chart.js does not handle matrix plots well.

### Pass 5 — Group Comparisons

**Question:** Do values differ systematically across natural groupings (segments, regions, cohorts)?

**Method:**
1. For each plausible grouping variable, compute target / key-metric mean, median, and 95% CI per group.
2. Run the appropriate test from the `statistical-tests` skill — t-test / Mann-Whitney / ANOVA / Kruskal-Wallis.
3. Always report effect size, not just p-value.
4. Visualize as grouped bar (Chart.js) or faceted box plot (Plotly).

**Exit condition:** Table of group differences with effect size and significance, plus a one-line interpretation.

### Pass 6 — Leakage Detection

**Question:** Is any feature suspiciously predictive of the target in a way that wouldn't exist at inference time?

**Method:**
1. Single-feature univariate AUC / R² against the target — anything > 0.95 deserves scrutiny.
2. Check timestamps: any feature derived from data that post-dates the target?
3. Check identifiers: any column that uniquely identifies the row in a way that encodes the label?
4. Look for "future" suffixes or aggregations computed across the whole dataset (e.g., `mean_target_by_region` calculated on train+test together).
5. Look for columns that are essentially restatements of the target (e.g., `is_churned` ≈ `last_login_days_ago > 90`).

**Exit condition:** Leakage suspect list with severity (critical / probable / unlikely) and remediation.

### Pass 7 — Target Imbalance

**Question:** For classification — is the target balanced enough for the chosen modeling approach?

**Method:**
1. Class frequency table.
2. Minority class proportion.
3. Decision tree:
   - Minority > 30% → no action.
   - Minority 10-30% → stratified sampling, use AUC/F1 over accuracy.
   - Minority 1-10% → class weights, SMOTE (with caution), or threshold tuning.
   - Minority < 1% → reframe as anomaly detection.
4. For regression — check target distribution: heavy tails suggest log/Box-Cox transform.

**Exit condition:** Class distribution table and an explicit recommendation for the modeling strategy.

### Pass 8 — Feature Engineering Opportunities

**Question:** What transformations or derived features would meaningfully improve downstream analysis?

**Method:**
1. **Temporal** — extract hour-of-day, day-of-week, month, quarter, is_weekend, is_holiday from any timestamp.
2. **Cyclic** — encode hour/day/month as `sin(2π × x / period), cos(2π × x / period)` to preserve cyclicity.
3. **Log transform** — any right-skewed strictly-positive feature (income, count, duration).
4. **Binning** — convert continuous to categorical only when there is a domain reason (age bands, income tiers).
5. **Interactions** — flag plausible interaction terms based on domain knowledge.
6. **Aggregations** — for entity-event data, group-level statistics (`user_event_count_30d`, `user_avg_order_value`).
7. **Text** — length, word count, presence of keywords, sentiment, embedding.
8. **High-cardinality categorical** — target encoding, frequency encoding, hashing.

**Exit condition:** Feature engineering shortlist with rationale.

### Pass 9 — Sanity Checks

**Question:** Do the data tell a story that matches reality?

**Method:**
1. Domain-specific sanity: negative ages, future dates, prices = $0, duplicate primary keys.
2. Cross-field consistency: `end_date >= start_date`, `total = sum(parts)`.
3. Reference checks: foreign keys actually exist in their referenced tables.
4. Volume over time: row count by day — sudden gaps or spikes indicate ingestion issues.

**Exit condition:** List of integrity violations with row counts.

---

## Output Template

The agent returns this markdown structure. Placeholders in `<...>` are filled from the nine passes.

```
# EDA Report — <dataset name>

## 1. Overview
- Rows: <n>
- Columns: <n>
- Memory: <MB>
- Primary key: <column or "none identified">
- Time range (if temporal): <min> → <max>
- Grain: <one row = ...>

## 2. Schema
| Column | Type | Unique | % Null | Example |
|--------|------|--------|--------|---------|
| ...    | ...  | ...    | ...    | ...     |

## 3. Missingness
- Top 5 most-missing columns: <list with %>
- Missingness pattern: <MCAR / MAR / MNAR with justification>
- Decisions: <per-column>

> Suggested visualization: missingness heatmap via dev agent `plotly` skill.

## 4. Distributions
- Numeric summary (mean / median / sd / skew / kurtosis): <table>
- Outliers: <column → count flagged by IQR rule>
- Skewed candidates for log transform: <list>
- Bimodal candidates: <list>
- Categorical cardinality: <table>

> Suggested visualization: faceted histograms via dev agent `chartjs` skill (one canvas per variable).

## 5. Correlations
- Continuous-continuous (Pearson + Spearman): <heatmap reference>
- Redundant pairs (|r| > 0.9): <list>
- Categorical-categorical (Cramér's V): <list of strong associations>

> Suggested visualization: correlation heatmap via dev agent `plotly` skill.

## 6. Group Comparisons
| Group var | Metric | Group A | Group B | Effect size | p-value |
|-----------|--------|---------|---------|-------------|---------|
| ...       | ...    | ...     | ...     | ...         | ...     |

> Suggested visualization: grouped bar via dev agent `chartjs` or box plot via `plotly`.

## 7. Leakage Suspects
| Feature | Risk | Reason | Remediation |
|---------|------|--------|-------------|
| ...     | ...  | ...    | ...         |

## 8. Target Profile
- Type: <classification / regression>
- Distribution: <table or summary>
- Imbalance: <minority class %>
- Recommendation: <stratify / class-weight / SMOTE / threshold tune / reframe>

## 9. Feature Engineering Shortlist
- <transformation> on <column> — rationale: <...>
- <transformation> on <column> — rationale: <...>

## 10. Integrity Violations
| Check | Violations |
|-------|------------|
| ...   | ...        |

## 11. Next Steps
- <one-line recommendation 1>
- <one-line recommendation 2>
- <one-line recommendation 3>
```

---

## Quality Checklist

Before returning the EDA report, confirm:

- [ ] Every column appears in the schema table
- [ ] Missingness percentage reported for every column with at least one null
- [ ] Distribution summary includes skewness AND kurtosis, not just mean/std
- [ ] Both Pearson AND Spearman correlations computed
- [ ] Categorical-categorical association measured (Cramér's V), not skipped
- [ ] Group comparisons use the right test from `statistical-tests` skill with effect size
- [ ] Leakage section is non-empty even if only to say "no suspects after review"
- [ ] Target imbalance recommendation is explicit and actionable
- [ ] Feature engineering shortlist references domain context, not just "log-transform everything"
- [ ] Integrity violations include exact row counts, not adjectives
- [ ] Visualization references hand off to the correct dev agent skill (`chartjs` / `plotly`)
- [ ] No claim is made without a number or a chart to back it

---

## Common Mistakes

**Skipping the shape pass.** Jumping straight to distributions without confirming row count, grain, and primary key leads to subtle bugs — a duplicated join can double every count and you won't notice.

**Treating missingness as MCAR by default.** Most real missingness is MAR or MNAR. Always cross-tab missingness against the target and other features before deciding to impute.

**Reporting mean and std for skewed data.** Mean is misleading for heavy-tailed distributions. Use median + IQR by default; switch to mean + std only after confirming symmetry.

**Only computing Pearson correlations.** Pearson misses non-linear monotonic relationships. Always compute Spearman as well, especially during exploration.

**Ignoring high-cardinality categoricals.** A column with 10,000 unique strings is not "just a categorical" — it needs hashing, target encoding, or grouping before any model touches it.

**Forgetting leakage from group statistics computed on the full dataset.** Computing `mean_target_by_region` on train+test combined and using it as a feature is silent leakage. Compute aggregations on training data only.

**Treating outliers as errors.** Outliers may be the most informative rows (fraud, churn, breakthrough customers). Investigate before removing.

**Using accuracy on imbalanced classification.** A model that always predicts the majority class gets 99% accuracy on a 1% minority problem. Always report AUC, F1, precision, and recall.

**Producing charts without rendering hints.** The data agent does not render visualizations — it must hand off to the dev agent's `chartjs` or `plotly` skills with explicit data shape and chart type.

**Skipping integrity checks.** The most embarrassing post-analysis discovery is a foreign key that doesn't join, a date in the year 1900, or a price of -$1. Run sanity checks early.
