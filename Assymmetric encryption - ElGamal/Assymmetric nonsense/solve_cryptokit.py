"""Assymmetric nonsense -- ElGamal nonce reuse (same c1) + known plaintext."""
import sys, pathlib; HERE = pathlib.Path(__file__).parent; sys.path.insert(0, str(HERE.parents[1] / "hacking session 2"))
from cryptokit import *
d = load_json(HERE / "challenge(2).json")
print(show(elgamal_known_plaintext(d["cipher_known"][1], b2i(d["known_plaintext"]), d["cipher_flag"][1], d["p"])))
