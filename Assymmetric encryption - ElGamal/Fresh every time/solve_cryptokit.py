"""Fresh every time -- ElGamal nonces from a counter (k+1) + known plaintext."""
import sys, pathlib; HERE = pathlib.Path(__file__).parent; sys.path.insert(0, str(HERE.parents[1] / "hacking session 2"))
from cryptokit import *
d = load_json(HERE / "ElGamal_challenge.json")
print(show(elgamal_related_nonce(d["p"], d["g"], d["y"], d["cipher_known"], b2i(d["known_plaintext"]), d["cipher_flag"])))
