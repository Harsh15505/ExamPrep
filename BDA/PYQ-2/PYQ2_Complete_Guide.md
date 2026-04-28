# 📘 PYQ-2: Spark Processing on Product Reviews Dataset — Complete Guide

> **Source:** PDEU End Semester Exam, April-May 2025, SET II  
> **Topic:** Spark Processing on Product Reviews Dataset  
> **Total Marks:** 30 (6 parts × 5 marks each)  
> **Key Difference from PYQ-1:** Two datasets, JOIN operation, and text-based sentiment analysis

---

## 📌 What This Question Tests

You're given **TWO files**:

**Reviews:** review_id, product_id, user_id, review_date, rating, review_text  
**Products:** product_id, product_name, product_category, price

You must: load both, clean reviews, do aggregations, JOIN them together, and do basic text analysis. The new concepts vs PYQ-1 are **JOINs** and **string matching**.

---

## 🧠 New Theory (Beyond PYQ-1)

### JOINs in Spark

A JOIN combines two DataFrames based on a common column. Like SQL JOINs.

```python
result = df1.join(df2, "common_column", "join_type")
```

| Join Type | What It Keeps |
|-----------|--------------|
| `"inner"` | Only rows that match in BOTH tables |
| `"left"` | All rows from left + matching from right |
| `"right"` | All rows from right + matching from left |
| `"outer"` | All rows from both, nulls where no match |

**For this exam, you'll almost always use `"inner"`.**

Example:
```python
# Reviews has product_id P123, P124, P999
# Products has product_id P123, P124, P125
# Inner join → only P123, P124 (both must exist)
reviews.join(products, "product_id", "inner")
```

### String Matching with `rlike()`

`rlike()` matches text using regex patterns. `|` means OR.

```python
# Check if review_text contains "great" OR "excellent" OR "recommended"
col("review_text").rlike("great|excellent|recommended")

# Case-insensitive: wrap with lower()
lower(col("review_text")).rlike("great|excellent|recommended")
```

### `when().otherwise()` — Spark's IF-ELSE

```python
from pyspark.sql.functions import when

# If condition is true → 1, else → 0
df.withColumn("new_col",
    when(CONDITION, VALUE_IF_TRUE).otherwise(VALUE_IF_FALSE)
)
```

### Using JOIN to Filter (Q1's Trick)

"Only include reviews for products that exist in the Products dataset" = do an inner join. Any review with a product_id NOT in Products will be dropped automatically.

```python
valid_products = products.select("product_id")
reviews_clean = reviews.join(valid_products, "product_id", "inner")
```

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
from pyspark.sql.types import *

print("✅ Spark Ready!", spark.version)
```

---

### CELL 2: Q1 — Load Both Datasets & Filter (5 Marks)

```python
# Load both datasets
reviews = spark.read.csv("/work/reviews.txt", header=True, inferSchema=True)
products = spark.read.csv("/work/products.txt", header=True, inferSchema=True)

print("=== Raw Reviews ===")
reviews.show(truncate=False)
print("=== Products ===")
products.show()

# Get valid product IDs from Products table
valid_products = products.select("product_id")

# Filter: remove null ratings, ratings < 1.0, and invalid product IDs
reviews_clean = reviews.filter(
    (col("rating").isNotNull()) &
    (col("rating") >= 1.0)
).join(valid_products, "product_id", "inner")

print("=== Cleaned Reviews ===")
reviews_clean.show(truncate=False)
print(f"Rows after filtering: {reviews_clean.count()}")
```

**Line-by-line:**
- Load two separate CSV files into two DataFrames
- `truncate=False` — show full text of review_text column (default truncates at 20 chars)
- `valid_products = products.select("product_id")` — extract just the product_id column from Products
- `filter(... & ...)` — remove nulls and ratings below 1.0
- `.join(valid_products, "product_id", "inner")` — keeps only reviews whose product_id exists in the Products table. Review R14 (P999) gets dropped because P999 isn't in Products.

**What gets removed:**
- R6 (rating is null/missing)
- R4 (rating 0.5 is below 1.0)
- R14 (product P999 doesn't exist in Products)

---

### CELL 3: Q2 — Average Rating by Product (5 Marks)

```python
avg_by_product = reviews_clean.groupBy("product_id") \
    .agg(avg("rating").alias("average_rating"))

print("=== Average Rating by Product ===")
avg_by_product.show()
```

**Line-by-line:**
- `groupBy("product_id")` — group reviews by product
- `avg("rating")` — calculate mean rating for each product
- Same pattern as PYQ-1's aggregations

---

### CELL 4: Q3 — Top 5 Most Reviewed Products (5 Marks)

```python
most_reviewed = reviews_clean.groupBy("product_id") \
    .agg(count("*").alias("review_count")) \
    .orderBy(desc("review_count")) \
    .limit(5)

print("=== Top 5 Most Reviewed Products ===")
most_reviewed.show()
```

**Line-by-line:**
- `count("*")` — counts how many reviews each product has
- `orderBy(desc(...))` — most reviewed first
- `limit(5)` — top 5 only

---

### CELL 5: Q4 — Join Datasets (5 Marks) ⭐ NEW CONCEPT

```python
joined = reviews_clean.join(products, "product_id", "inner") \
    .select("product_name", "review_date", "rating", "user_id", "review_text")

print("=== Joined Data (Reviews + Product Info) ===")
joined.show(truncate=False)
```

**Line-by-line:**
- `reviews_clean.join(products, "product_id", "inner")` — combines both tables on product_id. Each review row now has the product_name, product_category, and price columns added to it.
- `.select(...)` — picks only the columns the question asks for. The question specifically says: product_name, review_date, rating, user_id, review_text.
- `"inner"` — only rows where product_id exists in BOTH tables

**How JOIN works visually:**
```
Reviews:  R1, P123, U456, 4.5, "Great..."
Products: P123, "Wireless Mouse", "Electronics", 25.0

After JOIN: "Wireless Mouse", 2024-10-01, 4.5, U456, "Great..."
```

---

### CELL 6: Q5 — Average Rating by Category (5 Marks)

```python
avg_by_category = reviews_clean.join(products, "product_id", "inner") \
    .groupBy("product_category") \
    .agg(avg("rating").alias("average_rating"))

print("=== Average Rating by Category ===")
avg_by_category.show()
```

**Line-by-line:**
- Reviews don't have `product_category` — it's in the Products table
- So we JOIN first to bring in the category, THEN groupBy category
- This is the key insight: **JOIN first, then aggregate**

---

### CELL 7: Q6 — Sentiment Analysis (5 Marks) ⭐ NEW CONCEPT

```python
positive_keywords = ["great", "excellent", "recommended"]

# Add a column: 1 if review contains any positive keyword, 0 otherwise
sentiment = reviews_clean.withColumn(
    "is_positive",
    when(
        lower(col("review_text")).rlike("great|excellent|recommended"),
        1
    ).otherwise(0)
)

# Calculate percentage of positive reviews per product
sentiment_result = sentiment.groupBy("product_id") \
    .agg(
        (sum("is_positive") / count("*") * 100).alias("positive_review_percentage")
    )

print("=== Sentiment Analysis ===")
sentiment_result.show()
```

**Line-by-line:**
- `lower(col("review_text"))` — converts text to lowercase so "Great" and "great" both match
- `.rlike("great|excellent|recommended")` — regex match. The `|` means OR. Returns true if the text contains ANY of these words
- `when(CONDITION, 1).otherwise(0)` — creates a new column: 1 if positive, 0 if not
- `.withColumn("is_positive", ...)` — adds this new column to the DataFrame
- `sum("is_positive") / count("*") * 100` — (number of positive reviews / total reviews) × 100 = percentage
- This is grouped by product_id so you get percentage per product

**Example:** If P123 has 5 reviews and 3 contain positive keywords → 3/5 × 100 = 60%

---

## 📝 Spark SQL Version

```python
reviews_clean.createOrReplaceTempView("reviews")
products.createOrReplaceTempView("products")

# Q2: Avg rating by product
spark.sql("SELECT product_id, AVG(rating) AS average_rating FROM reviews GROUP BY product_id").show()

# Q3: Top 5 most reviewed
spark.sql("SELECT product_id, COUNT(*) AS review_count FROM reviews GROUP BY product_id ORDER BY review_count DESC LIMIT 5").show()

# Q4: Join
spark.sql("""
    SELECT p.product_name, r.review_date, r.rating, r.user_id, r.review_text
    FROM reviews r
    INNER JOIN products p ON r.product_id = p.product_id
""").show(truncate=False)

# Q5: Avg rating by category
spark.sql("""
    SELECT p.product_category, AVG(r.rating) AS average_rating
    FROM reviews r
    INNER JOIN products p ON r.product_id = p.product_id
    GROUP BY p.product_category
""").show()

# Q6: Sentiment
spark.sql("""
    SELECT product_id,
        SUM(CASE WHEN LOWER(review_text) RLIKE 'great|excellent|recommended' THEN 1 ELSE 0 END) / COUNT(*) * 100
        AS positive_review_percentage
    FROM reviews
    GROUP BY product_id
""").show()
```

---

## 🔀 RDD Version

```python
# Load reviews
rev_rdd = sc.textFile("/work/reviews.txt")
rev_header = rev_rdd.first()
rev_rdd = rev_rdd.filter(lambda x: x != rev_header)

# Parse reviews: (review_id, product_id, user_id, date, rating, text)
def parse_review(line):
    parts = line.split(",", 5)  # max 5 splits (text may have commas)
    rid, pid, uid, date = parts[0], parts[1], parts[2], parts[3]
    try:
        rating = float(parts[4])
    except:
        rating = None
    text = parts[5].strip('"') if len(parts) > 5 else ""
    return (rid, pid, uid, date, rating, text)

reviews_rdd = rev_rdd.map(parse_review)

# Load products
prod_rdd = sc.textFile("/work/products.txt")
prod_header = prod_rdd.first()
prod_rdd = prod_rdd.filter(lambda x: x != prod_header)
products_rdd = prod_rdd.map(lambda x: x.split(","))
valid_pids = set(products_rdd.map(lambda x: x[0]).collect())

# Filter
clean = reviews_rdd.filter(lambda x: x[4] is not None and x[4] >= 1.0 and x[1] in valid_pids)

# Q2: Avg by product → (pid, (rating, 1)) → reduceByKey → divide
avg_rdd = clean.map(lambda x: (x[1], (x[4], 1))) \
    .reduceByKey(lambda a, b: (a[0]+b[0], a[1]+b[1])) \
    .mapValues(lambda x: x[0]/x[1])
print("Avg by product:", avg_rdd.collect())

# Q3: Top 5 most reviewed
count_rdd = clean.map(lambda x: (x[1], 1)).reduceByKey(lambda a, b: a+b)
top5 = count_rdd.sortBy(lambda x: x[1], ascending=False).take(5)
print("Top 5:", top5)

# Q6: Sentiment
keywords = ["great", "excellent", "recommended"]
def is_positive(text):
    t = text.lower()
    return any(k in t for k in keywords)

sent = clean.map(lambda x: (x[1], (1 if is_positive(x[5]) else 0, 1))) \
    .reduceByKey(lambda a, b: (a[0]+b[0], a[1]+b[1])) \
    .mapValues(lambda x: (x[0]/x[1]) * 100)
print("Sentiment:", sent.collect())
```

---

## ❓ Viva Questions & Answers (PYQ-2 Specific)

**Q: What types of JOINs does Spark support?**
A: inner, left (left_outer), right (right_outer), outer (full_outer), cross, left_semi, left_anti. Inner keeps only matching rows from both sides.

**Q: Why use inner join to filter valid products?**
A: An inner join only keeps rows where the key exists in both DataFrames. So if a review has product_id P999 but Products doesn't have P999, that review is automatically dropped.

**Q: What is `rlike()` vs `like()`?**
A: `like()` uses SQL wildcard patterns (`%` = any chars, `_` = one char). `rlike()` uses full regex patterns (`.*` = any chars, `.` = one char, `|` = OR). For matching multiple keywords, `rlike("word1|word2")` is much cleaner.

**Q: What does `lower()` do and why use it?**
A: Converts text to lowercase. "Great" and "great" and "GREAT" all become "great". This ensures case-insensitive matching so we don't miss any positive reviews.

**Q: What is `when().otherwise()`?**
A: Spark's equivalent of IF-ELSE. `when(condition, value_if_true).otherwise(value_if_false)`. You can chain multiple: `when(c1, v1).when(c2, v2).otherwise(v3)`.

**Q: How does the sentiment percentage formula work?**
A: `sum("is_positive") / count("*") * 100`. is_positive is 1 or 0. Sum gives total positive count. Divide by total count. Multiply by 100 for percentage.

**Q: What does `withColumn()` do?**
A: Adds a new column (or replaces an existing one) to the DataFrame. `df.withColumn("new_col", expression)` returns a new DataFrame with the added column.

**Q: What's the difference between `select()` and `withColumn()`?**
A: `select()` picks specific columns (like SQL SELECT). `withColumn()` adds/replaces ONE column while keeping all others.

**Q: Why `split(",", 5)` with max splits for review text?**
A: The review_text field might contain commas (e.g., "Great product, very useful!"). Using `split(",", 5)` limits to 5 splits so the text stays intact as one field. This is only relevant for RDD parsing — DataFrames handle quoted CSV fields automatically.

---

## 🔑 Key Patterns Summary

### PYQ-1 Pattern (Single Dataset):
```
load → filter → groupBy → agg → show
```

### PYQ-2 New Patterns (Two Datasets):
```
load both → filter → JOIN → groupBy → agg → show
                   ↑ NEW        
                   
load → filter → withColumn(when/rlike) → groupBy → agg(percentage) → show
                ↑ NEW: text analysis
```

### The JOIN + Aggregate Pattern (Q5):
When you need to aggregate by a column that's in a DIFFERENT table:
```python
df1.join(df2, "common_key", "inner").groupBy("col_from_df2").agg(...)
```

### The Sentiment Pattern (Q6):
```python
df.withColumn("flag", when(lower(col("text")).rlike("word1|word2"), 1).otherwise(0)) \
  .groupBy("group_col") \
  .agg((sum("flag") / count("*") * 100).alias("percentage"))
```

---

## 🔄 Variations to Expect

If you see **two datasets** in the exam, expect:
- A JOIN question (combine them)
- An aggregation that requires joining first (groupBy a column from the other table)
- Some form of text analysis (keyword matching, word count, sentiment)

Possible keyword variations for sentiment:
```python
# Positive
.rlike("great|excellent|recommended|amazing|fantastic|love|outstanding|perfect")
# Negative
.rlike("terrible|poor|bad|worst|awful|hate|horrible|waste")
```

---

## ⚡ Common Mistakes for PYQ-2

1. **Forgetting to JOIN before grouping by category** — product_category is in Products, not Reviews. You MUST join first.
2. **Not handling commas in review text** — DataFrame with `spark.read.csv()` handles quoted fields automatically. RDD `split(",")` does NOT.
3. **Case sensitivity in sentiment** — Always use `lower()` before `rlike()`. "Great" won't match "great" otherwise.
4. **Using `contains()` for multiple keywords** — `contains("great")` only checks one word. Use `rlike("great|excellent|recommended")` for multiple.
5. **Forgetting `truncate=False`** — review text gets cut off at 20 chars by default. Use `df.show(truncate=False)` to see full text.
