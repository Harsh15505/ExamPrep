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

def generateKeys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 2
    while gcd(e, phi) != 1:
        e += 1
    d = moduloInverse(e, phi)
    return (e, n), (d, n)

def encrypt(plaintext, public_key):
    e, n = public_key
    ciphertext = []

    for char in plaintext:
        m = ord(char)
        c = powerMod(m, e, n)
        ciphertext.append(c)

    return ciphertext

def decrypt(ciphertext, private_key):
    d, n = private_key
    plaintext = ""

    for c in ciphertext:
        m = powerMod(c, d, n)
        plaintext += chr(m)

    return plaintext

def CCA2(ciphertext,p,q,S):
    public_key, private_key = generateKeys(p,q)
    e,n = public_key
    d,n = private_key

    S_e = powerMod(S, e, n)
    newciphertext = []
    for c in ciphertext:
        newciphertext.append((c * S_e) % n)
    
        d, n = private_key
    
    M_dash = []
    for c in newciphertext:
        m = powerMod(c, d, n)
        M_dash.append(m)

    print(f"M_dash: {M_dash}")
    s_inv = moduloInverse(S, n)

    M = ""

    for m in M_dash:
        new_m = (m * s_inv) % n
        M += chr(new_m)

    return M

def main():
    p = 19
    q = 17
    public_key, private_key = generateKeys(p, q)
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")

    plaintext = input("Enter plaintext: ")
    ciphertext = encrypt(plaintext, public_key)
    print(f"Ciphertext: {ciphertext}")

    decrypted_plaintext = decrypt(ciphertext, private_key)
    print(f"Decrypted Plaintext: {decrypted_plaintext}")

    S=2
    CCA_plaintext = CCA2(ciphertext, p, q, S)
    print(f"Recovered Plaintext: {CCA_plaintext}")

if __name__ == "__main__":
    main()

