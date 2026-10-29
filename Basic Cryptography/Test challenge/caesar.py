"""
Test challenge -- Caesar cipher.

    "My name is Caesar and they will never find out my secret message:
     fqv{iluvw-fkdoohqjh}"

The hint names Caesar, so this is a Caesar shift (a mono-alphabetic shift
cipher). Each letter is shifted by a fixed amount k; decryption shifts back by
the same k. There are only 25 non-trivial keys, so we just try them all and
keep the one that produces the known flag prefix "cns{".

The match is shift k = 3 -- which is the *original* Caesar cipher (Julius
Caesar's own ROT-3), fitting the "My name is Caesar" hint exactly.

    Flag: cns{first-challenge}

Lesson: a shift cipher has a 25-key space, so brute force is instant and there
is no security at all -- the key may as well be public.
"""

CIPHERTEXT = "fqv{iluvw-fkdoohqjh}"


def shift(text, k):
    """Shift letters by -k (decrypt); leave non-letters untouched."""
    out = ""
    for c in text:
        if c.isalpha():
            out += chr((ord(c) - ord("a") - k) % 26 + ord("a"))
        else:
            out += c
    return out


def solve():
    for k in range(26):
        candidate = shift(CIPHERTEXT, k)
        if candidate.startswith("cns{"):
            print(f"shift {k}: {candidate}")
            return candidate
    print("no cns{...} flag found")


if __name__ == "__main__":
    solve()
