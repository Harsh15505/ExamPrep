import random

def modInverse(x, p):
    x = x % p
    if x < 0:
        x += p
    for i in range(1, p):
        if (x * i) % p == 1:
            return i
    return -1

def splitSecret(secret, n, k, p):
    coeffs = [secret]
    for _ in range(k - 1):
        coeffs.append(random.randint(1, p - 1))
    
    shares = []
    for x in range(1, n + 1):
        y = 0
        for i in range(len(coeffs)):
            y = (y + coeffs[i] * (x ** i)) % p
        shares.append((x, y))
    
    return shares

def reconstructSecret(shares, p):
    secret = 0
    for i in range(len(shares)):
        xi, yi = shares[i]
        num = 1
        den = 1
        for j in range(len(shares)):
            if i != j:
                xj, yj = shares[j]
                num = (num * -xj) % p
                den = (den * (xi - xj)) % p
        
        term = (yi * num * modInverse(den, p)) % p
        secret = (secret + term) % p
        
    return secret

def main():
    p = 257
    secret = 123
    n = 5
    k = 3
    
    shares = splitSecret(secret, n, k, p)
    print("All Shares:", shares)
    
    subset = shares[:k]
    print("Subset of shares used:", subset)
    
    reconstructed = reconstructSecret(subset, p)
    print("Reconstructed Secret:", reconstructed)

if __name__ == "__main__":
    main()
