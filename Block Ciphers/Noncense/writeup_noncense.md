# Noncense

**Course:** Cryptography & Network Security — Block Ciphers chapter
**Category:** AES-CTR / nonce (counter) reuse → keystream reuse
**Hint:** *"The guys in IT told me those nonces are nonsense."*
**Flag:** `cns{aes_ctr_nonce_reuse_is_dangerous}` (recovered by running `challenge.py` with the provided `known_message.txt`)

---

## 1. Challenge

We are given the encryption routine and two ciphertexts:

```python
def encrypt(key, nonce, msg):
    ctr = Counter.new(64, prefix=nonce)       # 64-bit nonce prefix + 64-bit counter
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher.encrypt(msg)
```

- `ciphertext_flag.hex` — the **flag** encrypted with some `(key, nonce)`.
- `ciphertext_known.hex` — a **known message** encrypted with the **same** `(key, nonce)`.
- `known_message.txt` — the plaintext of that known message.

We never get the key. The hint ("those nonces are nonsense") is the whole giveaway:
the same nonce is reused for two encryptions.

## 2. How AES-CTR actually works

CTR mode doesn't encrypt the plaintext with AES directly. It turns AES into a **keystream
generator**. For each 16-byte block `i` it builds a counter block and encrypts *that*:

```
keystream_i = AES_encrypt(key, nonce ‖ counter_i)
ciphertext_i = plaintext_i XOR keystream_i
```

Here `Counter.new(64, prefix=nonce)` means each counter block is:

```
[ 64-bit nonce ][ 64-bit block counter: 0,1,2,... ]
```

The crucial point: **the keystream depends only on `(key, nonce, block index)` — never on
the plaintext.** So if you encrypt two different messages with the *same* key and the
*same* nonce, you XOR both of them against the **identical keystream**.

## 3. The vulnerability — reuse the nonce, reuse the keystream

This is the classic **two-time pad**. Let `KS` be the shared keystream:

```
ct_known = known XOR KS
ct_flag  = flag  XOR KS
```

Because `KS` is the same in both lines, you can cancel it out **without ever knowing the
key**:

```
KS   = known   XOR ct_known          # we know `known`, so we recover the keystream
flag = ct_flag XOR KS                # then strip the keystream off the flag ciphertext
```

Equivalently, XORing the two ciphertexts removes `KS` entirely:

```
ct_known XOR ct_flag = known XOR flag   ⇒   flag = known XOR ct_known XOR ct_flag
```

Either way, the key is irrelevant. The reused nonce is the entire break.

## 4. The solve (`challenge.py`)

```python
def recover(ct_secret, ct_known, known):
    """Same key + nonce => same keystream, so the key isn't needed."""
    keystream = xor(known, ct_known)     # KS = known XOR ct_known
    return xor(ct_secret, keystream)     # flag = ct_flag XOR KS
```

`challenge.py` does two things:

1. **Sanity check** — it picks its *own* random key and nonce, encrypts a dummy flag and
   the known message under that reused `(key, nonce)`, and asserts `recover(...)` returns
   the dummy flag. This proves the attack logic is correct using `encrypt()` exactly the
   way the challenge does.

2. **The real recovery** — it loads `ciphertext_flag.hex`, `ciphertext_known.hex` and
   `known_message.txt`, and prints `recover(ct_flag, ct_known, known).decode()`.

Run it from inside this folder:

```bash
python3 challenge.py
# encrypt() test passed: nonce reuse leaks the plaintext
# cns{aes_ctr_nonce_reuse_is_dangerous}
```

## 5. Step-by-step reproduction

1. **Read the hint as "nonce reuse".** `encrypt()` takes `nonce` as a parameter and the
   challenge calls it twice — nothing re-randomises it. Same key + same nonce = same
   keystream.
2. **Write down the two-time-pad equations** (Section 3). Notice the keystream cancels.
3. **Recover the keystream** from the pair you fully know: `KS = known XOR ct_known`. You
   only need as many keystream bytes as the flag is long.
4. **Decrypt the flag** by XORing: `flag = ct_flag XOR KS`.
5. **Confirm with a self-test** before trusting it on the real data (the assert in
   `challenge.py`): encrypt two messages yourself under one reused nonce and check recovery.

### If you don't have the known plaintext
You can still crib-drag. XOR the two ciphertexts to get `known XOR flag`, then slide a
guessed word (a "crib") along it. Guessing the flag prefix `cns{` immediately reveals the
first bytes of the known message (and vice-versa), and you extend from there. Full
recovery this way, though, needs you to guess the **entire** known message — recovering
`N` bytes of the flag requires knowing `N` bytes of the known plaintext. That is exactly
why `known_message.txt` is required to print the complete flag.

## 6. Why it works / lessons

A stream cipher (and CTR turns AES into one) is only ever as strong as the uniqueness of
its keystream. The whole security argument assumes **each keystream block is used once**.
Reuse the nonce under the same key and that assumption collapses: the key never leaks, but
the plaintexts XOR against each other and fall out.

**Mitigations**

- **Never reuse a (key, nonce) pair.** Generate a fresh random nonce per message, or use a
  strictly increasing counter you persist — and rotate the key long before the nonce space
  can wrap.
- Prefer a **misuse-resistant mode** (AES-GCM-SIV, or XChaCha20-Poly1305 with its large
  random nonce) where an accidental repeat degrades gracefully instead of catastrophically.
- Add **authentication** (an AEAD) so ciphertexts can't be silently tampered with — though
  note that authentication alone would *not* have saved this challenge; nonce reuse breaks
  confidentiality regardless.
- Treat the nonce as a correctness-critical input, not a throwaway: "nonce" means
  *number used once*, and using it twice is precisely the "nonsense" the IT guys warned
  about.
