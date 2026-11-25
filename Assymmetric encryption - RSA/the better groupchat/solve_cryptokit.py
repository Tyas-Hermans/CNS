"""the better groupchat -- Hastad broadcast attack (M^3 now really wraps around each n)."""
import sys, pathlib; HERE = pathlib.Path(__file__).parent; sys.path.insert(0, str(HERE.parents[1] / "hacking session 2"))
from cryptokit import *
k, c = read_vars(HERE / "public_keys.txt"), read_vars(HERE / "ciphertexts.txt")
print(show(hastad(c["c1"] + c["c2"] + c["c3"], k["n"], k["e"][0])))
