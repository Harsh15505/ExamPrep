# =============================================================
# BDA PYQ-1: Spark Data Processing Pipeline - COMPLETE SOLUTION
# =============================================================

# ===================== CELL 1: INITIALIZATION =====================
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


# =============== CELL 2: Q1a - LOAD DATA (2 Marks) ===============
# Load as DataFrame
df = spark.read.csv("/work/sample_transactions.txt", header=True, inferSchema=True)

print("=== Raw Data ===")
df.show()
df.printSchema()
print(f"Total rows: {df.count()}")


# ============ CELL 3: Q1b - FILTER BAD DATA (3 Marks) ============
# Remove rows where transaction_amount is null, zero, or negative
df_clean = df.filter(
    (col("transaction_amount").isNotNull()) &
    (col("transaction_amount") > 0)
)

print("=== Clean Data (nulls, zeros, negatives removed) ===")
df_clean.show()
print(f"Rows after filtering: {df_clean.count()}")


# ========= CELL 4: Q2 - TOTAL EXPENDITURE BY CUSTOMER (5 Marks) =========
total_by_customer = df_clean.groupBy("customer_id") \
    .agg(sum("transaction_amount").alias("total_expenditure"))

print("=== Total Expenditure by Customer ===")
total_by_customer.show()


# ========= CELL 5: Q3 - AVG AMOUNT BY CATEGORY (5 Marks) =========
avg_by_category = df_clean.groupBy("product_category") \
    .agg(avg("transaction_amount").alias("average_transaction_amount"))

print("=== Average Transaction Amount by Product Category ===")
avg_by_category.show()


# ========= CELL 6: Q4 - TOP 3 CUSTOMERS (5 Marks) =========
top3 = df_clean.groupBy("customer_id") \
    .agg(sum("transaction_amount").alias("total_expenditure")) \
    .orderBy(desc("total_expenditure")) \
    .limit(3)

print("=== Top 3 Customers by Expenditure ===")
top3.show()


# ========= CELL 7: Q5 - TRANSACTION COUNT PER DAY (5 Marks) =========
count_per_day = df_clean.groupBy("transaction_date") \
    .agg(count("*").alias("transaction_count"))

print("=== Transaction Count per Day ===")
count_per_day.orderBy("transaction_date").show()


# ========= CELL 8: Q6 - MOST POPULAR CATEGORY (5 Marks) =========
popular_category = df_clean.groupBy("product_category") \
    .agg(count("*").alias("transaction_count")) \
    .orderBy(desc("transaction_count")) \
    .limit(1)

print("=== Most Popular Product Category ===")
popular_category.show()


# ========= CELL 9: STOP SPARK (Optional) =========
# spark.stop()
