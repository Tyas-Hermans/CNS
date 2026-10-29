from Cryptodome.Cipher import AES
from Cryptodome.Util import Counter
from Cryptodome.Random import get_random_bytes

def encrypt(key, nonce, msg):
    ctr = Counter.new(64, prefix=nonce)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher.encrypt(msg)

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def recover(ct_secret, ct_known, known):
    """Same key + nonce => same keystream, so the key isn't needed."""
    keystream = xor(known, ct_known)
    return xor(ct_secret, keystream)


def solve():
    with open("ciphertext_flag_new.hex") as f:
        ct_flag = bytes.fromhex(f.read().strip())
    with open("ciphertext_known_new.hex") as f:
        ct_known = bytes.fromhex(f.read().strip())
    with open("known_message_new.txt", "rb") as f:
        known = f.read()
    print(recover(ct_flag, ct_known, known).decode())


if __name__ == "__main__":
    solve()