from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Random import get_random_bytes

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
    with open("ciphertext_flag.hex") as f:
        ct_flag = bytes.fromhex(f.read().strip())
    with open("ciphertext_known.hex") as f:
        ct_known = bytes.fromhex(f.read().strip())
    with open("known_message.txt", "rb") as f:
        known = f.read()

    # Show the attack works using encrypt() with a key/nonce we pick
    # ourselves, reused for two messages like the challenge does.
    key, nonce = get_random_bytes(16), get_random_bytes(8)
    test_secret = b"cns{this_is_a_test_flag}"
    test_ct_known = encrypt(key, nonce, known)
    test_ct_secret = encrypt(key, nonce, test_secret)
    assert recover(test_ct_secret, test_ct_known, known) == test_secret
    print("encrypt() test passed: nonce reuse leaks the plaintext")

    # Now the real thing
    print(recover(ct_flag, ct_known, known).decode())


if __name__ == "__main__":
    solve()
