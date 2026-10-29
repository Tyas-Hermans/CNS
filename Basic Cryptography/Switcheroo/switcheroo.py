"""
Switcheroo -- mono-alphabetic substitution cipher.

We are handed the full substitution table directly:

    Plain : ABCDEFGHIJKLMNOPQRSTUVWXYZ
    Cipher: QWERTYUIOPASDFGHJKLZXCVBNM

Encryption maps each plaintext letter to the Cipher letter in the same column
(A->Q, B->W, ...). Since the whole key alphabet is given, decryption is just the
inverse map: for each ciphertext letter, find it in Cipher and take the Plain
letter in the same column.

    Ciphertext: EFL{STZZTK-LGXH}
    Flag:       CNS{LETTER-SOUP}

Lesson: a substitution cipher has a huge key space (26! keys) so brute force is
hopeless, yet it leaks the plaintext's letter-frequency structure, so it falls
instantly to frequency analysis -- or, as here, to simply being handed the key.
"""

PLAIN = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CIPHER = "QWERTYUIOPASDFGHJKLZXCVBNM"
CIPHERTEXT = "EFL{STZZTK-LGXH}"


def decrypt(text):
    """Invert the substitution: Cipher letter -> Plain letter."""
    table = {c: p for p, c in zip(PLAIN, CIPHER)}
    return "".join(table.get(ch, ch) for ch in text)


def solve():
    flag = decrypt(CIPHERTEXT)
    print(flag)
    return flag


if __name__ == "__main__":
    solve()
