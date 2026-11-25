"""
Assymmetric nonsense -- ElGamal nonce reuse (and related nonces).

ElGamal encryption of message m with public key (p, g, y = g^x):
    pick random k
    c1 = g^k        mod p
    c2 = m * y^k    mod p
The value s = y^k is a one-time "mask". It must be different for every message.

Step 1: with one known plaintext we recover the mask of that message:
    s_known = c2_known * m_known^-1   mod p

Step 2: find the flag's mask s_flag.
  * Same c1  -> same k -> s_flag = s_known               (this challenge)
  * k_flag = k_known + d (small d):
        c1_flag = c1_known * g^d  ->  s_flag = s_known * y^d
  * k_flag = a * k_known (small a):
        c1_flag = c1_known^a      ->  s_flag = s_known^a
  This is where g and y are needed: g to detect the relation, y to shift the mask.
  If k_flag is fresh and random, none of this works: that is ElGamal's security.

Step 3: m_flag = c2_flag * s_flag^-1   mod p
"""
import json
import sys
from pathlib import Path

SEARCH = 1 << 20  # how far to look for d or a


def to_int(text: str) -> int:
    return int.from_bytes(text.encode(), "big")


def to_bytes(n: int) -> bytes:
    return n.to_bytes((n.bit_length() + 7) // 8, "big")


def flag_mask(p, g, y, c1_known, c1_flag, s_known):
    if c1_known == c1_flag:
        print("[+] same c1: nonce reused")
        return s_known

    # Additive: k_flag = k_known + d, for d in [-SEARCH, SEARCH]
    g_inv = pow(g, -1, p)
    up = down = c1_known
    for d in range(1, SEARCH + 1):
        up = up * g % p
        down = down * g_inv % p
        if up == c1_flag:
            print(f"[+] related nonce: k_flag = k_known + {d}")
            return s_known * pow(y, d, p) % p
        if down == c1_flag:
            print(f"[+] related nonce: k_flag = k_known - {d}")
            return s_known * pow(y, -d, p) % p

    # Multiplicative: k_flag = a * k_known, for a in [2, SEARCH]
    c = c1_known
    for a in range(2, SEARCH + 1):
        c = c * c1_known % p
        if c == c1_flag:
            print(f"[+] related nonce: k_flag = {a} * k_known")
            return pow(s_known, a, p)

    return None


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "challenge(2).json"
    data = json.loads(path.read_text())
    p, g, y = data["p"], data["g"], data["y"]
    c1_known, c2_known = data["cipher_known"]
    c1_flag, c2_flag = data["cipher_flag"]

    s_known = c2_known * pow(to_int(data["known_plaintext"]), -1, p) % p
    s_flag = flag_mask(p, g, y, c1_known, c1_flag, s_known)
    if s_flag is None:
        sys.exit("[-] c1 values are unrelated: nonce looks fresh, this attack does not apply")

    print(to_bytes(c2_flag * pow(s_flag, -1, p) % p).decode())


if __name__ == "__main__":
    main()
