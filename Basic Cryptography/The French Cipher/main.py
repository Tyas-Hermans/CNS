"""
The French Cipher -- Vigenere cipher.

    "The French pattisiers are in a bake-off with the Italian pizza
     restaurants. Can you decrypt their communication?
     eeg{kjgiflceha-sje-oxvksz-lzaa-ikqni}
     The key is France's favorite moon-shaped breakfast item!"

A Vigenere cipher is a poly-alphabetic shift: letter i of the plaintext is
shifted by letter (i mod len(key)) of a repeating keyword. Decryption subtracts
the key letters back out. Non-letters ({ } -) pass through untouched and do NOT
advance the key position.

The hint -- France's moon-shaped breakfast item -- is a CROISSANT, so the key
is "croissant" (singular; "croissants" produces garbage).

    Flag: cns{croissants-are-better-than-pizza}

Lesson: Vigenere hides single-letter frequencies but the key repeats, so once
the key length is known each position reduces to a Caesar cipher. Here the key
was simply guessable from the theme -- a human-memorable key is a weak key.
"""

CIPHERTEXT = "eeg{kjgiflceha-sje-oxvksz-lzaa-ikqni}"
KEY = "croissant"


def text_to_numbers(text):
    return [ord(c) - ord("a") for c in text if c.isalpha()]


def numbers_to_text(numbers):
    return "".join(chr(n + ord("a")) for n in numbers)


def right_output(text, output):
    """Re-insert the non-letter characters ({ } -) at their original spots."""
    result = ""
    index = 0
    for ch in text:
        if ch.isalpha():
            result += output[index]
            index += 1
        else:
            result += ch
    return result


def french_cipher(text, key):
    """Vigenere decrypt: subtract the repeating key, mod 26."""
    text_nums = text_to_numbers(text)
    key_nums = text_to_numbers(key)
    out_nums = [
        (text_nums[i] - key_nums[i % len(key_nums)]) % 26
        for i in range(len(text_nums))
    ]
    return right_output(text, numbers_to_text(out_nums))


def solve():
    flag = french_cipher(CIPHERTEXT, KEY)
    print(flag)
    return flag


if __name__ == "__main__":
    solve()
