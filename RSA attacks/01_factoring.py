"""
RSA attacks (1/6): FACTORING n.

If you can factor n you have the private key: phi, then d = e^-1 mod phi.
Recognise these from the key itself -- no ciphertext tricks needed.

  demo                          what makes n weak                 toolkit call
  ----------------------------- --------------------------------- ---------------------
  close_primes                  |p - q| small                     fermat_factor
  smooth_p_minus_1              p-1 only has small factors         pollard_p1
  smooth_p_plus_1              p+1 only has small factors         williams_p1
  small_factor                  one prime is much smaller          pollard_rho
  shared_prime_batchgcd         two public keys reuse a prime      shared_prime_factors
  perfect_power / multiprime    n = p^k or more than two primes    factor
  auto                          "just factor it"                   factor  (tries all)
"""
from _harness import *


def _decrypt_with_factors(n, e, factors):
    d = pow(e, -1, phi_from_factors(factors))
    return i2b(pow(pow(M, e, n), d, n))


def demo_close_primes():
    """p and q only ~2^30 apart -> Fermat's method (a^2 - b^2)."""
    p = prime(512)
    q = nextprime(p + random.randrange(1 << 28))
    n, e = p * q, 65537
    pf, qf = fermat_factor(n)
    assert _decrypt_with_factors(n, e, [pf, qf]) == FLAG
    return "fermat: p,q too close (tip: 'twin', 'sand', 'nearby')"


def demo_smooth_p_minus_1():
    """p-1 is smooth -> Pollard p-1."""
    p, q = smooth_prime(512), prime(512)
    f = pollard_p1(p * q, 1 << 17)
    assert f in (p, q)
    assert _decrypt_with_factors(p * q, 65537, [p, q]) == FLAG
    return "pollard p-1: p-1 smooth (tip: 'smooth', 'sifting')"


def demo_smooth_p_plus_1():
    """p+1 is smooth -> Williams p+1."""
    p, q = smooth_plus_prime(400), prime(400)
    f = williams_p1(p * q, 1 << 13)
    assert f in (p, q)
    return "williams p+1: p+1 smooth"


def demo_small_factor():
    """One prime is tiny next to the other -> Pollard rho finds it in ~sqrt(p) steps."""
    p, q = prime(32), prime(500)
    assert pollard_rho(p * q) in (p, q)
    return "pollard rho: one small prime"


def demo_shared_prime_batchgcd():
    """Two users whose moduli share a prime: gcd(n1, n2) cracks both."""
    p, q1, q2 = prime(512), prime(512), prime(512)
    n1, n2 = p * q1, p * q2
    found = shared_prime_factors([n1, n2])
    assert found[0] == (p, q1) and found[1] == (p, q2)
    assert _decrypt_with_factors(n1, 65537, found[0]) == FLAG
    return "batch gcd: a prime reused across keys"


def demo_multiprime_and_power():
    """n = p*q*r*s or n = p^3: phi still comes straight from the factors."""
    ps = [prime(160) for _ in range(4)]
    n = math.prod(ps)
    assert _decrypt_with_factors(n, 65537, ps) == FLAG
    r = prime(200)
    assert factor(r ** 3, verbose=False) == {r: 3}
    return "multi-prime / perfect power"


def demo_auto_factor():
    """When unsure: factor() tries Fermat, p-1, rho, p+1, powers, then sympy."""
    p, q = smooth_prime(300), prime(380)
    assert factor(p * q, verbose=False) == dict(sorted({p: 1, q: 1}.items()))
    return "factor(): the one-call fallback (also try factordb.com)"


if __name__ == "__main__":
    run(globals())
