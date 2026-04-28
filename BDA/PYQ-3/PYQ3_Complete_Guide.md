# 📘 PYQ-3: Spark SQL Queries on Transaction Data — Complete Guide

> **Source:** PDEU End Semester Exam, April-May 2025, SET1 (Afternoon Batch 4:00-6:30 PM)  
> **Topic:** Spark SQL — Pure SQL queries on inline data  
> **Total Marks:** 30 (3 sections)  
> **Key Difference:** ALL questions are Spark SQL queries. Data is given inline, not from a file.

---

## 📌 What This Question Tests

You're given **hardcoded data** (no CSV file) with columns:
- `transaction_id`, `product_id`, `customer_id`, `amount`, `transaction_date`, `city`

Three sections:
1. **Data Manipulation & Analysis** (10 marks) — basic GROUP BY, TOP N, date functions
2. **Data Filtering & Aggregation** (10 marks) — WHERE clause, date filtering
3. **Advanced Analytics** (10 marks) — subqueries, MAX

Everything is **pure SQL** — no DataFrame API needed (though you can use it).

---

## 🧠 New Theory (Beyond PYQ-1 & PYQ-2)

### Creating Data Inline (No File)

When the question gives you data directly (not a CSV file):

```python
data = [
    (1, 101, 1001, 50, "2024-01-01", "New York"),
    (2, 102, 1002, 75, "2024-01-02", "Los Angeles"),
]
schema = ["transaction_id", "product_id", "customer_id", "amount", "transaction_date", "city"]
df = spark.createDataFrame(data, schema)
```

### Registering as SQL Table

Before writing SQL queries, you must register the DataFrame as a temporary view:

```python
df.createOrReplaceTempView("transactions")
```

Now you can write: `spark.sql("SELECT * FROM transactions")`

### SQL Date Functions

| Function | What It Does | Example |
|----------|-------------|---------|
| `YEAR(date)` | Extracts year | `YEAR('2024-01-15')` → 2024 |
| `MONTH(date)` | Extracts month | `MONTH('2024-01-15')` → 1 |
| `DAY(date)` | Extracts day | `DAY('2024-01-15')` → 15 |

### Date Filtering in SQL

```sql
WHERE transaction_date > '2024-01-06'    -- after Jan 6
WHERE YEAR(transaction_date) = 2024      -- only year 2024
WHERE transaction_date BETWEEN '2024-01-01' AND '2024-01-31'  -- range
```

### Subqueries (Nested Queries)

A query inside another query. Used when you need to aggregate twice:

```sql
-- "Average total spent by customers" = first get total per customer, then average those totals
SELECT city, AVG(customer_total) AS avg_spending
FROM (
    SELECT city, customer_id, SUM(amount) AS customer_total
    FROM transactions
    GROUP BY city, customer_id
)
GROUP BY city
```

The inner query runs first, produces a temporary result, then the outer query aggregates that result.

---

## 💻 Complete Solution — Cell by Cell

### CELL 1: Initialization (Same as always)

```python
import findspark
findspark.init()

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("BDA-Exam") \
    .master("local[*]") \
    .getOrCreate()

sc = spark.sparkContext
from pyspark.sql.functions import *

print("✅ Spark Ready!", spark.version)
```

---

### CELL 2: Create the Dataset (Copy from question)

```python
data = [
    (1, 101, 1001, 50, "2024-01-01", "New York"),
    (2, 102, 1002, 75, "2024-01-02", "Los Angeles"),
    (3, 103, 1001, 100, "2024-01-03", "Chicago"),
    (4, 104, 1003, 120, "2024-01-04", "Houston"),
    (5, 105, 1002, 80, "2024-01-05", "New York"),
    (6, 106, 1004, 90, "2024-01-06", "Chicago"),
    (7, 107, 1005, 110, "2024-01-07", "Los Angeles"),
    (8, 108, 1006, 130, "2024-01-08", "Houston"),
    (9, 109, 1004, 70, "2024-01-09", "New York"),
    (10, 110, 1007, 85, "2024-01-10", "Chicago"),
    (11, 111, 1005, 95, "2024-01-11", "Los Angeles"),
    (12, 112, 1008, 105, "2024-01-12", "Houston"),
    (13, 113, 1006, 115, "2024-01-13", "New York"),
    (14, 114, 1009, 125, "2024-01-14", "Chicago"),
    (15, 115, 1010, 135, "2024-01-15", "Los Angeles"),
]

schema = ["transaction_id", "product_id", "customer_id",
          "amount", "transaction_date", "city"]
df = spark.createDataFrame(data, schema)

# IMPORTANT: Register as SQL table
df.createOrReplaceTempView("transactions")

print("=== Dataset ===")
df.show()
```

**Line-by-line:**
- `data = [...]` — list of tuples, each tuple is one row
- `schema = [...]` — list of column names, must match the order of values in tuples
- `spark.createDataFrame(data, schema)` — creates a DataFrame from Python data (no file needed)
- `createOrReplaceTempView("transactions")` — registers as a SQL table named "transactions". Without this, `spark.sql()` can't find the table.

---

### CELL 3: Q1a — Total Sales by City (3 Marks)

```python
spark.sql("""
    SELECT city, SUM(amount) AS total_sales
    FROM transactions
    GROUP BY city
""").show()
```

**Breakdown:**
- `SELECT city, SUM(amount)` — pick city and sum of amounts
- `FROM transactions` — from our registered table
- `GROUP BY city` — one row per city
- `AS total_sales` — rename the output column

---

### CELL 4: Q1b — Top 3 Cities (3 Marks)

```python
spark.sql("""
    SELECT city, SUM(amount) AS total_sales
    FROM transactions
    GROUP BY city
    ORDER BY total_sales DESC
    LIMIT 3
""").show()
```

**Breakdown:**
- Same as Q1a but add `ORDER BY total_sales DESC` (highest first) and `LIMIT 3`
- This is just Q1a + sorting + limiting — the question says "extend the previous query"

---

### CELL 5: Q1c — Avg Amount Per Month for 2024 (4 Marks)

```python
spark.sql("""
    SELECT MONTH(transaction_date) AS month,
           AVG(amount) AS average_transaction_amount
    FROM transactions
    WHERE YEAR(transaction_date) = 2024
    GROUP BY MONTH(transaction_date)
    ORDER BY month
""").show()
```

**Breakdown:**
- `MONTH(transaction_date)` — extracts the month number (1=Jan, 2=Feb, etc.)
- `WHERE YEAR(transaction_date) = 2024` — only 2024 data
- `GROUP BY MONTH(transaction_date)` — one row per month
- `ORDER BY month` — chronological order

---

### CELL 6: Q2a — Filter After Jan 6 (3 Marks)

```python
spark.sql("""
    SELECT *
    FROM transactions
    WHERE transaction_date > '2024-01-06'
""").show()
```

**Breakdown:**
- `WHERE transaction_date > '2024-01-06'` — string comparison works for dates in `YYYY-MM-DD` format because they sort lexicographically
- `>` means strictly after (Jan 6 itself is NOT included)

---

### CELL 7: Q2b — Total Expenditure by City After Jan 6 (4 Marks)

```python
spark.sql("""
    SELECT city, SUM(amount) AS total_expenditure
    FROM transactions
    WHERE transaction_date > '2024-01-06'
    GROUP BY city
""").show()
```

**Breakdown:**
- "Extend the previous query" = add GROUP BY and SUM
- Same filter + aggregation

---

### CELL 8: Q2c — Avg Amount in Chicago (3 Marks)

```python
spark.sql("""
    SELECT AVG(amount) AS average_transaction_amount
    FROM transactions
    WHERE city = 'Chicago'
""").show()
```

**Breakdown:**
- `WHERE city = 'Chicago'` — filter to one city
- `AVG(amount)` — average of those rows
- No GROUP BY needed since we're filtering to one city

---

### CELL 9: Q3a — Avg Customer Spending per City (5 Marks) ⭐ HARDEST

```python
spark.sql("""
    SELECT city, AVG(customer_total) AS avg_customer_spending
    FROM (
        SELECT city, customer_id, SUM(amount) AS customer_total
        FROM transactions
        GROUP BY city, customer_id
    )
    GROUP BY city
""").show()
```

**Breakdown (this is a SUBQUERY — read inside-out):**

**Inner query runs first:**
```sql
SELECT city, customer_id, SUM(amount) AS customer_total
FROM transactions
GROUP BY city, customer_id
```
This gives total spent by each customer in each city. Example:
- customer 1001 in New York spent 50 → customer_total = 50
- customer 1002 in New York spent 80 → customer_total = 80

**Outer query then runs on that result:**
```sql
SELECT city, AVG(customer_total)
GROUP BY city
```
This averages those per-customer totals by city. Example:
- New York: AVG(50, 80, 70, 115) = 78.75

**Why a subquery?** Because "average total per customer" needs TWO aggregations: first SUM per customer, then AVG of those sums. SQL can't do two aggregations in one query, so you nest them.

---

### CELL 10: Q3b — City with Highest Single Transaction (5 Marks)

```python
spark.sql("""
    SELECT city, amount AS highest_transaction
    FROM transactions
    ORDER BY amount DESC
    LIMIT 1
""").show()
```

**Breakdown:**
- No GROUP BY — we want the single row with the highest amount
- `ORDER BY amount DESC` — highest first
- `LIMIT 1` — just the top one

**Alternative approach:**
```python
spark.sql("""
    SELECT city, MAX(amount) AS highest_transaction
    FROM transactions
    GROUP BY city
    ORDER BY highest_transaction DESC
    LIMIT 1
""").show()
```

---

## 📝 DataFrame API Equivalents (If you prefer)

```python
# Q1a
df.groupBy("city").agg(sum("amount").alias("total_sales")).show()

# Q1b
df.groupBy("city").agg(sum("amount").alias("total_sales")) \
    .orderBy(desc("total_sales")).limit(3).show()

# Q1c
df.filter(year("transaction_date") == 2024) \
    .groupBy(month("transaction_date").alias("month")) \
    .agg(avg("amount").alias("avg_amount")) \
    .orderBy("month").show()

# Q2a
df.filter(col("transaction_date") > "2024-01-06").show()

# Q2b
df.filter(col("transaction_date") > "2024-01-06") \
    .groupBy("city").agg(sum("amount").alias("total_expenditure")).show()

# Q2c
df.filter(col("city") == "Chicago") \
    .agg(avg("amount").alias("avg_amount")).show()

# Q3b
df.orderBy(desc("amount")).limit(1).select("city", "amount").show()
```

---

## ❓ Viva Questions & Answers (PYQ-3 Specific)

**Q: What is `createOrReplaceTempView()`?**
A: Registers a DataFrame as a temporary SQL table in Spark's catalog. "Temp" means it only exists for the current SparkSession. "OrReplace" means if a view with that name already exists, it gets overwritten.

**Q: Difference between `createOrReplaceTempView` and `createGlobalTempView`?**
A: TempView is session-scoped (only your SparkSession can see it). GlobalTempView is application-scoped (all sessions can see it), accessed as `global_temp.tablename`.

**Q: Can you compare dates as strings in SQL?**
A: Yes, but ONLY if they're in `YYYY-MM-DD` format. This format sorts correctly as strings because year comes first, then month, then day. `'2024-01-06' < '2024-01-07'` is true.

**Q: What is a subquery?**
A: A query nested inside another query. The inner query runs first and produces a temporary result set. The outer query then operates on that result. Used when you need to aggregate an already-aggregated result.

**Q: When do you need a subquery?**
A: When you need to apply an aggregate function on the result of another aggregate function. Example: "average of totals" = first SUM (inner), then AVG (outer). SQL doesn't allow `AVG(SUM(x))` directly.

**Q: What does `MONTH()` return?**
A: An integer from 1 to 12. January=1, February=2, ..., December=12.

**Q: Difference between `>` and `>=` in date filters?**
A: `> '2024-01-06'` excludes Jan 6. `>= '2024-01-06'` includes Jan 6. Read the question carefully — "after January 6" means `>`, not `>=`.

**Q: Why `spark.sql()` and not just SQL?**
A: Spark SQL is not a database — there's no SQL prompt. You call `spark.sql("query string")` which returns a DataFrame. You then call `.show()` to display it.

**Q: Difference between `spark.sql()` and DataFrame API?**
A: Both do the same thing, just different syntax. `spark.sql("SELECT city, SUM(amount) FROM t GROUP BY city")` is equivalent to `df.groupBy("city").agg(sum("amount"))`. Spark's Catalyst optimizer generates the same execution plan for both. Use whichever the question asks for.

---

## 🔑 SQL Patterns Summary

```sql
-- Basic aggregation
SELECT group_col, AGG(value_col) FROM table GROUP BY group_col

-- Top N
... ORDER BY col DESC LIMIT N

-- Date filtering
WHERE transaction_date > '2024-01-06'
WHERE YEAR(date_col) = 2024
WHERE MONTH(date_col) = 1

-- Filter by specific value
WHERE city = 'Chicago'

-- Subquery (aggregate of aggregate)
SELECT col, AGG(inner_result)
FROM (SELECT col, AGG(val) AS inner_result FROM t GROUP BY col, col2)
GROUP BY col

-- Single max row
SELECT * FROM table ORDER BY col DESC LIMIT 1
```

---

## ⚡ Common Mistakes for PYQ-3

1. **Forgetting `createOrReplaceTempView()`** → `spark.sql()` throws "Table or view not found"
2. **Using `=` instead of `>` for "after"** — "after Jan 6" = `> '2024-01-06'`, NOT `>= '2024-01-06'`
3. **Forgetting `AS` aliases** — always name your output columns: `SUM(amount) AS total_sales`
4. **Nested aggregation without subquery** — `AVG(SUM(amount))` is INVALID SQL. Must use a subquery.
5. **Wrong date format** — must be `'YYYY-MM-DD'` with quotes and hyphens
6. **Forgetting `.show()`** — `spark.sql(...)` returns a DataFrame but doesn't display it. Always end with `.show()`
