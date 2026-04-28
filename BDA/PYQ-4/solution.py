# =============================================================
# BDA PYQ-4: E-Commerce Transactions — Spark SQL (SET II Afternoon)
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

print("✅ Spark Ready!", spark.version)


# ===================== CELL 2: CREATE DATA =====================
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

print("=== Dataset ===")
df.show(truncate=False)


# ===== CELL 3: Q1a - Total Sales by Product Category (3 Marks) =====
print("=== Q1a: Total Sales by Product Category ===")
spark.sql("""
    SELECT product_category, SUM(amount) AS total_sales
    FROM orders
    GROUP BY product_category
""").show()


# ===== CELL 4: Q1b - Top 3 Categories (3 Marks) =====
print("=== Q1b: Top 3 Product Categories by Sales ===")
spark.sql("""
    SELECT product_category, SUM(amount) AS total_sales
    FROM orders
    GROUP BY product_category
    ORDER BY total_sales DESC
    LIMIT 3
""").show()


# ===== CELL 5: Q1c - Avg Amount Per Region for 2024 (4 Marks) =====
print("=== Q1c: Avg Transaction Amount Per Region for 2024 ===")
spark.sql("""
    SELECT region, AVG(amount) AS average_transaction_amount
    FROM orders
    WHERE YEAR(order_date) = 2024
    GROUP BY region
""").show()


# ===== CELL 6: Q2a - Filter After Jan 6 (3 Marks) =====
print("=== Q2a: Orders After January 6, 2024 ===")
spark.sql("""
    SELECT *
    FROM orders
    WHERE order_date > '2024-01-06'
""").show()


# ===== CELL 7: Q2b - Total Expenditure by Region (4 Marks) =====
print("=== Q2b: Total Expenditure by Region (After Jan 6) ===")
spark.sql("""
    SELECT region, SUM(amount) AS total_expenditure
    FROM orders
    WHERE order_date > '2024-01-06'
    GROUP BY region
""").show()


# ===== CELL 8: Q2c - Avg for Electronics (3 Marks) =====
print("=== Q2c: Avg Transaction Amount for Electronics ===")
spark.sql("""
    SELECT AVG(amount) AS average_transaction_amount
    FROM orders
    WHERE product_category = 'Electronics'
""").show()


# ===== CELL 9: Q3a - Total per Customer + Top 3 (5 Marks) =====
print("=== Q3a: Total Sales per Customer ===")
spark.sql("""
    SELECT customer_id, SUM(amount) AS total_sales
    FROM orders
    GROUP BY customer_id
    ORDER BY total_sales DESC
""").show()

print("=== Top 3 Highest-Spending Customers ===")
spark.sql("""
    SELECT customer_id, SUM(amount) AS total_sales
    FROM orders
    GROUP BY customer_id
    ORDER BY total_sales DESC
    LIMIT 3
""").show()


# ===== CELL 10: Q3b - Region with Highest Single Order (5 Marks) =====
print("=== Q3b: Region with Highest Single Order Amount ===")
spark.sql("""
    SELECT region, amount AS highest_order
    FROM orders
    ORDER BY amount DESC
    LIMIT 1
""").show()
