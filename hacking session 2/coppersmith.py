"""
Pure-Python LLL + Coppersmith small-roots, so the lattice RSA attacks work
without fpylll or SageMath.  Slower than Sage but fine for CTF-sized problems.

Main entry points (also re-exported from cryptokit):
    lll(B)                               -> LLL-reduced integer basis
    coppersmith_univariate(f, N, ...)    -> small integer roots of f = 0 (mod divisor)
    factor_high_bits(n, p_high, bits)    -> factor n given the top bits of p
    stereotyped_e3(c, n, prefix_int, unknown_bytes)  -> recover a padded message
"""
from __future__ import annotations

# --------------------------------------------------------------------------
# tiny integer-polynomial helpers (coefficients low -> high degree)
# --------------------------------------------------------------------------


def p_trim(a: list[int]) -> list[int]:
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def p_mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                out[i + j] += ai * bj
    return p_trim(out)


def p_pow(a: list[int], e: int) -> list[int]:
    out = [1]
    base = list(a)
    while e:
        if e & 1:
            out = p_mul(out, base)
        base = p_mul(base, base)
        e >>= 1
    return out


def p_eval(a: list[int], x: int) -> int:
    v = 0
    for c in reversed(a):
        v = v * x + c
    return v


# --------------------------------------------------------------------------
# Integer LLL  (Cohen, "A Course in Computational Algebraic Number Theory",
# Algorithm 2.6.7).  Exact, all-integer, O(n^3 M(size)) -- fast enough here.
# --------------------------------------------------------------------------


def _dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def lll(basis: list[list[int]], delta=(99, 100)) -> list[list[int]]:
    """Lenstra-Lenstra-Lovasz reduction. Rows = vectors. delta = (num, den)."""
    b = [list(map(int, row)) for row in basis]
    n = len(b)
    if n < 2:
        return b
    dn, dd = delta
    lam = [[0] * n for _ in range(n)]
    d = [0] * (n + 1)
    d[0] = 1
    d[1] = _dot(b[0], b[0])

    def red(k, l):
        if 2 * abs(lam[k][l]) <= d[l + 1]:
            return
        q = (2 * lam[k][l] + d[l + 1]) // (2 * d[l + 1])  # nearest integer
        b[k] = [bk - q * bl for bk, bl in zip(b[k], b[l])]
        lam[k][l] -= q * d[l + 1]
        for i in range(l):
            lam[k][i] -= q * lam[l][i]

    def swap(k):
        b[k], b[k - 1] = b[k - 1], b[k]
        for j in range(k - 1):
            lam[k][j], lam[k - 1][j] = lam[k - 1][j], lam[k][j]
        lamm = lam[k][k - 1]
        B = (d[k - 1] * d[k + 1] + lamm * lamm) // d[k]
        for i in range(k + 1, kmax + 1):
            t = lam[i][k]
            lam[i][k] = (d[k + 1] * lam[i][k - 1] - lamm * t) // d[k]
            lam[i][k - 1] = (B * t + lamm * lam[i][k]) // d[k + 1]
        d[k] = B

    kmax = 0
    k = 1
    while k < n:
        if k > kmax:
            kmax = k
            for j in range(k + 1):
                u = _dot(b[k], b[j])
                for i in range(j):
                    u = (d[i + 1] * u - lam[k][i] * lam[j][i]) // d[i]
                if j < k:
                    lam[k][j] = u
                else:
                    d[k + 1] = u
        red(k, k - 1)
        if dd * (d[k - 1] * d[k + 1] + lam[k][k - 1] ** 2) < dn * d[k] * d[k]:
            swap(k)
            k = max(k - 1, 1)
        else:
            for l in range(k - 2, -1, -1):
                red(k, l)
            k += 1
    return b


# --------------------------------------------------------------------------
# Coppersmith (Howgrave-Graham):  small roots of f mod a divisor of N
# --------------------------------------------------------------------------


def _integer_roots(coeffs_low_high: list[int], bound: int) -> list[int]:
    """Integer roots r of a polynomial (|r| < bound) using exact root isolation."""
    from sympy import Poly, Symbol
    p_trim(coeffs_low_high)
    if len(coeffs_low_high) <= 1:
        return []
    x = Symbol("x")
    poly = Poly(list(reversed(coeffs_low_high)), x)
    cands: set[int] = set()
    try:
        for r in poly.real_roots():
            ri = int(r)  # CRootOf.__int__ floors; check neighbours too
            cands.update((ri - 1, ri, ri + 1))
    except Exception:
        pass
    return [c for c in cands if abs(c) < bound and p_eval(coeffs_low_high, c) == 0]


def coppersmith_univariate(f: list[int], N: int, X: int, beta: float = 1.0,
                           m: int = 4, t: int | None = None) -> list[int]:
    """Integer roots x0 of a MONIC polynomial f with f(x0) = 0 (mod b), where
    b >= N**beta divides N (beta = 1.0 means mod N itself) and |x0| < X.

    f: coefficients low->high, monic.  Returns integer roots found (verify them
    in the caller).  Increase m if nothing comes back.
    """
    d = len(f) - 1
    assert f[-1] == 1, "f must be monic"
    if t is None:
        t = max(int((1.0 / beta - 1) * m) * d, 1) if beta < 1.0 else 1

    polys: list[list[int]] = []
    for i in range(m):
        fi = p_pow(f, i)
        Nmi = N ** (m - i)
        for j in range(d):
            polys.append(p_mul([0] * j + [1], [c * Nmi for c in fi]))
    fm = p_pow(f, m)
    for i in range(t):
        polys.append(p_mul([0] * i + [1], fm))

    dim = d * m + t
    B = [[0] * dim for _ in range(dim)]
    for r, g in enumerate(polys):
        for k in range(min(len(g), dim)):
            B[r][k] = g[k] * (X ** k)

    B = lll(B)

    # shortest vector -> polynomial over the integers (undo the X^k scaling)
    g0 = [B[0][k] // (X ** k) for k in range(dim)]
    return _integer_roots(g0, X)


def factor_high_bits(n: int, p_high: int, unknown_bits: int, m: int = 8) -> tuple[int, int] | None:
    """Factor n = p*q when you know p except its low `unknown_bits` bits.
    p_high has the unknown low bits zeroed.  Needs unknown_bits < ~ bits(p)/2;
    raise m if it returns None (cost grows with 2**unknown_bits and m)."""
    X = 1 << unknown_bits
    for x0 in coppersmith_univariate([p_high, 1], n, X=X, beta=0.5, m=m, t=m // 2 + 1):
        p = p_high + x0
        if 1 < p < n and n % p == 0:
            return p, n // p
    return None


def stereotyped_e3(c: int, n: int, known_prefix_int: int, unknown_bytes: int,
                   e: int = 3, m: int = 4) -> bytes | None:
    """Recover m = known_prefix_int + x  (0 <= x < 256**unknown_bytes) from
    c = m^e mod n, when the unknown part sits in the LOW bytes (fixed header).
    Works while unknown_bytes < bits(n)/(8*e); raise m if it returns None."""
    X = 1 << (8 * unknown_bytes)
    f = p_pow([known_prefix_int % n, 1], e)
    f[0] = (f[0] - c) % n
    f = [coef % n for coef in f]
    f[-1] = 1  # monic
    for x0 in coppersmith_univariate(f, n, X=X, beta=1.0, m=m, t=1):
        msg = known_prefix_int + x0
        if pow(msg, e, n) == c % n:
            return msg.to_bytes((msg.bit_length() + 7) // 8, "big")
    return None
