"""Sifting Sand -- weak (tiny) primes: factor n, then decrypt block by block."""
import sys, pathlib; HERE = pathlib.Path(__file__).parent; sys.path.insert(0, str(HERE.parents[1] / "hacking session 2"))
from cryptokit import *
d = load_json(HERE / "challenge.json")
f = factor(d["n"])
print(b"".join(i2b(rsa_decrypt(c, d["e"], d["n"], f), d["block_size"]) for c in d["ciphertext"])[:d["original_length"]].decode())
