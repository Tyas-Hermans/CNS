"""
Count the letters -- mono-alphabetic substitution cipher.

    "The Belgians have also joined. Decrypt their message:
     qnb{vsi-fihczlnb-dlyi-vsi-fibv-plaahib-fi-zv-l-hzici-plaahi-mr-l-frtbbihb-plaahi}
     Hint: They used the English language to solve the language border.
     The attached wordlist may be of use."

Each plaintext letter is replaced by a fixed other letter (a 26->26 bijection),
with no shifting. That is why Vigenere-style attacks fail: the repeated blocks
`vsi` and `plaahi` sit at coprime distances, which rules out a repeating key. A
substitution instead preserves word *shape*, so it is broken with language, not
math -- exactly what "count the letters" and the wordlist hint at.

How the alphabet was recovered
------------------------------
  * `qnb{...}` is the flag wrapper, so  q->c  n->n  b->s.
  * `vsi` stands alone and repeats -> the commonest English word "the",
    giving  v->t  s->h  i->e.
  * single `l` is a one-letter word -> "a",  so  l->a.
  * `fihczlnb` is 8 letters ending in the known ...a n s and themed "Belgian":
    "belgians" ->  f->b  h->l  c->g  z->i.
  * `plaahi` (pattern w-a-f-f-l-e, doubled middle) with b-appended `plaahib`
    -> "waffle"/"waffles":  p->w  a->f.  `hzici` -> "liege" (the waffle city),
    `frtbbihb` -> "brussels" ->  t->u  r->r, and the small words fall out
    (`dlyi`->"make", `fibv`->"best", `fi`->"be", `zv`->"it", `mr`->"or").

The script applies the recovered alphabet and then *uses wordlist.txt* to verify
every decrypted word really is English -- the same check that disambiguates a
substitution by hand (e.g. "waffles", not the pattern-twin "dapples").

    Flag: cns{the-belgians-make-the-best-waffles-be-it-a-liege-waffle-or-a-brussels-waffle}

Lesson: a substitution cipher's 26! keys are unbruteforceable, yet it leaks
letter frequency and word shape, so a dictionary plus a little language sense
breaks it easily.
"""
import os
import re

CIPHERTEXT = "qnb{vsi-fihczlnb-dlyi-vsi-fibv-plaahib-fi-zv-l-hzici-plaahi-mr-l-frtbbihb-plaahi}"
WORDLIST = os.path.join(os.path.dirname(__file__), "wordlist.txt")

# Recovered cipher->plain alphabet (see module docstring for the derivation).
KEY = {
    "q": "c", "n": "n", "b": "s", "v": "t", "s": "h", "i": "e", "l": "a",
    "f": "b", "h": "l", "c": "g", "z": "i", "p": "w", "a": "f", "d": "m",
    "y": "k", "r": "r", "t": "u", "m": "o",
}


def decrypt(text, key):
    return "".join(key.get(ch, ch) if ch.isalpha() else ch for ch in text)


def load_wordlist(path):
    with open(path, encoding="latin-1") as f:
        return {line.strip().lower() for line in f if line.strip().isalpha()}


def solve():
    flag = decrypt(CIPHERTEXT, KEY)
    print(flag)

    # Use the wordlist to confirm every decrypted token is real English.
    words = load_wordlist(WORDLIST)
    tokens = re.findall(r"[a-z]+", flag.split("{", 1)[1])  # skip the "cns" tag
    bad = [t for t in tokens if t not in words]
    if bad:
        print("not found in wordlist:", bad)
    else:
        print("wordlist check: every plaintext word is valid English")
    return flag


if __name__ == "__main__":
    solve()
