# =============================================================
# BDA PYQ-5: ML Classification — Affairs Dataset
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


# ========== CELL 2: CREATE DATAFRAME (3 Marks) ==========
data = [
    (5, 32, 5, 2, 2, 1),
    (4, 31, 4, 1, 1, 1),
    (3, 29, 4, 0, 3, 1),
    (3, 28, 2, 2, 1, 0),
    (4, 31, 3, 1, 3, 1),
    (2, 25, 1, 0, 2, 1),
    (3, 27, 2, 1, 3, 0),
    (5, 30, 7, 2, 2, 0),
    (4, 23, 2, 0, 1, 1),
]

schema = ["rate_marriage", "age", "yrs_married", "children", "religious", "affairs"]
df = spark.createDataFrame(data, schema)

print("=== Dataset ===")
df.show()
df.printSchema()


# ========== CELL 3: GROUP BY rate_marriage (2 Marks) ==========
print("=== Group by rate_marriage, count ===")
df.groupBy("rate_marriage").count().show()


# ========== CELL 4: GROUP BY affairs (2 Marks) ==========
print("=== Group by affairs, count ===")
df.groupBy("affairs").count().show()


# ========== CELL 5: GROUP BY rate_marriage, affairs (4 Marks) ==========
print("=== Group by rate_marriage & affairs, ordered ===")
df.groupBy("rate_marriage", "affairs") \
    .count() \
    .orderBy("rate_marriage", "affairs", "count", ascending=True) \
    .show()


# ========== CELL 6: VECTOR ASSEMBLER (5 Marks) ==========
from pyspark.ml.feature import VectorAssembler

feature_cols = ["rate_marriage", "age", "yrs_married", "children", "religious"]

assembler = VectorAssembler(
    inputCols=feature_cols,
    outputCol="features"
)

df_assembled = assembler.transform(df)

print("=== Assembled Features ===")
df_assembled.select("features", "affairs").show(truncate=False)


# ========== CELL 7: FEATURE SELECTION (6 Marks) ==========
import numpy as np

# Method: Correlation analysis
print("=== Feature Correlation with 'affairs' ===")
for col_name in feature_cols:
    corr_val = df.stat.corr(col_name, "affairs")
    print(f"  {col_name:15s} : {corr_val:.4f}")

# Select features with higher absolute correlation
# (In practice, pick features with |corr| > some threshold, e.g., 0.1)
# For this small dataset, we'll use all features or select top ones
selected_features = ["rate_marriage", "yrs_married", "children", "religious"]

assembler_selected = VectorAssembler(
    inputCols=selected_features,
    outputCol="selected_features"
)

df_selected = assembler_selected.transform(df)
print("\n=== Selected Features ===")
df_selected.select("selected_features", "affairs").show(truncate=False)


# ========== CELL 8: MODEL BUILDING (8 Marks) ==========
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator

# Use the full feature set for the model
model_df = df_assembled.select("features", col("affairs").alias("label"))

# Split into train/test (80/20)
train, test = model_df.randomSplit([0.8, 0.2], seed=42)

print(f"Training rows: {train.count()}, Testing rows: {test.count()}")

# Train a Logistic Regression model
lr = LogisticRegression(featuresCol="features", labelCol="label", maxIter=10)
lr_model = lr.fit(train)

# Make predictions
predictions = lr_model.transform(test)

print("\n=== Predictions ===")
predictions.select("features", "label", "prediction", "probability").show(truncate=False)

# Evaluate — Accuracy
evaluator_acc = MulticlassClassificationEvaluator(
    labelCol="label", predictionCol="prediction", metricName="accuracy"
)
accuracy = evaluator_acc.evaluate(predictions)
print(f"Accuracy:  {accuracy:.4f}")

# Evaluate — Precision
evaluator_prec = MulticlassClassificationEvaluator(
    labelCol="label", predictionCol="prediction", metricName="weightedPrecision"
)
precision = evaluator_prec.evaluate(predictions)
print(f"Precision: {precision:.4f}")

# Evaluate — Recall
evaluator_rec = MulticlassClassificationEvaluator(
    labelCol="label", predictionCol="prediction", metricName="weightedRecall"
)
recall = evaluator_rec.evaluate(predictions)
print(f"Recall:    {recall:.4f}")

# Evaluate — F1
evaluator_f1 = MulticlassClassificationEvaluator(
    labelCol="label", predictionCol="prediction", metricName="f1"
)
f1 = evaluator_f1.evaluate(predictions)
print(f"F1 Score:  {f1:.4f}")

# AUC (Binary classification)
evaluator_auc = BinaryClassificationEvaluator(
    labelCol="label", rawPredictionCol="rawPrediction", metricName="areaUnderROC"
)
auc = evaluator_auc.evaluate(predictions)
print(f"AUC-ROC:   {auc:.4f}")

print("\n✅ ML Pipeline Complete!")
