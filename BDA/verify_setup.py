from pyspark.sql import SparkSession, Row
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

print("=" * 50)
print("BDA EXAM SETUP VERIFICATION")
print("=" * 50)

# Library versions
print("\n--- Library Versions ---")
print(f"NumPy:      {np.__version__}")
print(f"Pandas:     {pd.__version__}")
print(f"Matplotlib: {matplotlib.__version__}")
print(f"Seaborn:    {sns.__version__}")
print(f"NetworkX:   {nx.__version__}")

# Spark Session
spark = SparkSession.builder.appName("BDA-Verify").getOrCreate()
sc = spark.sparkContext
print(f"Spark:      {spark.version}")

# RDD Test
print("\n--- RDD Test ---")
rdd = sc.parallelize([1, 2, 3, 4, 5])
print(f"RDD Sum: {rdd.reduce(lambda a, b: a + b)}")
print(f"RDD Map: {rdd.map(lambda x: x * 2).collect()}")
print(f"RDD Filter: {rdd.filter(lambda x: x > 3).collect()}")

# Spark SQL Test
print("\n--- Spark SQL Test ---")
df = spark.createDataFrame([
    Row(name="Alice", age=30, dept="Engineering"),
    Row(name="Bob", age=25, dept="Marketing"),
    Row(name="Charlie", age=35, dept="Engineering"),
])
df.show()
df.createOrReplaceTempView("people")
spark.sql("SELECT dept, AVG(age) as avg_age FROM people GROUP BY dept").show()

# ML Test
print("\n--- ML Test ---")
data = spark.createDataFrame([(1.0, 2.0, 3.0), (2.0, 4.0, 6.0), (3.0, 6.0, 9.0)], ["a", "b", "label"])
assembler = VectorAssembler(inputCols=["a", "b"], outputCol="features")
assembled = assembler.transform(data)
lr = LinearRegression(featuresCol="features", labelCol="label")
model = lr.fit(assembled)
print(f"ML Model Coefficients: {model.coefficients}")
print("ML Pipeline: OK")

# NetworkX Test
print("\n--- NetworkX Test ---")
G = nx.Graph()
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)])
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print(f"Shortest Path 1->4: {nx.shortest_path(G, 1, 4)}")

# Matplotlib Test
print("\n--- Matplotlib Test ---")
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
plt.savefig("/work/test_plot.png")
print("Plot saved to /work/test_plot.png")

print("\n" + "=" * 50)
print("ALL CHECKS PASSED! YOU ARE READY FOR THE EXAM!")
print("=" * 50)

spark.stop()
