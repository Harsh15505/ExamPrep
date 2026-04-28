# 🚀 BDA Lab Exam — Complete Setup Guide

> **Exam Date:** Tomorrow (29 April 2026)  
> **Stack:** Docker → Apache Spark 3.5.1 → PySpark + Python Libraries  
> **Goal:** A fully offline, self-contained environment ready for the exam

---

## Phase 1 — Verify Docker Installation

### Step 1: Check Docker is Running

Open **PowerShell** (or Terminal) and run:

```powershell
docker --version
docker info
```

✅ You should see Docker version info and the daemon status.  

> [!WARNING]
> If `docker` is not recognized, download and install **Docker Desktop** from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/).  
> After installation, **restart your PC** and ensure Docker Desktop is running (whale icon in system tray).

### Step 2: Verify Docker Works

```powershell
docker run hello-world
```

✅ You should see `"Hello from Docker!"`. If yes, Docker is ready.

---

## Phase 2 — Pull & Save the Spark Image

### Step 3: Pull the Official Spark Image

```powershell
docker pull apache/spark:3.5.1
```

This downloads the ~1.5 GB image. Wait for it to complete.

### Step 4: Verify the Image Exists Locally

```powershell
docker images | findstr spark
```

✅ You should see `apache/spark` with tag `3.5.1`.

### Step 5: Save Image to a Backup `.tar` File (Insurance)

```powershell
docker save -o spark.tar apache/spark:3.5.1
```

This creates a `spark.tar` file in your current directory. If anything goes wrong tomorrow, you can reload it:

```powershell
docker load -i spark.tar
```

> [!TIP]
> Keep this `spark.tar` file on your machine. If Docker resets or images get cleared, this is your lifeline.

---

## Phase 3 — Build Your Custom Image (with all libraries)

### Step 6: Create a Project Folder

```powershell
mkdir D:\College\BDA-Exam
cd D:\College\BDA-Exam
```

### Step 7: Create the Dockerfile

Create a file named `Dockerfile` (no extension) in `D:\College\BDA-Exam\` with this content:

```dockerfile
FROM apache/spark:3.5.1

# Switch to root to install packages
USER root

# Install required Python libraries
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    matplotlib \
    seaborn \
    networkx

# Switch back to the default spark user
USER spark
```

> [!IMPORTANT]
> The file must be named exactly `Dockerfile` — no `.txt`, no `.docker`, just `Dockerfile`.

### Step 8: Build the Custom Image

```powershell
cd D:\College\BDA-Exam
docker build -t spark-bda .
```

Wait for the build to complete. You'll see each layer being installed.

### Step 9: Verify the Custom Image

```powershell
docker images | findstr spark-bda
```

✅ You should see `spark-bda` with tag `latest`.

---

## Phase 4 — Test the Container End-to-End

### Step 10: Launch a PySpark Shell

```powershell
docker run -it --name bda-test spark-bda /opt/spark/bin/pyspark
```

You should land in the PySpark interactive shell with the Spark logo.

### Step 11: Verify All Libraries are Importable

Inside the PySpark shell, run each of these:

```python
import numpy as np
print("NumPy:", np.__version__)

import pandas as pd
print("Pandas:", pd.__version__)

import matplotlib
print("Matplotlib:", matplotlib.__version__)

import seaborn as sns
print("Seaborn:", sns.__version__)

import networkx as nx
print("NetworkX:", nx.__version__)

print("\n✅ ALL LIBRARIES OK!")
```

✅ All five should print their versions with no errors.

### Step 12: Verify Spark Core Functionality

Still inside PySpark shell:

```python
# --- RDD Test ---
rdd = sc.parallelize([1, 2, 3, 4, 5])
print("RDD Sum:", rdd.reduce(lambda a, b: a + b))  # Should print 15

# --- Spark SQL Test ---
from pyspark.sql import Row
df = spark.createDataFrame([Row(name="Alice", age=30), Row(name="Bob", age=25)])
df.show()
df.createOrReplaceTempView("people")
spark.sql("SELECT * FROM people WHERE age > 26").show()

# --- ML Test ---
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
print("ML imports OK!")

print("\n✅ SPARK FULLY FUNCTIONAL!")
```

### Step 13: Exit and Clean Up Test Container

```python
exit()
```

Then remove the test container:

```powershell
docker rm bda-test
```

---

## Phase 5 — Save Your Custom Image (Backup)

### Step 14: Save the Custom Image as a Backup

```powershell
docker save -o spark-bda.tar spark-bda
```

This ensures even if Docker resets, you can reload your complete setup:

```powershell
docker load -i spark-bda.tar
```

---

## Phase 6 — Exam Day Quick Reference

### 🟢 Starting the Container

**Option A — Interactive PySpark Shell:**

```powershell
docker run -it --name bda-exam spark-bda /opt/spark/bin/pyspark
```

**Option B — Run a Python Script (mount a folder):**

```powershell
docker run -it --name bda-exam -v D:\College\BDA-Exam:/work spark-bda /opt/spark/bin/spark-submit /work/your_script.py
```

**Option C — Interactive Bash (then launch PySpark manually):**

```powershell
docker run -it --name bda-exam -v D:\College\BDA-Exam:/work spark-bda /bin/bash
```
Then inside the container:
```bash
cd /work
/opt/spark/bin/pyspark
# OR
/opt/spark/bin/spark-submit your_script.py
```

> [!TIP]
> **Option C is the most flexible** — you get a full shell, can navigate your files, and launch PySpark or spark-submit as needed.

### 📂 Mounting Your Work Folder

The `-v D:\College\BDA-Exam:/work` flag maps your local folder to `/work` inside the container. Any files you place in `D:\College\BDA-Exam` will be visible at `/work` inside the container.

### 🔄 If Container Already Exists

```powershell
# List all containers (including stopped)
docker ps -a

# Start a stopped container
docker start -i bda-exam

# Remove a container to create a fresh one
docker rm bda-exam
```

---

## 📋 Exam Day Checklist

| # | Task | Status |
|---|------|--------|
| 1 | Docker Desktop is running (whale icon in tray) | ☐ |
| 2 | `docker images` shows `spark-bda` | ☐ |
| 3 | Container launches successfully | ☐ |
| 4 | PySpark shell opens without errors | ☐ |
| 5 | All 5 libraries import correctly | ☐ |
| 6 | Spark RDD/SQL operations work | ☐ |
| 7 | `spark-bda.tar` backup exists on disk | ☐ |
| 8 | Work folder mounted and accessible | ☐ |

---

## 🧠 Quick PySpark Cheat Sheet

### RDD Operations

```python
# Create RDD
rdd = sc.parallelize([1, 2, 3, 4, 5])
rdd = sc.textFile("/work/data.txt")

# Transformations
rdd.map(lambda x: x * 2)
rdd.filter(lambda x: x > 3)
rdd.flatMap(lambda x: x.split(" "))
rdd.reduceByKey(lambda a, b: a + b)
rdd.sortByKey()
rdd.distinct()
rdd.union(other_rdd)

# Actions
rdd.collect()
rdd.count()
rdd.first()
rdd.take(5)
rdd.reduce(lambda a, b: a + b)
rdd.foreach(lambda x: print(x))
```

### Spark SQL

```python
# Read CSV
df = spark.read.csv("/work/data.csv", header=True, inferSchema=True)

# Basic Operations
df.show()
df.printSchema()
df.select("col1", "col2").show()
df.filter(df["age"] > 25).show()
df.groupBy("dept").count().show()
df.orderBy("salary", ascending=False).show()

# SQL Queries
df.createOrReplaceTempView("table")
result = spark.sql("SELECT * FROM table WHERE age > 25")
result.show()

# Write Output
df.write.csv("/work/output", header=True)
df.write.parquet("/work/output.parquet")
```

### Basic ML (PySpark MLlib)

```python
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.regression import LinearRegression
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier
from pyspark.ml.evaluation import RegressionEvaluator, MulticlassClassificationEvaluator
from pyspark.ml import Pipeline

# Assemble features
assembler = VectorAssembler(inputCols=["col1", "col2"], outputCol="features")
df = assembler.transform(df)

# Train/Test Split
train, test = df.randomSplit([0.8, 0.2], seed=42)

# Linear Regression
lr = LinearRegression(featuresCol="features", labelCol="label")
model = lr.fit(train)
predictions = model.transform(test)

# Evaluate
evaluator = RegressionEvaluator(labelCol="label", metricName="rmse")
print("RMSE:", evaluator.evaluate(predictions))
```

### NetworkX (Graph Processing)

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create a graph
G = nx.Graph()
G.add_edges_from([(1,2), (2,3), (3,4), (4,1), (1,3)])

# Analysis
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print("Degree:", dict(G.degree()))
print("Shortest Path:", nx.shortest_path(G, source=1, target=4))
print("Clustering:", nx.clustering(G))
print("PageRank:", nx.pagerank(G))

# Visualization
nx.draw(G, with_labels=True, node_color='lightblue', node_size=700)
plt.savefig("/work/graph.png")
plt.show()
```

---

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| `docker: command not found` | Install Docker Desktop, restart PC |
| `docker daemon is not running` | Open Docker Desktop app, wait for it to start |
| `pip: command not found` in Dockerfile | Add `USER root` before the `RUN pip install` line |
| `Permission denied` errors | Ensure `USER root` is set before `pip install` |
| Container name conflict | `docker rm <name>` then re-create |
| Image not found after restart | `docker load -i spark-bda.tar` |
| `matplotlib` display errors | Save to file with `plt.savefig()` instead of `plt.show()` |
| Can't see files in container | Check your `-v` mount path is correct |

---

> [!CAUTION]
> **Do NOT rely on internet access during the exam.** Run through this entire guide tonight and verify everything works offline. Disconnect your Wi-Fi and test the container one more time before sleeping.

**Good luck tomorrow! 🎯**
