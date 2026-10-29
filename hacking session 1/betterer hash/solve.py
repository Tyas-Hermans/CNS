

#

"""
Invert the "better_hash" challenge.

better_hash is not a hash: it is a reversible, length-preserving permutation.
A real digest is one-way because it *compresses* (information is destroyed);
here every step is invertible and the output is the same length as the input
(37 bytes -> 37-byte flag), so we just run the eight rounds backwards.

Each forward step and its inverse:
    state[i] ^= (rnd*41 + i*17) & 0xff   ->  XOR the same constant again
    state[i] = rol(state[i], (rnd+i)&7)  ->  ror by the same amount
    state[i] ^= state[i-1]  (i ascending) ->  same XOR, i descending
    state = state[1:] + state[:1]  (rol 1) ->  rotate right by one

    Flag: cns{7f91c6f8c3d14af8b9f52d6b7f6e13c4}

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
        # undo the prefix-rol chain, in reverse index order
        for i in range(1,len(state)):
            state[i] ^= ror(state[i-1], i & 7)
        # undo (constant-XOR then rol) per byte, reversed
        for i in range(len(state)):
            x = state[i]
            x = (x + ((rnd + 1) * (i + 3))) & 0xff
            x = ror(x ^ ((rnd * 23 + i * 17) & 0xff),
                    ((rnd ^ i) & 7))
            state[i] = x
    return bytes(state)
def normal(hash_hex):
    return bytes(hash_hex)


def main():
    flag = invert(HASH)
    print("FLAG:", flag.decode(errors="replace"))


if __name__ == "__main__":
    main()