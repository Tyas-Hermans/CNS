
import json
import random
import math
from sympy import isprime

# --------------------------------------------------
# Load challenge
# --------------------------------------------------

with open("challenge.json", "r") as f:
    challenge = json.load(f)

n = challenge["n"]
e = challenge["e"]
ciphertext = challenge["ciphertext"]

block_size = challenge["block_size"]
original_length = challenge["original_length"]


def p_and_q_generator(n):
    while True:
        x = y = random.randrange(2, n)
        c = random.randrange(1, n)
        g = 1
        while g == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            g = math.gcd(abs(x - y), n)
        if g != n:
            return g, n // g
# --------------------------------------------------
# Participant input
# --------------------------------------------------

print("RSA Decryption Challenge")
print("------------------------")

print(f"n = {n}")
print(f"e = {e}")
p = p_and_q_generator(n)[0]
q = p_and_q_generator(n)[1]
print(f"p = {p}, q = {q}")
xn = (p-1)*(q-1)
d = pow(e, -1, xn)

#d = int(input("\nEnter recovered private exponent d: "))


# --------------------------------------------------
# Decryption
# --------------------------------------------------



def decrypt(ciphertext, d, n):
    plaintext = bytearray()

    for c in ciphertext:
        m = pow(c, d, n)

        block = m.to_bytes(block_size, byteorder="big")

        plaintext.extend(block)

    # Remove padding caused by fixed-size block encoding
    plaintext = plaintext[:original_length]

    return plaintext


# --------------------------------------------------
# Output
# --------------------------------------------------

try:
    result = decrypt(ciphertext, d, n)
    message = result.decode("utf-8")

    print("\n[+] Decrypted message:")
    print("---------------------")
    print(message)

except (ValueError, OverflowError):
    print("[-] Invalid private key or decryption failed.")

