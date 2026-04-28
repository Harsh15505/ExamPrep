# 🚀 BDA Lab Exam — Complete Setup & Jupyter Guide

> **Exam Stack:** Docker → Apache Spark 3.5.1 → PySpark → Jupyter Notebook  
> **Rules:** Only Jupyter Notebook. No internet (-20 marks). No external IDEs. No assistance.  
> **Duration:** 30 min planning + 1 hour coding

---

# Part 1 — Setup (Do This BEFORE Exam Day)

---

## Phase 1 — Verify Docker Installation

### Step 1: Check Docker is Running

Open **PowerShell** and run:

```powershell
docker --version
docker info
```

✅ You should see Docker version info and the daemon status.

> ⚠️ If `docker` is not recognized, download and install **Docker Desktop** from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/).  
> After installation, **restart your PC** and ensure Docker Desktop is running (whale icon in system tray).

### Step 2: Verify Docker Works

```powershell
docker run hello-world
```

✅ You should see `"Hello from Docker!"`.

---

## Phase 2 — Pull & Save the Spark Image

### Step 3: Pull the Official Spark Image

```powershell
docker pull apache/spark:3.5.1
```

### Step 4: Verify the Image Exists

```powershell
docker images
```

✅ You should see `apache/spark` with tag `3.5.1`.

### Step 5: Save Image as Backup (Optional)

```powershell
docker save -o spark.tar apache/spark:3.5.1
```

To reload later: `docker load -i spark.tar`

---

## Phase 3 — Build Custom Image (With All Libraries + Jupyter)

### Step 6: Create a Project Folder

```powershell
mkdir D:\BDA-Exam
cd D:\BDA-Exam
```

### Step 7: Create the Dockerfile

Create a file named `Dockerfile` (no extension) with this exact content:

```dockerfile
FROM apache/spark:3.5.1

USER root

RUN pip install --no-cache-dir \
    numpy \
    pandas \
    matplotlib \
    seaborn \
    networkx \
    jupyter \
    findspark

ENV SPARK_HOME=/opt/spark
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3
ENV PATH="${SPARK_HOME}/bin:${PATH}"

RUN mkdir -p /work && chmod 777 /work
WORKDIR /work
EXPOSE 8888

USER root
```

> ⚠️ **IMPORTANT:** The file must be named exactly `Dockerfile` — no `.txt`, no `.docker`.

### Step 8: Build the Custom Image

```powershell
cd D:\BDA-Exam
docker build -t spark-bda .
```

Wait for the build to complete (~1-2 minutes).

### Step 9: Verify

```powershell
docker images | findstr spark-bda
```

✅ You should see `spark-bda` with tag `latest`.

---

## Phase 4 — Test Everything

### Step 10: Launch Jupyter

```powershell
docker run -d --name bda-test -p 8888:8888 -v "D:\BDA-Exam:/work" spark-bda jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token="" --NotebookApp.password=""
```

### Step 11: Open Browser

Go to **http://localhost:8888** — Jupyter should open directly (no password).

### Step 12: Test in Notebook

Click **New → Python 3 (ipykernel)** and paste this in the first cell:

```python
import findspark
findspark.init()
from pyspark.sql import SparkSession
import numpy as np, pandas as pd, matplotlib, seaborn as sns, networkx as nx

spark = SparkSession.builder.appName("Test").master("local[*]").getOrCreate()
rdd = spark.sparkContext.parallelize([1,2,3,4,5])
print("RDD Sum:", rdd.reduce(lambda a,b: a+b))
print("NumPy:", np.__version__)
print("Pandas:", pd.__version__)
print("Spark:", spark.version)
print("✅ ALL OK!")
```

Press **Shift+Enter** to run. You should see `✅ ALL OK!`

### Step 13: Cleanup Test

```powershell
docker stop bda-test
docker rm bda-test
```

---

## Phase 5 — Save Backup Image

```powershell
docker save -o spark-bda.tar spark-bda
```

> 💡 **Keep this file!** If Docker resets overnight:  
> `docker load -i spark-bda.tar`

---

## ⚠️ Pre-Exam Night Checklist

| # | Task | ✓ |
|---|------|---|
| 1 | Docker Desktop installed and running | ☐ |
| 2 | `docker images` shows `spark-bda` | ☐ |
| 3 | Jupyter opens at `localhost:8888` | ☐ |
| 4 | PySpark + all 5 libraries work in notebook | ☐ |
| 5 | `spark-bda.tar` backup saved on disk | ☐ |
| 6 | Know where to put CSV/data files (`D:\BDA-Exam\`) | ☐ |

---

# Part 2 — Exam Day Guide

---

## 🟢 Launch Command (Copy-Paste This on Exam Day)

```powershell
docker run -d --name bda-exam -p 8888:8888 -v "D:\BDA-Exam:/work" spark-bda jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token="" --NotebookApp.password=""
```

Then open: **http://localhost:8888**

> 💡 Change `D:\BDA-Exam` to wherever your work folder is.  
> Any file you put in that Windows folder appears at `/work/` inside Jupyter.

---

## 🟢 First Cell (ALWAYS Paste This First in Every Notebook)

```python
# === SPARK INITIALIZATION ===
import findspark
findspark.init()

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("BDA-Exam") \
    .master("local[*]") \
    .getOrCreate()

sc = spark.sparkContext

# Common imports
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

from pyspark.sql import Row
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.ml.feature import VectorAssembler, StringIndexer, StandardScaler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, RandomForestClassifier
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import RegressionEvaluator, MulticlassClassificationEvaluator, BinaryClassificationEvaluator
from pyspark.ml import Pipeline

print("✅ Spark Ready! Version:", spark.version)
```

> ⚠️ Run this cell FIRST and wait for `✅ Spark Ready!` before doing anything else (~5-10 seconds).

---

## 📋 Quick Reference — All Patterns You'll Need

---

### 📁 Loading Data

```python
# CSV
df = spark.read.csv("/work/data.csv", header=True, inferSchema=True)

# JSON
df = spark.read.json("/work/data.json")

# Quick look
df.show()
df.printSchema()
df.describe().show()
print(f"Rows: {df.count()}, Columns: {len(df.columns)}")
```

---

### 🔧 RDD Operations

```python
# Create
rdd = sc.parallelize([1, 2, 3, 4, 5])
rdd = sc.textFile("/work/data.txt")

# Transformations
rdd.map(lambda x: x * 2).collect()
rdd.filter(lambda x: x > 3).collect()
rdd.flatMap(lambda x: x.split(" ")).collect()
rdd.reduceByKey(lambda a, b: a + b).collect()
rdd.sortByKey().collect()
rdd.distinct().collect()
rdd.union(other_rdd).collect()

# Actions
rdd.collect()                       # All elements
rdd.count()                         # Count
rdd.first()                         # First element
rdd.take(5)                         # First 5
rdd.reduce(lambda a, b: a + b)     # Aggregate
rdd.foreach(lambda x: print(x))    # Print each

# ⭐ Word Count (Classic Exam Question)
text_rdd = sc.textFile("/work/text.txt")
word_counts = text_rdd \
    .flatMap(lambda line: line.split(" ")) \
    .map(lambda word: (word.lower(), 1)) \
    .reduceByKey(lambda a, b: a + b) \
    .sortBy(lambda x: x[1], ascending=False)
word_counts.collect()
```

---

### 🗃️ Spark SQL

```python
# Register as table
df.createOrReplaceTempView("data")

# SQL queries
result = spark.sql("""
    SELECT column1, AVG(column2) as avg_val, COUNT(*) as cnt
    FROM data
    WHERE column3 > 100
    GROUP BY column1
    ORDER BY avg_val DESC
""")
result.show()

# DataFrame API (same thing)
df.select("col1", "col2") \
  .filter(col("col3") > 100) \
  .groupBy("col1") \
  .agg(avg("col2").alias("avg_val"), count("*").alias("cnt")) \
  .orderBy(desc("avg_val")) \
  .show()

# Joins
df1.join(df2, df1["id"] == df2["id"], "inner").show()
# Types: "inner", "left", "right", "outer"

# Window Functions
from pyspark.sql.window import Window
w = Window.partitionBy("dept").orderBy(desc("salary"))
df.withColumn("rank", row_number().over(w)).show()
```

---

### 🤖 Machine Learning

```python
# 1. Handle string columns
indexer = StringIndexer(inputCol="category", outputCol="category_idx")

# 2. Assemble features
assembler = VectorAssembler(
    inputCols=["feature1", "feature2", "category_idx"],
    outputCol="features"
)

# 3. Split data
train, test = df.randomSplit([0.8, 0.2], seed=42)

# 4. Choose model
# --- Regression ---
model = LinearRegression(featuresCol="features", labelCol="target")
# --- Classification ---
model = LogisticRegression(featuresCol="features", labelCol="label")
model = DecisionTreeClassifier(featuresCol="features", labelCol="label")
model = RandomForestClassifier(featuresCol="features", labelCol="label")
# --- Clustering ---
model = KMeans(featuresCol="features", k=3)

# 5. Build & run pipeline
pipeline = Pipeline(stages=[indexer, assembler, model])
fitted = pipeline.fit(train)
predictions = fitted.transform(test)
predictions.select("features", "label", "prediction").show()

# 6. Evaluate
# Regression
evaluator = RegressionEvaluator(labelCol="target", metricName="rmse")
print("RMSE:", evaluator.evaluate(predictions))
evaluator2 = RegressionEvaluator(labelCol="target", metricName="r2")
print("R²:", evaluator2.evaluate(predictions))

# Classification
evaluator = MulticlassClassificationEvaluator(labelCol="label", metricName="accuracy")
print("Accuracy:", evaluator.evaluate(predictions))
```

---

### 🔀 Data Engineering Pipeline

```python
# Read → Clean → Transform → Aggregate → Write

# 1. Read
raw_df = spark.read.csv("/work/raw_data.csv", header=True, inferSchema=True)

# 2. Clean
clean_df = raw_df.dropna()                             # Remove nulls
clean_df = clean_df.dropDuplicates()                    # Remove duplicates
clean_df = clean_df.withColumn("amount", col("amount").cast("double"))
clean_df = clean_df.fillna({"column": 0})               # Fill specific nulls

# 3. Transform
transformed_df = clean_df \
    .withColumn("year", year(col("date"))) \
    .withColumn("month", month(col("date"))) \
    .withColumn("amount_norm", col("amount") / 1000) \
    .withColumnRenamed("old_name", "new_name")

# 4. Aggregate
agg_df = transformed_df.groupBy("year", "month").agg(
    sum("amount").alias("total"),
    avg("amount").alias("average"),
    count("*").alias("transactions"),
    max("amount").alias("max_amount")
)

# 5. Write
agg_df.write.mode("overwrite").csv("/work/output", header=True)
agg_df.write.mode("overwrite").parquet("/work/output.parquet")

agg_df.show()
```

---

### 🕸️ NetworkX — Graph Processing

```python
# Create graph
G = nx.Graph()
G.add_edges_from([(1,2), (2,3), (3,4), (4,1), (1,3)])

# From DataFrame
edges = [(row.src, row.dst) for row in df.select("src", "dst").collect()]
G = nx.from_edgelist(edges)

# Analysis
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print("Degree:", dict(G.degree()))
print("Density:", nx.density(G))
print("Connected:", nx.is_connected(G))
print("Clustering Coeff:", nx.average_clustering(G))
print("Shortest Path:", nx.shortest_path(G, source=1, target=4))
print("Diameter:", nx.diameter(G))
print("PageRank:", nx.pagerank(G))
print("Betweenness:", nx.betweenness_centrality(G))
print("Degree Centrality:", nx.degree_centrality(G))

# Directed Graph
DG = nx.DiGraph()
DG.add_edges_from([(1,2), (2,3), (3,1)])
print("In-Degree:", dict(DG.in_degree()))
print("Out-Degree:", dict(DG.out_degree()))

# Visualize
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue',
        node_size=700, font_size=12, edge_color='gray', width=2)
plt.title("Graph Visualization")
plt.savefig("/work/graph.png", dpi=150, bbox_inches='tight')
plt.show()
```

---

### 📊 Plotting (Matplotlib + Seaborn)

```python
# Convert Spark DataFrame to Pandas for plotting
pdf = df.toPandas()

# Bar Chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(pdf["category"], pdf["value"], color='steelblue')
ax.set_title("Bar Chart")
ax.set_xlabel("Category")
ax.set_ylabel("Value")
plt.tight_layout()
plt.savefig("/work/bar_chart.png", dpi=150, bbox_inches='tight')
plt.show()

# Line Chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(pdf["x"], pdf["y"], marker='o')
ax.set_title("Line Chart")
plt.savefig("/work/line_chart.png", dpi=150, bbox_inches='tight')
plt.show()

# Scatter Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(pdf["x"], pdf["y"], c='coral', alpha=0.7)
plt.savefig("/work/scatter.png", dpi=150, bbox_inches='tight')
plt.show()

# Seaborn Heatmap (Correlation)
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(pdf.corr(), annot=True, cmap='coolwarm', ax=ax, fmt='.2f')
plt.savefig("/work/heatmap.png", dpi=150, bbox_inches='tight')
plt.show()

# Seaborn Distribution
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(pdf["column"], kde=True, ax=ax)
plt.savefig("/work/distribution.png", dpi=150, bbox_inches='tight')
plt.show()

# Seaborn Pairplot
sns.pairplot(pdf[["col1", "col2", "col3", "label"]], hue="label")
plt.savefig("/work/pairplot.png", dpi=150, bbox_inches='tight')
plt.show()
```

> 💡 Always use `plt.savefig("/work/filename.png")` — plots are saved to your Windows folder too.

---

## ⌨️ Jupyter Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Shift + Enter` | Run cell, move to next |
| `Ctrl + Enter` | Run cell, stay |
| `B` (command mode) | Insert cell below |
| `A` (command mode) | Insert cell above |
| `DD` (command mode) | Delete cell |
| `M` (command mode) | Convert to Markdown |
| `Y` (command mode) | Convert to Code |
| `Esc` | Enter command mode |
| `Enter` | Enter edit mode |
| `Ctrl + S` | Save notebook |
| `Ctrl + Z` | Undo (edit mode) |
| `Z` (command mode) | Undo delete cell |

> 💡 Press `Esc` first to enter command mode, then use shortcuts.

---

## 🔄 Container Management (Troubleshooting)

```powershell
# Name conflict error? Remove old container:
docker rm bda-exam

# Restart a stopped container:
docker start bda-exam

# Check running containers:
docker ps

# View logs:
docker logs bda-exam

# Stop container:
docker stop bda-exam

# Port 8888 already in use?
docker ps                       # find what's using it
docker stop <container_name>    # stop it
```

---

## 🆘 Emergency Recovery

```powershell
# If images are gone after restart:
docker load -i spark-bda.tar

# Then launch normally:
docker run -d --name bda-exam -p 8888:8888 -v "D:\BDA-Exam:/work" spark-bda jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token="" --NotebookApp.password=""
```

---

## ⚠️ Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| `docker: command not found` | Install Docker Desktop, restart PC |
| `docker daemon is not running` | Open Docker Desktop app, wait for green status |
| Name conflict on `docker run` | `docker rm bda-exam` then re-run |
| Port 8888 in use | `docker stop <old_container>` or use `-p 9999:8888` and open `localhost:9999` |
| Image not found after restart | `docker load -i spark-bda.tar` |
| `matplotlib` display errors | Use `matplotlib.use('Agg')` + `plt.savefig()` |
| Can't see files in Jupyter | Check your `-v` mount path matches your folder |
| Kernel dies / out of memory | Restart kernel: Kernel menu → Restart |
| `findspark` not found | Run init cell first, ensure image was built with Dockerfile above |

---

## 📂 File Access Mapping

```
Windows:    D:\BDA-Exam\data.csv
Jupyter:    /work/data.csv

Windows:    D:\BDA-Exam\output\
Jupyter:    /work/output/
```

Put exam data files in your BDA-Exam folder → Access them as `/work/filename` in notebooks.

---

> ⚠️ **FINAL REMINDER:**  
> 1. Open Docker Desktop BEFORE the exam  
> 2. Run the launch command  
> 3. Open `http://localhost:8888`  
> 4. Create notebook → Paste init cell → Wait for `✅ Spark Ready!`  
> 5. **DISCONNECT INTERNET** before exam starts  
>  
> **Good luck! 🎯**
