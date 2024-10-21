# TOY EXAMPLE 
from Crypto.Util.number import getPrime, bytes_to_long, GCD 

p, q = getPrime(1024), getPrime(1024) # SECRET
N = p * q
e = 65537
phi = (p - 1) * (q - 1) # SECRET
d = pow(e, -1, phi) # SECRET
d_p = d % (p - 1)
d_q = d % (q - 1)

M = b'Solution_for_PROBLEM_1_RSA_signature'
M = bytes_to_long(M)

# calculating the signature
S = pow(M, d, N)
M_p = pow(M, d_p, p) # Attacker knows this 
M_q = pow(M, d_q, q) # UNKNOWN

assert M_p != M_q 

# Attack 

M_pe = pow(M_p, e, N)
calculated_p = GCD(M_pe - M, N)

assert calculated_p == p

calculated_q = N // calculated_p 
calculated_phi = (calculated_p - 1) * (calculated_q - 1)
calculated_d = pow(e, -1, calculated_phi)

print(calculated_d == d) # True 
