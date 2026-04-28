# =============================================================
# BDA PYQ-3: Spark SQL Queries on Transaction Data
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


# ===================== CELL 2: CREATE DATA =====================
# Data given in the question — create it directly
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

schema = ["transaction_id", "product_id", "customer_id", "amount", "transaction_date", "city"]
df = spark.createDataFrame(data, schema)

# Register as SQL table
df.createOrReplaceTempView("transactions")

print("=== Dataset ===")
df.show()
df.printSchema()


# ===== CELL 3: SECTION 1a - Total Sales by City (3 Marks) =====
print("=== Q1a: Total Sales Amount for Each City ===")
spark.sql("""
    SELECT city, SUM(amount) AS total_sales
    FROM transactions
    GROUP BY city
""").show()


# ===== CELL 4: SECTION 1b - Top 3 Cities (3 Marks) =====
print("=== Q1b: Top 3 Cities with Highest Sales ===")
spark.sql("""
    SELECT city, SUM(amount) AS total_sales
    FROM transactions
    GROUP BY city
    ORDER BY total_sales DESC
    LIMIT 3
""").show()


# ===== CELL 5: SECTION 1c - Avg Amount Per Month (4 Marks) =====
print("=== Q1c: Average Transaction Amount Per Month for 2024 ===")
spark.sql("""
    SELECT MONTH(transaction_date) AS month,
           AVG(amount) AS average_transaction_amount
    FROM transactions
    WHERE YEAR(transaction_date) = 2024
    GROUP BY MONTH(transaction_date)
    ORDER BY month
""").show()


# ===== CELL 6: SECTION 2a - Filter After Jan 6 (3 Marks) =====
print("=== Q2a: Transactions After January 6, 2024 ===")
spark.sql("""
    SELECT *
    FROM transactions
    WHERE transaction_date > '2024-01-06'
""").show()


# ===== CELL 7: SECTION 2b - Total Expenditure by City (4 Marks) =====
print("=== Q2b: Total Expenditure for Each City (After Jan 6) ===")
spark.sql("""
    SELECT city, SUM(amount) AS total_expenditure
    FROM transactions
    WHERE transaction_date > '2024-01-06'
    GROUP BY city
""").show()


# ===== CELL 8: SECTION 2c - Avg Amount in Chicago (3 Marks) =====
print("=== Q2c: Average Transaction Amount in Chicago ===")
spark.sql("""
    SELECT AVG(amount) AS average_transaction_amount
    FROM transactions
    WHERE city = 'Chicago'
""").show()


# ===== CELL 9: SECTION 3a - Avg Total per Customer per City (5 Marks) =====
print("=== Q3a: Average Total Amount Spent by Customers in Each City ===")
spark.sql("""
    SELECT city, AVG(customer_total) AS avg_customer_spending
    FROM (
        SELECT city, customer_id, SUM(amount) AS customer_total
        FROM transactions
        GROUP BY city, customer_id
    )
    GROUP BY city
""").show()


# ===== CELL 10: SECTION 3b - City with Highest Single Transaction (5 Marks) =====
print("=== Q3b: City with Highest Single Transaction Amount ===")
spark.sql("""
    SELECT city, amount AS highest_transaction
    FROM transactions
    ORDER BY amount DESC
    LIMIT 1
""").show()
