# Heart Disease Prediction PYQ - Deep Learning Implementation

> Detailed Solution, Theory, and Code Breakdown for predicting the risk of a heart attack using a Deep Neural Network.

---

## 📌 Phase 1: Detailed Theoretical Concepts

Before diving into the code, it is absolutely essential to understand the theoretical components that make up this deep learning pipeline, especially the concepts specifically asked for in the question.

### 1. Data Splitting: Training, Validation, and Test Sets
In machine learning, we never evaluate our model on the data it was trained on. We split our data into three distinct sets:
*   **Training Phase (Set)**: The largest chunk of data (usually 70-80%). The model "sees" this data and calculates gradients to adjust its weights. It learns the patterns from this set.
*   **Validation Phase (Set)**: A smaller chunk of data (usually 10-15%). The model evaluates itself on this data at the end of *every epoch* during training. The model **does not** adjust its weights based on the validation set. It is used strictly to tune hyperparameters (like learning rate or network size) and to detect *overfitting*.
*   **Test Phase (Set)**: The final holdout set (usually 10-15%). This data is completely hidden from the model until training is 100% complete. It provides the final, unbiased metric of how the model will perform in the real world. 

**Difference between Training and Validation Phase:**
The training phase is for *learning* (weights are updated). The validation phase is for *checking* (weights are frozen, performance is measured). If training accuracy is 99% but validation accuracy is 60%, the model has memorized the training data and failed to generalize (overfitting).

### 2. The Dropout Layer
Neural networks are powerful, but they have a bad habit of **overfitting** (memorizing the noise in the training data). 
*   **What it is**: A Dropout layer randomly "turns off" a percentage of neurons in the previous layer during each training step. The question specifically asked for a **10% dropout rate** (`0.10`).
*   **Why we use it**: By randomly turning off 10% of neurons, the network cannot rely too heavily on any single neuron or specific feature. It forces the network to learn multiple, redundant, and robust pathways to make predictions. 
*   **Note**: Dropout is *only* active during the training phase. During validation and testing, all neurons are turned on, but their weights are scaled down by 10% to balance the total signal.

### 3. Confusion Matrix
A Confusion Matrix is a tabular summary of the number of correct and incorrect predictions made by a classifier. For binary classification (Heart Attack vs No Heart Attack), it is a 2x2 grid:

| | Predicted Negative (0) | Predicted Positive (1) |
|---|---|---|
| **Actual Negative (0)** | True Negative (TN) | False Positive (FP) |
| **Actual Positive (1)** | False Negative (FN) | True Positive (TP) |

*   **True Positives (TP)**: Model predicted heart attack, and patient actually had one.
*   **True Negatives (TN)**: Model predicted no heart attack, and patient did not have one.
*   **False Positives (FP)**: Model predicted heart attack, but patient was healthy (Type I Error).
*   **False Negatives (FN)**: Model predicted no heart attack, but patient actually had one (Type II Error - **Fatal in medicine!**).

### 4. Classification Report
The classification report builds on the Confusion Matrix to provide advanced metrics:
*   **Precision**: Out of all the people the model *predicted* would have a heart attack, how many actually did? (`TP / (TP + FP)`)
*   **Recall (Sensitivity)**: Out of all the people who *actually* had a heart attack, how many did the model correctly find? (`TP / (TP + FN)`). In medical diagnosis, maximizing Recall is crucial because missing a sick patient (False Negative) is deadly.
*   **F1-Score**: The harmonic mean of Precision and Recall. It is the best metric to use if the dataset is imbalanced.
*   **Accuracy**: Overall percentage of correct predictions (`(TP + TN) / Total`).

### 5. Loss and Accuracy (Interpretation of Plots)
When plotting the Learning Curves (Loss and Accuracy) across epochs, we interpret the model's health:
*   **Loss Curve**: Represents the error (how far off predictions are). Both Training Loss and Validation Loss should steadily decrease and stabilize. 
*   **Accuracy Curve**: Represents the percentage of correct guesses. Both should steadily increase and stabilize.

**How to Interpret the Plots:**
1.  **Good Fit**: Train and Validation lines hug each other closely, converging at a high accuracy / low loss.
2.  **Overfitting**: Training accuracy keeps going up (loss goes down), but Validation accuracy flatlines or drops (loss spikes). The model is memorizing training data.
3.  **Underfitting**: Both Training and Validation accuracy are very low and fail to improve. The model is too simple to learn the patterns.

---

## 📌 Phase 2: Line-by-Line Code Breakdown

Below is the complete, line-by-line breakdown of the Python code implementation found in `pyq.py`, meticulously mapping to the marks and requirements specified in the PYQ.

### 1. Data Splitting (10 Marks)
The question requires splitting into Training, Validation, and Test sets. `scikit-learn`'s `train_test_split` only splits into two sets at a time. Therefore, we must call it twice.

```python
# First split: We hold out 15% of the data for the final Test set.
# The remaining 85% is stored in 'temp' variables.
X_train_temp, X_test, y_train_temp, y_test = train_test_split(
    X, y, test_size=0.15, random_state=42, stratify=y
)

# Second split: We take that 85% 'temp' data and split it again.
# We want 15% of the ORIGINAL data for validation. 
# 15 / 85 = 0.1764. So we split 17.64% of the temp data into Validation.
# The remaining ~70% becomes the actual Training set.
X_train, X_val, y_train, y_val = train_test_split(
    X_train_temp, y_train_temp, test_size=0.1765, random_state=42, stratify=y_train_temp
)
```
*   `stratify=y`: This is critical in medical datasets. It ensures that the ratio of Heart Attack to No Heart Attack patients is perfectly balanced across all three sets.

### 2. Data Preprocessing (5 Marks)

```python
# a) Handling missing values
# Identify numeric and categorical columns
numeric_cols = df.select_dtypes(include=['number']).columns
categorical_cols = df.select_dtypes(include=['object']).columns

# Fill numeric NaNs with the mean of that column
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

# Fill categorical NaNs with the mode (most frequent value)
for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])
```
*   Neural networks crash if fed `NaN` (null) values. We impute missing numbers with the average, and missing text with the most common category.

```python
# b) Encoding categorical variables
le = LabelEncoder()
for col in categorical_cols:
    df[col] = le.fit_transform(df[col])
```
*   `LabelEncoder()` converts text like "Male" / "Female" into integers `0` / `1`. Neural networks can only perform math on numbers.

```python
# c) Normalization / Feature Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)
```
*   `StandardScaler()` normalizes features so they have a mean of 0 and standard deviation of 1.
*   **Crucial Concept**: Notice we only `.fit_transform()` on `X_train`. We only `.transform()` the validation and test sets. We must never fit the scaler on test data, as that causes **data leakage** (the model would secretly learn the mean of the test set).

### 3. Neural Network Architecture with Dropout (5 Marks)

```python
model = keras.Sequential([
    # Hidden Layer 1
    layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dropout(0.10), # 10% dropout as requested

    # Hidden Layer 2
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.10),

    # Output Layer for Binary Classification
    layers.Dense(1, activation='sigmoid')
])
```
*   `keras.Sequential`: Builds the network layer-by-layer.
*   `Dense(64, activation='relu')`: 64 neurons utilizing the Rectified Linear Unit function to capture non-linear patterns.
*   `Dropout(0.10)`: Specifically requested by the PYQ. Drops 10% of connections to prevent overfitting.
*   `Dense(1, activation='sigmoid')`: Because predicting a heart attack is binary (Yes/No), we use 1 output neuron with a `sigmoid` activation. Sigmoid squashes the output into a probability between 0.0 and 1.0.

```python
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
```
*   **Loss**: `binary_crossentropy` is the mathematically correct loss function for binary classification. It measures how far the predicted probability is from the actual class (0 or 1).

### 4. Training, Confusion Matrix, and Plots (10 Marks)

```python
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=50,
    batch_size=32
)
```
*   Trains the model using the `X_train` set, but validates its performance simultaneously on `X_val` at the end of each of the 50 epochs.

```python
# Predictions return probabilities (e.g., 0.85). 
y_pred_probs = model.predict(X_test)

# Convert probabilities > 0.5 to Class 1 (Heart Attack), else Class 0.
y_pred_classes = (y_pred_probs > 0.5).astype(int)

cm = confusion_matrix(y_test, y_pred_classes)
print(classification_report(y_test, y_pred_classes))
```
*   `model.predict()` generates raw probabilities based on the unseen `X_test` data. We convert these to hard class labels using a standard 0.5 threshold.
*   We pass the predicted classes against the true `y_test` labels to generate the confusion matrix and classification report.

```python
plt.plot(epochs_range, history.history['accuracy'], label='Training Accuracy')
plt.plot(epochs_range, history.history['val_accuracy'], label='Validation Accuracy')
```
*   The `history` object inherently stores the metrics from every epoch. We access `history.history['accuracy']` and `['val_accuracy']` to plot the learning curves, visually proving whether our model generalized well or overfit the data.

### 5. Generated Output Plots

**Confusion Matrix:**
![Confusion Matrix Output](file:///d:/College/AWT%20Lab/EXAMSS/AI/DeepLearning/confusion_matrix.png)

**Learning Curves:**
![Learning Curves Output](file:///d:/College/AWT%20Lab/EXAMSS/AI/DeepLearning/learning_curves.png)
