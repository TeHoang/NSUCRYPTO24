from sage.all import * 

# The padding defined in the problem 
padding = '123456' 

def pad(P: str, padding: str) -> str: 
    # We pad the str if its length is not divisible by 6 
    while len(P) % 6 != 0: 
        P += padding[:6 - (len(P) % 6)]
    return P 

def hash(P: str, K: str) -> int: 
    # Remember to pad before hashing
    P = pad(P, padding)

    # Divide into blocks and do hash operation on each block 
    blocks, H = [P[i:i+6] for i in range(0, len(P), 6)], 0
    for k, block in enumerate(blocks):
        h = 0 
        for i, digit in enumerate(block): 
            # The formula defined in the problem 
            h += (-1) ** int(K[i]) * int(digit)
        H += (-1) ** k * h 
    return H 

P = '134875512293'
K = '001101'

# Sanity check, the problem calculated this value wrong (expected -8 - 6 but -8 + 6 found)
assert hash(P, K) == -14


# Try to find P' of length l such that H(P', K) = H(P, K) for all K in [0, 63]
for l in range(1, 8):
    mat = []
    u = []

    for K in range(64):
        # For each K, we calculate H(P, K), the target will be H(P, K) - H(the padding of pad(P'), K) 
        K = bin(K)[2:].zfill(6)
        H = hash(P, K)
        H2 = (-1) ** (((l - 1) // 6) % 2) * hash(pad('0' * (l % 6), padding), K) 
        u.append(H - H2)
        vec = [(-1) ** int(K[i % 6]) * (-1) ** ((i // 6) % 2) for i in range(l)]
        mat.append(vec)

    A = matrix(ZZ, mat)
    U = matrix(ZZ, 64, 1, u)     

    try:
        # Try to see if this has solution 
        v0 = A.solve_right(U)
        print(l, v0.list())

    except ValueError as e:
        pass


P = '134875512293'

# l = 7, we can find v0 = [-4, 3, 4, 9, 2, 7, 0], although this is not a valid vector (contains negative number), we can fix by increment
# the number in the first position in second block -> we get [0, 3, 4, 9, 2, 7, 4], [1, 3, 4, 9, 2, 7, 5], ..., [5, 3, 4, 9, 2, 7, 9]

P_prime = pad('0349274', padding)
# P_prime = pad('1349275', padding)
# P_prime = pad('2349276', padding)
# P_prime = pad('3349277', padding)
# P_prime = pad('4349278', padding)
# P_prime = pad('5349279', padding)

for K in range(0, 2 ** 6): 
    K = bin(K)[2:].zfill(6)
    assert (hash(P, K) == hash(P_prime, K)), f"{K}"
