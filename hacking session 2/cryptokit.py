"""
cryptokit -- reusable helpers for the asymmetric-crypto hacking session.

Only needs the standard library + sympy.  Import it from a solve script with:

    import sys; sys.path.insert(0, "../hacking session 2")   # adjust path
    from cryptokit import *

Every attack has a self-test in test_cryptokit.py; see CHEATSHEET.md for
"what do I see -> which function do I call".
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import socket
import time
from fractions import Fraction
from typing import Callable, Iterable

# ---------------------------------------------------------------------------
# Conversions
# ---------------------------------------------------------------------------


def b2i(b: bytes | str) -> int:
    """bytes/str -> int (big endian), like Crypto.Util.number.bytes_to_long."""
    if isinstance(b, str):
        b = b.encode()
    return int.from_bytes(b, "big")


def i2b(n: int, length: int | None = None) -> bytes:
    """int -> bytes (big endian), like long_to_bytes."""
    if length is None:
        length = max(1, (n.bit_length() + 7) // 8)
    return n.to_bytes(length, "big")


def show(n: int) -> str:
    """Best-effort printable version of a recovered plaintext integer."""
    b = i2b(n)
    try:
        return b.decode()
    except UnicodeDecodeError:
        # maybe it is padded (PKCS#1 v1.5: 00 02 <random> 00 <msg>)
        if b"\x00" in b[1:]:
            tail = b[b.index(b"\x00", 1) + 1:]
            try:
                return "[after padding] " + tail.decode()
            except UnicodeDecodeError:
                pass
        return repr(b)


def load_json(path: str) -> dict:
    """json.load that turns numeric strings / hex strings into ints where obvious
    and tolerates junk before the first '{' (seen in the Double Entry file)."""
    raw = open(path, encoding="utf-8").read()
    raw = raw[raw.index("{"):] if "{" in raw else raw
    data = json.loads(raw)

    def conv(v):
        if isinstance(v, str):
            s = v.strip()
            if s.isdigit():
                return int(s)
            if s.lower().startswith("0x"):
                try:
                    return int(s, 16)
                except ValueError:
                    return v
        if isinstance(v, list):
            return [conv(x) for x in v]
        if isinstance(v, dict):
            return {k: conv(x) for k, x in v.items()}
        return v

    return conv(data)


def read_vars(path: str) -> dict[str, list[int]]:
    """Parse text files with lines like 'n = 123' / 'c1 = 0xabc'.
    Returns {name: [values in file order]}, e.g. {'n': [n1, n2, n3], 'e': [3, 3, 3]}."""
    import re
    out: dict[str, list[int]] = {}
    for name, val in re.findall(r"^\s*(\w+)\s*[=:]\s*(0x[0-9a-fA-F]+|-?\d+)\s*$",
                                open(path, encoding="utf-8").read(), flags=re.M):
        out.setdefault(name, []).append(int(val, 0))
    return out


def flag_in(b: bytes | str, prefix: str = "cns{") -> bool:
    if isinstance(b, int):
        b = i2b(b)
    if isinstance(b, bytes):
        b = b.decode(errors="ignore")
    return prefix in b


# ---------------------------------------------------------------------------
# Number theory
# ---------------------------------------------------------------------------


def egcd(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, x, y) with a*x + b*y = g = gcd(a, b)."""
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def inv(a: int, n: int) -> int:
    return pow(a, -1, n)


def crt(remainders: Iterable[int], moduli: Iterable[int]) -> tuple[int, int]:
    """Chinese remainder theorem, also for NON-coprime moduli.
    Returns (x, lcm).  Raises ValueError if the system is inconsistent."""
    x, m = 0, 1
    for r, n in zip(remainders, moduli):
        g, p, _ = egcd(m, n)
        if (r - x) % g:
            raise ValueError("inconsistent CRT system")
        lcm = m // g * n
        x = (x + (r - x) // g * p % (n // g) * m) % lcm
        m = lcm
    return x, m


def iroot(x: int, k: int) -> tuple[int, bool]:
    """Integer k-th root: returns (floor(x**(1/k)), exact?)."""
    if x < 0:
        raise ValueError("negative")
    if x < 2:
        return x, True
    r = 1 << ((x.bit_length() + k - 1) // k)  # >= true root
    while True:
        y = ((k - 1) * r + x // r ** (k - 1)) // k
        if y >= r:
            break
        r = y
    return r, r ** k == x


def is_square(x: int) -> bool:
    return x >= 0 and math.isqrt(x) ** 2 == x


def is_probable_prime(n: int, rounds: int = 32) -> bool:
    """Miller-Rabin."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def continued_fraction(num: int, den: int) -> list[int]:
    out = []
    while den:
        q = num // den
        out.append(q)
        num, den = den, num - q * den
    return out


def convergents(cf: list[int]):
    """Yield (h, k) with h/k the convergents of the continued fraction."""
    h0, h1, k0, k1 = 0, 1, 1, 0
    for a in cf:
        h0, h1 = h1, a * h1 + h0
        k0, k1 = k1, a * k1 + k0
        yield h1, k1


def nth_roots_mod_prime(a: int, e: int, p: int) -> list[int]:
    """All x with x^e = a (mod p), p prime.  Works when gcd(e, p-1) != 1."""
    from sympy.ntheory.residue_ntheory import nthroot_mod
    a %= p
    if a == 0:
        return [0]
    roots = nthroot_mod(a, e, p, all_roots=True)
    return sorted(set(int(r) for r in roots)) if roots else []


def sqrt_mod_prime(a: int, p: int) -> list[int]:
    """Square roots mod an odd prime (Tonelli-Shanks via sympy)."""
    from sympy.ntheory import sqrt_mod
    r = sqrt_mod(a % p, p, all_roots=True)
    return sorted(int(x) for x in r) if r else []


# ---------------------------------------------------------------------------
# Factoring
# ---------------------------------------------------------------------------


def trial_division(n: int, limit: int = 1 << 16) -> list[int]:
    """Small prime factors (with multiplicity) below `limit`."""
    out, d = [], 2
    while d < limit and d * d <= n:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1 if d == 2 else 2
    return out


def fermat_factor(n: int, max_steps: int = 2_000_000) -> tuple[int, int] | None:
    """p and q close together (|p-q| small) -> n = a^2 - b^2."""
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    b2 = a * a - n
    for _ in range(max_steps):
        b = math.isqrt(b2)
        if b * b == b2:
            return a - b, a + b
        b2 += 2 * a + 1
        a += 1
    return None


def pollard_rho(n: int, max_steps: int = 10_000_000) -> int | None:
    """Brent's variant; finds a factor ~ sqrt(p) steps for smallest prime p."""
    if n % 2 == 0:
        return 2
    for c in range(1, 20):
        y, r, q, g = random.randrange(1, n), 1, 1, 1
        m = 128
        x = ys = y
        steps = 0
        while g == 1 and steps < max_steps:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = math.gcd(q, n)
                k += m
            r *= 2
            steps += r
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = math.gcd(abs(x - ys), n)
        if 1 < g < n:
            return g
    return None


def pollard_p1(n: int, bound: int = 1 << 20) -> int | None:
    """Works if p-1 is `bound`-smooth for some prime p | n."""
    from sympy import primerange
    a = 2
    for p in primerange(2, bound):
        pk = p
        while pk * p <= bound:
            pk *= p
        a = pow(a, pk, n)
        if p % 1024 == 1:  # check occasionally
            g = math.gcd(a - 1, n)
            if 1 < g < n:
                return g
            if g == n:
                return None
    g = math.gcd(a - 1, n)
    return g if 1 < g < n else None


def williams_p1(n: int, bound: int = 1 << 18) -> int | None:
    """Williams p+1: works if p+1 is smooth."""
    from sympy import primerange

    def lucas_v(v, k):  # V_k(v) mod n
        x, y = v, (v * v - 2) % n
        for bit in bin(k)[3:]:
            if bit == "1":
                x, y = (x * y - v) % n, (y * y - 2) % n
            else:
                x, y = (x * x - 2) % n, (x * y - v) % n
        return x

    for v0 in (3, 5, 7, 9, 11, 13):
        v = v0
        for p in primerange(2, bound):
            pk = p
            while pk * p <= bound:
                pk *= p
            v = lucas_v(v, pk)
        g = math.gcd(v - 2, n)
        if 1 < g < n:
            return g
    return None


def shared_prime_factors(ns: list[int]) -> dict[int, tuple[int, int]]:
    """Several moduli that share a prime: gcd factors them.  {index: (p, q)}."""
    found = {}
    for i in range(len(ns)):
        for j in range(i + 1, len(ns)):
            g = math.gcd(ns[i], ns[j])
            if 1 < g:
                for k in (i, j):
                    if g < ns[k]:
                        found[k] = (g, ns[k] // g)
    return found


def factor_from_d(n: int, e: int, d: int) -> tuple[int, int]:
    """Knowing (n, e, d) lets you factor n (Boneh's probabilistic method)."""
    k = e * d - 1
    t = (k & -k).bit_length() - 1
    r = k >> t
    while True:
        g = random.randrange(2, n - 1)
        y = pow(g, r, n)
        if y in (1, n - 1):
            continue
        for _ in range(t):
            x = pow(y, 2, n)
            if x == 1:
                p = math.gcd(y - 1, n)
                return p, n // p
            if x == n - 1:
                break
            y = x


def factor_from_phi(n: int, phi: int) -> tuple[int, int]:
    """n = pq and phi = (p-1)(q-1) -> p, q are roots of x^2 - (n-phi+1)x + n."""
    s = n - phi + 1
    disc = s * s - 4 * n
    r = math.isqrt(disc)
    assert r * r == disc, "phi does not belong to a 2-prime n"
    return (s + r) // 2, (s - r) // 2


def factor(n: int, verbose: bool = True, rho_steps: int = 3_000_000) -> dict[int, int]:
    """Try the cheap attacks in order, then fall back to sympy.factorint.
    Returns {prime: exponent}."""
    from sympy import factorint

    def log(msg):
        if verbose:
            print("[factor]", msg)

    result: dict[int, int] = {}
    stack = [n]
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if is_probable_prime(m):
            result[m] = result.get(m, 0) + 1
            continue
        for p in trial_division(m, 1 << 14):
            log(f"small factor {p}")
            result[p] = result.get(p, 0) + 1
            m //= p
        if m == 1:
            continue
        if is_probable_prime(m):
            result[m] = result.get(m, 0) + 1
            continue
        # perfect power?  (n = p^k)
        for k in range(2, 64):
            r, exact = iroot(m, k)
            if exact:
                log(f"perfect power: root^{k}")
                stack.extend([r] * k)
                break
        else:
            f = None
            for name, fn in (("fermat (close primes)", lambda: (fermat_factor(m, 200_000) or (None,))[0]),
                             ("pollard p-1 (smooth p-1)", lambda: pollard_p1(m, 1 << 18)),
                             ("pollard rho (small factor)", lambda: pollard_rho(m, rho_steps)),
                             ("williams p+1 (smooth p+1)", lambda: williams_p1(m, 1 << 15))):
                f = fn()
                if f and 1 < f < m:
                    log(f"{name} -> found {f.bit_length()}-bit factor")
                    break
                f = None
            if f:
                stack.extend([f, m // f])
            else:
                log("cheap methods failed, trying sympy.factorint (may take forever; "
                    "also try https://factordb.com)")
                for p, k in factorint(m).items():
                    result[p] = result.get(p, 0) + k
    return dict(sorted(result.items()))


# ---------------------------------------------------------------------------
# RSA
# ---------------------------------------------------------------------------


def phi_from_factors(factors: dict[int, int] | Iterable[int]) -> int:
    if not isinstance(factors, dict):
        f: dict[int, int] = {}
        for p in factors:
            f[p] = f.get(p, 0) + 1
        factors = f
    out = 1
    for p, k in factors.items():
        out *= p ** (k - 1) * (p - 1)
    return out


def rsa_decrypt(c: int, e: int, n: int, factors=None, d: int | None = None) -> int:
    """Decrypt given d, or given the factorisation of n (dict or list, multi-prime ok).
    If gcd(e, phi) != 1 this returns ONE candidate -- use rsa_decrypt_all."""
    if d is None:
        if factors is None:
            factors = factor(n)
        d = pow(e, -1, phi_from_factors(factors))
    return pow(c, d, n)


def rsa_decrypt_all(c: int, e: int, factors: dict[int, int] | list[int],
                    want: Callable[[int], bool] = flag_in) -> list[int]:
    """Decryption when e is NOT invertible mod phi (gcd(e, p-1) > 1, e.g. e = 2 Rabin,
    or e | p-1).  Finds all e-th roots mod each prime and combines with CRT.
    Only square-free n.  Returns candidates for which want(m) is true."""
    if isinstance(factors, dict):
        assert all(k == 1 for k in factors.values()), "prime powers not supported here"
        primes = list(factors)
    else:
        primes = list(factors)
    per_prime = [nth_roots_mod_prime(c, e, p) for p in primes]
    out = []

    def rec(i, rs):
        if i == len(primes):
            m, _ = crt(rs, primes)
            if want(m):
                out.append(m)
            return
        for r in per_prime[i]:
            rec(i + 1, rs + [r])

    rec(0, [])
    return out


def small_e_root(c: int, e: int, n: int, max_k: int = 100_000) -> int | None:
    """Unpadded m with m^e only slightly bigger than n: m^e = c + k*n."""
    for k in range(max_k):
        m, exact = iroot(c + k * n, e)
        if exact:
            return m
    return None


def common_modulus(c1: int, c2: int, e1: int, e2: int, n: int) -> int:
    """Same m, same n, two exponents.  Also handles gcd(e1, e2) = g > 1
    (then you get m^g and take a g-th root, assuming m^g < n)."""
    g, a, b = egcd(e1, e2)
    mg = pow(c1, a, n) * pow(c2, b, n) % n  # = m^g
    if g == 1:
        return mg
    m = small_e_root(mg, g, n)
    if m is None:
        raise ValueError(f"gcd(e1,e2)={g}: got m^{g} mod n but no small root")
    return m


def wiener(e: int, n: int) -> tuple[int, int, int] | None:
    """Small d (d < n^0.25 / 3).  Returns (d, p, q)."""
    for k, d in convergents(continued_fraction(e, n)):
        if k == 0 or (e * d - 1) % k:
            continue
        phi = (e * d - 1) // k
        s = n - phi + 1
        disc = s * s - 4 * n
        if disc >= 0 and is_square(disc):
            r = math.isqrt(disc)
            p, q = (s + r) // 2, (s - r) // 2
            if p * q == n:
                return d, p, q
    return None


def hastad(cs: list[int], ns: list[int], e: int, max_k: int = 10_000) -> int:
    """Same m sent to >= e recipients with the same small e (no padding)."""
    x, N = crt(cs, ns)
    m = small_e_root(x, e, N, max_k)
    if m is None:
        raise ValueError("no exact root: need more ciphertexts or the message is padded "
                         "(padded -> Coppersmith, see CHEATSHEET)")
    return m


def dp_leak(n: int, e: int, dp: int) -> tuple[int, int]:
    """Leaked CRT exponent dp = d mod (p-1)  ->  p = gcd(r^(e*dp) - r, n)."""
    for r in (2, 3, 5, 7):
        p = math.gcd(pow(r, e * dp, n) - r, n)
        if 1 < p < n:
            return p, n // p
    raise ValueError("dp leak failed")


def rsa_crt_fault(n: int, e: int, m: int, faulty_sig: int) -> tuple[int, int]:
    """Faulty RSA-CRT signature s' on known m: p = gcd(s'^e - m, n)  (Bellcore)."""
    p = math.gcd(pow(faulty_sig, e, n) - m, n)
    assert 1 < p < n
    return p, n // p


def rsa_blind_decrypt(c: int, e: int, n: int, oracle: Callable[[int], int], r: int = 2) -> int:
    """Chosen-ciphertext attack: oracle decrypts anything EXCEPT c.
    Send c * r^e, get m*r, divide by r."""
    mr = oracle(c * pow(r, e, n) % n)
    return mr * pow(r, -1, n) % n


def rsa_blind_sign(m: int, e: int, n: int, sign_oracle: Callable[[int], int], r: int = 2) -> int:
    """Signing oracle refuses m: sign m*r^e instead and divide by r."""
    s = sign_oracle(m * pow(r, e, n) % n)
    return s * pow(r, -1, n) % n


def rsa_multiplicative_forge(sig_a: int, sig_b: int, n: int) -> int:
    """Textbook RSA signatures: sig(a) * sig(b) = sig(a*b)."""
    return sig_a * sig_b % n


def lsb_oracle(c: int, e: int, n: int, parity: Callable[[int], int]) -> int:
    """Parity / LSB oracle: parity(c') returns (c'^d mod n) & 1.
    Needs ~log2(n) queries.  Exact integer version (no float drift)."""
    k = n.bit_length()
    two_e = pow(2, e, n)
    lo, hi = Fraction(0), Fraction(n)
    cur = c
    for _ in range(k):
        cur = cur * two_e % n
        mid = (lo + hi) / 2
        if parity(cur):
            lo = mid
        else:
            hi = mid
    m = int(hi)
    # fix off-by-one at the end
    for cand in (m - 1, m, m + 1):
        if pow(cand, e, n) == c % n:
            return cand
    return m


def poly_gcd_mod(f: list[int], g: list[int], n: int) -> list[int]:
    """GCD of polynomials over Z_n (coefficients low -> high).  n must be 'prime-like'."""

    def trim(p):
        while p and p[-1] % n == 0:
            p.pop()
        return p

    f, g = trim([x % n for x in f]), trim([x % n for x in g])
    while g:
        inv_lead = pow(g[-1], -1, n)
        while len(f) >= len(g):
            coef = f[-1] * inv_lead % n
            shift = len(f) - len(g)
            for i, gc in enumerate(g):
                f[shift + i] = (f[shift + i] - coef * gc) % n
            trim(f)
            if not f:
                break
        f, g = g, f
    inv_lead = pow(f[-1], -1, n)
    return [x * inv_lead % n for x in f]


def _poly_pow_linear(a: int, b: int, e: int, n: int) -> list[int]:
    """(a*x + b)^e mod n as coefficient list (binomial theorem)."""
    out, binom = [], 1
    for i in range(e + 1):
        out.append(binom * pow(a, i, n) * pow(b, e - i, n) % n)
        binom = binom * (e - i) // (i + 1)
    return out


def franklin_reiter(c1: int, c2: int, e: int, n: int, a: int, b: int) -> int:
    """Related messages: m2 = a*m1 + b, both encrypted with the same (n, e).
    gcd(x^e - c1, (a x + b)^e - c2) = x - m1.  Practical for small e (<= ~ 1000)."""
    f1 = [(-c1) % n] + [0] * (e - 1) + [1]
    f2 = _poly_pow_linear(a, b, e, n)
    f2[0] = (f2[0] - c2) % n
    g = poly_gcd_mod(f1, f2, n)
    if len(g) != 2:
        raise ValueError(f"gcd has degree {len(g) - 1}, expected 1")
    return (-g[0]) % n


def rsa_sig_e3_forge(msg_digest_info: bytes, n: int, e: int = 3) -> int:
    """Bleichenbacher '06 forgery for verifiers that don't check the padding length:
    build 00 01 FF 00 <digestinfo> <garbage> and take the cube root."""
    k = (n.bit_length() + 7) // 8
    prefix = b"\x00\x01\xff\x00" + msg_digest_info
    garbage = k - len(prefix)
    lo = b2i(prefix + b"\x00" * garbage)
    hi = b2i(prefix + b"\xff" * garbage)
    s, _ = iroot(hi, e)
    if s ** e < lo:
        raise ValueError("no cube in range (key too small?)")
    return s


# ---------------------------------------------------------------------------
# Discrete log / Diffie-Hellman / ElGamal
# ---------------------------------------------------------------------------


def bsgs(g: int, h: int, p: int, order: int | None = None) -> int | None:
    """Baby-step giant-step: x with g^x = h mod p, in O(sqrt(order)) memory/time."""
    N = order or (p - 1)
    m = math.isqrt(N) + 1
    table = {}
    e = 1
    for j in range(m):
        table.setdefault(e, j)
        e = e * g % p
    factor_ = pow(g, -m, p)
    gamma = h % p
    for i in range(m + 1):
        if gamma in table:
            return i * m + table[gamma]
        gamma = gamma * factor_ % p
    return None


def dlog(g: int, h: int, p: int, order: int | None = None, verbose: bool = True) -> int:
    """Pohlig-Hellman + BSGS.  Fast when the group order (p-1) is smooth.
    Prints the factorisation so you can see whether it is feasible."""
    from sympy import factorint
    N = order or (p - 1)
    fac = factorint(N)
    if verbose:
        big = max(fac)
        print(f"[dlog] order factors: largest prime factor has {big.bit_length()} bits")
    xs, ms = [], []
    for q, k in fac.items():
        qk = q ** k
        gi = pow(g, N // qk, p)
        hi = pow(h, N // qk, p)
        # solve x mod q^k digit by digit
        gamma = pow(gi, qk // q, p)  # order q
        x = 0
        for j in range(k):
            hk = pow(pow(gi, -x, p) * hi % p, qk // q ** (j + 1), p)
            d = bsgs(gamma, hk, p, q)
            if d is None:
                raise ValueError(f"no log mod {q}")
            x += d * q ** j
        xs.append(x)
        ms.append(qk)
    x, _ = crt(xs, ms)
    assert pow(g, x, p) == h % p, "dlog check failed (is g a generator / order right?)"
    return x


def dlog_partial(g: int, h: int, p: int, max_bits: int = 48, verbose: bool = True) -> tuple[int, int]:
    """When p-1 has ONE huge prime factor: still recover x mod (smooth part).
    Useful if the secret x is small (< smooth part) -> that IS x.
    Returns (x mod M, M)."""
    from sympy import factorint
    N = p - 1
    fac = factorint(N, limit=1 << 20)
    smooth = {q: k for q, k in fac.items() if q.bit_length() <= max_bits and is_probable_prime(q)}
    xs, ms = [], []
    for q, k in smooth.items():
        qk = q ** k
        gi, hi = pow(g, N // qk, p), pow(h, N // qk, p)
        x = dlog(gi, hi, p, order=qk, verbose=False) if qk > 1 else 0
        xs.append(x % qk)
        ms.append(qk)
    x, M = crt(xs, ms)
    if verbose:
        print(f"[dlog_partial] know x mod a {M.bit_length()}-bit number")
    return x, M


def elgamal_decrypt(c1: int, c2: int, x: int, p: int) -> int:
    s = pow(c1, x, p)
    return c2 * pow(s, -1, p) % p


def elgamal_known_plaintext(c2_known: int, m_known: int, c2_target: int, p: int) -> int:
    """Same k (same c1) used twice: mask cancels."""
    s = c2_known * pow(m_known, -1, p) % p
    return c2_target * pow(s, -1, p) % p


def elgamal_related_nonce(p: int, g: int, y: int, ct_known: tuple[int, int], m_known: int,
                          ct_target: tuple[int, int], search: int = 1 << 20,
                          verbose: bool = True) -> int | None:
    """Known plaintext + a target whose nonce is related to the known one:
    same k, k + d, k - d, or a*k (|d|, a <= search).  Returns the target plaintext."""
    (c1k, c2k), (c1t, c2t) = ct_known, ct_target
    s_known = c2k * pow(m_known, -1, p) % p
    s_t = None
    if c1k == c1t:
        how, s_t = "same k", s_known
    else:
        g_inv = pow(g, -1, p)
        up = down = mult = c1k
        for d in range(1, search + 1):
            up, down = up * g % p, down * g_inv % p
            mult = mult * c1k % p  # c1k^(d+1)
            if up == c1t:
                how, s_t = f"k + {d}", s_known * pow(y, d, p) % p
            elif down == c1t:
                how, s_t = f"k - {d}", s_known * pow(y, -d, p) % p
            elif mult == c1t:
                how, s_t = f"{d + 1} * k", pow(s_known, d + 1, p)
            if s_t is not None:
                break
    if s_t is None:
        return None
    if verbose:
        print(f"[elgamal] target nonce = {how}")
    return c2t * pow(s_t, -1, p) % p


def elgamal_malleate(c1: int, c2: int, factor_: int, p: int) -> tuple[int, int]:
    """(c1, c2*t) decrypts to m*t -- ElGamal is multiplicatively malleable."""
    return c1, c2 * factor_ % p


def legendre(a: int, p: int) -> int:
    """1 if quadratic residue, p-1 (== -1) if not, 0 if divisible."""
    return pow(a, (p - 1) // 2, p)


def elgamal_qr_leak(c1: int, c2: int, g: int, y: int, p: int) -> int | None:
    """If g generates all of Z_p^*, ElGamal leaks whether m is a quadratic residue
    (one bit, breaks semantic security).  Returns 1 (QR), 0 (non-QR) or None."""
    y_is_qr = legendre(y, p) == 1
    c1_is_qr = legendre(c1, p) == 1
    mask_qr = y_is_qr or c1_is_qr  # y^k is QR iff x even or k even
    c2_qr = legendre(c2, p) == 1
    return int(c2_qr == mask_qr)


# ---------------------------------------------------------------------------
# Signatures: DSA / ECDSA / ElGamal / Schnorr nonce problems
# ---------------------------------------------------------------------------


def H_int(msg: bytes | str, q: int | None = None, algo: str = "sha256") -> int:
    if isinstance(msg, str):
        msg = msg.encode()
    h = int(hashlib.new(algo, msg).hexdigest(), 16)
    return h % q if q else h


def dsa_reused_k(r: int, s1: int, h1: int, s2: int, h2: int, q: int) -> tuple[int, int]:
    """Two (EC)DSA signatures with the same r (same k).  Returns (x, k)."""
    k = (h1 - h2) * pow(s1 - s2, -1, q) % q
    x = (s1 * k - h1) * pow(r, -1, q) % q
    return x, k


def dsa_known_k(r: int, s: int, h: int, k: int, q: int) -> int:
    """Known nonce -> private key."""
    return (s * k - h) * pow(r, -1, q) % q


def dsa_related_k(r1, s1, h1, r2, s2, h2, q, a: int, b: int) -> int:
    """Nonces related by k2 = a*k1 + b (e.g. counter: a=1, b=1; LCG).
    Returns x.  Two linear equations in (k1, x)."""
    # s1 k1 = h1 + x r1 ;  s2 (a k1 + b) = h2 + x r2
    # from first: k1 = (h1 + x r1)/s1  -> substitute
    s1i = pow(s1, -1, q)
    # s2*a*(h1 + x r1)*s1i + s2*b = h2 + x r2
    coef_x = (s2 * a * r1 * s1i - r2) % q
    const = (h2 - s2 * a * h1 * s1i - s2 * b) % q
    return const * pow(coef_x, -1, q) % q


def dsa_sign(h: int, x: int, k: int, p: int, q: int, g: int) -> tuple[int, int]:
    r = pow(g, k, p) % q
    s = pow(k, -1, q) * (h + x * r) % q
    return r, s


def dsa_verify(h: int, r: int, s: int, y: int, p: int, q: int, g: int) -> bool:
    if not (0 < r < q and 0 < s < q):
        return False
    w = pow(s, -1, q)
    v = pow(g, h * w % q, p) * pow(y, r * w % q, p) % p % q
    return v == r


def elgamal_sig_reused_k(r, s1, h1, s2, h2, p) -> list[tuple[int, int]]:
    """ElGamal signatures s = k^-1 (h - x r) mod (p-1), same k twice.
    Returns candidate (k, x) pairs (gcd issues mod p-1 give several)."""
    n = p - 1
    out = []
    ds, dh = (s1 - s2) % n, (h1 - h2) % n
    g = math.gcd(ds, n)
    if dh % g:
        return out
    k0 = (dh // g) * pow(ds // g, -1, n // g) % (n // g)
    for i in range(g):
        k = k0 + i * (n // g)
        rhs = (h1 - s1 * k) % n  # x r = h - s k
        g2 = math.gcd(r, n)
        if rhs % g2:
            continue
        x0 = (rhs // g2) * pow(r // g2, -1, n // g2) % (n // g2)
        for j in range(g2):
            out.append((k, x0 + j * (n // g2)))
    return out


def elgamal_sig_existential_forgery(g: int, y: int, p: int, e: int = 1, v: int = 1):
    """Forge (m, r, s) for a RANDOM message m when the verifier signs the raw m
    (no hash):  r = g^e y^v, s = -r v^-1, m = e s  (mod p-1)."""
    n = p - 1
    r = pow(g, e, p) * pow(y, v, p) % p
    s = (-r * pow(v, -1, n)) % n
    m = e * s % n
    return m, r, s


# ---------------------------------------------------------------------------
# Networking helper (pwntools-like, stdlib only)
# ---------------------------------------------------------------------------


class Remote:
    """Tiny pwntools-style socket wrapper.

        io = Remote("cns-test.idlab.uantwerpen.be", 50012)
        print(io.recvuntil(b"> "))
        io.sendline(b"hello")
        line = io.recvline()
    """

    def __init__(self, host: str, port: int, timeout: float = 10.0, debug: bool = False):
        self.s = socket.create_connection((host, port), timeout=timeout)
        self.buf = b""
        self.debug = debug

    def _fill(self) -> bool:
        chunk = self.s.recv(4096)
        if self.debug and chunk:
            print("<<", chunk)
        self.buf += chunk
        return bool(chunk)

    def recvuntil(self, delim: bytes | str) -> bytes:
        if isinstance(delim, str):
            delim = delim.encode()
        while delim not in self.buf:
            if not self._fill():
                break
        i = self.buf.find(delim)
        if i < 0:
            out, self.buf = self.buf, b""
            return out
        out, self.buf = self.buf[:i + len(delim)], self.buf[i + len(delim):]
        return out

    def recvline(self) -> bytes:
        return self.recvuntil(b"\n")

    def recvall(self) -> bytes:
        while self._fill():
            pass
        out, self.buf = self.buf, b""
        return out

    def send(self, data: bytes | str):
        if isinstance(data, str):
            data = data.encode()
        if self.debug:
            print(">>", data)
        self.s.sendall(data)

    def sendline(self, data: bytes | str | int):
        if isinstance(data, int):
            data = str(data)
        if isinstance(data, str):
            data = data.encode()
        self.send(data + b"\n")

    def sendlineafter(self, delim, data) -> bytes:
        out = self.recvuntil(delim)
        self.sendline(data)
        return out

    def timed(self, data: bytes | str, delim: bytes | str) -> tuple[float, bytes]:
        """Send and measure the time until `delim` arrives (timing attacks)."""
        t = time.perf_counter()
        self.sendline(data)
        out = self.recvuntil(delim)
        return time.perf_counter() - t, out

    def close(self):
        self.s.close()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()


def ints_in(text: bytes | str) -> list[int]:
    """Pull every (decimal or 0x-hex) integer out of server output."""
    import re
    if isinstance(text, bytes):
        text = text.decode(errors="ignore")
    return [int(t, 0) for t in re.findall(r"0x[0-9a-fA-F]+|\d+", text)]
