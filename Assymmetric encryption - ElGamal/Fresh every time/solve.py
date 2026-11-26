"""
Fresh every time -- ElGamal nonces from a counter (k, k+1) + known plaintext.

ElGamal encryption of message m with public key (p, g, y = g^x):
    pick random k
    c1 = g^k        mod p
    c2 = m * y^k    mod p
The value s = y^k is a one-time "mask". It must be different for every message.

Here c1_flag == c1_known * g, so k_flag = k_known + 1:
    s_known = c2_known * m_known^-1          (mask of the known message: y^k)
    s_flag  = s_known * y                    (y^(k+1) = y^k * y)
    m_flag  = c2_flag * s_flag^-1
We never need to know k itself.
"""
import json
from pathlib import Path

d = json.loads((Path(__file__).parent / "ElGamal_challenge.json").read_text())
p, g, y = d["p"], d["g"], d["y"]
(c1_k, c2_k), (c1_f, c2_f) = d["cipher_known"], d["cipher_flag"]

assert c1_f == c1_k * g % p, "nonce is not k+1, see the general version below"

m_k = int.from_bytes(d["known_plaintext"].encode(), "big")
s_k = c2_k * pow(m_k, -1, p) % p
s_f = s_k * y % p
m_f = c2_f * pow(s_f, -1, p) % p

print(m_f.to_bytes((m_f.bit_length() + 7) // 8, "big").decode())


# ---------------------------------------------------------------------------
# General version (not needed for this challenge).
#
# If the nonces are related in some other way, search for the relation:
#   * Same c1  -> same k -> s_flag = s_known
#   * k_flag = k_known + d (small d):
#         c1_flag = c1_known * g^d  ->  s_flag = s_known * y^d
#   * k_flag = a * k_known (small a):
#         c1_flag = c1_known^a      ->  s_flag = s_known^a
# If k_flag is fresh and random, none of this works: that is ElGamal's security.
#
# SEARCH = 1 << 20  # how far to look for d or a
#
# def flag_mask(p, g, y, c1_known, c1_flag, s_known):
#     if c1_known == c1_flag:
#         print("[+] same c1: nonce reused")
#         return s_known
#
#     # Additive: k_flag = k_known + d, for d in [-SEARCH, SEARCH]
#     g_inv = pow(g, -1, p)
#     up = down = c1_known
#     for d in range(1, SEARCH + 1):
#         up = up * g % p
#         down = down * g_inv % p
#         if up == c1_flag:
#             print(f"[+] related nonce: k_flag = k_known + {d}")
#             return s_known * pow(y, d, p) % p
#         if down == c1_flag:
#             print(f"[+] related nonce: k_flag = k_known - {d}")
#             return s_known * pow(y, -d, p) % p
#
#     # Multiplicative: k_flag = a * k_known, for a in [2, SEARCH]
#     c = c1_known
#     for a in range(2, SEARCH + 1):
#         c = c * c1_known % p
#         if c == c1_flag:
#             print(f"[+] related nonce: k_flag = {a} * k_known")
#             return pow(s_known, a, p)
#
#     return None
#
# Usage:
#     s_flag = flag_mask(p, g, y, c1_k, c1_f, s_k)
#     m_flag = c2_f * pow(s_flag, -1, p) % p
# ---------------------------------------------------------------------------
