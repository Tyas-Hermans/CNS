"""
AES 2 -- double AES-128-ECB broken by a meet-in-the-middle attack.

    "AES 2" encrypts each block twice, under two independent keys:
        C = E_{K2}( E_{K1}(P) )
    We are given enc.bmp (a double-encrypted image) and a promo ciphertext,
    and must recover the flag inside the promo message.

From problem to solution
------------------------
1. Why double encryption is NOT twice as strong. Two keys *look* like 2x the
   key bits (here 2x20 = 40 bits), so a naive brute force is 2^40. But you never
   have to search both keys at once. Rewrite the equation around the midpoint:

        E_{K1}(P)  =  D_{K2}(C)

   The left side depends only on K1, the right side only on K2. So:
     * forward:  compute E_{K1}(P) for every K1  and store it in a table
     * backward: compute D_{K2}(C) for every K2  and look each up in the table
   A collision gives (K1, K2). Cost drops from 2^40 to ~2^20 + 2^20 time (and
   2^20 memory). That is the meet-in-the-middle attack -- and the reason
   "encrypt it twice" buys almost nothing.

   (Demo version: keys are only 20 bits -- 3 low bytes, the rest zero -- so each
    sweep is 2^20 = ~1e6 AES calls and finishes in seconds. key_of() builds the
    full 16-byte key from a 20-bit integer.)

2. MITM needs ONE known plaintext/ciphertext pair (P, C). We get it for free
   from the BMP file format. A 32-bit BMP uses a 124-byte BITMAPV5HEADER, and
   the author left the header cleartext and only encrypted the body -- starting
   at file offset 54. Bytes [54:70] of that header are the four BI_BITFIELDS
   colour masks (red, green, blue, alpha channel), which for a standard BMP are
   fixed, well-known values. So:

        P  = the 16-byte colour-mask block (known from the format)
        C  = enc.bmp[54:70]                (the matching encrypted block)

   enc.bmp[:54] == dec.bmp[:54] (identical cleartext), they diverge at 54, and
   the encrypted region is a whole number of 16-byte blocks -- confirming 54 is
   the ECB block boundary where encryption begins. We try the few standard mask
   layouts (RGBA/BGRA/ARGB/ABGR) as candidate P; RGBA is the hit.

3. Recover the keys, then decrypt the real target. The collision yields K1, K2.
   The flag is not in the image -- it is in a separate promo message encrypted
   under the SAME two keys, so we undo both layers:
        plaintext = D_{K1}( D_{K2}(promo) )

Result
------
    K1 = 041d4a00...00   K2 = 0e628d00...00   (masks = RGBA)
    flag = cns{use-code-AES-2-electric-boogaloo-for-20-euro-off-on-your-purchase}

Lesson: composing a cipher with itself does not multiply its strength. Double
encryption adds only ~1 bit of security against meet-in-the-middle, not a second
full key's worth -- which is exactly why real triple-DES uses THREE keys to buy
an effective doubling, and why you should reach for a wider cipher (AES-256)
rather than stacking a narrow one.
"""

from Crypto.Cipher import AES

NKEYS = 1 << 20
ENC_START = 54  # first encrypted byte in enc.bmp (start of the colour masks)

PROMO_HEX = ("df7c7dfbd5e1ba2af108d658132d5f20d34de27da16375ceabd7a79cbfe73824"
             "4027a4a0b26ec498a2c223a545b9567c20bf423bb38514e6cd6f043ab9e23a84"
             "ffa6745294c224068e1cffd9e8c9e294")

data = open("enc.bmp", "rb").read()
C0 = data[ENC_START:ENC_START + 16]   # first encrypted block = known BMP masks

# Candidate plaintexts for the colour-mask block (R,G,B,A masks, little-endian).
le = lambda v: v.to_bytes(4, "little")
CANDIDATES = {
    "RGBA 00FF0000/0000FF00/000000FF/FF000000":
        le(0x00FF0000) + le(0x0000FF00) + le(0x000000FF) + le(0xFF000000),
    "BGRA 000000FF/0000FF00/00FF0000/FF000000":
        le(0x000000FF) + le(0x0000FF00) + le(0x00FF0000) + le(0xFF000000),
    "ARGB FF000000/00FF0000/0000FF00/000000FF":
        le(0xFF000000) + le(0x00FF0000) + le(0x0000FF00) + le(0x000000FF),
    "ABGR FF000000/000000FF/0000FF00/00FF0000":
        le(0xFF000000) + le(0x000000FF) + le(0x0000FF00) + le(0x00FF0000),
}


def key_of(small):
    return small.to_bytes(3, "big") + b"\x00" * 13


def main():
    print(f"crib C0 = data[54:70] = {C0.hex()}")
    print("building backward table D_K2(C0) for 2^20 keys ...")
    back = {}
    for k2 in range(NKEYS):
        back[AES.new(key_of(k2), AES.MODE_ECB).decrypt(C0)] = k2
    print(f"  done ({len(back)} entries)")

    promo = bytes.fromhex(PROMO_HEX)

    for name, p0 in CANDIDATES.items():
        print(f"forward sweep, assuming masks = {name}")
        for k1 in range(NKEYS):
            mid = AES.new(key_of(k1), AES.MODE_ECB).encrypt(p0)
            k2 = back.get(mid)
            if k2 is None:
                continue
            K1, K2 = key_of(k1), key_of(k2)
            inner = AES.new(K2, AES.MODE_ECB).decrypt(promo)
            pt = AES.new(K1, AES.MODE_ECB).decrypt(inner)
            print(f"\n>>> MITM hit  k1_small={k1} k2_small={k2}")
            print(f"    K1={K1.hex()}  K2={K2.hex()}")
            print(f"    promo plaintext (raw): {pt!r}")
            with open("solved_keys.txt", "w") as f:
                f.write(f"k1_small={k1}\nk2_small={k2}\n"
                        f"K1={K1.hex()}\nK2={K2.hex()}\nmasks={name}\n")
            return (k1, k2, K1, K2)
    print("no hit for the tried mask layouts")


if __name__ == "__main__":
    main()
