"""
RSA attacks (5/6): SIGNATURE FORGERY and FAULT ATTACKS.

  demo                  situation                                   toolkit call
  --------------------- ------------------------------------------- -------------------
  multiplicative_forge  textbook (no-hash) signatures               rsa_multiplicative_forge
  e3_pkcs_forge         e=3 verifier that ignores padding length    rsa_sig_e3_forge
  crt_fault             one glitched RSA-CRT signature              rsa_crt_fault
  known_high_bits       top bits of p known (partial key exposure)  factor_high_bits *
  (* lattice: pure-Python demo size only; see sage_snippets.md for 1024-bit)
"""
from _harness import *


def demo_multiplicative_forge():
    """Textbook RSA signs raw m: sig(a)*sig(b) = sig(a*b). Forge sig(a*b)."""
    p, q = prime(512), prime(512)
    n, e = p * q, 65537
    d = pow(e, -1, (p - 1) * (q - 1))
    a, b = 1234567, 7654321
    forged = rsa_multiplicative_forge(pow(a, d, n), pow(b, d, n), n)
    assert pow(forged, e, n) == a * b % n
    return "multiplicative forgery of a textbook signature"


def demo_e3_pkcs_forge():
    """e=3 verifiers that only scan for the hash (Bleichenbacher '06)."""
    n = prime(1536) * prime(1536)
    digest_info = bytes.fromhex("3031300d060960864801650304020105000420") + hashlib.sha256(FLAG).digest()
    s = rsa_sig_e3_forge(digest_info, n)
    em = i2b(pow(s, 3, n), (n.bit_length() + 7) // 8)
    assert em.startswith(b"\x00\x01\xff\x00" + digest_info)   # a lazy parser accepts it
    return "bleichenbacher e=3: forged PKCS#1 v1.5 signature, no private key"


def demo_crt_fault():
    """A single faulty RSA-CRT signature on a known message factors n (Bellcore)."""
    p, q = prime(512), prime(512)
    n, e = p * q, 65537
    d = pow(e, -1, (p - 1) * (q - 1))
    sp = pow(M, d % (p - 1), p)
    sq = (pow(M, d % (q - 1), q) + 1) % q      # glitch in the q half
    s_bad, _ = crt([sp, sq], [p, q])
    assert set(rsa_crt_fault(n, e, M, s_bad)) == {p, q}
    return "bellcore CRT fault: one bad signature -> factor n"


def demo_known_high_bits():
    """Top bits of p leaked (partial key exposure) -> Coppersmith factoring.
    Small modulus so the pure-Python lattice runs in ~2s."""
    p, q = prime(160), prime(160)
    ub = 55                                    # low 55 bits of p unknown
    res = factor_high_bits(p * q, (p >> ub) << ub, ub, m=6)
    assert set(res) == {p, q}
    return "coppersmith high-bits (DEMO size; real sizes -> sage_snippets.md)"


if __name__ == "__main__":
    run(globals())
