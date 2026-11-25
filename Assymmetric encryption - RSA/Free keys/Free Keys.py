import json
import random
import math
from sympy import isprime

# --------------------------------------------------
# Load challenge
# --------------------------------------------------

with open("challenge.json", "r") as f:
    challenge = json.load(f)

n = challenge["n"]
e1 = challenge["e1"]
e2 = challenge["e2"]

c1 = challenge["c1"]
c2 = challenge["c2"]

def find_a_and_b(e1,e2):
    # Extended Euclid: every row keeps  r[i] == a[i]*e1 + b[i]*e2
    r = [e1, e2]
    a = [1, 0]   # e1 = 1*e1 + 0*e2
    b = [0, 1]   # e2 = 0*e1 + 1*e2
    while r[-1] != 0:
        q = r[-2] // r[-1]          # quotient BEFORE appending (same fix as key_generation)
        r.append(r[-2] % r[-1])
        a.append(a[-2] - q * a[-1])
        b.append(b[-2] - q * b[-1])
    # r[-1] is 0, so r[-2] is gcd(e1, e2); its a and b are the ones we want
    if r[-2] != 1:
        raise ValueError("gcd(e1, e2) != 1, the common modulus attack won't work")
    return a[-2], b[-2]
a, b = find_a_and_b(e1,e2)
m = pow(c1, a, n) * pow(c2, b, n) % n
print(m.to_bytes((m.bit_length() + 7) // 8, "big").decode())
