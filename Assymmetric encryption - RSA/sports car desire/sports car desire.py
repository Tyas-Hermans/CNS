import json
import random
import math
from sympy import isprime

# --------------------------------------------------
# Load challenge
# --------------------------------------------------

with open("challenge(1).json", "r") as f:
    challenge = json.load(f)

n = challenge["n"]
e = challenge["e"]
c = challenge["c"]


def find_d(e, n):
    # Wiener's attack: if d is small, k/d shows up as a convergent of e/n.

    # 1. continued fraction terms of e/n = the quotients of the Euclid loop
    quotients = []
    r = [e, n]
    while r[-1] != 0:
        quotients.append(r[-2] // r[-1])
        r.append(r[-2] % r[-1])

    # 2. walk through the convergents num/den, each one is a guess for k/d
    num = [0, 1]
    den = [1, 0]
    for q in quotients:
        num.append(q * num[-1] + num[-2])
        den.append(q * den[-1] + den[-2])
        k = num[-1]
        d = den[-1]

        # 3. test the guess: phi = (e*d - 1) / k has to be a whole number
        if k == 0 or (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) // k

        # p and q are the roots of x^2 - s*x + n = 0 with s = p + q = n - phi + 1,
        # so the discriminant s^2 - 4n must be a perfect square
        s = n - phi + 1
        disc = s * s - 4 * n
        if disc < 0:
            continue
        root = math.isqrt(disc)       # isqrt, not sqrt: floats can't hold 1024-bit numbers
        if root * root == disc:
            p = (s + root) // 2
            q = (s - root) // 2
            if p * q == n:
                return d

    raise ValueError("no convergent worked, d is too big for Wiener's attack")
d = find_d(e, n)
m = pow(c,d,n)
print(m.to_bytes((m.bit_length() + 7) // 8, "big"))