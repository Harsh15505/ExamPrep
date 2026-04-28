# 📘 PYQ-5: ML Classification Pipeline — Complete Guide

> **Topic:** PySpark ML — GroupBy, VectorAssembler, Feature Selection, Classification  
> **Total Marks:** 30  
> **Key Difference:** This is an **ML question**, not just SQL/aggregation. You build a full pipeline.

---

## 📌 What This Question Tests

Given a small dataset about marriage/affairs with features and a binary label (`affairs`: 0 or 1), you must:
1. Create DataFrame from inline data (3 marks)
2. Do GroupBy operations (8 marks)
3. Use VectorAssembler to prepare features (5 marks)
4. Do feature selection using correlation (6 marks)
5. Build, train, and evaluate a classifier (8 marks)

---

## 🧠 Theory You MUST Know

### What is VectorAssembler?

ML models in Spark need ALL features combined into a single column called `features`. VectorAssembler does this.

```
Before:  rate_marriage=5, age=32, yrs_married=5
After:   features=[5.0, 32.0, 5.0]
```

```python
from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(
    inputCols=["col1", "col2", "col3"],  # input feature columns
    outputCol="features"                  # output: single vector column
)
df_assembled = assembler.transform(df)
```

### What is Feature Selection?

Picking the most important features for your model. Two common methods:

**Method 1 — Correlation Analysis:**
```python
# Check how each feature correlates with the label
corr = df.stat.corr("feature_col", "label_col")
# Values close to +1 or -1 = strong relationship
# Values close to 0 = weak/no relationship
```

**Method 2 — Feature Importance (from tree models):**
```python
model = RandomForestClassifier(...).fit(train)
print(model.featureImportances)
```

### Train/Test Split

Split data into training (to learn) and testing (to evaluate):
```python
train, test = df.randomSplit([0.8, 0.2], seed=42)
# 80% for training, 20% for testing
# seed=42 ensures reproducible split
```

### Classification Models in PySpark

| Model | When to Use | Import |
|-------|-------------|--------|
| `LogisticRegression` | Binary classification (0/1) | `from pyspark.ml.classification import LogisticRegression` |
| `DecisionTreeClassifier` | Simple, interpretable | `from pyspark.ml.classification import DecisionTreeClassifier` |
| `RandomForestClassifier` | Better accuracy, handles noise | `from pyspark.ml.classification import RandomForestClassifier` |

All three follow the same API:
```python
model = ModelClass(featuresCol="features", labelCol="label")
fitted = model.fit(train)
predictions = fitted.transform(test)
```

### Evaluation Metrics

| Metric | What It Measures | metricName |
|--------|-----------------|------------|
| Accuracy | % of correct predictions overall | `"accuracy"` |
| Precision | Of predicted positives, how many were correct | `"weightedPrecision"` |
| Recall | Of actual positives, how many were found | `"weightedRecall"` |
| F1-Score | Balance of precision and recall | `"f1"` |
| AUC-ROC | Overall ranking quality (binary only) | `"areaUnderROC"` |

```python
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

evaluator = MulticlassClassificationEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="accuracy"  # change this for different metrics
)
score = evaluator.evaluate(predictions)
```

---

## 💻 Complete Solution — Cell by Cell

### CELL 1: Initialization (Same as always)

```python
import findspark
findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("BDA-Exam").master("local[*]").getOrCreate()
sc = spark.sparkContext
from pyspark.sql.functions import *
from pyspark.sql.types import *
print("✅ Spark Ready!", spark.version)
```

---

### CELL 2: Create DataFrame (3 Marks)

```python
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
df.show()
```

---

### CELL 3 & 4: GroupBy Operations (4 Marks)

```python
# Group by rate_marriage
df.groupBy("rate_marriage").count().show()

# Group by affairs
df.groupBy("affairs").count().show()
```

---

### CELL 5: GroupBy Two Columns + Order (4 Marks)

```python
df.groupBy("rate_marriage", "affairs") \
    .count() \
    .orderBy("rate_marriage", "affairs", "count", ascending=True) \
    .show()
```

**Why:** Shows the distribution — how many people with each marriage rating had/didn't have affairs.

---

### CELL 6: VectorAssembler (5 Marks)

```python
from pyspark.ml.feature import VectorAssembler

feature_cols = ["rate_marriage", "age", "yrs_married", "children", "religious"]

assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
df_assembled = assembler.transform(df)

df_assembled.select("features", "affairs").show(truncate=False)
```

**Line-by-line:**
- `feature_cols` — all columns EXCEPT the label (`affairs`)
- `VectorAssembler(inputCols=..., outputCol="features")` — configure what goes in, what comes out
- `.transform(df)` — actually creates the `features` column. Each row now has a vector like `[5.0, 32.0, 5.0, 2.0, 2.0]`

---

### CELL 7: Feature Selection (6 Marks)

```python
# Correlation analysis
for col_name in feature_cols:
    corr_val = df.stat.corr(col_name, "affairs")
    print(f"  {col_name:15s} : {corr_val:.4f}")
```

**Line-by-line:**
- `df.stat.corr(col1, col2)` — Pearson correlation between two columns
- Returns a value between -1 and +1
- Close to 0 = no relationship (bad feature)
- Close to +1 or -1 = strong relationship (good feature)
- Drop features with very low correlation, keep the rest

Then re-assemble with only selected features:
```python
selected_features = ["rate_marriage", "yrs_married", "children", "religious"]
assembler2 = VectorAssembler(inputCols=selected_features, outputCol="selected_features")
df_selected = assembler2.transform(df)
```

---

### CELL 8: Model Building & Evaluation (8 Marks)

```python
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator

# Prepare: rename label column
model_df = df_assembled.select("features", col("affairs").alias("label"))

# Split
train, test = model_df.randomSplit([0.8, 0.2], seed=42)

# Train
lr = LogisticRegression(featuresCol="features", labelCol="label", maxIter=10)
lr_model = lr.fit(train)

# Predict
predictions = lr_model.transform(test)
predictions.select("features", "label", "prediction").show(truncate=False)

# Evaluate
for metric in ["accuracy", "weightedPrecision", "weightedRecall", "f1"]:
    evaluator = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName=metric
    )
    print(f"{metric}: {evaluator.evaluate(predictions):.4f}")
```

**Line-by-line:**
- `col("affairs").alias("label")` — ML models expect the target column to be named `label`
- `randomSplit([0.8, 0.2], seed=42)` — 80% train, 20% test, seed for reproducibility
- `lr.fit(train)` — train the model on training data
- `lr_model.transform(test)` — make predictions on test data. Adds `prediction` and `probability` columns
- Evaluator loop — prints all four metrics in one go

---

## 🔄 Alternative Models (Drop-in Replacements)

Replace the LogisticRegression block with any of these:

```python
# Decision Tree
from pyspark.ml.classification import DecisionTreeClassifier
dt = DecisionTreeClassifier(featuresCol="features", labelCol="label")
model = dt.fit(train)

# Random Forest
from pyspark.ml.classification import RandomForestClassifier
rf = RandomForestClassifier(featuresCol="features", labelCol="label", numTrees=10)
model = rf.fit(train)
```

The rest (predict + evaluate) stays exactly the same. They all use `.fit()` and `.transform()`.

---

## ❓ Viva Questions & Answers

**Q: What is VectorAssembler and why is it needed?**
A: PySpark ML models require all input features in a single vector column. VectorAssembler combines multiple columns into one `DenseVector`. Without it, the model doesn't know which columns are features.

**Q: What is the difference between a feature and a label?**
A: Features are the input variables (what you use to predict). Label is the output/target variable (what you're predicting). In this dataset, `affairs` is the label, everything else is a feature.

**Q: Why split into train and test?**
A: To prevent overfitting. The model learns patterns from training data. We test on unseen data to see if it actually learned general patterns, not just memorized the training data.

**Q: What is overfitting?**
A: When a model performs well on training data but poorly on new/test data. It memorized the training examples instead of learning general patterns.

**Q: What does `seed=42` do in randomSplit?**
A: Makes the split reproducible. Same seed = same split every time. Without it, you get a different split each run, making results inconsistent.

**Q: Explain Precision vs Recall.**
A: Precision = "Of all items I predicted as positive, how many actually were?" Recall = "Of all actual positives, how many did I find?" Precision penalizes false positives, recall penalizes false negatives.

**Q: What is F1-Score?**
A: The harmonic mean of precision and recall: `F1 = 2 * (P * R) / (P + R)`. It balances both metrics. Use F1 when you care equally about precision and recall.

**Q: When to use Logistic Regression vs Decision Tree vs Random Forest?**
A: Logistic Regression — simple, fast, works well for linearly separable data. Decision Tree — interpretable, handles non-linear data, but can overfit. Random Forest — ensemble of trees, more accurate, handles noise, but slower and less interpretable.

**Q: What is Pearson correlation?**
A: Measures linear relationship between two variables. Range: -1 to +1. +1 = perfect positive correlation, -1 = perfect negative, 0 = no linear relationship. Used for feature selection — drop features with correlation near 0.

**Q: What is AUC-ROC?**
A: Area Under the Receiver Operating Characteristic curve. Measures how well the model distinguishes between classes. 1.0 = perfect, 0.5 = random guessing.

---

## 🔑 The ML Pipeline Pattern (Memorize This)

```
1. Create DataFrame
2. GroupBy exploratory analysis
3. VectorAssembler → combine features into one column
4. Feature Selection → correlation or importance
5. Train/Test Split → randomSplit([0.8, 0.2])
6. Train Model → model.fit(train)
7. Predict → model.transform(test)
8. Evaluate → MulticlassClassificationEvaluator
```

Every ML question follows this exact flow. The only thing that changes is the dataset and the model choice.
