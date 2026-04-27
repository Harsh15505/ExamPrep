# Deep Learning & Neural Networks — Complete Viva & Theory Notes

> Comprehensive guide covering Architectures, Data Preprocessing, Gradient Descent, Optimization Algorithms, Regularization, and Hebbian Learning.

---

## 📌 1. Neural Network Architectures & Interconnections

The arrangement and interconnection of processing elements (neurons) define the network's architecture.

### Types of Networks
- **Feedforward Network**: Information moves in exactly one direction (input $\rightarrow$ hidden $\rightarrow$ output). There are no cycles or loops. Example: Standard Artificial Neural Networks (ANN), Convolutional Neural Networks (CNN).
- **Feedback Network**: The output of some neurons is fed back to the network as input. This creates "memory", allowing the network to process sequences. Example: Recurrent Neural Networks (RNN).
- **Lateral Feedback**: Output from a neuron is fed back to other neurons in the **same** layer. Used for self-organization and competitive learning (e.g., Kohonen SOM).
- **Recurrent Network**: A specific type of feedback network forming closed loops, capable of maintaining internal states. Ideal for time-series and NLP. Example: LSTM, GRU.

### Interconnection Geometries
1. **Single-Layer Feedforward**: Only an input and output layer (input isn't computational). Example: Perceptron.
2. **Multilayer Feedforward**: Includes hidden layers for complex, non-linear problems. Example: Multilayer Perceptron (MLP).
3. **Single Node with Own Feedback**: A single neuron loops its output to itself; used in adaptive filters.
4. **Single-Layer Recurrent**: Feedback within the same layer. Example: Hopfield Networks.
5. **Multilayer Recurrent**: Multiple hidden layers with recurrent connections. Example: Deep LSTM networks.

---

## 📌 2. Data Preprocessing & Encoding

Neural networks require purely numerical input. Preprocessing formats raw data into optimal numerical representations.

### Feature Scaling
Unscaled data causes erratic gradient updates and slows down convergence.
- **Normalization (Min-Max Scaling)**: Bounds data to a specific range, usually `[0, 1]`. 
  - *Formula*: $X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}}$
  - *Use Case*: When boundaries are strict (e.g., image pixels 0-255).
- **Standardization (Z-Score)**: Centers data around a mean of 0 with a standard deviation of 1.
  - *Formula*: $X_{std} = \frac{X - \mu}{\sigma}$
  - *Use Case*: Preferred for Deep Learning. It keeps activation functions (like Sigmoid/Tanh) in their active, non-saturated range, preventing vanishing gradients early in training.

### Encoding Categorical Data
- **Label Encoding**: Assigns an integer to each category (e.g., `Red=0, Green=1`). 
  - *Drawback*: Models may misinterpret these integers as an ordinal hierarchy.
- **One-Hot Encoding**: Creates a binary column for each category. `Red = [1, 0]`, `Green = [0, 1]`.
  - *Drawback*: "Curse of Dimensionality" — causes massive, sparse datasets if cardinality is high.
- **Embeddings**: Learns a dense vector representation for categories during training. Ideal for high-cardinality data like words (Word2Vec) or User IDs.

---

## 📌 3. Gradient Descent & Its Variants

Gradient Descent is the core algorithm used to minimize the cost (loss) function by iteratively updating the model's weights in the opposite direction of the gradient.

### 1. Batch Gradient Descent (BGD)
- **How it works**: Calculates the error for the **entire training dataset**, then updates the weights once.
- **Pros**: Stable error gradient and convergence.
- **Cons**: Extremely slow and memory-intensive for large datasets. Cannot update weights dynamically as new data arrives.

### 2. Stochastic Gradient Descent (SGD)
- **How it works**: Updates the weights for **every single training example**.
- **Pros**: Very fast, uses little memory. Can escape shallow local minima due to high variance/noise in updates.
- **Cons**: High variance causes the loss to fluctuate heavily, meaning it might never settle exactly at the global minimum.

### 3. Mini-Batch Gradient Descent (MBGD)
- **How it works**: The "Goldilocks" approach. Splits the data into small batches (e.g., 32, 64, 128) and performs an update after each batch.
- **Pros**: Balances the robustness of SGD and the efficiency of BGD. Takes advantage of hardware (GPU) matrix vectorization. **This is the industry standard.**

---

## 📌 4. Optimization Algorithms (Beyond Standard SGD)

Standard SGD can struggle with ravines (surfaces curving much more steeply in one dimension) and saddle points. Optimizers accelerate training and navigate complex loss landscapes.

### 1. Momentum
- **What it is**: Adds a fraction of the *previous* update vector to the current update.
- **Analogy**: A ball rolling down a hill gathers momentum, rolling faster and blasting through small local minima.
- **When to use**: When standard SGD is oscillating too much in ravines.

### 2. Adagrad (Adaptive Gradient Algorithm)
- **What it is**: Adapts the learning rate individually for each weight. It lowers the learning rate for frequently occurring features and increases it for rare features.
- **Pros**: Good for sparse data (e.g., NLP).
- **Cons**: The learning rate shrinks constantly and eventually becomes so small that the model stops learning entirely.

### 3. RMSprop (Root Mean Square Propagation)
- **What it is**: Fixes Adagrad's diminishing learning rate by using an exponentially decaying average of past squared gradients. 
- **When to use**: Excellent for Recurrent Neural Networks (RNNs) and handling non-stationary objectives.

### 4. Adam (Adaptive Moment Estimation)
- **What it is**: The ultimate combination of **Momentum** (keeps track of past gradients) and **RMSprop** (adapts learning rates based on recent squared gradients).
- **When to use**: **Default choice for almost all Deep Learning tasks.** It requires little tuning, converges quickly, and handles sparse gradients and noisy data exceptionally well.

---

## 📌 5. Regularization & Preventing Overfitting

Overfitting occurs when a model memorizes noise in the training data and fails to generalize to unseen data.

### 1. Dropout
- **Mechanism**: Randomly deactivates a percentage of neurons (e.g., 50%) during each training forward-pass.
- **Why it works**: Prevents neurons from co-adapting (relying on specific neighbor neurons). Forces the network to distribute learned representations across the entire network.
- **Important**: Only applied during **training**. During testing/inference, all neurons are active, but their weights are scaled down to compensate.

### 2. Early Stopping
- **Mechanism**: Monitors the Validation Loss during training. If the Training Loss decreases but the Validation Loss starts to rise, training is halted immediately to prevent overfitting.

### 3. L1 & L2 Regularization (Weight Decay)
- Adds a penalty to the loss function based on the size of the weights.
- **L1 (Lasso)**: Penalizes the absolute value of weights. Can drive some weights to exactly zero (Feature Selection).
- **L2 (Ridge)**: Penalizes the squared value of weights. Prevents any single weight from becoming too large. (Most commonly used in NNs).

---

## 📌 6. Activation Functions & Hebbian Learning

### Sigmoid Function Properties
- **Weight ($w$)**: Controls steepness. Large $|w|$ = sharp, step-like transition. Small $|w|$ = smooth, gradual transition. Negative $w$ flips the curve horizontally.
- **Bias ($b$)**: Controls the midpoint. Increasing $b$ shifts the curve left (easier to activate). Decreasing $b$ shifts it right.

### Hebbian Learning Rule
"Neurons that fire together, wire together." Weight update is based on the product of input and target.
Formula: $w_{new} = w_{old} + X_i \cdot y$

### Python Implementation (AND Gate using Bipolar Logic)

```python
import numpy as np

weights = np.array([0.0, 0.0])
bias = 0.0

# Bipolar inputs/targets for AND Gate (-1 is False, 1 is True)
inputs = np.array([ [-1, -1], [-1, 1], [1, -1], [1, 1] ])
targets = np.array([-1, -1, -1, 1]) 

# Hebbian Learning Loop
for i in range(len(inputs)):
    weights += inputs[i] * targets[i]  # w_new = w_old + x*y
    bias += targets[i]                 # b_new = b_old + y

print("Trained Weights:", weights)
print("Trained Bias:", bias)

def predict(x):
    return 1 if (np.dot(weights, x) + bias) > 0 else -1
```

---

## 🎯 Viva Questions & Answers

### Preprocessing & Regularization
**Q1. Why do we prefer Standardization over Normalization in Neural Networks?**
**A**: Standardization centers the data at zero. This keeps activation functions like Sigmoid and Tanh in their linear, non-saturated regions initially, preventing the vanishing gradient problem early in training.

**Q2. What is the Curse of Dimensionality in One-Hot Encoding?**
**A**: If a categorical feature has 10,000 unique values, One-Hot Encoding creates 10,000 new columns. This massively increases the computational cost and makes the dataset sparse, leading to overfitting.

**Q3. Is Dropout applied during model testing?**
**A**: No, Dropout is only used during training. During testing, the full network is used, but the weights are multiplied by the dropout probability to ensure the output signal remains balanced.

### Gradient Descent & Optimizers
**Q4. Why is Mini-Batch Gradient Descent preferred over Batch or Stochastic Gradient Descent?**
**A**: Batch GD is too slow and memory-heavy. Stochastic GD is too noisy and fluctuates wildly. Mini-Batch strikes the perfect balance—it is computationally efficient (leverages GPU matrix multiplication) while providing a stable, fast convergence.

**Q5. How does the Adam Optimizer work?**
**A**: Adam combines the best parts of Momentum and RMSprop. It computes adaptive learning rates for each parameter by calculating an exponentially decaying average of past gradients (like Momentum) and past squared gradients (like RMSprop).

**Q6. What happens if the Learning Rate is too high or too low?**
**A**: If too high, the optimizer may overshoot the global minimum and diverge. If too low, training will be excruciatingly slow and the model may get stuck in a shallow local minimum.

**Q7. What problem does Adagrad have that RMSprop fixes?**
**A**: Adagrad aggressively decreases the learning rate over time. Eventually, the learning rate becomes so infinitesimally small that the network completely stops learning. RMSprop fixes this by using a decaying moving average, preventing the learning rate from vanishing.

### Architecture & Hebbian
**Q8. What is Lateral Feedback?**
**A**: It is when the output of a neuron is fed back to other neurons within the *same* layer, heavily used in Self-Organizing Maps (SOMs) for competitive learning.

**Q9. Why use Bipolar [-1, 1] instead of Binary [0, 1] in Hebbian Learning?**
**A**: In Hebbian learning ($w = w + x \cdot y$), if an input feature $x$ is 0, the weight update is zero. The network learns nothing from zero inputs. Bipolar values ensure every input contributes to the weight update.
