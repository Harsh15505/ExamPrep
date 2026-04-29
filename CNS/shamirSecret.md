# Shamir's Secret Sharing Scheme

## Theoretical Background

**Shamir's Secret Sharing (SSS)** is an algorithm in cryptography created by Adi Shamir. It is a form of secret sharing, where a secret is divided into parts (shares), giving each participant its own unique part. 

To reconstruct the original secret, a minimum number of parts (the threshold) must be combined. This is often referred to as a **$(k, n)$ threshold scheme**.

![Shamir Polynomial Curve](https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Shamir_secret_sharing_example.svg/512px-Shamir_secret_sharing_example.svg.png)
*(A generic $(k=3)$ polynomial curve where any 3 points perfectly reconstruct the y-intercept)*

### Mathematical Foundation

The scheme relies on the mathematical principle that it takes $k$ points to define a polynomial of degree $k-1$. 
- It takes 2 points to define a line (degree 1).
- It takes 3 points to define a parabola (degree 2).
- It takes $k$ points to define a polynomial of degree $k-1$.

### Algorithm Steps

1. **Setup & Splitting the Secret:**
   - Let $S$ be the secret to share.
   - Choose a large prime $p$ such that $p > S$ and $p > n$. All math will be done modulo $p$.
   - To create a $(k, n)$ threshold scheme, construct a random polynomial $f(x)$ of degree $k-1$:
     $$f(x) = a_0 + a_1 x + a_2 x^2 + \dots + a_{k-1} x^{k-1} \pmod p$$
   - Set the constant term $a_0 = S$ (the secret).
   - Generate the remaining coefficients $a_1, \dots, a_{k-1}$ randomly.
   - Generate $n$ shares by evaluating the polynomial at $n$ distinct points (e.g., $x = 1, 2, \dots, n$).
   - A share is a pair $(x, f(x))$.

2. **Reconstruction (Lagrange Interpolation):**
   - Given any $k$ distinct shares $(x_1, y_1), (x_2, y_2), \dots, (x_k, y_k)$, you can reconstruct the polynomial using **Lagrange Interpolation**.
   - Since the secret is $a_0 = f(0)$, we evaluate the interpolated polynomial at $x=0$:
     $$S = f(0) = \sum_{i=1}^{k} y_i \prod_{j \neq i} \frac{-x_j}{x_i - x_j} \pmod p$$

---

## Line-by-Line Code Breakdown (`shamirSecret.py`)

### Helper Function

```python
import random

def modInverse(x, p):
    x = x % p
    if x < 0:
        x += p
    for i in range(1, p):
        if (x * i) % p == 1:
            return i
    return -1
```
**Explanation:** A utility function to calculate the modular multiplicative inverse of `x` modulo `p`. It handles negative `x` values (which occur during the Lagrange interpolation subtraction step) by making them positive modulo `p` before running a linear search.

### Splitting the Secret

```python
def splitSecret(secret, n, k, p):
    coeffs = [secret]
    for _ in range(k - 1):
        coeffs.append(random.randint(1, p - 1))
```
**Explanation:** 
- Initializes the polynomial coefficients array `coeffs`. 
- The very first element `coeffs[0]` (which represents $a_0$) is set to the `secret`.
- A loop runs $k-1$ times to randomly choose the higher-order coefficients $a_1$ through $a_{k-1}$, ensuring they are strictly between $1$ and $p-1$.

```python
    shares = []
    for x in range(1, n + 1):
        y = 0
        for i in range(len(coeffs)):
            y = (y + coeffs[i] * (x ** i)) % p
        shares.append((x, y))
    
    return shares
```
**Explanation:** 
- Iterates $n$ times to generate $n$ shares for participants $1$ through $n$.
- For each participant ID $x$, it evaluates the polynomial $f(x) \pmod p$ using a nested loop over the coefficients.
- The tuple `(x, y)` representing the share is appended to the `shares` list and returned.

### Reconstructing the Secret

```python
def reconstructSecret(shares, p):
    secret = 0
    for i in range(len(shares)):
        xi, yi = shares[i]
        num = 1
        den = 1
```
**Explanation:** 
- Initializes the reconstructed `secret` accumulator to $0$.
- Starts the outer loop over the $k$ provided shares to calculate the Lagrange basis polynomials. For each term, it initializes a `num` (numerator) and `den` (denominator) to $1$.

```python
        for j in range(len(shares)):
            if i != j:
                xj, yj = shares[j]
                num = (num * -xj) % p
                den = (den * (xi - xj)) % p
```
**Explanation:** 
- The inner loop iterates over all other shares to calculate the product $\prod_{j \neq i} \frac{0 - x_j}{x_i - x_j} \pmod p$.
- Notice `0 - xj` is written simply as `-xj`. The numerator and denominator are built up separately.

```python
        term = (yi * num * modInverse(den, p)) % p
        secret = (secret + term) % p
        
    return secret
```
**Explanation:** 
- Instead of performing standard floating-point division (which doesn't exist in finite field cryptography), it multiplies the numerator by the modular inverse of the denominator.
- It multiplies by $y_i$ to complete the term.
- It adds this term to the running `secret` total, and once the loop completes, it returns the exactly reconstructed secret.

---

## Potential Viva Questions & Tricky Questions

**Q1: In a $(k, n)$ threshold scheme, what happens if an attacker compromises $k-1$ shares?**
*Answer:* They learn absolutely nothing about the secret. In Shamir's scheme, having $k-1$ shares leaves the secret completely undetermined; any possible value for the secret is equally likely. This is called "perfect secrecy" (information-theoretically secure).

**Q2: Why do we use finite field arithmetic (modulo a prime $p$) instead of regular floating-point arithmetic for the polynomials?**
*Answer:* If we used regular numbers on a standard continuous graph, an attacker could use geometric approximation (like finding the slope of a line with just 1 point) to narrow down the possible values of the secret. Finite field arithmetic scrambles the graph into discrete points, removing any geometric clues and ensuring perfect secrecy.

**Q3: When reconstructing the secret using Lagrange interpolation, why do we evaluate the polynomial at $x = 0$?**
*Answer:* In the setup phase, the secret is explicitly placed as the constant term $a_0$ of the polynomial $f(x)$. Mathematically, evaluating any polynomial at $x=0$ collapses all terms with an $x$ variable to $0$, leaving only the constant term $a_0$. Therefore, $f(0)$ evaluates exactly to the secret.

**Q4: What is "Information-Theoretic Security" and how does Shamir's scheme achieve it?**
*Answer:* Information-theoretic security means the system cannot be broken even if the attacker has infinite computing power. Shamir's scheme achieves this because, with less than $k$ shares, there are mathematically infinite (or $p$) valid polynomials that could fit the points, making all possible secrets equally probable.

**Q5: In a $(5, 10)$ threshold scheme, can 4 participants ever recreate the secret?**
*Answer:* No. 4 participants only have 4 points. To define a polynomial of degree 4 (which requires 5 points), an infinite number of curves can pass through those 4 points, each intersecting the y-axis at a different secret value $S$.

**Q6: How does adding a new participant to the Shamir scheme work after the initial setup?**
*Answer:* The dealer simply evaluates the original polynomial $f(x)$ at a brand new, previously unused $x$-coordinate (e.g., $x=11$). They hand this new share $(11, f(11))$ to the new participant. This does not affect the existing shares or the threshold $k$.

**Q7: Why is it important that the random coefficients $a_1$ through $a_{k-1}$ are generated securely?**
*Answer:* If an attacker can predict the random number generator used for the coefficients, they can guess the shape of the polynomial. With the shape known, they might only need 1 or 2 shares to deduce the entire polynomial and extract the constant term $a_0$ (the secret).

**Q8: What is a Finite Field (Galois Field), and why is it essential for this scheme?**
*Answer:* A finite field is a set of numbers with a finite number of elements where addition, subtraction, multiplication, and division always result in a number within the set. Using modulo prime $p$ arithmetic ensures that errors in division don't occur and that the geometric predictability of standard polynomials is destroyed.

**Q9: Is it possible to share multiple secrets using the same polynomial?**
*Answer:* It is extremely dangerous. If you evaluate a second secret using the same polynomial, you leak information. To share a new secret securely, an entirely new random polynomial must be generated from scratch.

**Q10: Explain Lagrange Interpolation in your own words as it applies to reconstructing the secret.**
*Answer:* Lagrange interpolation is a mathematical formula that reconstructs a curve perfectly by combining multiple "basis polynomials." In SSS, we don't care about the whole curve, only the y-intercept ($x=0$). The formula allows us to mathematically weigh each participant's $y$-value against the $x$-coordinates of all other participants to extract the exact constant $S$.
