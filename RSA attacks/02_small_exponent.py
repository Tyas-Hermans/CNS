"""
RSA attacks (2/6): SMALL PUBLIC EXPONENT e (usually e = 3).

A small e means m^e barely wraps around n -- or not at all -- so the message
can be pulled back out without factoring.

  demo                  situation                                   toolkit call
  --------------------- ------------------------------------------- -------------------
  cube_root             m^e < n (short/unpadded message)            small_e_root
  hastad_broadcast      same m to >= e recipients                   hastad
  franklin_reiter       two messages, m2 = a*m1 + b, same n         franklin_reiter
  coppersmith_stereo    most of m known, small unknown part         stereotyped_e3 *
  (* lattice: pure-Python demo size only; see sage_snippets.md for 1024-bit)
"""
from _harness import *


def demo_cube_root():
    """Short message, e=3, no padding: m^3 < n, so take an exact cube root."""
    n = prime(512) * prime(512)          # 1024-bit, but the flag is short
    c = pow(M, 3, n)
    assert i2b(small_e_root(c, 3, n)) == FLAG
    return "plain cube root: unpadded short message"


def demo_hastad_broadcast():
    """Same m sent to 3 people, all with e=3: CRT then a cube root."""
    ns = [prime(512) * prime(512) for _ in range(3)]
    cs = [pow(M, 3, n) for n in ns]
    assert i2b(hastad(cs, ns, 3)) == FLAG
    return "hastad: one message, >= e recipients"


def demo_franklin_reiter():
    """Two related messages (m2 = 3*m1 + 42) under the same key leak m1."""
    n = prime(512) * prime(512)
    m2 = (3 * M + 42) % n
    c1, c2 = pow(M, 3, n), pow(m2, 3, n)
    assert i2b(franklin_reiter(c1, c2, 3, n, 3, 42)) == FLAG
    return "franklin-reiter: known linear relation between two messages"


def demo_coppersmith_stereotyped():
    """Known header + small unknown tail, e=3 -> Coppersmith.
    Small modulus here so the pure-Python lattice stays fast (~10s)."""
    n = prime(160) * prime(160)
    msg = b"the code is: " + FLAG[-6:]   # last 6 bytes unknown
    unknown = 6
    known = (b2i(msg) >> (8 * unknown)) << (8 * unknown)
    c = pow(b2i(msg), 3, n)
    assert stereotyped_e3(c, n, known, unknown, m=3) == msg
    return "coppersmith stereotyped (DEMO size; real sizes -> sage_snippets.md)"


if __name__ == "__main__":
    run(globals())
