"""
RSA attacks (3/6): WEAK OR LEAKED KEY MATERIAL.

  demo                  situation                                   toolkit call
  --------------------- ------------------------------------------- -------------------
  common_modulus        same n, two coprime exponents, same m       common_modulus
  common_modulus_gcd    ...and gcd(e1, e2) = g > 1                   common_modulus
  wiener                d very small (huge e)                       wiener
  leaked_d              d is given -> factor n                      factor_from_d
  leaked_phi            phi(n) is given                             factor_from_phi
  leaked_dp             CRT exponent d mod (p-1) leaks              dp_leak
  e_shares_factor       gcd(e, p-1) > 1 (e.g. e=2, Rabin)           rsa_decrypt_all
"""
from _harness import *


def demo_common_modulus():
    """One n, two public keys e1,e2 (coprime), same message to both."""
    n = prime(512) * prime(512)
    e1, e2 = 17, 65537
    c1, c2 = pow(M, e1, n), pow(M, e2, n)
    assert i2b(common_modulus(c1, c2, e1, e2, n)) == FLAG
    return "common modulus: same n, two exponents (tip: 'free keys')"


def demo_common_modulus_gcd():
    """Same idea but gcd(e1, e2) = 3: recover m^3 then take a cube root."""
    n = prime(512) * prime(512)
    e1, e2 = 3 * 17, 3 * 11
    assert i2b(common_modulus(pow(M, e1, n), pow(M, e2, n), e1, e2, n)) == FLAG
    return "common modulus with gcd(e1,e2) > 1"


def demo_wiener():
    """Small private exponent d -> d is a convergent of e/n."""
    p, q = prime(512), prime(512)
    n, phi = p * q, (p - 1) * (q - 1)
    while True:
        d = random.getrandbits(200) | 1
        if math.gcd(d, phi) == 1:
            break
    e = pow(d, -1, phi)
    rec_d, _, _ = wiener(e, n)
    assert rec_d == d
    assert i2b(pow(pow(M, e, n), d, n)) == FLAG
    return "wiener: tiny d, huge e (tip: 'sports car', 'small d')"


def demo_leaked_d():
    """A leaked d lets you factor n (then you own every message)."""
    p, q = prime(512), prime(512)
    n, e = p * q, 65537
    d = pow(e, -1, (p - 1) * (q - 1))
    assert set(factor_from_d(n, e, d)) == {p, q}
    return "leaked d -> factor n"


def demo_leaked_phi():
    """phi(n) reveals p, q as roots of x^2 - (n-phi+1)x + n."""
    p, q = prime(512), prime(512)
    assert set(factor_from_phi(p * q, (p - 1) * (q - 1))) == {p, q}
    return "leaked phi -> factor n"


def demo_leaked_dp():
    """A leaked CRT exponent dp = d mod (p-1): p = gcd(r^(e*dp) - r, n)."""
    p, q = prime(512), prime(512)
    n, e = p * q, 65537
    dp = pow(e, -1, (p - 1) * (q - 1)) % (p - 1)
    assert set(dp_leak(n, e, dp)) == {p, q}
    return "leaked dp (CRT exponent) -> factor n"


def demo_e_shares_factor():
    """e not invertible mod phi (here e=2, Rabin): e-th roots mod p,q + CRT."""
    while True:
        p, q = prime(256), prime(256)
        if p % 4 == 3 and q % 4 == 3:        # makes square roots easy
            break
    c = pow(M, 2, p * q)
    assert FLAG in [i2b(m) for m in rsa_decrypt_all(c, 2, [p, q])]
    return "gcd(e, phi) > 1: roots mod each prime + CRT (Rabin / e | p-1)"


if __name__ == "__main__":
    run(globals())
