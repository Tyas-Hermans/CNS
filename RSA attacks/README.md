# RSA attacks — study catalogue

Every RSA attack I could think of for the session, each as a **runnable demo**
that builds a deliberately weak key, runs the attack, and checks the flag comes
back. Study a file, run it, then tweak the vulnerable instance to see when the
attack stops working.

```bash
# run one theme (from this folder)
python3 "01_factoring.py"
# or all of them
for f in 0*.py; do python3 "$f"; done
```

Each demo calls the same `cryptokit` helpers your real `solve_cryptokit.py`
scripts use, so the catalogue doubles as worked examples of the toolkit. The
`CHEATSHEET.md` in `../hacking session 2/` maps "what you see" → which call.

## The files

| File | Attacks |
|---|---|
| `01_factoring.py` | close primes (Fermat), smooth p−1 (Pollard p−1), smooth p+1 (Williams), small factor (rho), shared prime across keys (batch gcd), multi-prime / perfect power, `factor()` fallback |
| `02_small_exponent.py` | cube root (unpadded), Håstad broadcast, Franklin–Reiter related messages, Coppersmith stereotyped message* |
| `03_key_relations.py` | common modulus (incl. gcd(e₁,e₂)>1), Wiener (small d), leaked d / φ / dp, e not invertible (Rabin / e∣p−1) |
| `04_oracles.py` | CCA decryption blinding, signing-oracle blinding, parity/LSB oracle |
| `05_signatures_and_faults.py` | multiplicative forgery, e=3 PKCS#1 forgery (Bleichenbacher '06), CRT fault (Bellcore), known-high-bits factoring* |

`*` = lattice attack. The demo runs at a **small modulus** so the pure-Python
LLL stays fast. For real 1024-bit challenges these need SageMath or `fpylll` —
ready-to-paste snippets are in **`sage_snippets.md`**.

## How to recognise which attack

1. **Look at the key first.** Tiny d, huge e → Wiener. Two keys, one n → common
   modulus. Several keys → shared primes (gcd every pair). e=3 and a short
   message → cube root.
2. **Factor n cheaply** before anything clever: `factor(n)` tries Fermat, p−1,
   rho and p+1, and https://factordb.com may already know n.
3. **A server in the challenge** → it's an oracle (decryption, signing, parity,
   or padding). RSA's malleability `(m·r)^e = c·r^e` is the lever every time.
4. **You know *part* of the message or key** → Coppersmith (`sage_snippets.md`).
5. **Signatures** → check whether the message is hashed, whether padding length
   is verified, and whether two signatures can be multiplied.

## Not covered here (know they exist)

- **Boneh–Durfee** (d < n^0.292, just past Wiener) — see `sage_snippets.md`.
- **Bleichenbacher padding oracle** (PKCS#1 v1.5 decryption, "million message
  attack") — a full interactive attack; if a server returns distinct
  "bad padding" vs "bad plaintext" errors, that's the tell. Use the
  implementation in `pycryptodome`/`felicitas` rather than writing it live.
- **ROCA** (Infineon key generation) — detectable by the structure of n.

## Requirements

`sympy` only (already in the project venv). Optional, for real-size lattice
attacks: `pip install fpylll gmpy2`, or just use the Sage web cell. `pip install
pycryptodomex` if a challenge's own code imports `Cryptodome`.
