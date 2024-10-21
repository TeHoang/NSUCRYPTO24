from random import getrandbits

# The function f_2n 
def get_f(n):
    R = BooleanPolynomialRing(2 * n, 'x')
    xs = R.gens()  
    f_2n = R(0)
    for i in range(n): 
        f_2n += xs[i] * xs[i + n]
        for j in range(i + 1, n): 
            f_2n *= (xs[j] + xs[j + n])
    return f_2n

n = 17

# The function models the addition of 2 n-bits integer a and b 
f = get_f(n)

while True: 

    a, b = getrandbits(n), getrandbits(n)

    # x_1, x_2, ..., x_n
    bin_a = list(bin(a)[2:].zfill(n))[::-1]
    # x_{n + 1}, x_{n + 2}, ... x_{2n}
    bin_b = list(bin(b)[2:].zfill(n))[::-1]

    bin_a = [int(x) for x in bin_a]
    bin_b = [int(x) for x in bin_b]

    inputs = bin_a + bin_b

    result = f(*inputs)  

    verdict = 1 if ((a + b).bit_length() > n) else 0 

    # we check if the output of the function = If (a + b) overflows n-bit 
    print(result == verdict)