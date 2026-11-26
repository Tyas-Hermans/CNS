#!/usr/bin/env python3
"""Starter for the Courier challenge"""
import hashlib
import requests
import secrets
BASE = "http://cns-test.idlab.uantwerpen.be:50013"


def get(path):
    return requests.get(BASE + path, timeout=10).json()


def post(path, body=None):
    return requests.post(BASE + path, json=body or {}, timeout=10).json()


def xor_stream(data: bytes, s: int) -> bytes:
    """Encrypts or decrypts `data` with the keystream derived from the shared secret s."""
    keystream = hashlib.shake_256(str(s).encode()).digest(len(data))
    return bytes(a ^ b for a, b in zip(data, keystream))



def main():
    params = get("/params")
    p, g = params["p"], params["g"]
    run,A = post("/start", {"name": 'alice', "y": 'start'})
    print(run)
    '''x = secrets.randbelow(p - 3) + 2        # our private key
    y = pow(g, x, p)                        # our public key
    name = "solver_pwn_" + secrets.token_hex(3)


    ct = get(f"/send?to={name}")
    c1, c2 = ct["c1"], ct["c2"]

    s = pow(c1, x, p)                       # y^k
    m = c2 * pow(s, -1, p) % p
    print(m.to_bytes((m.bit_length() + 7) // 8, "big").decode())'''


if __name__ == "__main__":
    main()
# Your work starts here.
cns{a_shared_secret}