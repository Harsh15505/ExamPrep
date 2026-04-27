# Deep Neural Network for Regression (House Price Prediction)

> Detailed Theory, Code Breakdown, Exam Workflow, and Viva Questions for the Keras/TensorFlow DNN Regression Experiment.

---

## 📌 1. Theoretical Background

### What is Regression in Deep Learning?
Regression is a type of supervised learning where the goal is to predict a **continuous numerical value** (e.g., predicting the price of a house, temperature, or stock price) rather than a discrete class label (classification). 

### How does a Neural Network handle Regression?
Unlike classification tasks that use a Softmax or Sigmoid activation function in the final layer to output probabilities, a regression network typically uses a **single neuron with no activation function** (or a linear activation function) in its output layer. This allows the network to predict continuous values directly.

### Key Concepts in this Experiment:
1. **Data Imputation**: Filling in missing values (using the mean) so the network doesn't crash on `NaN` data.
2. **Label Encoding**: Deep learning models only understand numbers. Label Encoding converts categorical text (like "Suburban", "Urban") into integers (0, 1).
3. **Standardization (Scaling)**: Bringing all features to a common scale (mean=0, standard deviation=1). This is crucial for Neural Networks because features on vastly different scales cause unstable gradient updates.
4. **Loss Function (MSE)**: Mean Squared Error is the standard loss function for regression. It penalizes large errors heavily by squaring the difference between predicted and actual values.
5. **Evaluation Metric (MAE)**: Mean Absolute Error tells us, on average, how far off our predictions are in the actual unit (e.g., dollars).

---

## 📌 2. Exam Workflow (Mental Steps for Implementation)

If you are given a **different dataset** and **target variable** in the exam, follow these mental steps to successfully code the solution from scratch:

#### Step 1: Import all necessary artillery
- Data: `pandas`, `numpy`
- Viz: `matplotlib.pyplot`, `seaborn`
- Preprocessing: `train_test_split`, `StandardScaler`, `LabelEncoder`
- Deep Learning: `keras`, `layers` from `tensorflow.keras`

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow import keras
from tensorflow.keras import layers
```

#### Step 2: Load and Clean Data
- Load CSV into a Pandas DataFrame.
- **Check/Fix Missing Values**: `df.fillna(df.mean(numeric_only=True), inplace=True)`
- **Check/Fix Categorical Data**: Find `object` columns and run `LabelEncoder` on them.

```python
df = pd.read_csv("dataset.csv")

# Handle missing numeric values
df.fillna(df.mean(numeric_only=True), inplace=True)

# Encode categorical text columns to integers
for col in df.select_dtypes(include=['object']).columns:
    df[col] = LabelEncoder().fit_transform(df[col])
```

#### Step 3: Split and Scale
- **X and y**: Drop the target column to get `X`, set the target column to `y`.
- **Train/Test Split**: Split data 80/20.
- **Scale**: Fit `StandardScaler` on `X_train`, then transform *both* `X_train` and `X_test`. **Never fit the scaler on test data!**

```python
# Drop the target column for X, isolate it for y
X = df.drop(columns=['Target_Column_Name'])
y = df['Target_Column_Name']

# 80/20 Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features (FIT ON TRAIN ONLY)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train) 
X_test = scaler.transform(X_test)       
```

#### Step 4: Build the Neural Network Architecture
- `keras.Sequential()`
- Add 2-3 Hidden Layers (`layers.Dense`) with `relu` activation. The first layer MUST have `input_shape=(X_train.shape[1],)`.
- **Output Layer**: A single neuron `layers.Dense(1)` with **NO** activation function (default is linear).

```python
model = keras.Sequential([
    # Input shape MUST match the number of features
    layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dense(32, activation='relu'),
    # Output Layer: 1 neuron, NO activation for Regression
    layers.Dense(1) 
])
```

#### Step 5: Compile and Train
- **Compile**: `optimizer='adam'`, `loss='mse'`, `metrics=['mae']`.
- **Fit**: Pass `X_train`, `y_train`, `epochs=50`, `batch_size=32`, and `validation_split=0.2`. Store this in a `history` variable.

```python
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2 # Holds 20% of training data for validation
)
```

#### Step 6: Evaluate and Plot
- Run `model.evaluate(X_test, y_test)`.
- Plot the training vs validation MAE using `history.history['mae']`.

```python
loss, mae = model.evaluate(X_test, y_test)
print(f"Mean Absolute Error: {mae:.2f}")

plt.plot(history.history['mae'], label='Train MAE')
plt.plot(history.history['val_mae'], label='Validation MAE')
plt.xlabel("Epochs")
plt.ylabel("MAE")
plt.legend()
plt.show()
```

---

## 📌 3. Line-by-Line Code Breakdown

```python
# 1. Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import LabelEncoder
```
*Self-explanatory. Bringing in data manipulation, visualization, preprocessing, and deep learning tools.*

```python
# 2. Load the dataset
df = pd.read_csv("house_price_dataset (1).csv")
```
*Reads the CSV file into a Pandas DataFrame.*

```python
# 3. Handle missing values
df.fillna(df.mean(numeric_only=True), inplace=True)
```
*Finds missing (`NaN`) values in purely numeric columns and replaces them with the mean of that specific column. `inplace=True` modifies the existing DataFrame directly.*

```python
# 4. Encode Categorical Data
categorical_cols = df.select_dtypes(include=['object']).columns

le = LabelEncoder()
for col in categorical_cols:
    df[col] = le.fit_transform(df[col])
```
*Selects all columns containing text/strings (`object`). It loops through them and uses `LabelEncoder` to convert the text categories into integer codes (e.g., 0, 1, 2).*

```python
# 5. Separate Features and Target
X = df.drop(columns=['Price'])   # target column
y = df['Price']
```
*`X` contains all input features (dropping 'Price'). `y` is exactly what we want to predict (the 'Price').*

```python
# 6. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```
*Splits the data randomly: 80% for training the network, 20% for testing its performance on unseen data. `random_state` ensures reproducibility.*

```python
# 7. Feature Scaling
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```
*`StandardScaler` standardizes features to have a mean of 0 and a standard dev of 1. We `fit` the scaler only on training data (to learn the mean/variance) and `transform` both train and test sets.*

```python
# 8. Build the Deep Neural Network
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dense(32, activation='relu'),
    layers.Dense(16, activation='relu'),
    layers.Dense(1)   # regression output
])
```
*Creates a sequential model. It has 3 hidden layers (64, 32, and 16 neurons respectively) all using the ReLU activation function to handle non-linearity. The input shape matches the number of features. The output layer has exactly 1 neuron with NO activation function because it's predicting a continuous price.*

```python
# 9. Compile the Model
model.compile(
    optimizer='adam',    
    loss='mse',
    metrics=['mae']
)
```
*Configures the learning process. Uses `adam` to update weights dynamically. Uses `mse` (Mean Squared Error) to calculate the loss to minimize. Tracks `mae` (Mean Absolute Error) to make the results human-readable.*

```python
# 10. Train the Model
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2
)
```
*Trains the network for 50 full passes over the data (`epochs`), updating weights after every 32 samples (`batch_size`). It holds back 20% of `X_train` internally to validate performance after every epoch.*

```python
# 11. Evaluate on unseen Test Data
loss, mae = model.evaluate(X_test, y_test)
print(f"Mean Absolute Error: {mae:.2f}")
```
*Tests the trained model on `X_test`. Returns the final MSE loss and MAE metric.*

```python
# 12. Plotting Learning Curves
plt.plot(history.history['mae'], label='Train MAE')
plt.plot(history.history['val_mae'], label='Validation MAE')
# ... plotting formatting ...
plt.show()
```
*Extracts the MAE tracked during training from the `history` object and plots it to visually inspect for overfitting (if train MAE drops but validation MAE spikes).*

---

## 🎯 4. Viva Questions & Answers

**Q1. Why does the final output layer in this network have 1 neuron and no activation function?**
**A**: Because this is a Regression task. We are predicting a continuous numerical value (house price), not a probability between 0 and 1. If we used an activation function like Sigmoid, our model could only predict prices between 0 and 1, which makes no sense for house prices.

**Q2. Why is it important to use `StandardScaler` before passing data to the Neural Network?**
**A**: Neural networks calculate gradients to update weights. If one feature is measured in millions (like price) and another in single digits (like number of bedrooms), the gradients will be heavily skewed, making the training process highly unstable and painfully slow. Scaling centers everything nicely.

**Q3. Why do we `fit_transform` on the training data, but only `transform` on the test data?**
**A**: This is to prevent "Data Leakage." If we fit the scaler on the test data, the model secretly learns information about the test set's mean and variance during training. The test set must remain completely unseen, so we scale it using the parameters learned strictly from the training data.

**Q4. What is the difference between MSE and MAE? Why use both?**
**A**: `MSE` (Mean Squared Error) squares the differences between actual and predicted values, heavily penalizing large outliers, which makes it an excellent loss function for the optimizer to minimize. `MAE` (Mean Absolute Error) is just the average of the absolute differences, making it highly interpretable for humans (e.g., "The model is off by $15,000 on average").

**Q5. What does the `validation_split=0.2` do during the `.fit()` process?**
**A**: It takes the training data (`X_train`) and holds back 20% of it. The model does not train on this 20%; instead, it evaluates its performance on it at the end of every single epoch. This allows us to track if the model is overfitting during the training process itself.

**Q6. What happens if you forget to handle missing (`NaN`) values before training?**
**A**: The mathematical operations (dot products and gradient calculations) within the neural network will propagate the `NaN` values, turning all weights and subsequent predictions into `NaN`. The model will completely fail to train.

**Q7. What is ReLU and why is it used in the hidden layers?**
**A**: ReLU (Rectified Linear Unit) outputs the input directly if it is positive, and outputs zero if it is negative. It is computationally efficient and solves the "vanishing gradient problem" that older activation functions (like Sigmoid or Tanh) suffered from in deep networks.
