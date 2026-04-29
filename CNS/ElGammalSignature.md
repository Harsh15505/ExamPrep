# ElGamal Digital Signature Scheme

## Theoretical Background

The **ElGamal Digital Signature Scheme** is an asymmetric cryptographic mechanism that allows a party to prove the authenticity and integrity of a message. Unlike the ElGamal encryption scheme which hides the message, the signature scheme binds the message to the sender's identity.

![Digital Signature Process](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Digital_Signature_diagram.svg/512px-Digital_Signature_diagram.svg.png)
*(General Digital Signature Verification Process)*

### Security Basis
Like its encryption counterpart, the security relies on the **Discrete Logarithm Problem (DLP)**. The signature proves that the sender possessed the private key without actually revealing it.

### Algorithm Steps

1. **Key Generation**
   - Choose a prime $p$ and a generator $\alpha$ (often written as $g$).
   - Choose a private key $x$ ($1 < x < p-1$).
   - Compute public key $y = \alpha^x \pmod p$.
   - **Public:** $(p, \alpha, y)$
   - **Private:** $x$

2. **Signing a Message ($M$)**
   - Hash the message: $m = H(M)$.
   - Choose a random $k$ such that $1 < k < p-1$ and $\gcd(k, p-1) = 1$.
   - Compute $S_1 = \alpha^k \pmod p$.
   - Compute $k^{-1} \pmod{p-1}$.
   - Compute $S_2 = k^{-1} \cdot (m - x \cdot S_1) \pmod{p-1}$.
   - The signature is $(S_1, S_2)$.

3. **Verification**
   - Hash the message: $m = H(M)$.
   - Compute $V_1 = \alpha^m \pmod p$.
   - Compute $V_2 = (y^{S_1} \cdot S_1^{S_2}) \pmod p$.
   - The signature is valid if and only if $V_1 \equiv V_2 \pmod p$.

---

## Line-by-Line Code Breakdown (`ElGammalSignature.py`)

### Mathematical Utility Functions

```python
def mod_inverse(a, m):
    m0 = m
    x0, x1 = 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1
```
**Explanation:** Implements the **Extended Euclidean Algorithm** to efficiently find the modular inverse. This is significantly faster and more robust than the linear search approach. It calculates $x$ such that $(a \cdot x) \pmod m = 1$.

```python
def hash_message(message):
    return int.from_bytes(hashlib.sha256(message.encode()).digest(), 'big')
```
**Explanation:** Converts the string message into a byte array, computes its SHA-256 cryptographic hash, and then converts the resulting 256-bit digest into a large integer format suitable for modular arithmetic.

### Core Cryptographic Functions

```python
def generate_keys(p, alpha):
    x = random.randint(2, p - 2)
    y = pow(alpha, x, p)
    return x, (p, alpha, y)
```
**Explanation:** Chooses a random private key $x$, computes $y = \alpha^x \pmod p$ (using Python's highly optimized built-in `pow` function), and returns the private/public keypair.

```python
def sign_message(message, p, alpha, private_key):
    m = hash_message(message)
    x = private_key
    while True:
        k = random.randint(2, p - 2)
        if gcd(k, p - 1) != 1:
            continue
        
        s1 = pow(alpha, k, p)
        k_inv = mod_inverse(k, p - 1)
        s2 = (k_inv * (m - x * s1)) % (p - 1)
        
        if s1 != 0 and s2 != 0:
            return (s1, s2)
```
**Explanation:**
- Hashes the message to integer $m$.
- Enters a loop to securely pick the ephemeral key $k$. It *must* be coprime to $p-1$ to ensure that $k^{-1} \pmod{p-1}$ exists. If $\gcd(k, p-1) \ne 1$, it rerolls $k$.
- Computes $S_1 = \alpha^k \pmod p$.
- Calculates the inverse of $k \pmod{p-1}$. Note the modulus is $p-1$, not $p$, derived from Fermat's Little Theorem.
- Calculates $S_2$. Ensures neither signature component is zero before returning the tuple `(s1, s2)`.

```python
def verify_signature(message, signature, p, alpha, y):
    s1, s2 = signature
    m = hash_message(message)

    v1 = pow(alpha, m, p)
    v2 = (pow(y, s1, p) * pow(s1, s2, p)) % p

    return v1 == v2
```
**Explanation:**
- Recalculates the integer hash $m$ of the received message.
- Computes the verification left-hand side $V_1 = \alpha^m \pmod p$.
- Computes the verification right-hand side $V_2 = y^{S_1} \cdot S_1^{S_2} \pmod p$.
- Returns a boolean indicating if the signature is valid.

---

## Potential Viva Questions & Tricky Questions

**Q1: Why is the modulus for calculating $S_2$ set to $(p-1)$ instead of $p$?**
*Answer:* Because the calculation of $S_2$ occurs in the exponent of the generator $\alpha$. According to Fermat's Little Theorem and group theory, calculations in the exponent of a modulo $p$ group wrap around at $p-1$ (the order of the group).

**Q2: In the signing process, what happens if $k$ is not relatively prime to $p-1$?**
*Answer:* If $\gcd(k, p-1) \ne 1$, then the modular inverse $k^{-1} \pmod{p-1}$ does not exist. The algorithm would fail when trying to calculate $S_2$. That is why we must keep generating a random $k$ until one is found that is coprime to $p-1$.

**Q3: What happens if the random value $k$ is leaked or predicted?**
*Answer:* If $k$ is known, an attacker can solve the equation $S_2 = k^{-1}(m - x S_1) \pmod{p-1}$ to find the private key $x$, compromising the entire signature scheme.

**Q4: How does the ElGamal Signature Scheme provide Non-Repudiation?**
*Answer:* Since the private key $x$ is required to generate a valid signature $(S_1, S_2)$, and only the sender possesses $x$, the sender cannot later deny having signed the message if the signature successfully verifies against their public key $y$.

**Q5: Why is it crucial to use a cryptographically secure hash function like SHA-256 before signing?**
*Answer:* Hashing maps any arbitrary-length message to a fixed-size integer suitable for modular arithmetic. More importantly, it prevents existential forgery attacks. Without a hash, an attacker could mathematically manipulate a valid signature into a new signature for a garbage message.

**Q6: What vulnerability arises if the hash function used is prone to collisions?**
*Answer:* If an attacker can find two different messages $M_1$ and $M_2$ that produce the same hash $m$, then the signature for $M_1$ will perfectly verify for $M_2$. The attacker could trick the signer into signing a benign document ($M_1$) and attach that signature to a malicious document ($M_2$).

**Q7: Can an attacker forge a signature if they don't know the private key $x$?**
*Answer:* Not without solving the Discrete Logarithm Problem. To create a valid $(S_1, S_2)$, the attacker would need to calculate $y = \alpha^x \pmod p$ backward to find $x$, which is computationally infeasible for large primes.

**Q8: Explain the difference between encryption keys and signature keys in ElGamal.**
*Answer:* While the underlying keys $(p, \alpha, x, y)$ are mathematically identical in both schemes, they are used differently. In encryption, the *sender* uses the *receiver's* public key to hide data. In signatures, the *sender* uses their *own* private key to bind their identity to the data.

**Q9: What happens if the verification equation $V_1 \equiv V_2 \pmod p$ evaluates to false?**
*Answer:* It means the signature is invalid. This could be due to three reasons: the message was tampered with in transit, the signature was tampered with, or the signature was not generated by the owner of the claimed public key.

**Q10: Why does the signature consist of two parts $(S_1, S_2)$?**
*Answer:* $S_1$ is essentially a commitment to the random ephemeral key $k$ (since $S_1 = \alpha^k \pmod p$). $S_2$ uses $k$ and the private key $x$ to mathematically bind the message $m$ to $S_1$. Both are required by the verifier to cancel out the unknowns and prove ownership of $x$.
