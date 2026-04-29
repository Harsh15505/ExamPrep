# Pseudorandom Number Generators (PRNG)

## Theoretical Background

A Pseudorandom Number Generator (PRNG) is an algorithm for generating a sequence of numbers whose properties approximate the properties of sequences of random numbers. The PRNG-generated sequence is not truly random, because it is completely determined by an initial value, called the PRNG's seed.

### 1. Linear Congruential Generator (LCG)
The LCG is one of the oldest and best-known pseudorandom number generator algorithms. The theory behind them is relatively easy to understand, and they are easily implemented and fast, especially on computer hardware which can provide modulo arithmetic by storage-bit truncation.

**Formula:**
$$X_{n+1} = (a \cdot X_n + c) \pmod m$$
- $X$ is the sequence of pseudorandom values.
- $m$ ($0 < m$) is the "modulus".
- $a$ ($0 < a < m$) is the "multiplier".
- $c$ ($0 \le c < m$) is the "increment".
- $X_0$ ($0 \le X_0 < m$) is the "seed" or "start value".

### 2. Blum Blum Shub (BBS) Generator
The Blum Blum Shub (BBS) is a pseudorandom number generator proposed in 1986 by Lenore Blum, Manuel Blum and Michael Shub. Its security reduces strictly to the computational difficulty of integer factorization (specifically, the quadratic residuosity problem).

**Algorithm:**
- Generate two large prime numbers, $p$ and $q$, such that $p \equiv 3 \pmod 4$ and $q \equiv 3 \pmod 4$ (Blum primes).
- Compute $M = p \cdot q$.
- Choose a random seed $s$ relatively prime to $M$.
- Initial State: $x_0 = s^2 \pmod M$.
- Sequence Generation: $x_{i} = x_{i-1}^2 \pmod M$.
- For each step, output the parity bit or the Least Significant Bit (LSB) of $x_i$.

---

## Line-by-Line Code Breakdown (`PRNG.py`)

### Linear Congruential Generator

```python
def linear_congruential_generator(seed, a, c, m, num_values):
    values = []
    current = seed
    for _ in range(num_values):
        current = (a * current + c) % m
        values.append(current)
    return values
```
**Explanation:** 
- Initializes the sequence with the provided `seed`.
- Loops `num_values` times.
- In each iteration, applies the core LCG equation: `current = (a * current + c) % m`.
- Appends the generated integer to the `values` array and returns it.

### Blum Blum Shub Generator

```python
def blum_blum_shub_generator(p, q, seed, num_bits):
    m = p * q
    
    # x_0 = seed^2 mod m
    current = (seed * seed) % m
```
**Explanation:** 
- Calculates the modulus $M = p \cdot q$. 
- Calculates the initial state $x_0 = s^2 \pmod M$ using the provided seed.

```python
    bits = []
    for _ in range(num_bits):
        # x_i = (x_{i-1})^2 mod m
        current = (current * current) % m
        # Extract least significant bit
        bits.append(current % 2)
        
    return bits
```
**Explanation:**
- Loops to generate the requested number of bits (`num_bits`).
- Calculates the next quadratic residue: `x_i = (x_{i-1})^2 mod m`.
- Extracts the Least Significant Bit (LSB) using `current % 2`. This operation guarantees the cryptographic unpredictability of the sequence, assuming $M$ is exceptionally hard to factor.
- Appends the bit (0 or 1) to the sequence and returns it.

### Main Execution

```python
def main():
    # LCG Example Parameters
    a = 1103515245
    c = 12345
    m = 2**31
    seed_lcg = 42
    num_values = 5
    
    # BBS Example Parameters
    p = 11
    q = 19
    seed_bbs = 3
    num_bits = 15
```
**Explanation:** The main block defines standard parameters. For LCG, it uses the constants historically associated with `glibc`. For BBS, it uses small primes $p=11$ and $q=19$ (which both satisfy $11 \pmod 4 = 3$ and $19 \pmod 4 = 3$) for demonstration purposes.

---

## Potential Viva Questions & Tricky Questions

**Q1: Why is the Linear Congruential Generator (LCG) not considered cryptographically secure?**
*Answer:* LCG outputs are highly predictable. If an attacker observes a small sequence of output numbers, they can easily set up a system of linear equations to solve for the unknown parameters ($a, c, m$) and the internal state, allowing them to predict all past and future values.

**Q2: What is a "Blum prime" in the context of the BBS generator?**
*Answer:* A Blum prime is a prime number $p$ that satisfies the congruence $p \equiv 3 \pmod 4$. BBS requires two distinct Blum primes. This property ensures that every quadratic residue modulo $M = p \cdot q$ has exactly one square root that is also a quadratic residue, which is necessary for the security proof of the algorithm.

**Q3: Why does BBS extract only the Least Significant Bit (LSB) instead of using the whole number $x_i$?**
*Answer:* Releasing the entire state $x_i$ would immediately reveal the sequence and allow an attacker to compute $x_{i+1}$. Releasing only the LSB (or a very small number of bits like $\log_2(\log_2 M)$) ensures that predicting the next bit is computationally as hard as factoring the modulus $M$.

**Q4: What distinguishes a True Random Number Generator (TRNG) from a Pseudorandom Number Generator (PRNG)?**
*Answer:* A TRNG derives its randomness from unpredictable physical phenomena (like atmospheric noise or radioactive decay). A PRNG uses a deterministic mathematical algorithm, meaning if you know the initial seed and the algorithm, you can perfectly recreate the entire sequence.

**Q5: Why is the seed value crucial in a PRNG?**
*Answer:* The seed is the starting state of the deterministic algorithm. If two identical PRNGs are initialized with the exact same seed, they will produce the exact same sequence of numbers.

**Q6: Can the LCG algorithm be used for generating cryptographic keys? Why or why not?**
*Answer:* Absolutely not. LCG is highly predictable and statistically flawed (e.g., lower-order bits often alternate or follow simple patterns). An attacker can easily deduce the internal state from a few outputs and predict all future keys.

**Q7: What is the period of a PRNG, and why is a long period desirable?**
*Answer:* The period is the number of values a PRNG generates before the sequence begins to repeat itself. A long period is desirable because repeating sequences can introduce vulnerabilities in cryptographic protocols and ruin the statistical distribution in simulations.

**Q8: What happens if an attacker knows the seed of a PRNG used in a stream cipher?**
*Answer:* They can generate the exact same keystream as the legitimate users. By XORing this keystream against the intercepted ciphertext, they can instantly decrypt all communications.

**Q9: Explain the Quadratic Residuosity Problem in the context of the BBS generator.**
*Answer:* It is the mathematical problem of determining whether a given number $a$ is a perfect square modulo $M$ (where $M = p \cdot q$). Without knowing the prime factors $p$ and $q$, it is computationally extremely difficult to determine the square root, making the BBS forward and backward unpredictable.

**Q10: How does the choice of $m$ (modulus) in LCG affect its period?**
*Answer:* The modulus $m$ dictates the absolute maximum possible period of the LCG (which is $m$). To achieve the maximum full period, specific mathematical conditions (Hull-Dobell Theorem) must be met between $a, c,$ and $m$ (e.g., $c$ and $m$ must be relatively prime).
