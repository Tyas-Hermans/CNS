"""Self-tests: build a vulnerable instance for every attack and check it is broken.

    python3 test_cryptokit.py          (run from this folder)
"""
import hashlib
import json
import math
import os
import random
import socket
import tempfile
import threading
import time
import traceback

from sympy import nextprime, primerange, primitive_root, randprime

from cryptokit import *

random.seed(1337)
FLAG = b"cns{test_flag_1234}"
M = b2i(FLAG)
results = []


def prime(bits):
    return randprime(1 << (bits - 1), 1 << bits)


def rsa_pair(bits=512, e=65537):
    while True:
        p, q = prime(bits), prime(bits)
        phi = (p - 1) * (q - 1)
        if p != q and math.gcd(e, phi) == 1:
            return p, q


def _sqfree(bits, B):
    pool = list(primerange(3, B))
    while True:
        random.shuffle(pool)
        n, i = 2, 0
        while n.bit_length() < bits and i < len(pool):
            n *= pool[i]; i += 1
        if n.bit_length() >= bits:
            return n


def smooth_prime(bits, B=1 << 16):
    """prime p with p-1 B-smooth (square-free, so every prime power <= B)"""
    while True:
        n = _sqfree(bits, B)
        if is_probable_prime(n + 1):
            return n + 1


def smooth_plus_prime(bits, B=1 << 13):
    """prime p with p+1 B-smooth"""
    while True:
        n = _sqfree(bits, B)
        if is_probable_prime(n - 1):
            return n - 1


def test(fn):
    t = time.perf_counter()
    try:
        fn()
        results.append((fn.__name__, "ok", time.perf_counter() - t))
    except Exception:
        traceback.print_exc()
        results.append((fn.__name__, "FAIL", time.perf_counter() - t))
    return fn


# --------------------------------------------------------------- basics
@test
def conversions_and_crt():
    assert i2b(b2i(FLAG)) == FLAG and show(M) == FLAG.decode()
    assert crt([2, 3, 2], [3, 5, 7]) == (23, 105)
    assert crt([3, 5], [4, 6]) == (11, 12)  # non-coprime moduli
    assert iroot(12345 ** 7, 7) == (12345, True)
    assert iroot(12345 ** 7 + 1, 7) == (12345, False)


@test
def json_loader():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        f.write('t{"n": "123", "c": 5, "h": "0xff", "l": ["1", "2"]}')
    d = load_json(f.name)
    os.unlink(f.name)
    assert d == {"n": 123, "c": 5, "h": 255, "l": [1, 2]}
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write("--- KEY 1 ---\nn = 55\ne = 3\n\n--- KEY 2 ---\nn = 0x4d\ne = 3\nc1 = 7\n")
    v = read_vars(f.name)
    os.unlink(f.name)
    assert v == {"n": [55, 77], "e": [3, 3], "c1": [7]}


# --------------------------------------------------------------- factoring
@test
def factor_close_primes():
    p = prime(512)
    q = nextprime(p + random.randrange(1 << 20))
    assert set(fermat_factor(p * q)) == {p, q}


@test
def factor_smooth_p_minus_1():
    p, q = smooth_prime(256), prime(256)
    f = pollard_p1(p * q, 1 << 16)
    assert f in (p, q)


@test
def factor_smooth_p_plus_1():
    p, q = smooth_plus_prime(256), prime(256)
    assert williams_p1(p * q, 1 << 13) in (p, q)


@test
def factor_small_factor_rho():
    p, q = prime(40), prime(256)
    assert pollard_rho(p * q) in (p, q)


@test
def factor_auto():
    p, q = smooth_prime(200), prime(300)
    assert factor(p * q, verbose=False) == dict(sorted({p: 1, q: 1}.items()))
    r = prime(100)
    assert factor(r ** 3, verbose=False) == {r: 3}


@test
def factor_shared_prime():
    p, q1, q2, q3, q4 = (prime(256) for _ in range(5))
    found = shared_prime_factors([p * q1, q2 * q4, p * q3])
    assert found == {0: (p, q1), 2: (p, q3)}


@test
def factor_given_d_or_phi():
    p, q = rsa_pair()
    n, e = p * q, 65537
    d = pow(e, -1, (p - 1) * (q - 1))
    assert set(factor_from_d(n, e, d)) == {p, q}
    assert set(factor_from_phi(n, (p - 1) * (q - 1))) == {p, q}


# --------------------------------------------------------------- RSA
@test
def rsa_multiprime():
    ps = [prime(128) for _ in range(4)]
    n = math.prod(ps)
    c = pow(M, 65537, n)
    assert rsa_decrypt(c, 65537, n, factors=ps) == M


@test
def rsa_e_not_invertible_rabin():
    while True:
        p, q = prime(256), prime(256)
        if p % 4 == 3 and q % 4 == 3:
            break
    c = pow(M, 2, p * q)
    assert M in rsa_decrypt_all(c, 2, [p, q])


@test
def rsa_small_e():
    p, q = rsa_pair(512, 3)
    assert small_e_root(pow(M, 3, p * q), 3, p * q) == M


@test
def rsa_common_modulus():
    p, q = rsa_pair(512)
    n = p * q
    assert common_modulus(pow(M, 17, n), pow(M, 65537, n), 17, 65537, n) == M
    # gcd(e1, e2) = 3 variant
    assert common_modulus(pow(M, 3 * 17, n), pow(M, 3 * 11, n), 51, 33, n) == M


@test
def rsa_wiener():
    p, q = rsa_pair(512)
    n, phi = p * q, (p - 1) * (q - 1)
    while True:
        d = random.getrandbits(240) | 1
        if math.gcd(d, phi) == 1:
            break
    e = pow(d, -1, phi)
    assert wiener(e, n)[0] == d


@test
def rsa_hastad():
    ns = [math.prod(rsa_pair(512, 3)) for _ in range(3)]
    assert hastad([pow(M, 3, n) for n in ns], ns, 3) == M


@test
def rsa_dp_leak():
    p, q = rsa_pair()
    d = pow(65537, -1, (p - 1) * (q - 1))
    assert set(dp_leak(p * q, 65537, d % (p - 1))) == {p, q}


@test
def rsa_crt_fault_attack():
    p, q = rsa_pair()
    n, e = p * q, 65537
    d = pow(e, -1, (p - 1) * (q - 1))
    sp = pow(M, d % (p - 1), p)
    sq = (pow(M, d % (q - 1), q) + 1) % q  # fault in the q half
    s_bad, _ = crt([sp, sq], [p, q])
    assert set(rsa_crt_fault(n, e, M, s_bad)) == {p, q}


@test
def rsa_cca_blinding():
    p, q = rsa_pair()
    n, e = p * q, 65537
    d = pow(e, -1, (p - 1) * (q - 1))
    c = pow(M, e, n)

    def oracle(x):
        assert x != c, "oracle refuses the target"
        return pow(x, d, n)

    assert rsa_blind_decrypt(c, e, n, oracle) == M
    assert rsa_blind_sign(M, e, n, lambda x: pow(x, d, n) if x != M else 0) == pow(M, d, n)


@test
def rsa_parity_oracle():
    p, q = rsa_pair(256)
    n, e = p * q, 65537
    d = pow(e, -1, (p - 1) * (q - 1))
    c = pow(M, e, n)
    assert lsb_oracle(c, e, n, lambda x: pow(x, d, n) & 1) == M


@test
def rsa_franklin_reiter():
    p, q = rsa_pair(512, 3)
    n = p * q
    m2 = (3 * M + 42) % n
    assert franklin_reiter(pow(M, 3, n), pow(m2, 3, n), 3, n, 3, 42) == M


@test
def rsa_bleichenbacher_e3_forgery():
    n = prime(1536) * prime(1536)
    digest_info = bytes.fromhex("3031300d060960864801650304020105000420") + hashlib.sha256(b"hi").digest()
    s = rsa_sig_e3_forge(digest_info, n)
    em = i2b(pow(s, 3, n), (n.bit_length() + 7) // 8)
    # a sloppy verifier: checks the prefix and parses the hash right after it
    assert em.startswith(b"\x00\x01\xff\x00" + digest_info)


# --------------------------------------------------------------- discrete log
@test
def coppersmith_stereotyped_small():
    # small modulus so pure-Python LLL stays fast; real sizes need Sage/fpylll
    n = prime(160) * prime(160)
    msg = b"launch code: cns{z}"
    unknown = 4
    known = (b2i(msg) >> (8 * unknown)) << (8 * unknown)
    c = pow(b2i(msg), 3, n)
    assert stereotyped_e3(c, n, known, unknown, m=3) == msg


@test
def coppersmith_high_bits_small():
    p, q = prime(160), prime(160)
    ub = 55
    assert set(factor_high_bits(p * q, (p >> ub) << ub, ub, m=6)) == {p, q}


@test
def dlog_pohlig_hellman():
    p = smooth_prime(256, 1 << 20)
    g = primitive_root(p)
    x = random.randrange(p - 1)
    assert dlog(g, pow(g, x, p), p, verbose=False) == x


@test
def dlog_small_secret_partial():
    small = math.prod(list(primerange(3, 400)))  # ~ 500 bits of small factors
    while True:
        big = prime(128)
        p = 2 * small * big + 1
        if is_probable_prime(p):
            break
    g = primitive_root(p)
    x = random.getrandbits(300)  # x < smooth part
    xm, mod = dlog_partial(g, pow(g, x, p), p, verbose=False)
    assert xm == x % mod and xm == x


@test
def bsgs_plain():
    p = prime(40)
    g = primitive_root(p)
    x = random.randrange(p - 1)
    assert pow(g, bsgs(g, pow(g, x, p), p), p) == pow(g, x, p)


# --------------------------------------------------------------- ElGamal
@test
def elgamal_tricks():
    p = nextprime(random.getrandbits(256))
    g = primitive_root(p)
    x = random.randrange(2, p - 1)
    y = pow(g, x, p)
    k = random.randrange(2, p - 1)
    m_known = b2i(b"known plaintext!")
    c1, c2k = pow(g, k, p), m_known * pow(y, k, p) % p
    c2f = M * pow(y, k, p) % p
    assert elgamal_known_plaintext(c2k, m_known, c2f, p) == M
    assert elgamal_decrypt(c1, c2f, x, p) == M
    for k2 in (k, k + 7, k - 3, 5 * k):  # same / counter / multiple nonce
        ct_t = (pow(g, k2, p), M * pow(y, k2, p) % p)
        assert elgamal_related_nonce(p, g, y, (c1, c2k), m_known, ct_t, 100, verbose=False) == M
    a, b = elgamal_malleate(c1, c2f, 2, p)
    assert elgamal_decrypt(a, b, x, p) == 2 * M % p
    for m in (4, 5, 6, 7, 9, 10):  # mix of QR / non-QR
        kk = random.randrange(2, p - 1)
        cc1, cc2 = pow(g, kk, p), m * pow(y, kk, p) % p
        assert elgamal_qr_leak(cc1, cc2, g, y, p) == int(legendre(m, p) == 1)


# --------------------------------------------------------------- signatures
def dsa_params():
    q = prime(160)
    while True:
        k = random.getrandbits(352)
        p = q * k + 1
        if is_probable_prime(p):
            break
    while True:
        g = pow(random.randrange(2, p - 1), (p - 1) // q, p)
        if g > 1:
            return p, q, g


@test
def dsa_nonce_attacks():
    p, q, g = dsa_params()
    x = random.randrange(1, q)
    y = pow(g, x, p)
    h1, h2 = H_int("Transfer 10 EUR", q), H_int("Transfer 9999 EUR", q)
    k = random.randrange(1, q)
    r, s1 = dsa_sign(h1, x, k, p, q, g)
    _, s2 = dsa_sign(h2, x, k, p, q, g)
    assert dsa_verify(h1, r, s1, y, p, q, g)
    assert dsa_reused_k(r, s1, h1, s2, h2, q) == (x, k)
    assert dsa_known_k(r, s1, h1, k, q) == x
    a, b = 1103515245, 12345  # LCG-related nonces
    r1, s1 = dsa_sign(h1, x, k, p, q, g)
    r2, s2 = dsa_sign(h2, x, (a * k + b) % q, p, q, g)
    assert dsa_related_k(r1, s1, h1, r2, s2, h2, q, a, b) == x


@test
def elgamal_signature_attacks():
    p = nextprime(random.getrandbits(128))
    g = primitive_root(p)
    x = random.randrange(2, p - 2)
    y = pow(g, x, p)
    while True:
        k = random.randrange(2, p - 1)
        if math.gcd(k, p - 1) == 1:
            break
    r = pow(g, k, p)
    h1, h2 = 1234567, 7654321
    s1 = pow(k, -1, p - 1) * (h1 - x * r) % (p - 1)
    s2 = pow(k, -1, p - 1) * (h2 - x * r) % (p - 1)
    assert any(xx == x for _, xx in elgamal_sig_reused_k(r, s1, h1, s2, h2, p))
    m, rf, sf = elgamal_sig_existential_forgery(g, y, p, e=5, v=1)
    assert pow(g, m, p) == pow(y, rf, p) * pow(rf, sf, p) % p


# --------------------------------------------------------------- networking
@test
def remote_helper():
    srv = socket.socket()
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]

    def serve():
        conn, _ = srv.accept()
        conn.sendall(b"n = 0x10\ne = 3\n> ")
        data = conn.recv(100)
        conn.sendall(b"echo " + data)
        conn.close()

    threading.Thread(target=serve, daemon=True).start()
    with Remote("127.0.0.1", port) as io:
        banner = io.recvuntil("> ")
        assert ints_in(banner) == [16, 3]
        io.sendline(42)
        assert io.recvall() == b"echo 42\n"
    srv.close()


if __name__ == "__main__":
    print()
    for name, status, t in results:
        print(f"{status:>4}  {t:6.2f}s  {name}")
    bad = [r for r in results if r[1] != "ok"]
    print(f"\n{len(results) - len(bad)}/{len(results)} passed")
    raise SystemExit(1 if bad else 0)
