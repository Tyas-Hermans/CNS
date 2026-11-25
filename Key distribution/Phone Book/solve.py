"""
Phone Book -- ElGamal key distribution without authentication.

The directory lets anyone register a public key under any name, and Alice
encrypts her secret to whatever key is listed. Nothing vouches for the keys,
so we register a key whose private key x we know, have Alice send to it, then
decrypt normally:

    c1 = g^k,  c2 = m * y^k      with  y = g^x  (our key)
    s  = c1^x = g^(kx) = y^k
    m  = c2 * s^-1   mod p
"""
import json, urllib.request, secrets

HOST = "cns-test.idlab.uantwerpen.be"
PORT = 50011
BASE = f"http://{HOST}:{PORT}"


def get(path):
    return json.load(urllib.request.urlopen(BASE + path))


def post(path, obj):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(obj).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    return json.load(urllib.request.urlopen(req))


def main():
    params = get("/params")
    p, g = params["p"], params["g"]

    x = secrets.randbelow(p - 3) + 2        # our private key
    y = pow(g, x, p)                        # our public key
    name = "solver_pwn_" + secrets.token_hex(3)
    post("/directory", {"name": name, "y": y})

    ct = get(f"/send?to={name}")
    c1, c2 = ct["c1"], ct["c2"]

    s = pow(c1, x, p)                       # y^k
    m = c2 * pow(s, -1, p) % p
    print(m.to_bytes((m.bit_length() + 7) // 8, "big").decode())


if __name__ == "__main__":
    main()
