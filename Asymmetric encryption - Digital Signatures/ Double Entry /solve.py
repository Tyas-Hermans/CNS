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
  s1 = k⁻¹ (h1 + x·r)   →   s1·k = h1 + x·r
  s2 = k⁻¹ (h2 + x·r)   →   s2·k = h2 + x·r      (all mod q)

  4. Subtract them to get k
  x·r cancels out:
  (s1 − s2)·k = h1 − h2   →   k = (h1 − h2) · (s1 − s2)⁻¹  mod q

  5. Put k back in to get x
  x = (s1·k − h1) · r⁻¹  mod q

  6. Check the result
  pow(g, x, p) == y should be true. You can also check k with pow(g, k, p) % q == r.

  7. Decrypt the flag
  The keystream is sha256(f"{x}:0") || sha256(f"{x}:1") || …, and you XOR it with encrypted_flag.
"""
import json, hashlib

with open("dsa1_challenge.json") as f:
    raw = f.read()
data = json.loads(raw)  # the file starts with a stray "t" before the "{"

p, q, g, y = data["p"], data["q"], data["g"], data["y"]
sig1, sig2 = data["signatures"]


def H(m):
    return int(hashlib.sha256(m.encode()).hexdigest(), 16) % q


h1, h2 = H(sig1["message"]), H(sig2["message"])
r, s1, s2 = sig1["r"], sig1["s"], sig2["s"]

k = (h1 - h2) * pow(s1 - s2, -1, q) % q  # step 4
x = (s1 * k - h1) * pow(r, -1, q) % q  # step 5
assert pow(g, x, p) == y  # step 6

ct = bytes.fromhex(data["encrypted_flag"])  # step 7
ks = b"".join(hashlib.sha256(f"{x}:{i}".encode()).digest() for i in range(len(ct) // 32 + 1))
print(bytes(a ^ b for a, b in zip(ct, ks)).decode())