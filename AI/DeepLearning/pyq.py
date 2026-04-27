import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def main():
    # ---------------------------------------------------------
    # 1. LOAD DATASET
    # ---------------------------------------------------------
    # Assuming the file is named 'dataset1.csv'
    try:
        df = pd.pd.read_csv("dataset1.csv")
    except FileNotFoundError:
        print("Error: 'dataset1.csv' not found. Please ensure the dataset is in the same directory.")
        # For demonstration purposes, we will create a dummy dataset if not found
        # so that the code can still be tested structurally.
        np.random.seed(42)
        df = pd.DataFrame({
            'age': np.random.randint(20, 80, 1000),
            'sex': np.random.choice(['M', 'F'], 1000),
            'cholesterol': np.random.randint(150, 300, 1000),
            'bp': np.random.randint(80, 180, 1000),
            'target': np.random.randint(0, 2, 1000)
        })

    # ---------------------------------------------------------
    # 2. DATA PREPROCESSING (5 Marks)
    # ---------------------------------------------------------
    print("--- Starting Data Preprocessing ---")
    
    # a) Handling missing values
    # For numeric columns, fill with mean. For categorical, fill with mode.
    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns

    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # b) Encoding categorical variables
    le = LabelEncoder()
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col])

    # Separate features and target (Assuming target column is named 'target')
    # Modify 'target' if your dataset uses a different column name for heart attack risk.
    if 'target' in df.columns:
        X = df.drop(columns=['target'])
        y = df['target']
    else:
        # Fallback if column name is unknown
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

    # c) Normalization / Feature Scaling
    # We will scale AFTER splitting to prevent data leakage, but as per general 
    # workflow we initialize the scaler here.
    scaler = StandardScaler()

    # ---------------------------------------------------------
    # 3. SPLIT DATASET: TRAIN, VALIDATION, AND TEST SETS (10 Marks)
    # ---------------------------------------------------------
    # First split: Train (70%) and Temp (30%)
    X_train_temp, X_test, y_train_temp, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )
    
    # Second split: Split Temp into Validation (15% overall) and Train (70% overall)
    # 0.15 / 0.85 approx 0.176
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_temp, y_train_temp, test_size=0.1765, random_state=42, stratify=y_train_temp
    )

    # Now apply the scaler
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)

    print(f"Data split successfully:")
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Validation set: {X_val.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")

    # ---------------------------------------------------------
    # 4. BUILD THE NEURAL NETWORK WITH DROPOUT (5 Marks)
    # ---------------------------------------------------------
    # Building a Deep Learning model for Binary Classification
    model = keras.Sequential([
        # Hidden Layer 1
        layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        layers.Dropout(0.10), # 10% dropout after each hidden layer

        # Hidden Layer 2
        layers.Dense(32, activation='relu'),
        layers.Dropout(0.10),

        # Hidden Layer 3
        layers.Dense(16, activation='relu'),
        layers.Dropout(0.10),

        # Output Layer (1 neuron, sigmoid for binary classification)
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    # ---------------------------------------------------------
    # 5. TRAIN THE MODEL 
    # ---------------------------------------------------------
    print("\n--- Training Model ---")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=50,
        batch_size=32,
        verbose=1
    )

    # ---------------------------------------------------------
    # 6. EVALUATE ON TEST SET & PRINT METRICS (5 Marks)
    # ---------------------------------------------------------
    print("\n--- Evaluating on Test Set ---")
    # Get probability predictions
    y_pred_probs = model.predict(X_test)
    
    # Convert probabilities to binary class labels (Threshold = 0.5)
    y_pred_classes = (y_pred_probs > 0.5).astype(int)

    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred_classes)
    print(cm)

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_classes))

    # Optional: Plot Confusion Matrix for better visualization
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title("Confusion Matrix (Test Set)")
    plt.xlabel("Predicted Labels")
    plt.ylabel("True Labels")
    plt.tight_layout()
    plt.savefig("confusion_matrix.png")
    plt.show()

    # ---------------------------------------------------------
    # 7. PLOT LOSS AND ACCURACY CURVES (5 Marks)
    # ---------------------------------------------------------
    print("\n--- Plotting Learning Curves ---")
    
    epochs_range = range(1, len(history.history['loss']) + 1)

    plt.figure(figsize=(12, 5))

    # Accuracy Plot
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, history.history['accuracy'], label='Training Accuracy', color='blue', marker='o')
    plt.plot(epochs_range, history.history['val_accuracy'], label='Validation Accuracy', color='orange', marker='o')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)

    # Loss Plot
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, history.history['loss'], label='Training Loss', color='red', marker='o')
    plt.plot(epochs_range, history.history['val_loss'], label='Validation Loss', color='green', marker='o')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("learning_curves.png")
    plt.show()

if __name__ == "__main__":
    main()
