# 🔥 BDA Exam — Ultimate Cheat Sheet

> Copy this file to your BDA-Exam folder. Open in Notepad during the exam for instant reference.

---

## ⚡ INIT CELL (Paste First in Every Notebook)

```python
import findspark
findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("BDA-Exam").master("local[*]").getOrCreate()
sc = spark.sparkContext
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import Row
print("✅ Ready!", spark.version)
```

---

## 1️⃣ LOADING DATA

### From CSV File
```python
df = spark.read.csv("/work/data.csv", header=True, inferSchema=True)
```
| Param | Why |
|-------|-----|
| `header=True` | First row = column names |
| `inferSchema=True` | Auto-detect types (int, double, string) |

### From Inline Data (No File)
```python
data = [
    (1, "Alice", 100, "2024-01-01"),
    (2, "Bob", 200, "2024-01-02"),
]
schema = ["id", "name", "amount", "date"]
df = spark.createDataFrame(data, schema)
```

### From RDD
```python
rdd = sc.textFile("/work/data.txt")
header = rdd.first()
rdd = rdd.filter(lambda line: line != header).map(lambda line: line.split(","))
df = rdd.map(lambda x: (int(x[0]), x[1].strip(), float(x[2]))).toDF(["id","name","amount"])
```

### Show Data
```python
df.show()                    # default 20 rows
df.show(truncate=False)      # full text (don't cut)
df.printSchema()             # column names + types
df.describe().show()         # stats (count, mean, stddev, min, max)
df.count()                   # total rows
```

---

## 2️⃣ FILTERING

```python
# Basic filters
df.filter(col("amount") > 0)                        # positive only
df.filter(col("amount").isNotNull())                 # remove nulls
df.filter(col("city") == "Chicago")                  # exact match
df.filter(col("date") > "2024-01-06")                # after a date

# Combine with & (AND) and | (OR) — PARENTHESES REQUIRED
df.filter((col("amount").isNotNull()) & (col("amount") > 0))
df.filter((col("city") == "A") | (col("city") == "B"))

# String matching
df.filter(lower(col("text")).rlike("great|excellent|recommended"))
df.filter(col("name").contains("Ali"))
df.filter(col("name").startswith("A"))
```

---

## 3️⃣ GROUPBY + AGGREGATION (Most Common Pattern)

```python
# Template:
df.groupBy("GROUP_COL").agg(FUNCTION("VALUE_COL").alias("OUTPUT_NAME")).show()
```

### All Aggregation Functions
| Function | Purpose | Example |
|----------|---------|---------|
| `sum("col")` | Total | `agg(sum("amount").alias("total"))` |
| `avg("col")` | Average | `agg(avg("amount").alias("average"))` |
| `count("*")` | Count all rows | `agg(count("*").alias("cnt"))` |
| `count("col")` | Count non-null | `agg(count("col").alias("cnt"))` |
| `max("col")` | Maximum | `agg(max("amount").alias("max_val"))` |
| `min("col")` | Minimum | `agg(min("amount").alias("min_val"))` |

### Multiple Aggregations
```python
df.groupBy("city").agg(
    sum("amount").alias("total"),
    avg("amount").alias("average"),
    count("*").alias("transactions")
).show()
```

### Sort + Limit (Top N)
```python
df.groupBy("city").agg(sum("amount").alias("total")) \
    .orderBy(desc("total")) \
    .limit(3) \
    .show()
```

### GroupBy Multiple Columns
```python
df.groupBy("col1", "col2").count().orderBy("col1", "col2").show()
```

---

## 4️⃣ JOINS (Two DataFrames)

```python
# Inner join (most common — keeps only matching rows)
result = df1.join(df2, "common_column", "inner")

# Other join types
result = df1.join(df2, "common_column", "left")     # all from left
result = df1.join(df2, "common_column", "right")    # all from right
result = df1.join(df2, "common_column", "outer")    # all from both

# Join then aggregate (when you need a column from the other table)
reviews.join(products, "product_id", "inner") \
    .groupBy("product_category") \
    .agg(avg("rating").alias("avg_rating")) \
    .show()
```

### Use JOIN to Filter Valid IDs
```python
valid_ids = products.select("product_id")
clean = reviews.join(valid_ids, "product_id", "inner")
# Drops any review with a product_id NOT in the products table
```

---

## 5️⃣ COLUMN OPERATIONS

```python
# Add new column
df.withColumn("doubled", col("amount") * 2)
df.withColumn("year", year(col("date")))
df.withColumn("month", month(col("date")))

# Rename column
df.withColumnRenamed("old_name", "new_name")

# Select specific columns
df.select("col1", "col2", "col3")

# Drop column
df.drop("unwanted_col")

# Cast type
df.withColumn("amount", col("amount").cast("double"))

# IF-ELSE (when/otherwise)
df.withColumn("flag",
    when(col("amount") > 100, "High")
    .when(col("amount") > 50, "Medium")
    .otherwise("Low")
)

# Sentiment flag (binary)
df.withColumn("is_positive",
    when(lower(col("text")).rlike("great|excellent|recommended"), 1).otherwise(0)
)
```

### Date Functions
| Function | Returns | Example |
|----------|---------|---------|
| `year(col("date"))` | 2024 | Extract year |
| `month(col("date"))` | 1-12 | Extract month |
| `dayofmonth(col("date"))` | 1-31 | Extract day |
| `current_date()` | today | Current date |

---

## 6️⃣ SPARK SQL

### Setup
```python
df.createOrReplaceTempView("tablename")
result = spark.sql("SELECT * FROM tablename")
result.show()
```

### All Patterns You'll Need
```sql
-- Basic aggregation
SELECT city, SUM(amount) AS total FROM orders GROUP BY city

-- Top N
SELECT city, SUM(amount) AS total FROM orders GROUP BY city ORDER BY total DESC LIMIT 3

-- Filter
SELECT * FROM orders WHERE order_date > '2024-01-06'
SELECT * FROM orders WHERE city = 'Chicago'
SELECT * FROM orders WHERE YEAR(order_date) = 2024

-- Filter + Aggregate
SELECT city, SUM(amount) AS total FROM orders WHERE order_date > '2024-01-06' GROUP BY city

-- Average by category
SELECT product_category, AVG(amount) AS avg_amount FROM orders WHERE product_category = 'Electronics'

-- Date grouping
SELECT MONTH(order_date) AS month, AVG(amount) AS avg FROM orders GROUP BY MONTH(order_date)

-- JOIN
SELECT p.product_name, r.rating
FROM reviews r INNER JOIN products p ON r.product_id = p.product_id

-- Subquery (aggregate of aggregate)
SELECT city, AVG(customer_total) AS avg_spending
FROM (
    SELECT city, customer_id, SUM(amount) AS customer_total
    FROM orders GROUP BY city, customer_id
)
GROUP BY city

-- Max single row
SELECT * FROM orders ORDER BY amount DESC LIMIT 1

-- Sentiment (CASE WHEN)
SELECT product_id,
    SUM(CASE WHEN LOWER(review_text) RLIKE 'great|excellent' THEN 1 ELSE 0 END) / COUNT(*) * 100
    AS positive_pct
FROM reviews GROUP BY product_id
```

---

## 7️⃣ RDD OPERATIONS

```python
# Create
rdd = sc.parallelize([1, 2, 3, 4, 5])
rdd = sc.textFile("/work/data.txt")

# Transformations (lazy — don't execute until action)
rdd.map(lambda x: x * 2)                              # transform each element
rdd.filter(lambda x: x > 3)                           # keep matching
rdd.flatMap(lambda x: x.split(" "))                    # split + flatten
rdd.reduceByKey(lambda a, b: a + b)                    # sum by key
rdd.sortByKey()                                        # sort
rdd.distinct()                                         # unique values

# Actions (trigger execution)
rdd.collect()                  # return all as list
rdd.count()                    # count elements
rdd.first()                    # first element
rdd.take(5)                    # first 5
rdd.reduce(lambda a, b: a+b)  # aggregate all

# Word Count (classic)
sc.textFile("/work/text.txt") \
    .flatMap(lambda line: line.split(" ")) \
    .map(lambda word: (word.lower(), 1)) \
    .reduceByKey(lambda a, b: a + b) \
    .sortBy(lambda x: x[1], ascending=False) \
    .collect()

# RDD Aggregations
# Total by key:  map to (key, value) → reduceByKey(+)
# Avg by key:    map to (key, (value, 1)) → reduceByKey → mapValues(sum/count)
rdd.map(lambda x: (x[1], (x[2], 1))) \
    .reduceByKey(lambda a, b: (a[0]+b[0], a[1]+b[1])) \
    .mapValues(lambda x: x[0]/x[1]).collect()
```

---

## 8️⃣ ML PIPELINE

### Step 1: VectorAssembler
```python
from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(
    inputCols=["feat1", "feat2", "feat3"],   # all feature columns
    outputCol="features"                      # output vector
)
df = assembler.transform(df)
```

### Step 2: Feature Selection (Correlation)
```python
for c in feature_cols:
    print(f"{c}: {df.stat.corr(c, 'label'):.4f}")
# Keep features with |correlation| > 0.1
```

### Step 3: Prepare + Split
```python
model_df = df.select("features", col("target").alias("label"))
train, test = model_df.randomSplit([0.8, 0.2], seed=42)
```

### Step 4: Train (Pick ONE)
```python
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, RandomForestClassifier
from pyspark.ml.regression import LinearRegression
from pyspark.ml.clustering import KMeans

# Classification (predict category: 0/1, A/B/C)
model = LogisticRegression(featuresCol="features", labelCol="label")
model = DecisionTreeClassifier(featuresCol="features", labelCol="label")
model = RandomForestClassifier(featuresCol="features", labelCol="label", numTrees=10)

# Regression (predict number: price, salary)
model = LinearRegression(featuresCol="features", labelCol="label")

# Clustering (find groups, no label needed)
model = KMeans(featuresCol="features", k=3)

fitted = model.fit(train)
predictions = fitted.transform(test)
predictions.select("features", "label", "prediction").show()
```

### Step 5: Evaluate
```python
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, RegressionEvaluator

# Classification metrics
for m in ["accuracy", "weightedPrecision", "weightedRecall", "f1"]:
    e = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName=m)
    print(f"{m}: {e.evaluate(predictions):.4f}")

# Regression metrics
for m in ["rmse", "r2", "mae"]:
    e = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName=m)
    print(f"{m}: {e.evaluate(predictions):.4f}")
```

### StringIndexer (If You Have String Labels/Features)
```python
from pyspark.ml.feature import StringIndexer
indexer = StringIndexer(inputCol="category_string", outputCol="category_num")
df = indexer.fit(df).transform(df)
# Now use "category_num" in VectorAssembler instead
```

### Pipeline (All Steps Combined)
```python
from pyspark.ml import Pipeline
pipeline = Pipeline(stages=[indexer, assembler, model])
fitted = pipeline.fit(train)
predictions = fitted.transform(test)
```

---

## 9️⃣ PLOTTING (matplotlib + seaborn)

```python
import matplotlib
matplotlib.use('Agg')       # REQUIRED in Docker (no display)
import matplotlib.pyplot as plt
import seaborn as sns
```

### Convert Spark → Pandas for Plotting
```python
pdf = df.toPandas()
```

### Charts
```python
# Bar Chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(pdf["category"], pdf["value"], color='steelblue')
ax.set_title("Title"); ax.set_xlabel("X"); ax.set_ylabel("Y")
plt.tight_layout(); plt.savefig("/work/bar.png"); plt.show()

# Line Chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(pdf["x"], pdf["y"], marker='o')
plt.savefig("/work/line.png"); plt.show()

# Scatter Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(pdf["x"], pdf["y"], c='coral', alpha=0.7)
plt.savefig("/work/scatter.png"); plt.show()

# Histogram
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(pdf["values"], bins=20, color='skyblue', edgecolor='black')
plt.savefig("/work/hist.png"); plt.show()

# Heatmap (Correlation Matrix)
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(pdf.corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
plt.savefig("/work/heatmap.png"); plt.show()

# Distribution Plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(pdf["column"], kde=True, ax=ax)
plt.savefig("/work/dist.png"); plt.show()

# Pairplot
sns.pairplot(pdf[["col1", "col2", "label"]], hue="label")
plt.savefig("/work/pairplot.png"); plt.show()

# Boxplot
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x="category", y="value", data=pdf, ax=ax)
plt.savefig("/work/boxplot.png"); plt.show()
```

> ⚠️ ALWAYS use `plt.savefig("/work/file.png")` — images appear in your Windows folder AND in Jupyter file browser.

---

## 🔟 NETWORKX (Graph Processing)

```python
import networkx as nx

# Create graph
G = nx.Graph()                                    # Undirected
G = nx.DiGraph()                                  # Directed
G.add_edges_from([(1,2), (2,3), (3,4), (4,1)])

# From DataFrame
edges = [(row.src, row.dst) for row in df.select("src", "dst").collect()]
G = nx.from_edgelist(edges)

# Analysis
G.number_of_nodes()                # total nodes
G.number_of_edges()                # total edges
dict(G.degree())                   # degree of each node
nx.density(G)                      # edge density (0 to 1)
nx.is_connected(G)                 # is fully connected?
nx.shortest_path(G, 1, 4)          # shortest path between nodes
nx.diameter(G)                     # longest shortest path
nx.average_clustering(G)           # clustering coefficient
nx.pagerank(G)                     # PageRank scores
nx.betweenness_centrality(G)       # betweenness centrality
nx.degree_centrality(G)            # degree centrality
nx.closeness_centrality(G)         # closeness centrality

# Directed graph extras
dict(G.in_degree())                # incoming edges
dict(G.out_degree())               # outgoing edges

# Visualize
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue',
        node_size=700, font_size=12, edge_color='gray', width=2)
plt.title("Graph")
plt.savefig("/work/graph.png"); plt.show()
```

---

## 📐 DATA ENGINEERING PIPELINE

```python
# Read
raw = spark.read.csv("/work/data.csv", header=True, inferSchema=True)

# Clean
clean = raw.dropna()                                    # remove null rows
clean = clean.dropDuplicates()                           # remove duplicates
clean = clean.filter(col("amount") > 0)                  # remove invalid
clean = clean.fillna({"col": 0})                         # fill nulls with value
clean = clean.withColumn("amount", col("amount").cast("double"))

# Transform
trans = clean \
    .withColumn("year", year(col("date"))) \
    .withColumn("month", month(col("date"))) \
    .withColumnRenamed("old", "new")

# Aggregate
agg = trans.groupBy("year").agg(
    sum("amount").alias("total"),
    avg("amount").alias("average"),
    count("*").alias("count")
)

# Write
agg.write.mode("overwrite").csv("/work/output", header=True)
agg.write.mode("overwrite").parquet("/work/output.parquet")
```

---

## 🧩 EXAM PATTERN MAP

Based on all 5 PYQs, every exam question is a combination of these blocks:

```
┌──────────────┐
│  LOAD DATA   │  spark.read.csv() OR spark.createDataFrame()
└──────┬───────┘
       │
┌──────▼───────┐
│  FILTER/CLEAN│  .filter(isNotNull & > 0) OR .join(valid_ids)
└──────┬───────┘
       │
┌──────▼───────┐
│  GROUPBY+AGG │  .groupBy("X").agg(sum/avg/count("Y").alias("Z"))
└──────┬───────┘
       │
┌──────▼───────┐
│  SORT+LIMIT  │  .orderBy(desc("Z")).limit(N)
└──────┬───────┘
       │
┌──────▼───────┐
│    SHOW      │  .show()
└──────────────┘

Optional additions:
  + JOIN         → two datasets
  + SQL          → createOrReplaceTempView + spark.sql()
  + ML           → VectorAssembler → fit → predict → evaluate
  + PLOT         → toPandas → plt/sns → savefig
  + GRAPH        → nx.Graph → analysis → draw
  + SENTIMENT    → withColumn + when(rlike) → groupBy percentage
```
