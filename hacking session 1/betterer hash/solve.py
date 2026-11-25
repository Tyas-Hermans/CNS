

#

"""
Invert the "better_hash" challenge.

better_hash is not a hash: it is a reversible, length-preserving permutation.
A real digest is one-way because it *compresses* (information is destroyed);
here every step is invertible and the output is the same length as the input
(37 bytes -> 37-byte flag), so we just run the eight rounds backwards.

Each forward step and its inverse (8 rounds, per round):
    per byte i:
        x = rol(x ^ (rnd*23 + i*17), (rnd^i)&7)  ->  ror by same, then XOR C
        x = (x + (rnd+1)*(i+3)) & 0xff           ->  subtract the same amount
    chain i=1..n-1 (ascending):
        s[i] ^= rol(s[i-1], i&7)                 ->  same XOR, i descending

    Flag: cns{i_should_just_stick_to_sha_256}

Lesson: confusion + diffusion without compression (or a secret) is just
encryption you can trivially reverse -- not a preimage-resistant hash.
"""

HASH = "2647457a3b8ecb1cfedef2ce42958eeaa0016bb097c81b0948913d08e619a42e59f30e"

def rol(x, n):
    return ((x << n) | (x >> (8 - n))) & 0xff


def ror(x, n):
    n &= 7
    return ((x >> n) | (x << (8 - n))) & 0xff

def bettererhash(msg):
    s = bytearray(msg.encode()) if isinstance(msg, str) else bytearray(msg)

    for rnd in range(8):

        for i in range(len(s)):
            x = s[i]

            x = rol(x ^ ((rnd * 23 + i * 17) & 0xff),
                    ((rnd ^ i) & 7))

            x = (x + ((rnd + 1) * (i + 3))) & 0xff

            s[i] = x

        for i in range(1, len(s)):
            s[i] ^= rol(s[i - 1], i & 7)

    return s.hex()


def invert(hash_hex):
    state = bytearray.fromhex(hash_hex)
    for rnd in range(7, -1, -1):
        # undo the prefix-rol chain: XOR is self-inverse, so re-apply the
        # SAME rol(s[i-1]); walk the indices in reverse so each s[i-1] still
        # holds its post-chaining value when we use it.
        for i in range(len(state) - 1, 0, -1):
            state[i] ^= rol(state[i - 1], i & 7)
        # undo the per-byte step, reversing (rol(x ^ C, r); x = x + A):
        # first subtract A, then ror by r, then XOR C back.
        for i in range(len(state)):
            x = state[i]
            x = (x - ((rnd + 1) * (i + 3))) & 0xff
            x = ror(x, ((rnd ^ i) & 7)) ^ ((rnd * 23 + i * 17) & 0xff)
            state[i] = x
    return bytes(state)
def normal(hash_hex):
    return bytes(hash_hex)


def main():
    flag = invert(HASH)
    print("FLAG:", flag.decode(errors="replace"))


if __name__ == "__main__":
    main()