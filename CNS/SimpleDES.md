# Simplified Data Encryption Standard (S-DES) & Brute Force Attack

## Theoretical Background (S-DES)

Simplified DES (S-DES) is an educational symmetric-key encryption algorithm designed by Edward Schaefer. It shares the same properties and structure as the actual Data Encryption Standard (DES), but with much smaller parameters, making it possible to calculate by hand for educational purposes.

![Feistel Network Diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Feistel_cipher_diagram_en.svg/512px-Feistel_cipher_diagram_en.svg.png)
*(General Feistel Network Structure used in DES/S-DES)*

### Algorithm Structure

S-DES operates on an **8-bit block of plaintext** and uses a **10-bit key** to produce an 8-bit ciphertext block. 

1. **Key Generation ($K_1, K_2$)**
   - The 10-bit key is subjected to a Permutation (P10).
   - The result is split into two 5-bit halves.
   - Both halves are left-shifted by 1 bit (`LS-1`).
   - The halves are combined and put through a Permutation (P8) to create the 8-bit **Subkey 1 ($K_1$)**.
   - The halves from the `LS-1` step are left-shifted again by 2 bits (`LS-2`).
   - They are combined and put through P8 to create **Subkey 2 ($K_2$)**.

2. **Encryption Process**
   - **Initial Permutation (IP):** The 8-bit plaintext is permuted.
   - **Complex Function ($f_K$) Round 1:** Uses Subkey 1 ($K_1$). The right 4 bits are expanded using Expansion Permutation (EP), XORed with $K_1$, passed through Substitution Boxes (S0 and S1), permuted by P4, and XORed with the left 4 bits.
   - **Switch (SW):** Swaps the left and right 4-bit halves.
   - **Complex Function ($f_K$) Round 2:** Uses Subkey 2 ($K_2$). Same process as above.
   - **Inverse Initial Permutation (IP$^{-1}$):** Final permutation to produce the ciphertext.

3. **Decryption Process**
   - Exact same structure as encryption, but the subkeys are applied in reverse order (Round 1 uses $K_2$, Round 2 uses $K_1$).

---

## Line-by-Line Code Breakdown (`SimpleDES.py`)

### Constants and Tables

```python
P10 = [3,5,2,7,4,10,1,9,8,6]
P8  = [6,3,7,4,8,5,10,9]
IP  = [2,6,3,1,4,8,5,7]
EP  = [4,1,2,3,2,3,4,1] 
```
**Explanation:** These are the hardcoded permutation tables that define how bits are shuffled or expanded. For instance, `IP` moves the 2nd bit of the input to the 1st position, the 6th bit to the 2nd position, and so on.

```python
S0 = [[1,0,3,2], [3,2,1,0], [0,2,1,3], [3,1,3,2]]
S1 = [[0,1,2,3], [2,0,1,3], [3,0,1,0], [2,1,0,3]]
```
**Explanation:** Substitution boxes (S-boxes) provide the non-linear "confusion" in the cipher. They map a 4-bit input to a 2-bit output based on a 2D array lookup.

### Helper Functions

```python
def permute(bits, table):
    out = ''
    for i in table:
        out += bits[i-1]
    return out
```
**Explanation:** A generic function to shuffle a binary string based on a given table array. `i-1` is used because Python lists are 0-indexed, while S-DES literature uses 1-indexed tables.

```python
def left_shift(bits, n):
    return bits[n:] + bits[:n]

def xor(a, b):
    out = ''
    for i, j in zip(a, b):
        out += '0' if i == j else '1'
    return out
```
**Explanation:** `left_shift` rotates a binary string left by `n` places. `xor` performs a bitwise Exclusive-OR between two binary strings of the same length.

### Key Generation

```python
def generate_keys(key):
    key = permute(key, P10)
    left, right = key[:5], key[5:]

    left1 = left_shift(left, 1)
    right1 = left_shift(right, 1)
    K1 = permute(left1 + right1, P8)

    left2 = left_shift(left1, 2)
    right2 = left_shift(right1, 2)
    K2 = permute(left2 + right2, P8)

    return K1, K2
```
**Explanation:** This precisely follows the S-DES key schedule algorithm described in the theory section to generate $K_1$ and $K_2$ from the 10-bit master key.

### The Feistel Function ($f_K$)

```python
def sbox_lookup(bits, sbox):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return format(sbox[row][col], '02b')
```
**Explanation:** Given 4 bits, the outer bits (0 and 3) dictate the row, and the inner bits (1 and 2) dictate the column. It returns the 2-bit binary representation of the matrix value.

```python
def fk(bits, key):
    left, right = bits[:4], bits[4:]
    expanded = permute(right, EP)
    temp = xor(expanded, key)
    
    left_temp = temp[:4]
    right_temp = temp[4:]

    s0_out = sbox_lookup(left_temp, S0)
    s1_out = sbox_lookup(right_temp, S1)

    p4 = permute(s0_out + s1_out, P4)
    return xor(left, p4) + right
```
**Explanation:** The core mixing function. It expands the right half to 8 bits, XORs it with the 8-bit subkey, passes the result through S-boxes to shrink back to 4 bits, permutes it with P4, and finally XORs it with the original left half. The original right half is appended unmodified.

### Encryption and Decryption Flow

```python
def swap(bits):
    return bits[4:] + bits[:4]

def encrypt(plaintext, key):
    K1, K2 = generate_keys(key)
    bits = permute(plaintext, IP)
    bits = fk(bits, K1)
    bits = swap(bits)
    bits = fk(bits, K2)
    encrypted = permute(bits, IP_INV)
    return encrypted
```
**Explanation:** Orchestrates the encryption. It generates keys, applies the Initial Permutation, runs round 1 (`fk` with $K_1$), swaps the halves, runs round 2 (`fk` with $K_2$), and applies the Inverse Initial Permutation to get the ciphertext.

```python
def decrypt(ciphertext, key):
    K1, K2 = generate_keys(key)
    # ... applies IP, fk with K2, swap, fk with K1, IP_INV ...
```
**Explanation:** Decryption is identical to encryption, except the subkeys are used in reverse order ($K_2$ then $K_1$).

---

## Theoretical Background (Brute Force Attack)

A **Brute Force Attack** (or exhaustive key search) is a cryptanalytic attack that involves systematically checking all possible keys until the correct one is found. 

### Feasibility in Cryptography
The feasibility of a brute force attack depends entirely on the size of the key space. 
- In **Simplified DES (S-DES)**, the key is only **10 bits long**. Therefore, there are only $2^{10} = 1024$ possible keys. Because 1024 is such a small number, a modern computer can check every single possible key in a fraction of a millisecond. 
- For comparison, **Modern DES** has a 56-bit key ($2^{56}$ keys), and **AES-256** has a 256-bit key ($2^{256}$ keys), making AES computationally impossible to brute force.

### Mechanism of the Attack
To execute a known-plaintext brute force attack:
1. The attacker possesses a piece of ciphertext and the corresponding known plaintext.
2. The attacker loops through every possible key from $0$ to the maximum key limit.
3. They decrypt the ciphertext using the current guessed key.
4. If the resulting plaintext matches the expected known plaintext, they have successfully recovered the key.

---

## Line-by-Line Code Breakdown (`bruteFroce.py`)

### Dependencies and Core Attack Function

```python
import SimpleDES

def bruteForce(ciphertext, expected_plaintext):
    found = []
    for key in range(1024):
```
**Explanation:** 
- Imports the `SimpleDES` module to reuse its `decrypt` logic.
- Initializes an empty array `found`.
- Starts a `for` loop from `0` to `1023`. Since S-DES uses a 10-bit key, the max value is $2^{10} - 1 = 1023$. This loop systematically checks every possibility.

```python
        key_bits = format(key, '010b')
        decrypted = SimpleDES.decrypt(ciphertext, key_bits)
        
        if decrypted == expected_plaintext:
            found.append(key_bits)
            
    return found
```
**Explanation:** 
- `format(key, '010b')` converts the integer `key` into a 10-bit binary string (e.g., `'0000000101'`).
- Calls the S-DES `decrypt` function using the guessed key.
- If the output matches the `expected_plaintext`, the key is appended to the `found` list.
- Returns all successful keys *(Note: S-DES can sometimes suffer from key collisions where multiple keys yield the same plaintext/ciphertext pair)*.

---

## Potential Viva Questions & Tricky Questions

**Q1: How does a Feistel Network (like the one used in DES/S-DES) simplify decryption?**
*Answer:* In a Feistel network, the decryption process is exactly the same algorithm as the encryption process, just with the subkeys applied in reverse order. The complex mixing function ($f_K$) does *not* need to be mathematically invertible.

**Q2: What is the purpose of the S-Boxes in S-DES?**
*Answer:* The S-Boxes are the only non-linear component of the cipher. They provide "confusion" (in Shannon's terms), obscuring the relationship between the plaintext and the ciphertext. Without S-Boxes, S-DES would just be a series of linear XORs and permutations, which could be easily broken with simple algebra.

**Q3: Why is a brute-force attack trivial on S-DES but impossible on modern AES?**
*Answer:* It's entirely about the key space. S-DES uses a 10-bit key, meaning there are only $2^{10} = 1024$ possible keys to check. AES uses a minimum 128-bit key ($2^{128}$ possibilities), which would take billions of years to brute-force with current computing power.

**Q4: What is an Avalanche Effect, and how do S-Boxes contribute to it?**
*Answer:* The avalanche effect is a desirable property where a small change in the plaintext or key (e.g., flipping a single bit) causes a massive, unpredictable change in the ciphertext (ideally flipping 50% of the bits). S-Boxes are highly non-linear, meaning a 1-bit input change drastically alters the multi-bit output, driving this effect.

**Q5: Describe the difference between Confusion and Diffusion in block ciphers.**
*Answer:* **Confusion** obscures the relationship between the plaintext and the ciphertext (achieved by S-Boxes). **Diffusion** spreads the influence of a single plaintext bit over many ciphertext bits (achieved by permutations like P4, P8, and EP).

**Q6: What is the purpose of the Expansion Permutation (EP) in the $f_K$ function?**
*Answer:* The right half of the Feistel network is only 4 bits, but it needs to be XORed with the 8-bit subkey $K_1$. The EP duplicates certain bits to expand the 4-bit input into an 8-bit output, allowing the XOR operation and providing diffusion.

**Q7: Why does the Switch (SW) operation occur between the two rounds?**
*Answer:* In a Feistel network, only one half of the data is modified per round (the left half in S-DES). The Switch operation swaps the left and right halves so that the unmodified half from Round 1 becomes the target for modification in Round 2, ensuring the entire block is encrypted.

**Q8: How does a Known-Plaintext Attack differ from a Ciphertext-Only Attack?**
*Answer:* In a Ciphertext-Only attack, the attacker only has the encrypted data and must rely on statistical analysis or brute force. In a Known-Plaintext attack, the attacker has pairs of (Plaintext, Ciphertext), making brute-force much easier to verify or allowing them to solve algebraic equations to find the key.

**Q9: What is a "key collision" in the context of a brute force attack on S-DES?**
*Answer:* Because the S-DES block size is incredibly small (8 bits = 256 possible messages) but the key space is slightly larger (1024 keys), multiple different 10-bit keys will map the exact same 8-bit plaintext to the exact same 8-bit ciphertext.

**Q10: Why are permutations alone not sufficient to secure a block cipher?**
*Answer:* Permutations only shuffle bits around; they are completely linear operations. If a cipher only used permutations, an attacker could easily track the bit movements and reverse the cipher using basic linear algebra, completely bypassing the key.
