"""Phone Book -- unauthenticated key directory: register our own key, have Alice encrypt to it.
Talks to the course server (same requests as solve.py)."""
import sys, pathlib; HERE = pathlib.Path(__file__).parent; sys.path.insert(0, str(HERE.parents[1] / "hacking session 2"))
from cryptokit import *
import json, secrets, urllib.request
BASE = "http://cns-test.idlab.uantwerpen.be:50011"
api = lambda path, body=None: json.load(urllib.request.urlopen(urllib.request.Request(BASE + path, data=body and json.dumps(body).encode(), headers={"Content-Type": "application/json"})))
prm = api("/params"); x = secrets.randbelow(prm["p"] - 3) + 2; name = "solver_" + secrets.token_hex(3)
api("/directory", {"name": name, "y": pow(prm["g"], x, prm["p"])})
ct = api(f"/send?to={name}")
print(show(elgamal_decrypt(ct["c1"], ct["c2"], x, prm["p"])))
