# ElGamal Public-Key Encryption Scheme

## Theoretical Background

The **ElGamal encryption system** is an asymmetric key encryption algorithm for public-key cryptography which is based on the Diffie–Hellman key exchange. It was described by Taher Elgamal in 1985. 

![Public Key Encryption Concept](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Public_key_encryption.svg/512px-Public_key_encryption.svg.png)
*(General Public Key Encryption Process)*

### Cryptographic Foundation
The security of the ElGamal encryption scheme is rooted in the **Discrete Logarithm Problem (DLP)**. While it is computationally easy to calculate $h = g^x \pmod p$, it is practically impossible to find the private key $x$ given only $p$, $g$, and $h$.

### Algorithm Steps

1. **Key Generation**
   - Choose a large prime number $p$.
   - Choose a generator $g$ of the multiplicative group $\mathbb{Z}^*_p$.
   - Choose a private key $x$ such that $1 \le x \le p-2$.
   - Compute $h = g^x \pmod p$.
   - **Public Key:** $(p, g, h)$
   - **Private Key:** $x$

2. **Encryption**
   - For a message $m$, choose a random ephemeral key $k$ where $1 \le k \le p-2$.
   - Compute ciphertext pair $(C_1, C_2)$:
     - $C_1 = g^k \pmod p$
     - $C_2 = m \cdot h^k \pmod p$

3. **Decryption**
   - Calculate the shared secret using the private key: $s = C_1^x \pmod p$.
   - Find the modular inverse of $s$: $s^{-1} \pmod p$.
   - Recover the message: $m = C_2 \cdot s^{-1} \pmod p$.

> [!NOTE]
> **Probabilistic Nature:** Because a new random $k$ is chosen for every encryption, encrypting the exact same message with the same public key yields completely different ciphertexts.

---

## Line-by-Line Code Breakdown (`ElGammal.py`)

### Helper Functions

```python
def powerMod(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if (exponent % 2) == 1:
            result = (result * base) % modulus
        exponent = exponent // 2
        base = (base * base) % modulus
    return result
```
**Explanation:** This is a custom implementation of Fast Modular Exponentiation (also known as exponentiation by squaring). It efficiently calculates `(base^exponent) % modulus` in $O(\log(\text{exponent}))$ time.

```python
def moduloInverse(x, modulo):
    inverse = -1
    x = x % modulo
    if x < 0:
        x += modulo
    for i in range(1, modulo):
        if (x * i) % modulo == 1:
            inverse = i
            break
    return inverse
```
**Explanation:** This finds the modular inverse of $x$ modulo $p$. It uses a naive linear search, checking every number from $1$ to $modulo - 1$ to see if `(x * i) % modulo == 1`. It is suitable for small educational primes, but in real scenarios, the Extended Euclidean Algorithm should be used.

### Core Cryptographic Functions

```python
def generatePublicKey(p, g, x):
    h = powerMod(g, x, p)
    return (p, g, h)
```
**Explanation:** Generates the public key component $h$ using the formula $h = g^x \pmod p$ and returns the public key tuple.

```python
def encrypt(plaintext, public_key):
    p, g, h = public_key
    ciphertext = []
    for char in plaintext:
        m = ord(char)
        k = random.randint(1, p - 2)
        c1 = powerMod(g, k, p)
        c2 = (m * powerMod(h, k, p)) % p
        ciphertext.append((c1, c2))
    return ciphertext
```
**Explanation:** 
- Iterates over the string character by character.
- Converts the character to its ASCII numerical value $m$.
- Picks a random integer $k$ for **each** character.
- Calculates $C_1 = g^k \pmod p$.
- Calculates $C_2 = m \cdot h^k \pmod p$.
- Appends the tuple `(c1, c2)` to the ciphertext array.

```python
def decrypt(ciphertext, private_key):
    p, g, x = private_key
    decrypted_text = ""
    for c1, c2 in ciphertext:
        s = powerMod(c1, x, p)
        s_inv = moduloInverse(s, p)
        m = (c2 * s_inv) % p
        decrypted_text += chr(m)
    return decrypted_text
```
**Explanation:** 
- Loops through each ciphertext tuple `(c1, c2)`.
- Reconstructs the shared secret $s = C_1^x \pmod p$.
- Finds the modular inverse $s^{-1}$.
- Recovers the ASCII character value $m = C_2 \cdot s^{-1} \pmod p$ and converts it back to a character, appending it to the final string.

### Main Execution Block

```python
def main():
    p = 683
    g = 2
    x = 15
    # ... handles input, generation, encryption, and decryption prints ...
```
**Explanation:** The entry point sets up the global domain parameters ($p=683$, $g=2$) and the chosen private key ($x=15$), then runs a demonstration of the full cycle.

---

## Potential Viva Questions & Tricky Questions

**Q1: How is ElGamal encryption different from RSA encryption?**
*Answer:* RSA relies on the integer factorization problem, whereas ElGamal relies on the Discrete Logarithm Problem (DLP). Furthermore, textbook RSA is deterministic (same plaintext yields same ciphertext), while ElGamal is natively probabilistic (same plaintext yields different ciphertexts due to the random ephemeral key $k$).

**Q2: What happens if the ephemeral key $k$ is reused for different messages?**
*Answer:* It completely breaks the encryption. If $k$ is reused, an attacker who knows one plaintext message can compute the shared secret $h^k$, and then immediately decrypt all other messages that used the same $k$ without needing the private key.

**Q3: Is ElGamal encryption secure against Chosen Ciphertext Attacks (CCA)?**
*Answer:* No, textbook ElGamal is homomorphic with respect to multiplication. An attacker can multiply the ciphertext pair $(C_1, C_2)$ by some factor to predictably alter the decrypted plaintext.

**Q4: What is the role of the generator $g$ in the ElGamal encryption scheme?**
*Answer:* The generator $g$ is a primitive root modulo $p$. It ensures that its powers $g^1, g^2, \dots, g^{p-1}$ generate all possible elements in the multiplicative group $\mathbb{Z}^*_p$, maximizing the key space and security against discrete logarithm attacks.

**Q5: Why must the ephemeral key $k$ be kept strictly secret?**
*Answer:* The ephemeral key $k$ acts as a one-time pad for the message. If an attacker discovers $k$, they can easily calculate $s = h^k \pmod p$, find its modular inverse, and decrypt the message $C_2$ without needing the private key $x$.

**Q6: How does the size of the prime $p$ affect the security and performance of ElGamal?**
*Answer:* A larger prime $p$ exponentially increases security against discrete logarithm solvers (like the General Number Field Sieve), but it linearly increases the computational time for exponentiation, slowing down encryption and decryption.

**Q7: Can ElGamal encryption be used for digital signatures?**
*Answer:* The exact encryption algorithm cannot be used directly, but the mathematical foundation (ElGamal over DLP) was adapted by Taher Elgamal to create the ElGamal Digital Signature scheme, which uses a different signing and verifying procedure.

**Q8: Describe the Diffie-Hellman key exchange and its relation to ElGamal encryption.**
*Answer:* Diffie-Hellman allows two parties to securely establish a shared secret $s = g^{xy} \pmod p$ over a public channel. ElGamal encryption is essentially a Diffie-Hellman key exchange where the shared secret is immediately used to multiply (encrypt) the message $m$.

**Q9: Why does ElGamal ciphertext have a size that is twice the size of the plaintext? (Ciphertext expansion)**
*Answer:* Because for every single plaintext message block $m$, the algorithm produces two ciphertext blocks: $C_1$ (the hint to reconstruct the shared secret) and $C_2$ (the actual encrypted payload).

**Q10: What is the purpose of the modular inverse in the decryption phase of ElGamal?**
*Answer:* The message is hidden inside $C_2$ via modular multiplication: $C_2 = m \cdot s \pmod p$. In finite field arithmetic, division is not possible, so to "divide" by $s$ and isolate $m$, we must multiply by the modular multiplicative inverse of $s$.
