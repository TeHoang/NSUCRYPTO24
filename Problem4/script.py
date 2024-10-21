from Crypto.Util.number import bytes_to_long as btl 
import itertools
import os

# ref: https://emadalsuwat.github.io/cryptography/DES.pdf

pc1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4
]

pc2 = [
    14, 17, 11, 24,  1,  5,
    3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

ROTATES = [
    1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1,
]

IP = [
    58,    50,   42,    34,    26,   18,    10,    2,
    60,    52,   44,    36,    28,   20,    12,    4,
    62,    54,   46,    38,    30,   22,    14,    6,
    64,    56,   48,    40,    32,   24,    16,    8,
    57,    49,   41,    33,    25,   17,     9,    1,
    59,    51,   43,    35,    27,   19,    11,    3,
    61,    53,   45,    37,    29,   21,    13,    5,
    63,    55,   47,    39,    31,   23,    15,    7
]

EXPANSION = [
    32,     1,    2,     3,     4,    5,
    4,    5,    6,     7,     8,    9,
    8,    9,   10,    11,    12,   13,
    12,    13,   14,    15,    16,   17,
    16,    17,   18,    19,    20,   21,
    20,    21,   22,    23,    24,   25,
    24,    25,   26,    27,    28,   29,
    28,    29,   30,    31,    32,    1
]

SB = (
    (
        14, 4,  13, 1,  2,  15, 11, 8,  3,  10, 6,  12, 5,  9,  0,  7,
        0,  15, 7,  4,  14, 2,  13, 1,  10, 6,  12, 11, 9,  5,  3,  8,
        4,  1,  14, 8,  13, 6,  2,  11, 15, 12, 9,  7,  3,  10, 5,  0,
        15, 12, 8,  2,  4,  9,  1,  7,  5,  11, 3,  14, 10, 0,  6,  13,
    ),
    (
        15, 1,  8,  14, 6,  11, 3,  4,  9,  7,  2,  13, 12, 0,  5,  10,
        3,  13, 4,  7,  15, 2,  8,  14, 12, 0,  1,  10, 6,  9,  11, 5,
        0,  14, 7,  11, 10, 4,  13, 1,  5,  8,  12, 6,  9,  3,  2,  15,
        13, 8,  10, 1,  3,  15, 4,  2,  11, 6,  7,  12, 0,  5,  14, 9,
    ),
    (
        10, 0,  9,  14, 6,  3,  15, 5,  1,  13, 12, 7,  11, 4,  2,  8,
        13, 7,  0,  9,  3,  4,  6,  10, 2,  8,  5,  14, 12, 11, 15, 1,
        13, 6,  4,  9,  8,  15, 3,  0,  11, 1,  2,  12, 5,  10, 14, 7,
        1,  10, 13, 0,  6,  9,  8,  7,  4,  15, 14, 3,  11, 5,  2,  12,
    ),
    (
        7,  13, 14, 3,  0,  6,  9,  10, 1,  2,  8,  5,  11, 12, 4,  15,
        13, 8,  11, 5,  6,  15, 0,  3,  4,  7,  2,  12, 1,  10, 14, 9,
        10, 6,  9,  0,  12, 11, 7,  13, 15, 1,  3,  14, 5,  2,  8,  4,
        3,  15, 0,  6,  10, 1,  13, 8,  9,  4,  5,  11, 12, 7,  2,  14,
    ),
    (
        2,  12, 4,  1,  7,  10, 11, 6,  8,  5,  3,  15, 13, 0,  14, 9,
        14, 11, 2,  12, 4,  7,  13, 1,  5,  0,  15, 10, 3,  9,  8,  6,
        4,  2,  1,  11, 10, 13, 7,  8,  15, 9,  12, 5,  6,  3,  0,  14,
        11, 8,  12, 7,  1,  14, 2,  13, 6,  15, 0,  9,  10, 4,  5,  3,
    ),
    (
        12, 1,  10, 15, 9,  2,  6,  8,  0,  13, 3,  4,  14, 7,  5,  11,
        10, 15, 4,  2,  7,  12, 9,  5,  6,  1,  13, 14, 0,  11, 3,  8,
        9,  14, 15, 5,  2,  8,  12, 3,  7,  0,  4,  10, 1,  13, 11, 6,
        4,  3,  2,  12, 9,  5,  15, 10, 11, 14, 1,  7,  6,  0,  8,  13,
    ),
    (
        4,  11,  2, 14, 15, 0,  8,  13, 3,  12, 9,  7,  5,  10, 6,  1,
        13, 0,  11, 7,  4,  9,  1,  10, 14, 3,  5,  12, 2,  15, 8,  6,
        1,  4,  11, 13, 12, 3,  7,  14, 10, 15, 6,  8,  0,  5,  9,  2,
        6,  11, 13, 8,  1,  4,  10, 7,  9,  5,  0,  15, 14, 2,  3,  12,
    ),
    (
        13, 2,  8,  4,  6,  15, 11, 1,  10, 9,  3,  14, 5,  0,  12, 7,
        1,  15, 13, 8,  10, 3,  7,  4,  12, 5,  6,  11, 0,  14, 9,  2,
        7,  11, 4,  1,  9,  12, 14, 2,  0,  6,  10, 13, 15, 3,  5,  8,
        2,  1,  14, 7,  4,  10, 8,  13, 15, 12, 9,  0,  3,  5,  6,  11,
    ),
)

P = [                   
    16,   7,  20,  21, 
    29,  12,  28,  17, 
    1 , 15,  23,  26, 
    5 , 18,  31,  10, 
    2 ,  8,  24,  14, 
    32,  27,   3,   9, 
    19,  13,  30,   6, 
    22,  11,   4,  25 
]

Pinv = [
    9,17,23,31,13,28,2,18,24,16,30,6,26,20,10,1,8,14,25,3,4,29,11,19,32,12,22,7,5,27,15,21 
]

IP_inv = [
40,     8,   48,    16,    56,   24,    64,   32, 
39,     7,   47,    15,    55,   23,    63,   31, 
38,     6,   46,    14,    54,   22,    62,   30, 
37,     5,   45,    13,    53,   21,    61,   29, 
36,     4,   44,    12,    52,   20,    60,   28, 
35,     3,   43,    11,    51,   19,    59,   27, 
34,     2,   42,    10,    50,   18,    58,   26, 
33,     1,   41,     9,    49,   17,    57,   25 
]

# key is 64 bit length


def create_subkeys(key: int) -> list[str]:
    K, Ks = bin(key)[2:].zfill(64), []
    # apply permutation
    K_plus = [K[i - 1] for i in pc1]
    K_plus = ''.join(K_plus)
    Cs, Ds = [K_plus[:28]], [K_plus[28:]]
    for i, r in enumerate(ROTATES):
        Cs.append(Cs[i][r:] + Cs[i][:r])
        Ds.append(Ds[i][r:] + Ds[i][:r])

    for Ci, Di in zip(Cs, Ds):
        K = Ci + Di
        K = [K[i - 1] for i in pc2]
        K = ''.join(K)
        Ks.append(K)

    return Ks


def strxor(R: str, K: str) -> str: 
    return ''.join(['0' if r == k else '1' for (r, k) in zip (R, K)])

def f(R: str, K: str) -> str:
    R = [R[i - 1] for i in EXPANSION]
    R = ''.join(R)
    RK = strxor(R, K)
    B = [RK[i:i+6] for i in range(0, len(RK), 6)]
    B = [SB[i][int(b[0] + b[-1], 2) * 16 + int(b[1:-1], 2)] for i, b in enumerate(B)]
    B = [bin(b)[2:].zfill(4) for b in B]
    B = ''.join(b for b in B)
    B = [B[i - 1] for i in P]
    return ''.join(B)

# def encode(M: int, Ks: list):
#     M = bin(M)[2:].zfill(64)
#     M = [M[i - 1] for i in IP]
#     Ls, Rs = [''.join(M[:32])], [''.join(M[32:])]
#     for n in range(1, 17):
#         Ln = Rs[n - 1]
#         Rn = strxor(Ls[n - 1], f(Rs[n - 1], Ks[n]))  
#         Ls.append(Ln)
#         Rs.append(Rn)
    
#     RL16 = Rs[-1] + Ls[-1]
#     RL16 = ''.join([RL16[i - 1] for i in IP_inv]) 
#     RL16 = int(RL16, 2)
#     return hex(RL16)[2:].zfill(16)

def encode(M: int, Ks: list, mode=1):
    M = bin(M)[2:].zfill(64)
    M = [M[i - 1] for i in IP]
    Ls, Rs = [''.join(M[:32])], [''.join(M[32:])]
    for n in range(1, 17):
        Ln = Rs[n - 1]
        Rn = strxor(Ls[n - 1], f(Rs[n - 1], Ks[0])) # Alice's bug, we use index 0 just for convenience 
        if not mode: return Ln + Rn 
        Ls.append(Ln)
        Rs.append(Rn)
    
    RL16 = Rs[-1] + Ls[-1]
    RL16 = ''.join([RL16[i - 1] for i in IP_inv]) 
    RL16 = int(RL16, 2)
    return hex(RL16)[2:].zfill(16)


# key = int('0E329232EA6D0D73', 16)
# Ks = create_subkeys(key)
# M = int('8787878787878787', 16)
# print(encode(M, Ks) == "0" * 16) # True

# pt = open("Book.txt", "rb").read()[:-1]
# ct = open("Book_cipher.txt", "rb").read()

# pt_blocks = [pt[i:i + 8] for i in range(0, len(pt), 8)]
# ct_blocks = [ct[i:i + 8] for i in range(0, len(ct), 8)]

# pt_bits = [[int(x) for x in bin(int(y.hex(), 16))[2:].zfill(64)] for y in pt_blocks]
# pt_bits = [[x[i - 1] for i in IP] for x in pt_bits]

# ct_bits = [[int(x) for x in bin(int(y.hex(), 16))[2:].zfill(64)] for y in ct_blocks]

# ls = [''.join(str(y) for y in x[:32]) for x in pt_bits]
# rs = [''.join(str(y) for y in x[32:]) for x in pt_bits]

# print(set(ls).intersection(set(rs)))

def find_key(P0, P1, CT):
    L0, R0 = P0[:32], P0[32:]
    L1, R1 = P1[:32], P1[32:]
    assert R0 == L1, "nope"
    R1 = strxor(L0, R1) # R1 = L0 + f(R0, K), remove L0 to get f(R0, K)
    # Apply Pinv to remove permutation P 
    R1 = ''.join([R1[i - 1] for i in Pinv]) 
    # Next split in block of 4 bits 
    R1 = [R1[i:i+4] for i in range(0, len(R1), 4)]
    # Find mapping from SB
    xs = []
    for i, y in enumerate(R1): 
        y = int(y, 2)
        res = []
        for j in range(len(SB[i])): 
            if SB[i][j] == y: 
                pos = bin(j // 16)[2:].zfill(2)
                res.append(pos[0] + bin(j % 16)[2:].zfill(4) + pos[1])
        xs.append(res)
    combinations = list(itertools.product(*xs))

    # M = apply IP_inv on P0, use M and key to encrypt 16 rounds, If it maches CT -> found Alice's key 
    M = ''.join([P0[i - 1] for i in IP_inv])
    M = int(M, 2)

    R_expanded = ''.join([R0[i - 1] for i in EXPANSION])

    for combo in combinations:
        possible_k = ''.join(x for x in combo)
        possible_k = strxor(R_expanded, possible_k)
        check = encode(M, [possible_k], mode=0) # mode = 0 to encrypt 1 round only 
        assert check == P1
        if (bin(int(encode(M, [possible_k]), 16))[2:].zfill(64) == CT):
            print(f"found key: {possible_k}")
            return possible_k

P0 = '1101111101000101000110011001100000000000101111101000001001000100'
P1 = '0000000010111110100000100100010000000000111111111000001000000010'
CT = '0001000101110100001011011110110001111101110000110111100110101011'

key = find_key(P0, P1, CT)

Ks = [key] 

msg = """86991641D28259604412D6BA88A5C0A6471CA7222C52482BF2D0
E841D4343DFB877DC8E0147F3D5F20FC18FF28CB5C4DA8A0F4694861AB5E98F37ADBC2D69B35779D9001BB4B648518FE6EBC00B2AB10""".replace('\n', '')

msg_block = [msg[i:i+16] for i in range(0, len(msg), 16)]

recover_msg = b''

for msg_b in msg_block:
    recover_msg += bytes.fromhex(encode(int(msg_b, 16), Ks))

print(recover_msg.decode())

"""
found key: 000011000111010011111010011010100110010000101010
It is better to be in chains with friends, than to be in a garden with strangers
"""

