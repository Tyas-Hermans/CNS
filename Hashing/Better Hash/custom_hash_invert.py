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

HASH = "5f070b54361613bca31a123e95321cff154ba64f549bb34fdc7688f10efb569aed4ccbd6ba"


def rol(x, n):
    return ((x << n) | (x >> (8 - n))) & 0xff


def ror(x, n):
    n &= 7
    return ((x >> n) | (x << (8 - n))) & 0xff


def better_hash(msg):
    """The original forward function, kept for round-trip verification."""
    state = bytearray(msg.encode()) if isinstance(msg, str) else bytearray(msg)
    for rnd in range(8):
        for i in range(len(state)):
            state[i] ^= (rnd * 41 + i * 17) & 0xff
            state[i] = rol(state[i], (rnd + i) & 7)
        for i in range(1, len(state)):
            state[i] ^= state[i - 1]
        state = state[1:] + state[:1]
    return state.hex()


def invert(hash_hex):
    state = bytearray.fromhex(hash_hex)
    for rnd in range(7, -1, -1):
        # undo the rotate-left-by-one of the whole state
        state = state[-1:] + state[:-1]
        # undo the prefix-XOR chain, in reverse index order
        for i in range(len(state) - 1, 0, -1):
            state[i] ^= state[i - 1]
        # undo (constant-XOR then rol) per byte, reversed
        for i in range(len(state)):
            state[i] = ror(state[i], (rnd + i) & 7)
            state[i] ^= (rnd * 41 + i * 17) & 0xff
    return bytes(state)


def main():
    flag = invert(HASH)
    print("FLAG:", flag.decode(errors="replace"))
    print("round-trip OK:", better_hash(flag) == HASH)


if __name__ == "__main__":
    main()
