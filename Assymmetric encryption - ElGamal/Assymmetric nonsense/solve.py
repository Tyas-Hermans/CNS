"""
Assymmetric nonsense -- ElGamal nonce reuse.

ElGamal encryption:  c1 = g^k mod p,  c2 = m * y^k mod p
Both ciphertexts have the same c1, so the same k (and the same mask s = y^k) was used.

1. s = c2_known * m_known^-1   mod p
2. m_flag = c2_flag * s^-1     mod p
"""
import json

with open("challenge(2).json") as f:
    data = json.load(f)

p = data["p"]
c1_known, c2_known = data["cipher_known"]
c1_flag, c2_flag = data["cipher_flag"]
assert c1_known == c1_flag  # same c1 -> same k

m_known = int.from_bytes(data["known_plaintext"].encode(), "big")
s = c2_known * pow(m_known, -1, p) % p
m_flag = c2_flag * pow(s, -1, p) % p

print(m_flag.to_bytes((m_flag.bit_length() + 7) // 8, "big").decode())
