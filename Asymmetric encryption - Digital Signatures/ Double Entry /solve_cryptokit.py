"""Double Entry -- two DSA signatures with the same r (reused k) give the private key x."""
import sys, pathlib; HERE = pathlib.Path(__file__).parent; sys.path.insert(0, str(HERE.parents[1] / "hacking session 2"))
from cryptokit import *
d = load_json(HERE / "dsa1_challenge.json")
(a, b), q = d["signatures"], d["q"]
x, k = dsa_reused_k(a["r"], a["s"], H_int(a["message"], q), b["s"], H_int(b["message"], q), q)
ct = bytes.fromhex(d["encrypted_flag"])
print(bytes(c ^ s for c, s in zip(ct, b"".join(hashlib.sha256(f"{x}:{i}".encode()).digest() for i in range(len(ct) // 32 + 1)))).decode())
