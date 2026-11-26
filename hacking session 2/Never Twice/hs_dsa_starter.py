#!/usr/bin/env python3
"""Starter for the Never Twice challenge."""
import hashlib
import json
from cmath import log

from sympy import discrete_log

d = json.load(open("hs_dsa_challenge.json"))
p, q, g, y = d["p"], d["q"], d["g"], d["y"]
first, second = d["signatures"]          # each has "order", "message", "r", "s"


def H(message: str) -> int:
    """The hash that is signed."""
    return int.from_bytes(hashlib.sha256(message.encode()).digest(), "big") % q


def decrypt_flag(x: int) -> bytes:
    """Decrypts the flag, given the private signing key x."""
    ct = bytes.fromhex(d["encrypted_flag"])
    ks, i = b"", 0
    while len(ks) < len(ct):
        ks += hashlib.sha256(f"{x}:{i}".encode()).digest()
        i += 1
    return bytes(c ^ s for c, s in zip(ct, ks))


# Your work starts here.
h1, h2 = H(first["message"]), H(second["message"])
r1, r2, s1, s2 = first["r"], second["r"], first["s"], second["s"]

k1 = log(r1,10)/log(g,10)
print(k1)
#k2 = discrete_log(p,r2,g)

#x = (s1 * k - h1) * pow(r, -1, q) % q   # step 5
"""
 How the challenge works

  1. DSA from slides 74–76
  - Public values: p, q, g, and the public key y = g^x mod p. The private key is x.
  - Signing: choose a secret random k that must be different for every signature. Then:
    - r = (g^k mod p) mod q
    - s = k⁻¹ · (H(m) + x·r) mod q
  - Verifying: w = s⁻¹, u1 = H(m)·w, u2 = r·w, v = (g^u1 · y^u2 mod p) mod q. The signature is valid if v == r.

  2. Spot the mistake
  r only depends on k. Both signatures in the JSON have the same r = 2594245…, so the signer used the same k twice. That's the "Double Entry" in the name. Slide
  75 says k must be "unique for each signing", and the ElGamal key-reuse slide makes the same point.

  3. Write down the two signing equations
  s1 = k⁻¹ (h1 + x·r)   →   s1·k = h1 + x·r1
  s2 = k⁻¹ (h2 + x·r)   →   s2·k = h2 + x·r2      (all mod q)

  4. Subtract them to get k
  x·r cancels out:
  (s1 − s2)·k = h1 − h2   →   k = ((h1 − h2) + x(r1-r2)) · (s1 − s2)⁻¹  mod q

  5. Put k back in to get x
  x = (s1·k − h1) · r⁻¹  mod q

  6. Check the result
  pow(g, x, p) == y should be true. You can also check k with pow(g, k, p) % q == r.

  7. Decrypt the flag
  The keystream is sha256(f"{x}:0") || sha256(f"{x}:1") || …, and you XOR it with encrypted_flag.
"""
#print(decrypt_flag(x))