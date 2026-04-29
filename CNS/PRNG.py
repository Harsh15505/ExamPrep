def linear_congruential_generator(seed, a, c, m, num_values):
    values = []
    current = seed
    for _ in range(num_values):
        current = (a * current + c) % m
        values.append(current)
    return values

def blum_blum_shub_generator(p, q, seed, num_bits):
    m = p * q
    
    # x_0 = seed^2 mod m
    current = (seed * seed) % m
    
    bits = []
    for _ in range(num_bits):
        # x_i = (x_{i-1})^2 mod m
        current = (current * current) % m
        # Extract least significant bit
        bits.append(current % 2)
        
    return bits

def main():
    print("--- Linear Congruential Generator (LCG) ---")
    # Common parameters (e.g., glibc uses similar)
    a = 1103515245
    c = 12345
    m = 2**31
    seed_lcg = 42
    num_values = 5
    
    lcg_values = linear_congruential_generator(seed_lcg, a, c, m, num_values)
    print(f"Generated LCG values (seed={seed_lcg}): {lcg_values}")


    print("\n--- Blum Blum Shub Generator (BBS) ---")
    # p and q must be congruent to 3 mod 4
    p = 11
    q = 19
    seed_bbs = 3
    num_bits = 15
    
    bbs_bits = blum_blum_shub_generator(p, q, seed_bbs, num_bits)
    print(f"Generated BBS bits (p={p}, q={q}, seed={seed_bbs}): {bbs_bits}")

if __name__ == "__main__":
    main()
