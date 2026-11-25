"""sports car desire -- huge e means small d: Wiener attack."""
import sys, pathlib; HERE = pathlib.Path(__file__).parent; sys.path.insert(0, str(HERE.parents[1] / "hacking session 2"))
from cryptokit import *
d = load_json(HERE / "challenge(1).json")
print(show(pow(d["c"], wiener(d["e"], d["n"])[0], d["n"])))
