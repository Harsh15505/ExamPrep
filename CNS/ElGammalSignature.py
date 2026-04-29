import random
import hashlib
from math import gcd

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


def hash_message(message):
    return int.from_bytes(hashlib.sha256(message.encode()).digest(), 'big')


def generate_keys(p, alpha):
    x = random.randint(2, p - 2)
    y = pow(alpha, x, p)
    private_key = x
    public_key = (p, alpha, y)
    return private_key, public_key

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


def verify_signature(message, signature, p, alpha, y):
    s1, s2 = signature
    m = hash_message(message)

    v1 = pow(alpha, m, p)
    v2 = (pow(y, s1, p) * pow(s1, s2, p)) % p

    return v1 == v2

def main():
    p = 19
    alpha = 10

    private_key, public_key = generate_keys(p, alpha)

    print("Private key:", private_key)
    print("Public key:", public_key)

    message = "Hello World"

    signature = sign_message(message, p, alpha, private_key)
    print("Signature:", signature)

    if verify_signature(message, signature, p, alpha, public_key[2]):
        print("Valid Signature")
    else:
        print("Invalid Signature")

if __name__ == "__main__":
    main()