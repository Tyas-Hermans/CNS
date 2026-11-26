"""
RSA attacks (4/6): ORACLES (a server that answers queries about ciphertexts).

These need interaction: the server decrypts, signs, or leaks one bit.  RSA is
multiplicatively malleable -- (m*r)^e = c * r^e -- which is what every one of
these exploits.

  demo                  the server gives you...                     toolkit call
  --------------------- ------------------------------------------- -------------------
  cca_decrypt_blinding  decrypts anything except the target c       rsa_blind_decrypt
  cca_sign_blinding     signs anything except the target message    rsa_blind_sign
  parity_oracle         one bit: is m*2^k even or odd?              lsb_oracle
"""
from _harness import *


def demo_cca_decrypt_blinding():
    """Decryption oracle refuses your exact c: send c*r^e, divide the reply by r."""
    p, q = prime(512), prime(512)
    n, e = p * q, 65537
    d = pow(e, -1, (p - 1) * (q - 1))
    c = pow(M, e, n)

    def oracle(x):                       # the server
        assert x != c, "oracle refuses the challenge ciphertext"
        return pow(x, d, n)

    assert i2b(rsa_blind_decrypt(c, e, n, oracle)) == FLAG
    return "blinding: multiply by r^e, strip r from the result"


def demo_cca_sign_blinding():
    """Signing oracle refuses message m: sign m*r^e, divide signature by r."""
    p, q = prime(512), prime(512)
    n, e = p * q, 65537
    d = pow(e, -1, (p - 1) * (q - 1))

    def sign(x):
        assert x != M, "oracle refuses to sign the target message"
        return pow(x, d, n)

    forged = rsa_blind_sign(M, e, n, sign)
    assert pow(forged, e, n) == M        # a valid signature on M
    return "blinding a signing oracle into signing a forbidden message"


def demo_parity_oracle():
    """Oracle leaks only the last bit of the decryption -> binary search for m."""
    p, q = prime(256), prime(256)
    n, e = p * q, 65537
    d = pow(e, -1, (p - 1) * (q - 1))
    c = pow(M, e, n)

    def parity(x):
        return pow(x, d, n) & 1

    assert i2b(lsb_oracle(c, e, n, parity)) == FLAG
    return "parity/LSB oracle: ~log2(n) queries, exact (no float drift)"


if __name__ == "__main__":
    run(globals())
