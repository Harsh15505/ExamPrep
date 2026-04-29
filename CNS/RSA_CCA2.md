# RSA Encryption and Chosen Ciphertext Attack (CCA2)

## Theoretical Background

**RSA (Rivest–Shamir–Adleman)** is one of the oldest and most widely used public-key cryptosystems for secure data transmission. The acronym stands for the surnames of its inventors.

### Core Mathematical Foundation
The security of RSA relies on the practical difficulty of factoring the product of two large prime numbers, the "factoring problem".

1. **Key Generation:**
   - Choose two distinct large random prime numbers $p$ and $q$.
   - Compute $n = pq$.
   - Compute the totient $\phi(n) = (p-1)(q-1)$.
   - Choose an integer $e$ such that $1 < e < \phi(n)$ and $\gcd(e, \phi(n)) = 1$.
   - Determine $d$ as $d \equiv e^{-1} \pmod{\phi(n)}$ (i.e., $d$ is the modular multiplicative inverse of $e$ modulo $\phi(n)$).
   - **Public Key:** $(e, n)$
   - **Private Key:** $(d, n)$

2. **Encryption:** $C = M^e \pmod n$
3. **Decryption:** $M = C^d \pmod n$

### The Malleability Problem (CCA2)
Textbook RSA is **malleable**, meaning an attacker can intercept a ciphertext $C$, multiply it by some value $S^e \pmod n$, and pass it to the receiver. When the receiver decrypts it, they will extract $M \cdot S$ instead of the original $M$. This is simulated in the code as a Chosen Ciphertext Attack property demonstration.

---

## Line-by-Line Code Breakdown (`RSA_CCA2.py`)

### Helper Math Functions

```python
def powerMod(base, exponent, modulus):
    # Fast Modular Exponentiation loop...
    return result

def moduloInverse(x, modulo):
    # Linear search for modular inverse...
    return inverse

def gcd(a, b):
    # Euclidean algorithm for Greatest Common Divisor...
    return a
```
**Explanation:** These are standard utility functions implemented from first principles. `powerMod` computes large exponents efficiently. `moduloInverse` linearly searches for the private exponent $d$ (fine for lab exams, slow for real RSA). `gcd` ensures the chosen public exponent $e$ is coprime to $\phi(n)$.

### Key Generation

```python
def generateKeys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 2
    while gcd(e, phi) != 1:
        e += 1
    d = moduloInverse(e, phi)
    return (e, n), (d, n)
```
**Explanation:** 
- Calculates the modulus $n$ and the totient $\phi(n)$.
- It starts searching for $e$ from $2$ upwards. The first value that satisfies $\gcd(e, \phi) = 1$ is chosen as the public exponent.
- Uses `moduloInverse` to find the corresponding private exponent $d$.
- Returns the public and private key tuples.

### Basic Encryption & Decryption

```python
def encrypt(plaintext, public_key):
    e, n = public_key
    ciphertext = []
    for char in plaintext:
        m = ord(char)
        c = powerMod(m, e, n)
        ciphertext.append(c)
    return ciphertext
```
**Explanation:** Iterates through every character in the plaintext, converts it to its integer ASCII equivalent `m`, and applies the RSA encryption formula $c = m^e \pmod n$. 

```python
def decrypt(ciphertext, private_key):
    d, n = private_key
    plaintext = ""
    for c in ciphertext:
        m = powerMod(c, d, n)
        plaintext += chr(m)
    return plaintext
```
**Explanation:** Applies the reverse formula $m = c^d \pmod n$ to each integer in the ciphertext array, returning the characters back to a readable string.

### Chosen Ciphertext Attack 2 (CCA2) Simulation

```python
def CCA2(ciphertext, p, q, S):
    public_key, private_key = generateKeys(p,q)
    e, n = public_key
    
    # Attacker intercepts C and multiplies by S^e
    S_e = powerMod(S, e, n)
    newciphertext = []
    for c in ciphertext:
        newciphertext.append((c * S_e) % n)
```
**Explanation:** This simulates an attacker modifying an encrypted message in transit. The attacker doesn't know $M$, but they want the receiver to decrypt a modified version of it (specifically $M \cdot S$). The attacker computes $S^e \pmod n$ using the public key and multiplies it into the intercepted ciphertext.

```python
    d, n = private_key
    M_dash = []
    for c in newciphertext:
        m = powerMod(c, d, n)
        M_dash.append(m)

    # ... recovery of original M from the tampered M_dash ...
```
**Explanation:** The receiver innocently decrypts the `newciphertext` thinking it is legitimate, resulting in `M_dash` (which is $M \cdot S$). The code then demonstrates that the mathematical relationship holds true by multiplying the output by $S^{-1}$ to prove that the underlying $M$ was predictably altered.

---

## Potential Viva Questions & Tricky Questions

**Q1: If $p=19$ and $q=17$, how do you determine if a number $e$ is a valid public exponent?**
*Answer:* First, calculate $\phi(n) = (19-1)(17-1) = 18 \times 16 = 288$. A valid $e$ must be between $1$ and $288$, and it must be coprime to $288$ ($\gcd(e, 288) = 1$). For example, $e=2, 3, 4, 6$ are not valid because they share factors with $288$, but $e=5$ is valid.

**Q2: What does "RSA is malleable" mean, and how did we demonstrate it in `CCA2`?**
*Answer:* Malleability means a ciphertext can be predictably altered without decrypting it. In textbook RSA, multiplying the ciphertext by $S^e \pmod n$ results in a new ciphertext that perfectly decrypts to $M \times S \pmod n$. We demonstrated this by modifying the ciphertext in transit and verifying the decrypted plaintext was tampered.

**Q3: How do modern systems fix the textbook RSA malleability vulnerability?**
*Answer:* By using padding schemes like **OAEP** (Optimal Asymmetric Encryption Padding). OAEP adds randomness and structure to the plaintext before encryption, meaning any algebraic tampering with the ciphertext will result in an invalid structure upon decryption, and the receiver will reject it.

**Q4: Explain the difference between Symmetric and Asymmetric encryption, and where RSA fits.**
*Answer:* Symmetric encryption uses the same key for both encryption and decryption (e.g., DES, AES). Asymmetric encryption uses a pair of keys: a public key for encryption and a private key for decryption. RSA is the quintessential asymmetric encryption algorithm.

**Q5: What is the significance of Euler's Totient Function $\phi(n)$ in RSA?**
*Answer:* $\phi(n)$ counts the number of integers up to $n$ that are relatively prime to $n$. According to Euler's theorem, $a^{\phi(n)} \equiv 1 \pmod n$. RSA uses this property to ensure that decrypting an encrypted message reverses the exponentiation: $M^{ed} \equiv M^{1} \pmod n$.

**Q6: Why must $p$ and $q$ be kept secret in RSA, even though $n$ is public?**
*Answer:* If an attacker knows $p$ and $q$, they can easily calculate $\phi(n) = (p-1)(q-1)$. With $\phi(n)$ and the public exponent $e$, they can instantly calculate the private exponent $d$ using the Extended Euclidean Algorithm, completely compromising the system.

**Q7: How would an attacker theoretically try to break an RSA encrypted message if they intercepted it?**
*Answer:* The most direct theoretical attack is integer factorization: trying to factor the public modulus $n$ back into its prime components $p$ and $q$. If successful, they derive the private key.

**Q8: What is the "padding oracle attack" and how does padding like OAEP mitigate it?**
*Answer:* A padding oracle attack exploits servers that return different error messages depending on whether the decrypted RSA padding is valid or invalid, allowing attackers to slowly decrypt the message. OAEP mitigates this by using randomized cryptographic hashing to structure the padding, making it impossible to manipulate without destroying the structure entirely.

**Q9: In your implementation, what would happen if $e$ was chosen such that $\gcd(e, \phi(n)) \neq 1$?**
*Answer:* If $e$ and $\phi(n)$ share a common factor, then the modular multiplicative inverse of $e \pmod{\phi(n)}$ does not exist. The algorithm would be fundamentally unable to generate a private key $d$.

**Q10: Why is RSA typically used for encrypting session keys rather than large volumes of data?**
*Answer:* RSA involves heavy mathematical operations (modular exponentiation of huge numbers), making it very slow computationally compared to symmetric ciphers like AES. Therefore, RSA is used to securely exchange a small AES session key, and AES is then used to encrypt the actual large data volume.
