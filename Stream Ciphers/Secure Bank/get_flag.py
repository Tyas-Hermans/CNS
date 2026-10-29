"""
Secure Bank -- Salsa20 stream-cipher malleability (no authentication).

    nc cns-test.idlab.uantwerpen.be 50001        (requires the UA-VPN)

    "They internally use Salsa20 with their proprietary JSON transaction
     format (see format.json). Maybe you can hack it to pay Bob back the
     money you owe him..."

================================================================================
1. The transaction format  (from format.json)
================================================================================
    {"from":"user1","to":"user2","amount":"xxxxxx"}

Serialised with json.dumps(..., separators=(",",":")) this is 47 bytes, and the
amount is a SIX-character quoted string. The 6 amount characters sit at byte
offset 39 (the opening quote is at 38, the closing quote at 46). Keeping that
6-char width is the whole game.

================================================================================
2. Why it is breakable
================================================================================
Salsa20 is a STREAM cipher:  ciphertext = plaintext XOR keystream, where the
keystream depends only on (key, nonce). The server reuses one secret KEY, sends
us `nonce + ciphertext`, and NEVER authenticates it -- there is no MAC or
signature. So even without the key we can tamper with the plaintext. Two
equivalent ways, both implemented below:

  (a) Differential bit-flip  -- forge_amount()  [robust, used by default]
      To turn plaintext byte pt[i] into pt'[i], flip ONLY that ciphertext byte:
          ct'[i] = ct[i] XOR pt[i] XOR pt'[i]
      The keystream cancels. Every byte we leave alone still decrypts to the
      original, so we only need to know the bytes we actually change: the
      amount. We never need the key or the rest of the plaintext.

  (b) Keystream recovery     -- forge_full()
      If we know the ENTIRE original plaintext, then
          keystream = ciphertext XOR plaintext
      and we can re-encrypt ANY plaintext of the same length:
          ct' = plaintext' XOR keystream
      More powerful (can change any field) but it needs the full plaintext and
      is fragile -- one wrong byte makes the whole JSON invalid server-side.

The catch of a stream cipher: we can change the message's BYTES but not its
LENGTH. The amount is exactly 6 characters, so we overwrite it with any other
6-character amount and the server processes the tampered transfer.

================================================================================
3. Running it  (needs the UA-VPN)
================================================================================
The nonce -- and therefore the keystream -- is fresh per connection, so each
attempt uses one new connection and its own pending ciphertext. Set OLD_AMOUNT
to the 6-char amount shown in your pending transaction and NEW_AMOUNT to the
6-char value that repays Bob, then run this file.

    Flag: <run on the VPN to obtain -- the server is not reachable from here>

================================================================================
4. Lesson
================================================================================
Encryption != integrity. Confidentiality (Salsa20) WITHOUT authentication lets
an attacker silently rewrite the plaintext. The fix is to authenticate the
ciphertext -- encrypt-then-MAC, or an AEAD such as ChaCha20-Poly1305 -- so any
tampering is detected and rejected.
"""
import json
import re
import socket

HOST, PORT = "cns-test.idlab.uantwerpen.be", 50001

# Known transaction layout (from format.json). Only the amount's offset and
# width must be exactly right; every other byte rides along unchanged.
TEMPLATE = json.dumps(
    {"from": "user1", "to": "user2", "amount": "xxxxxx"}, separators=(",", ":")
).encode()
AMOUNT_OFFSET = TEMPLATE.index(b"xxxxxx")  # 39
AMOUNT_LEN = 6

# --- fill these in from your live session -----------------------------------
OLD_AMOUNT = b"xxxxxx"   # the 6-char amount shown in your pending transaction
NEW_AMOUNT = b"999999"   # the 6-char amount you want to forge (repay Bob)
# ----------------------------------------------------------------------------


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


# --- attack (a): differential bit-flip, only the amount field ----------------
def forge_amount(pending_blob, old_amount, new_amount):
    if len(old_amount) != AMOUNT_LEN or len(new_amount) != AMOUNT_LEN:
        raise ValueError(f"amounts must be exactly {AMOUNT_LEN} chars")
    nonce, ct = pending_blob[:8], bytearray(pending_blob[8:])
    delta = xor(old_amount, new_amount)
    for i, d in enumerate(delta):
        ct[AMOUNT_OFFSET + i] ^= d
    return nonce + bytes(ct)


# --- attack (b): full keystream recovery, any field --------------------------
def forge_full(pending_blob, known_plaintext, forged_plaintext):
    if len(forged_plaintext) != len(known_plaintext):
        raise ValueError("forged plaintext must keep the original length")
    nonce, ct = pending_blob[:8], pending_blob[8:]
    keystream = xor(ct, known_plaintext)       # ks = ciphertext XOR plaintext
    return nonce + xor(forged_plaintext, keystream)


def recv_all(sock, timeout=4):
    sock.settimeout(timeout)
    buf = b""
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            buf += chunk
    except socket.timeout:
        pass
    return buf


def main():
    with socket.create_connection((HOST, PORT), timeout=8) as sock:
        banner = recv_all(sock)
        print(banner.decode(errors="replace"))

        m = re.search(rb"([0-9a-fA-F]{40,})", banner)
        if not m:
            print("could not find nonce+ciphertext hex in the banner")
            return
        pending = bytes.fromhex(m.group(1).decode())

        forged = forge_amount(pending, OLD_AMOUNT, NEW_AMOUNT)
        sock.sendall(forged.hex().encode() + b"\n")

        print("=== RESPONSE (look for the flag) ===")
        print(recv_all(sock).decode(errors="replace"))


if __name__ == "__main__":
    main()
