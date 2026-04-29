import random

def powerMod(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if (exponent % 2) == 1:
            result = (result * base) % modulus
        exponent = exponent // 2
        base = (base * base) % modulus
    return result

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

def gcd(a, b):
    while b:
        temp = b
        b = a % b
        a = temp
    return a

def generatePublicKey(p, g, x):
    h = powerMod(g, x, p)
    return (p, g, h)

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

def decrypt(ciphertext, private_key):
    p, g, x = private_key
    decrypted_text = ""
    for c1, c2 in ciphertext:
        s = powerMod(c1, x, p)
        s_inv = moduloInverse(s, p)
        m = (c2 * s_inv) % p
        decrypted_text += chr(m)
    return decrypted_text

def main():
    p = 683
    g = 2
    x = 15

    plaintext = input("Enter plaintext: ")

    public_key = generatePublicKey(p, g, x)
    private_key = (p, g, x)

    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")

    ciphertext = encrypt(plaintext, public_key)
    print(f"Ciphertext: {ciphertext}")

    decrypted_text = decrypt(ciphertext, private_key)
    print(f"Decrypted Text: {decrypted_text}")


main()