# 📘 PYQ-4: E-Commerce Transactions — Spark SQL (SET II Afternoon)

> **Source:** PDEU End Semester Exam, April-May 2025, SET II (Afternoon 4:00-6:30 PM)  
> **Topic:** Spark SQL on e-commerce data with regions and product categories  
> **Total Marks:** 30 (3 sections)  
> **Nearly identical to PYQ-3** — same structure, different column names

---

## 📌 How This Differs from PYQ-3

| PYQ-3 | PYQ-4 |
|-------|-------|
| `city` column | `region` column |
| No product_category | Has `product_category` |
| Filter by city="Chicago" | Filter by category="Electronics" |
| Avg per month | Avg per region |

**Same patterns, different column names.** If you understood PYQ-3, this is copy-paste with find-replace.

---

## 💻 Complete Solution — Cell by Cell

### CELL 1: Initialization

```python
import findspark
findspark.init()

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("BDA-Exam").master("local[*]").getOrCreate()
sc = spark.sparkContext
from pyspark.sql.functions import *
print("✅ Spark Ready!", spark.version)
```

---

### CELL 2: Create Data (Copy from question paper)

```python
data = [
    (1, "Electronics", 101, 120, "2024-01-01", "North America"),
    (2, "Clothing", 102, 75, "2024-01-02", "Europe"),
    (3, "Home Appliances", 103, 250, "2024-01-03", "Asia"),
    (4, "Books", 104, 30, "2024-01-04", "Africa"),
    (5, "Clothing", 105, 60, "2024-01-05", "North America"),
    (6, "Electronics", 106, 100, "2024-01-06", "Europe"),
    (7, "Electronics", 107, 150, "2024-01-07", "Asia"),
    (8, "Furniture", 108, 500, "2024-01-08", "South America"),
    (9, "Books", 109, 40, "2024-01-09", "North America"),
    (10, "Furniture", 110, 700, "2024-01-10", "South America"),
]

schema = ["order_id", "product_category", "customer_id",
          "amount", "order_date", "region"]
df = spark.createDataFrame(data, schema)
df.createOrReplaceTempView("orders")

df.show(truncate=False)
```

**Key point:** The data is given as Scala `Seq(...)` in the question. Just convert each row to a Python tuple. Replace `val data = Seq(` with `data = [` and `)` with `]`.

---

### CELL 3: Q1a — Total Sales by Product Category (3 Marks)

```python
spark.sql("""
    SELECT product_category, SUM(amount) AS total_sales
    FROM orders
    GROUP BY product_category
""").show()
```

Pattern: `GROUP BY product_category` + `SUM(amount)`

---

### CELL 4: Q1b — Top 3 Categories (3 Marks)

```python
spark.sql("""
    SELECT product_category, SUM(amount) AS total_sales
    FROM orders
    GROUP BY product_category
    ORDER BY total_sales DESC
    LIMIT 3
""").show()
```

Pattern: Same as Q1a + `ORDER BY DESC LIMIT 3`

---

### CELL 5: Q1c — Avg Amount Per Region for 2024 (4 Marks)

```python
spark.sql("""
    SELECT region, AVG(amount) AS average_transaction_amount
    FROM orders
    WHERE YEAR(order_date) = 2024
    GROUP BY region
""").show()
```

Pattern: `WHERE YEAR(date) = 2024` + `GROUP BY region` + `AVG`

---

### CELL 6: Q2a — Filter After Jan 6 (3 Marks)

```python
spark.sql("""
    SELECT *
    FROM orders
    WHERE order_date > '2024-01-06'
""").show()
```

Pattern: `WHERE date > 'YYYY-MM-DD'`

---

### CELL 7: Q2b — Total Expenditure by Region After Jan 6 (4 Marks)

```python
spark.sql("""
    SELECT region, SUM(amount) AS total_expenditure
    FROM orders
    WHERE order_date > '2024-01-06'
    GROUP BY region
""").show()
```

Pattern: "Extend the previous" = add `GROUP BY` + `SUM`

---

### CELL 8: Q2c — Avg for Electronics (3 Marks)

```python
spark.sql("""
    SELECT AVG(amount) AS average_transaction_amount
    FROM orders
    WHERE product_category = 'Electronics'
""").show()
```

Pattern: `WHERE category = 'value'` + `AVG`. No GROUP BY needed (single category).

---

### CELL 9: Q3a — Total per Customer + Top 3 (5 Marks)

```python
# All customers
spark.sql("""
    SELECT customer_id, SUM(amount) AS total_sales
    FROM orders
    GROUP BY customer_id
    ORDER BY total_sales DESC
""").show()

# Top 3
spark.sql("""
    SELECT customer_id, SUM(amount) AS total_sales
    FROM orders
    GROUP BY customer_id
    ORDER BY total_sales DESC
    LIMIT 3
""").show()
```

Pattern: `GROUP BY customer_id` + `SUM` + `ORDER BY DESC LIMIT 3`

---

### CELL 10: Q3b — Region with Highest Single Order (5 Marks)

```python
spark.sql("""
    SELECT region, amount AS highest_order
    FROM orders
    ORDER BY amount DESC
    LIMIT 1
""").show()
```

Pattern: No GROUP BY — just sort all rows and take the first one.

---

## 📝 DataFrame API Equivalents

```python
# Q1a
df.groupBy("product_category").agg(sum("amount").alias("total_sales")).show()

# Q1b
df.groupBy("product_category").agg(sum("amount").alias("total_sales")) \
    .orderBy(desc("total_sales")).limit(3).show()

# Q1c
df.filter(year("order_date") == 2024) \
    .groupBy("region").agg(avg("amount").alias("avg_amount")).show()

# Q2a
df.filter(col("order_date") > "2024-01-06").show()

# Q2b
df.filter(col("order_date") > "2024-01-06") \
    .groupBy("region").agg(sum("amount").alias("total_expenditure")).show()

# Q2c
df.filter(col("product_category") == "Electronics") \
    .agg(avg("amount").alias("avg_amount")).show()

# Q3a
df.groupBy("customer_id").agg(sum("amount").alias("total_sales")) \
    .orderBy(desc("total_sales")).show()

# Q3b
df.orderBy(desc("amount")).limit(1).select("region", "amount").show()
```

---

## 🔑 The Pattern Map (PYQ-3 vs PYQ-4)

These two papers prove the exam follows a **template**. Here it is:

| Question | Pattern | PYQ-3 Column | PYQ-4 Column |
|----------|---------|-------------|-------------|
| 1a | GROUP BY + SUM | city | product_category |
| 1b | + ORDER BY DESC LIMIT 3 | city | product_category |
| 1c | DATE function + GROUP BY + AVG | MONTH | region |
| 2a | WHERE date > 'X' | Jan 6 | Jan 6 |
| 2b | 2a + GROUP BY + SUM | city | region |
| 2c | WHERE col='value' + AVG | Chicago | Electronics |
| 3a | GROUP BY + SUM + TOP 3 | customer | customer |
| 3b | ORDER BY DESC LIMIT 1 | city | region |

**It's the same exam with different column names.** Master the template, ace any variation.

---

## ❓ Additional Viva Questions

**Q: How do you convert Scala Seq data to PySpark?**
A: Replace `Seq(` with `[`, replace each `(...)` row with a Python tuple, use `spark.createDataFrame(data, schema)`.

**Q: What does `YEAR()` return for `'2024-01-15'`?**
A: Integer `2024`.

**Q: Why no GROUP BY in Q2c/Q3b?**
A: Q2c filters to a single category then averages — only one group. Q3b wants the single highest row, not a group summary.

**Q: Can you use `WHERE` and `GROUP BY` together?**
A: Yes. `WHERE` filters rows BEFORE grouping. `HAVING` filters AFTER grouping. Example: `WHERE date > 'X' GROUP BY region HAVING SUM(amount) > 100`.

**Q: What's the difference between `WHERE` and `HAVING`?**
A: `WHERE` filters individual rows before aggregation. `HAVING` filters groups after aggregation. You can't use aggregate functions in `WHERE` (e.g., `WHERE SUM(amount) > 100` is invalid — use `HAVING`).
