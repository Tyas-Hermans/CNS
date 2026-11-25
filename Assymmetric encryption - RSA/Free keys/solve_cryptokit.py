"""Free keys -- same n, two exponents: common modulus attack."""
import sys, pathlib; HERE = pathlib.Path(__file__).parent; sys.path.insert(0, str(HERE.parents[1] / "hacking session 2"))
from cryptokit import *
d = load_json(HERE / "challenge.json")
print(show(common_modulus(d["c1"], d["c2"], d["e1"], d["e2"], d["n"])))
