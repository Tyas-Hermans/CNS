"""
Dutch Exclusivity -- repeating-key XOR (with a hex-encoded inner layer).

    "The Dutch have some comments on the bake-off:
     Ciphertext: 555c4d46...5752414b4401   (hex)
     Key:        636f6d70...636f75727365   (hex)"

Two layers wrap the flag:

  1. Repeating-key XOR. Both ciphertext and key are given as hex. The key bytes
     spell ASCII -- `computerennetwerksecurityisthebestcourse` -- and are XORed
     over the ciphertext, repeating (plain[i] = cipher[i] XOR key[i % len]).

  2. The XOR output is not the flag yet: it is itself an ASCII string of
     space-separated hex pairs ("63 6e 73 7b ..."). Decoding that hex gives the
     real flag.

    Flag: cns{why-have-belgian-waffles-when-you-can-have-stroopwafels}

Lesson: XOR with a repeating key is only as strong as the key is long and
secret. Here the key is human-readable text as long as the message, so anyone
who guesses/receives it decrypts instantly -- and layering a trivial hex
encoding on top adds zero cryptographic strength (encoding is not encryption).
"""

CIPHERTEXT_HEX = (
    "555c4d461054524145590c45434045445353525a55400d544f515342594555535342564f47"
    "165353514f5b455542065253594e534d5753434b450043471649434e49454548535445454243"
    "591652455043585e5047104545524e585d544150525d16455111525e4d595f15545f50425717"
    "54555c55444245550a4d421154534a45585f45434145445e53570755455a544e5d53435a4554"
    "035342054f42425352544f5b4155425352535b4e53175752414b4401"
)
KEY_HEX = (
    "636f6d7075746572656e6e65747765726b7365637572697479697374686562657374636f7572"
    "7365"
)


def xor_repeating(data, key):
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def solve():
    key = bytes.fromhex(KEY_HEX)
    print("key (ascii):", key.decode())

    ciphertext = bytes.fromhex(CIPHERTEXT_HEX)
    layer1 = xor_repeating(ciphertext, key)        # -> ASCII hex string
    flag = bytes.fromhex(layer1.decode().replace(" ", "")).decode()
    print(flag)
    return flag


if __name__ == "__main__":
    solve()
