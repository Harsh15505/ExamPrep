# 📘 PYQ-1: Spark Data Processing Pipeline — Complete Guide

> **Source:** PDEU End Semester Exam, April-May 2025, SET1  
> **Topic:** Spark Data Processing Pipeline  
> **Total Marks:** 30 (6 parts × 5 marks each)  
> **Time:** 1.5 hours (30 min planning + 1 hour coding)

---

## 📌 What This Question Tests

You're given a **CSV/text file** of customer transactions with columns:
- `customer_id` — who made the purchase
- `transaction_date` — when
- `transaction_amount` — how much (can have nulls, zeros, negatives)
- `product_category` — what type of product

You must: load it, clean it, then do 5 different aggregation queries. That's it. It's all **groupBy + agg** operations.

---

## 🧠 Theory You MUST Know

### What is a DataFrame?
A distributed collection of data organized into named columns — like a SQL table or a Pandas DataFrame, but spread across a cluster. You create one by reading a file:
```python
df = spark.read.csv("path", header=True, inferSchema=True)
```
- `header=True` → first row is column names
- `inferSchema=True` → Spark auto-detects data types (int, double, string)

### What is an RDD?
Resilient Distributed Dataset — the low-level building block. A DataFrame is built on top of RDDs. You rarely need raw RDDs for this type of question, but if asked:
```python
rdd = sc.textFile("path")                        # load as RDD
rdd = rdd.map(lambda line: line.split(","))       # split each line
rdd = rdd.filter(lambda x: float(x[2]) > 0)      # filter
```

### Key DataFrame Operations
| Operation | What It Does | Syntax |
|-----------|-------------|--------|
| `filter()` | Keep rows matching a condition | `df.filter(col("x") > 0)` |
| `groupBy()` | Group rows by a column | `df.groupBy("col")` |
| `agg()` | Apply aggregation after groupBy | `.agg(sum("x"), avg("y"))` |
| `orderBy()` | Sort results | `.orderBy(desc("col"))` |
| `limit(n)` | Take first n rows | `.limit(3)` |
| `show()` | Display the output | `.show()` |
| `select()` | Pick specific columns | `df.select("col1", "col2")` |

### Key Aggregation Functions
| Function | Import | Usage |
|----------|--------|-------|
| `sum()` | `from pyspark.sql.functions import sum` | Total of a column |
| `avg()` | `from pyspark.sql.functions import avg` | Average of a column |
| `count()` | `from pyspark.sql.functions import count` | Count rows |
| `max()` / `min()` | same import | Max/Min value |
| `desc()` | same import | Sort descending |

### Filtering Nulls and Bad Data
```python
col("x").isNotNull()     # x is not null
col("x").isNull()        # x is null
col("x") > 0             # x is positive
```
Combine with `&` (AND) and `|` (OR):
```python
df.filter((col("x").isNotNull()) & (col("x") > 0))
```

---

## 💻 Complete Solution — Cell by Cell

### CELL 1: Initialization (Paste this FIRST, always)

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
from pyspark.sql.types import *

print("✅ Spark Ready!", spark.version)
```

**Line-by-line:**
- `findspark.init()` — tells Python where Spark is installed inside Docker
- `SparkSession.builder` — creates the main entry point to Spark
- `.appName("BDA-Exam")` — names your application (shows in Spark UI)
- `.master("local[*]")` — run locally using all CPU cores
- `.getOrCreate()` — reuse existing session if one exists
- `sc = spark.sparkContext` — gives you access to RDD-level operations
- `from pyspark.sql.functions import *` — imports sum, avg, count, col, desc, etc.

---

### CELL 2: Q1a — Load the Dataset (2 Marks)

```python
df = spark.read.csv("/work/sample_transactions.txt", header=True, inferSchema=True)

print("=== Raw Data ===")
df.show()
df.printSchema()
print(f"Total rows: {df.count()}")
```

**Line-by-line:**
- `spark.read.csv(path)` — reads a CSV file into a DataFrame
- `header=True` — first row has column names, don't treat it as data
- `inferSchema=True` — auto-detect types (integer, double, string) instead of treating everything as string
- `df.show()` — prints the table nicely (default 20 rows)
- `df.printSchema()` — shows column names and their data types
- `df.count()` — returns total number of rows

> **If they give you a text file without headers**, use:
> ```python
> schema = StructType([
>     StructField("customer_id", IntegerType(), True),
>     StructField("transaction_date", StringType(), True),
>     StructField("transaction_amount", DoubleType(), True),
>     StructField("product_category", StringType(), True),
> ])
> df = spark.read.csv("/work/data.txt", header=False, schema=schema)
> ```

> **If they ask for RDD loading instead:**
> ```python
> rdd = sc.textFile("/work/data.txt")
> header = rdd.first()
> rdd = rdd.filter(lambda line: line != header)
> rdd = rdd.map(lambda line: line.split(","))
> # Convert to DataFrame
> df = rdd.map(lambda x: (int(x[0]), x[1].strip(), float(x[2]), x[3].strip())) \
>     .toDF(["customer_id", "transaction_date", "transaction_amount", "product_category"])
> ```

---

### CELL 3: Q1b — Filter Bad Data (3 Marks)

```python
df_clean = df.filter(
    (col("transaction_amount").isNotNull()) &
    (col("transaction_amount") > 0)
)

print("=== Clean Data (nulls, zeros, negatives removed) ===")
df_clean.show()
print(f"Rows after filtering: {df_clean.count()}")
```

**Line-by-line:**
- `col("transaction_amount")` — refers to the column by name
- `.isNotNull()` — keeps only rows where the value exists (removes nulls/missing)
- `> 0` — keeps only positive amounts (removes zeros and negatives)
- `&` — AND operator (both conditions must be true)
- **Parentheses around each condition are REQUIRED** in PySpark

---

### CELL 4: Q2 — Total Expenditure by Customer (5 Marks)

```python
total_by_customer = df_clean.groupBy("customer_id") \
    .agg(sum("transaction_amount").alias("total_expenditure"))

print("=== Total Expenditure by Customer ===")
total_by_customer.show()
```

**Line-by-line:**
- `groupBy("customer_id")` — groups all rows with the same customer_id together
- `.agg(...)` — applies an aggregation function to each group
- `sum("transaction_amount")` — adds up all transaction amounts within each group
- `.alias("total_expenditure")` — renames the output column (otherwise it would be `sum(transaction_amount)`)

---

### CELL 5: Q3 — Avg Amount by Product Category (5 Marks)

```python
avg_by_category = df_clean.groupBy("product_category") \
    .agg(avg("transaction_amount").alias("average_transaction_amount"))

print("=== Average Transaction Amount by Product Category ===")
avg_by_category.show()
```

**Line-by-line:**
- Same pattern as Q2 but `groupBy("product_category")` instead
- `avg()` instead of `sum()` — computes the mean

---

### CELL 6: Q4 — Top 3 Customers by Expenditure (5 Marks)

```python
top3 = df_clean.groupBy("customer_id") \
    .agg(sum("transaction_amount").alias("total_expenditure")) \
    .orderBy(desc("total_expenditure")) \
    .limit(3)

print("=== Top 3 Customers by Expenditure ===")
top3.show()
```

**Line-by-line:**
- First does the same groupBy + sum as Q2
- `.orderBy(desc("total_expenditure"))` — sorts highest to lowest
- `desc()` — descending order (without this, it sorts ascending)
- `.limit(3)` — takes only the top 3 rows

---

### CELL 7: Q5 — Transaction Count per Day (5 Marks)

```python
count_per_day = df_clean.groupBy("transaction_date") \
    .agg(count("*").alias("transaction_count"))

print("=== Transaction Count per Day ===")
count_per_day.orderBy("transaction_date").show()
```

**Line-by-line:**
- `groupBy("transaction_date")` — groups by date
- `count("*")` — counts all rows in each group (the `"*"` means "count all rows")
- `.orderBy("transaction_date")` — sorts chronologically (ascending by default)

---

### CELL 8: Q6 — Most Popular Product Category (5 Marks)

```python
popular_category = df_clean.groupBy("product_category") \
    .agg(count("*").alias("transaction_count")) \
    .orderBy(desc("transaction_count")) \
    .limit(1)

print("=== Most Popular Product Category ===")
popular_category.show()
```

**Line-by-line:**
- Groups by category, counts transactions in each
- Sorts descending (most transactions first)
- `.limit(1)` — takes only the top one = the most popular

---

## 🔀 RDD Version (If They Specifically Ask for RDD)

```python
# Load
rdd = sc.textFile("/work/sample_transactions.txt")
header = rdd.first()
rdd = rdd.filter(lambda line: line != header)

# Parse
parsed = rdd.map(lambda line: line.split(",")) \
    .map(lambda x: (int(x[0]), x[1].strip(), float(x[2]) if x[2].strip() else 0.0, x[3].strip()))

# Filter (remove zero/negative)
clean = parsed.filter(lambda x: x[2] > 0)

# Q2: Total by customer → (customer_id, amount) → reduceByKey
total = clean.map(lambda x: (x[0], x[2])).reduceByKey(lambda a, b: a + b)
print("Total by customer:", total.collect())

# Q3: Avg by category
cat_amounts = clean.map(lambda x: (x[3], (x[2], 1)))
cat_sum = cat_amounts.reduceByKey(lambda a, b: (a[0]+b[0], a[1]+b[1]))
cat_avg = cat_sum.mapValues(lambda x: x[0]/x[1])
print("Avg by category:", cat_avg.collect())

# Q4: Top 3
top3 = total.sortBy(lambda x: x[1], ascending=False).take(3)
print("Top 3:", top3)

# Q5: Count per day
daily = clean.map(lambda x: (x[1], 1)).reduceByKey(lambda a, b: a + b)
print("Daily count:", daily.collect())

# Q6: Most popular
cat_count = clean.map(lambda x: (x[3], 1)).reduceByKey(lambda a, b: a + b)
popular = cat_count.sortBy(lambda x: x[1], ascending=False).first()
print("Most popular:", popular)
```

---

## 📝 Spark SQL Version (If They Ask for SQL Queries)

```python
df_clean.createOrReplaceTempView("transactions")

# Q2
spark.sql("SELECT customer_id, SUM(transaction_amount) AS total_expenditure FROM transactions GROUP BY customer_id").show()

# Q3
spark.sql("SELECT product_category, AVG(transaction_amount) AS average_transaction_amount FROM transactions GROUP BY product_category").show()

# Q4
spark.sql("SELECT customer_id, SUM(transaction_amount) AS total_expenditure FROM transactions GROUP BY customer_id ORDER BY total_expenditure DESC LIMIT 3").show()

# Q5
spark.sql("SELECT transaction_date, COUNT(*) AS transaction_count FROM transactions GROUP BY transaction_date ORDER BY transaction_date").show()

# Q6
spark.sql("SELECT product_category, COUNT(*) AS transaction_count FROM transactions GROUP BY product_category ORDER BY transaction_count DESC LIMIT 1").show()
```

---

## 🎯 Exam Strategy (What to Do Tomorrow)

1. **First 5 minutes:** Read the question. Identify columns, data types, and what each sub-question asks.
2. **Minutes 5-10:** Open Jupyter, paste init cell, run it.
3. **Minutes 10-15:** Load the data file they give you. Run `df.show()` and `df.printSchema()` to understand the data.
4. **Minutes 15-20:** Write the filter. Always check for nulls AND zeros AND negatives unless told otherwise.
5. **Minutes 20-60:** Do each sub-question one per cell. The pattern is ALWAYS the same:
   ```
   df.groupBy("some_column").agg(FUNCTION("some_other_column").alias("nice_name")).show()
   ```
6. **Last 10 minutes:** Add `print("===")` headers to each output. Run all cells top-to-bottom to make sure everything works. Save (`Ctrl+S`).

### The Universal Pattern

Every single question in this paper follows this exact pattern:

```
result = df_clean
    .groupBy("GROUP_COLUMN")          # what to group by
    .agg(FUNCTION("VALUE_COLUMN")     # what calculation
         .alias("OUTPUT_NAME"))       # what to name it
    .orderBy(desc("OUTPUT_NAME"))     # optional: sort
    .limit(N)                         # optional: top N
```

Just swap out the column names and the function (sum/avg/count). That's the entire exam.

---

## ❓ Viva Questions & Answers

### Basics

**Q: What is Apache Spark?**
A: An open-source distributed computing engine for large-scale data processing. It's faster than Hadoop MapReduce because it processes data in-memory instead of writing to disk after each step.

**Q: What is a SparkSession?**
A: The single entry point to all Spark functionality. Created with `SparkSession.builder.getOrCreate()`. It replaces the old SparkContext + SQLContext + HiveContext from Spark 1.x.

**Q: Difference between RDD and DataFrame?**
A: RDD is the low-level API — unstructured, no schema, uses lambda functions. DataFrame is the high-level API — has named columns, schema, and is optimized by Spark's Catalyst optimizer. DataFrames are faster because Spark can optimize the query plan.

**Q: What does `local[*]` mean?**
A: Run Spark locally using all available CPU cores. `local[2]` would use only 2 cores. In a cluster, you'd use `yarn` or `mesos` instead.

### About the Code

**Q: Why `inferSchema=True`?**
A: Without it, all columns are read as strings. With it, Spark automatically detects that `transaction_amount` is a double, `customer_id` is an integer, etc. This lets us do math operations directly.

**Q: What does `col()` do?**
A: References a column by name. `col("transaction_amount")` refers to that column. You can also use `df["transaction_amount"]` or `df.transaction_amount` but `col()` is the cleanest.

**Q: Why parentheses around filter conditions?**
A: Python operator precedence. Without parentheses, `&` binds tighter than `>`, causing a syntax error. Always wrap each condition: `(condition1) & (condition2)`.

**Q: Difference between `filter()` and `where()`?**
A: They are identical. `where()` is just an alias for `filter()`. Use whichever you prefer.

**Q: What does `.alias()` do?**
A: Renames a column. Without it, `sum("transaction_amount")` would create a column named `sum(transaction_amount)` which is ugly. `.alias("total")` renames it to `total`.

**Q: Difference between `orderBy()` and `sort()`?**
A: They are identical. Both sort the DataFrame. Use `desc("col")` for descending, default is ascending.

### Deeper Questions

**Q: What are transformations vs actions in Spark?**
A: **Transformations** are lazy — they define what to do but don't execute yet (filter, map, groupBy, select, orderBy). **Actions** trigger execution and return results (show, collect, count, take, reduce). Spark waits until an action to actually compute everything — this is called "lazy evaluation."

**Q: What is lazy evaluation and why does Spark use it?**
A: Spark doesn't execute transformations immediately. It builds a DAG (Directed Acyclic Graph) of operations and optimizes the entire plan before executing. This lets it skip unnecessary computations, combine operations, and minimize data shuffling.

**Q: What is a DAG?**
A: Directed Acyclic Graph — the execution plan Spark creates from your transformations. Each node is an operation, edges show data flow. Spark's DAG scheduler converts this into stages and tasks.

**Q: What is shuffling?**
A: Moving data between partitions across the cluster. Operations like `groupBy` require shuffling because rows with the same key might be on different nodes. Shuffling is expensive — it involves disk I/O and network transfer.

**Q: What are partitions?**
A: Chunks of data distributed across the cluster. A DataFrame is split into partitions, and each partition is processed by one task on one core. More partitions = more parallelism.

**Q: How is Spark different from Hadoop MapReduce?**
A: (1) Spark processes in-memory, Hadoop writes to disk after each step. (2) Spark supports iterative algorithms efficiently. (3) Spark has a rich API (SQL, ML, Streaming), Hadoop only has Map and Reduce. (4) Spark is 10-100x faster for most workloads.

**Q: What is the Catalyst Optimizer?**
A: Spark's query optimizer for DataFrames/SQL. It takes your query, creates a logical plan, optimizes it (predicate pushdown, column pruning, etc.), and generates an efficient physical plan. This is why DataFrames are faster than RDDs — Catalyst can optimize them.

---

## 🔄 Variations to Expect

The question pattern will be the same but with different data. Be ready for:

| Possible Dataset | Columns You'll See |
|---|---|
| E-commerce orders | order_id, customer_id, amount, product, date |
| Student grades | student_id, subject, marks, semester |
| Employee salary | emp_id, department, salary, join_date |
| Sales data | sale_id, region, revenue, product_type, date |
| Movie ratings | user_id, movie_id, rating, genre, timestamp |

The operations will always be some combination of:
- **Load + Filter** (remove nulls/invalid data)
- **GroupBy + Sum** (total by category)
- **GroupBy + Avg** (average by category)
- **GroupBy + Count** (count by category)
- **OrderBy + Limit** (top N)

If you know these 5 patterns, you can solve ANY variation of this question.

---

## ⚡ Common Mistakes to Avoid

1. **Forgetting `inferSchema=True`** → all columns become strings, math fails
2. **Missing parentheses in filter** → `df.filter(col("x") > 0 & col("y").isNotNull())` CRASHES. Must be `(col("x") > 0) & (col("y").isNotNull())`
3. **Using `count("column")` vs `count("*")`** → `count("column")` skips nulls, `count("*")` counts all rows. For "how many transactions", use `count("*")`
4. **Forgetting `.alias()`** → output column gets ugly name like `sum(transaction_amount)` instead of `total_expenditure`
5. **Not showing output** → always end with `.show()`. The examiner needs to see results
6. **Not filtering before aggregating** → always clean data FIRST, then do all queries on `df_clean`
