"""
Replanting -- stream cipher with an LCG keystream (known-plaintext + seed recovery).

    "You have obtained two encrypted messages:
      - A public server status message whose plaintext is known.
      - A confidential message containing a secret flag.
     Both messages were encrypted using the same stream cipher configuration."

The cipher
----------
The keystream is produced by a Linear Congruential Generator (LCG):

    state      = (A * state + C) mod M        A=1103515245  C=12345  M=2**31
    keybyte    = (state >> 16) & 0xff          # bits 16..23 of each new state

and encryption is a byte-wise XOR:  ciphertext = plaintext XOR keystream.
"Same configuration" means both messages use the SAME seed, hence the SAME
keystream -- the classic stream-cipher mistake.

The attack (two steps)
----------------------
1. Known-plaintext -> keystream.
   XOR the known status message with its ciphertext to recover the keystream
   bytes:  keystream = known XOR ciphertext.  Because the secret flag used the
   same seed, these same keystream bytes decrypt it directly. That alone already
   yields the flag for as many bytes as the known message is long.

2. Recover the LCG seed (so we can also regenerate/extend the keystream).
   Each keystream byte is bits 16..23 of a state. A key property of an LCG mod a
   power of two: the low k bits of the next state depend ONLY on the low k bits
   of the current state (carries move up, never down). So bits 0..23 are a
   closed sub-generator, and the extracted byte (bits 16..23) depends only on
   bits 0..23. We therefore:
     - take bits 16..23 of the first state from keystream[0],
     - brute force the 16 unknown low bits 0..15  (only 2**16 = 65536 tries),
     - leave bits 24..30 as 0 (they never affect the extracted bytes),
     - invert ONE LCG step (multiply by A^-1 mod M) to get the seed,
     - keep the seed whose keystream reproduces all recovered bytes.

That recovered seed regenerates the exact keystream, which we XOR into the
secret to reveal the flag.

    seed: 993285752
    Flag: cns{reusing_a_stream_cipher_is_dangerous}

Lesson: a stream cipher's keystream must NEVER be reused across messages, and an
LCG is not a cryptographic PRNG -- its state is tiny and its structure (low bits
form a closed cycle) lets you recover the whole seed from a sliver of output.
"""

# LCG parameters
A = 1103515245
C = 12345
M = 2**31


def next_state(state):
    """Generate the next PRNG state."""
    return (A * state + C) % M


def generate_keystream(seed, length):
    """Generate a pseudorandom keystream."""
    state = seed
    keystream = bytearray()
    for _ in range(length):
        state = next_state(state)
        keystream.append((state >> 16) & 0xff)
    return bytes(keystream)


def encrypt(plaintext, seed):
    """Encrypt plaintext using XOR."""
    keystream = generate_keystream(seed, len(plaintext))
    return bytes(p ^ k for p, k in zip(plaintext, keystream))


def decrypt(ciphertext, seed):
    """Decrypt ciphertext using XOR (XOR is its own inverse)."""
    return encrypt(ciphertext, seed)


def solve():
    """Solve the cipher with a known-plaintext attack + seed recovery."""
    known = b"STATUS: SERVER ONLINE"
    ciphertext = bytes.fromhex("22135cc0b9daa9e717f98a998e6ee5e92655e1a88f")
    with open("secret.txt") as f:
        secret = bytes.fromhex(f.read().strip())

    # Step 1: known plaintext XOR its ciphertext -> keystream bytes.
    keystream = bytes(p ^ c for p, c in zip(known, ciphertext))

    # Step 2: recover the seed. The first keystream byte is bits 16..23 of the
    # first state; guess the low 16 bits (bits 0..15) and leave the top bits 0.
    a_inv = pow(A, -1, M)
    for low in range(1 << 16):
        first_state = (keystream[0] << 16) | low
        # Undo one next_state() step to get the seed that produces first_state.
        seed = ((first_state - C) * a_inv) % M
        assert next_state(seed) == first_state
        if generate_keystream(seed, len(keystream)) == keystream:
            assert encrypt(known, seed) == ciphertext
            print("seed:", seed)
            print(decrypt(secret, seed).decode())
            return seed


if __name__ == "__main__":
    solve()
