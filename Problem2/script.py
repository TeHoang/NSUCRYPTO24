import sage.logic.propcalc as propcalc
from sage.all import *

Cx5 = propcalc.formula('(x1 | x2 | ~x5) & (~x1 | ~x2 | x5) & (x1 | x3 | ~x5) & (~x1 | ~x3 | x5) & (x2 | x3 | ~x5) & (~x2 | ~x3 | x5)')
Cx6 = propcalc.formula('(x1 | x2 | ~x6) & (~x1 | ~x2 | x6) & (x1 | x4 | ~x6) & (~x1 | ~x4 | x6) & (x2 | x4 | ~x6) & (~x2 | ~x4 | x6)')
Cx7 = propcalc.formula('(x1 | x3 | ~x7) & (~x1 | ~x3 | x7) & (x1 | x4 | ~x7) & (~x1 | ~x4 | x7) & (x3 | x4 | ~x7) & (~x3 | ~x4 | x7)')
Cx8 = propcalc.formula('(x2 | x3 | ~x8) & (~x2 | ~x3 | x8) & (x2 | x4 | ~x8) & (~x2 | ~x4 | x8) & (x3 | x4 | ~x8) & (~x3 | ~x4 | x8)')
 
x5_tt = Cx5.truthtable().get_table_list()[1:]
x5_tt = [list(map(int, x[:2] + x[-2:-1] + x[2:3])) for x in x5_tt if x[-1]]

x6_tt = Cx6.truthtable().get_table_list()[1:]
x6_tt = [list(map(int, x[:2] + x[-2:-1] + x[2:3])) for x in x6_tt if x[-1]]

x7_tt = Cx7.truthtable().get_table_list()[1:]
x7_tt = [list(map(int, x[:2] + x[-2:-1] + x[2:3])) for x in x7_tt if x[-1]]

x8_tt = Cx8.truthtable().get_table_list()[1:]
x8_tt = [list(map(int, x[:2] + x[-2:-1] + x[2:3])) for x in x8_tt if x[-1]]

tts = [{tuple(x[:3]):x[-1] for x in tt} for tt in [x5_tt, x6_tt, x7_tt, x8_tt]]

def calc(x1, x2, x3, x4):
    return [tts[0][(x1, x2, x3)], tts[1][(x1, x2, x4)], tts[2][(x1, x3, x4)], tts[3][(x2, x3, x4)]]

K1702 = "0101 1001 1111 0011 00X1 X111 1X00 00X0 111X X000 XXXX XXXX XXXX XXXX XXXX XXXX".split()
K1703 = "XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX X111 000X X010 01X1 0X10 0101 0000 1111".split()
ct = [int(x) for x in "1001 1000 0011 1101 0110 0011 1101 0101 1011 0011 1011 0111 0000 0000 1000 0011".replace(" ", "")]


output = {}
for i in range(16):
    bits = list(map(int, bin(i)[2:].zfill(4)))
    res = tuple(calc(*bits))
    if res not in output:
        output[res] = [bits]
    else:
        output[res].append(bits)

for i in range(16):
    if 'X' not in K1702[i]:
        K1703[i] = ''.join(str(x) for x in calc(*list(map(int, K1702[i]))))
    elif K1702[i].count('X') == 1:
        v1, v2 = K1702[i].replace('X', '0'), K1702[i].replace('X', '1')
        v1, v2 = tuple(map(int, v1)), tuple(map(int, v2))
        if v1 in output:
            K1703[i] = ''.join(str(x) for x in calc(*v1))
        elif v2 in output:
            K1703[i] = ''.join(str(x) for x in calc(*v2))
        else:
            raise ValueError("No solution found")
    elif K1703[i].count('X') == 1:
        v1, v2 = K1703[i].replace('X', '0'), K1703[i].replace('X', '1')
        v1, v2 = tuple(map(int, v1)), tuple(map(int, v2))
        if v1 in output:
            K1703[i] = ''.join(str(x) for x in v1)
        elif v2 in output:
            K1703[i] = ''.join(str(x) for x in v2)
        else:
            raise ValueError("No solution found")

K1704 = []        
for i in range(16):
    K1704.extend(calc(*list(map(int, K1703[i]))))

M1704 = [x ^ y for x, y in zip(ct, K1704)]
M1704 = [''.join(str(x) for x in M1704[i:i+4]) for i in range(0, len(M1704), 4)]
K1704 = [''.join(str(x) for x in K1704[i:i+4]) for i in range(0, len(K1704), 4)]
print('K1704:',' '.join(K1704))
print('M1704:',' '.join(M1704))