"""
Key standardisation -- DES with a predictable, "standardised" key.

    "I have standardised the keys for my IoT devices so they are easier to
     program! Since the devices are simple I decided to use DES.
     { "namespace": "IOTDEV",
       "message": "74eb40cf03b84d0bc4cd2c6e0fe97fb4e70546d3e09c530d35b344e530351bac" }"

From problem to solution
------------------------
1. Size up the cipher. A DES key is ALWAYS exactly 8 bytes (64 bits). So the key
   is 8 bytes and the message (64 hex chars = 32 bytes) is 4 DES blocks.

2. Read what "standardised" gives away. The author fixed the first part of every
   key to a constant namespace, here the 6 ASCII bytes of "IOTDEV":

       I  O  T  D  E  V  ??  ??
       └──── fixed 6 ────┘ └ 2 unknown ┘

   Only 2 bytes actually vary per device. That is the whole vulnerability: a
   56-bit cipher collapses to an effective 256*256 = 65536-key search. Not a
   weakness in DES -- a weakness in giving every key a predictable prefix.

3. Pick the mode. One 32-byte block, no IV supplied => ECB (each 8-byte block
   encrypted independently, nothing else to guess).

4. Brute force the 2 unknown bytes. For i in 0..65535, build the key
   prefix + i (big-endian), ECB-decrypt, and keep the candidate that both
   (a) decrypts to printable text after stripping PKCS#7 padding, and
   (b) matches the flag shape  name{...}  (the FLAG_RE regex). Readability alone
   leaves a few false hits among 65536 keys; the regex pins the real one.

Result
------
    key  = b"IOTDEV24"   (bytes 49 4f 54 44 45 56 32 34 -- the device id is "24")
    flag = cns{i-have-room-temperature-iq}

Notes
-----
  * DES ignores the low (parity) bit of each key byte, so only 56 of the 64 bits
    matter. PyCryptodome does not enforce parity, so we never have to fix it.
  * The plaintext is 31 chars + one 0x01 PKCS#7 pad byte = 32 bytes = 4 blocks.

Lesson: key *entropy* is what protects you, not the cipher's nominal strength.
A shared, structured key prefix across devices turns a brute-force-resistant key
into a 2-byte search. Every device should carry its own full-entropy random key.
"""
from Crypto.Cipher import DES
import argparse
import binascii
import json
import re
import string

FLAG_RE = re.compile(rb"[a-zA-Z0-9_]+\{[^}]*\}")
PRINTABLE = set(bytes(string.printable, "ascii"))


def strip_padding(pt: bytes) -> bytes:
    """Remove PKCS#7 padding if it looks valid, else return as-is."""
    if not pt:
        return pt
    n = pt[-1]
    if 1 <= n <= 8 and pt[-n:] == bytes([n]) * n:
        return pt[:-n]
    return pt


def is_readable(pt: bytes) -> bool:
    body = strip_padding(pt)
    if not body:
        return False
    return all(b in PRINTABLE for b in body)


def solve(text):
    """Brute-force the device-specific part of the key: NAMESPACE + 2 bytes."""
    data = json.loads(text)
    prefix = data["namespace"].encode()
    ciphertext = binascii.unhexlify(data["message"])

    n = 8 - len(prefix)  # DES keys are 8 bytes
    for i in range(256 ** n):
        key = prefix + i.to_bytes(n, "big")
        pt = DES.new(key, DES.MODE_ECB).decrypt(ciphertext)
        if is_readable(pt) and FLAG_RE.search(pt):
            print("key:", key)
            print(strip_padding(pt).decode())
            return


if __name__ == "__main__":
    solve('{ "namespace": "IOTDEV", "message": "74eb40cf03b84d0bc4cd2c6e0fe97fb4e70546d3e09c530d35b344e530351bac" }')

