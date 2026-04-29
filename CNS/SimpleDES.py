P10 = [3,5,2,7,4,10,1,9,8,6]
P8  = [6,3,7,4,8,5,10,9]
IP  = [2,6,3,1,4,8,5,7]
EP  = [4,1,2,3,2,3,4,1] 

S0 = [
    [1,0,3,2],
    [3,2,1,0],
    [0,2,1,3],
    [3,1,3,2]
]

S1 = [
    [0,1,2,3],
    [2,0,1,3],
    [3,0,1,0],
    [2,1,0,3]
]

P4  = [2,4,3,1] 
IP_INV = [4,1,3,5,7,2,8,6]


def permute(bits, table):
    out = ''
    for i in table:
        out += bits[i-1]
    return out


def left_shift(bits, n):
    return bits[n:] + bits[:n]

def xor(a, b):
    out = ''
    for i, j in zip(a, b):
        out += '0' if i == j else '1'
    return out

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

def sbox_lookup(bits, sbox):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return format(sbox[row][col], '02b')

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

def decrypt(ciphertext, key):
    K1, K2 = generate_keys(key)
    bits = permute(ciphertext, IP)
    bits = fk(bits, K2)
    bits = swap(bits)
    bits = fk(bits, K1)
    return permute(bits, IP_INV)

def main():
    key = input("Enter 10-bit key: ")
    K1, K2 = generate_keys(key)
    print(f"Generated Keys:\nK1: {K1}\nK2: {K2}")
    plaintext = input("Enter 8-bit plaintext: ")
    cipher = encrypt(plaintext, key)
    print("Encrypted text:", cipher)
    decrypted = decrypt(cipher, key)
    print("Decrypted text:", decrypted)

if __name__ == "__main__":
    main()
