from itertools import product
import sys

sys.setrecursionlimit(9000)

#---------------------------------------------------------SOLVE FOR STATES---------------------------------------------------------

def toList(s):
    return [int(c) for c in s]

with open('./keystream.txt', 'r') as f:
    K = [None] + toList(f.readline().strip())

A = toList('00101001110001001110111001100001010100000101110')
B = toList('0000010000101001000011000001010111001110000100101')

def check(t, sA, sB):
    res = (((sA[0] & sA[1]) ^ sA[12] ^ sA[43]) == sA[47])
    res = res and (((sB[0] & sB[1]) ^ sB[10] ^ sB[47]) == sB[49])
    res = res and (((sA[8] & sA[9]) ^ sA[4] ^ sA[1] ^ (sB[5] & sB[6]) ^ sB[8] ^ sB[1]) == K[t])
    return res

ans = []

def solve(t, sA, sB):
    if t == 1:
        ans.append((sA[1:], sB[1:]))
        return

    for i, j in product(range(2), range(2)):
        sA[0] = i
        sB[0] = j

        if check(t, sA, sB):
            solve(t - 1, [None] + sA[:47], [None] + sB[:49]) 


solve(8192, [None] + A, [None] + B)
state_A, state_B = ans[0]

#---------------------------------------------------------CHECK STATES------------------------------------------------------------

class Generator: 
    def __init__(self, state_A, state_B): 
        self.state_A = state_A
        self.state_B = state_B
    
    def _clock_A(self): 
        b = self.state_A[0] ^ (self.state_A[7] & self.state_A[8]) ^ self.state_A[3]
        self.state_A = self.state_A[1:] + [(self.state_A[0] & self.state_A[1]) ^ self.state_A[12] ^ self.state_A[43]]
        return b 

    def _clock_B(self): 
        b = self.state_B[0] ^ (self.state_B[4] & self.state_B[5]) ^ self.state_B[7]
        self.state_B = self.state_B[1:] + [(self.state_B[0] & self.state_B[1]) ^ self.state_B[10] ^ self.state_B[47]]
        return b 
    
    def _clock(self): 
        return self._clock_A() ^ self._clock_B()

key_stream = open('./keystream.txt', 'r').read().strip()
g = Generator(state_A, state_B)
k = ''

for _ in range(8192): 
    k += str(g._clock())

print(key_stream == k) # True 


