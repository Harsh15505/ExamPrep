import SimpleDES

def bruteForce(ciphertext, expected_plaintext):
    found = []
    for key in range(1024):
        key_bits = format(key, '010b')
        decrypted = SimpleDES.decrypt(ciphertext, key_bits)
        if decrypted == expected_plaintext:
            found.append(key_bits)
    return found

def main():
    ciphertext = input("Enter the ciphertext: ")
    expected_plaintext = input("Enter the expected plaintext: ")
    keys = bruteForce(ciphertext, expected_plaintext)
    if keys:
        for key in keys:
            print(f"Key found: {key}")
    else:
        print("Key not found.")

if __name__ == "__main__":
    main()