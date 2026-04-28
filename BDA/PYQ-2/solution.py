# =============================================================
# BDA PYQ-2: Spark Processing on Product Reviews Dataset
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


# =========== CELL 2: Q1 - LOAD & FILTER (5 Marks) ===========

# Load both datasets
reviews = spark.read.csv("/work/reviews.txt", header=True, inferSchema=True)
products = spark.read.csv("/work/products.txt", header=True, inferSchema=True)

print("=== Raw Reviews ===")
reviews.show(truncate=False)
print("=== Products ===")
products.show()

# Get list of valid product IDs
valid_products = products.select("product_id")

# Filter: remove nulls, rating < 1.0, and products not in Products dataset
reviews_clean = reviews.filter(
    (col("rating").isNotNull()) &
    (col("rating") >= 1.0)
).join(valid_products, "product_id", "inner")

print("=== Cleaned Reviews ===")
reviews_clean.show(truncate=False)
print(f"Rows after filtering: {reviews_clean.count()}")


# =========== CELL 3: Q2 - AVG RATING BY PRODUCT (5 Marks) ===========
avg_by_product = reviews_clean.groupBy("product_id") \
    .agg(avg("rating").alias("average_rating"))

print("=== Average Rating by Product ===")
avg_by_product.show()


# =========== CELL 4: Q3 - TOP 5 MOST REVIEWED (5 Marks) ===========
most_reviewed = reviews_clean.groupBy("product_id") \
    .agg(count("*").alias("review_count")) \
    .orderBy(desc("review_count")) \
    .limit(5)

print("=== Top 5 Most Reviewed Products ===")
most_reviewed.show()


# =========== CELL 5: Q4 - JOIN DATASETS (5 Marks) ===========
joined = reviews_clean.join(products, "product_id", "inner") \
    .select("product_name", "review_date", "rating", "user_id", "review_text")

print("=== Joined Data (Reviews + Product Info) ===")
joined.show(truncate=False)


# =========== CELL 6: Q5 - AVG RATING BY CATEGORY (5 Marks) ===========
# First join to get category, then group by category
avg_by_category = reviews_clean.join(products, "product_id", "inner") \
    .groupBy("product_category") \
    .agg(avg("rating").alias("average_rating"))

print("=== Average Rating by Category ===")
avg_by_category.show()


# =========== CELL 7: Q6 - SENTIMENT ANALYSIS (5 Marks) ===========
positive_keywords = ["great", "excellent", "recommended"]

# Create a column that checks if review_text contains any positive keyword
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
