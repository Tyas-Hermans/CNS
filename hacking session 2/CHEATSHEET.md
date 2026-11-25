# Hacking session 2 — cheat sheet

```python
import sys; sys.path.insert(0, "../hacking session 2")   # from a challenge folder
from cryptokit import *
d = load_json("challenge.json")        # numeric strings -> int, ignores junk before '{'
```

Run `python3 test_cryptokit.py` once at the start to check everything works.

## First 60 seconds on any challenge

1. **Read the title** — every weekly title was a hint (*Free keys* = common modulus, *sports car desire* = Wiener/“small d”, *Double Entry* = reused k, *Phone Book* = unauthenticated directory).
2. **Print sizes**: `n.bit_length()`, `e`, `d`, `c.bit_length()` vs `n.bit_length()`.
3. **Compare values**: same `n`? same `r`? same `c1`? same `c`? Anything repeated is a bug.
4. **Try the cheap stuff**: `factor(n)` (tries Fermat, p−1, rho, p+1), then factordb.com.
5. **Look at how randomness is made** in given source code: `random` seeded with time, counters, LCGs → related nonces.

## RSA: what you see → what to call

| You see | Attack | Call |
|---|---|---|
| `e = 3` (small), no padding, short message | cube root | `small_e_root(c, e, n)` |
| same `m`, small `e`, ≥ e different `n` | Håstad broadcast | `hastad(cs, ns, e)` |
| …and the moduli share a factor | gcd | `shared_prime_factors(ns)` |
| same `n`, two `e`, same `m` | common modulus | `common_modulus(c1, c2, e1, e2, n)` (also handles gcd(e1,e2) > 1) |
| huge `e` (close to `n`) | small `d` → Wiener | `wiener(e, n)` → `(d, p, q)` |
| many keys from the same generator | shared primes | `shared_prime_factors(ns)` |
| `p`, `q` close (`fermat` in the title, “twin”, “sand”…) | Fermat | `fermat_factor(n)` |
| “smooth”, “sifting”, small `p−1` | Pollard p−1 | `pollard_p1(n)` / `factor(n)` |
| one factor is small | Pollard rho | `pollard_rho(n)` |
| `n = p^k`, or > 2 primes | multi-prime phi | `factor(n)` then `rsa_decrypt(c, e, n, factors)` |
| `gcd(e, phi) ≠ 1` (e = 2, e divides p−1) | e-th roots + CRT | `rsa_decrypt_all(c, e, [p, q])` |
| leaked `d` | factor n | `factor_from_d(n, e, d)` |
| leaked `phi` | factor n | `factor_from_phi(n, phi)` |
| leaked `dp = d mod (p−1)` | gcd trick | `dp_leak(n, e, dp)` |
| faulty / glitched CRT signature | Bellcore | `rsa_crt_fault(n, e, m, s_bad)` |
| decryption oracle that refuses *your* `c` | blinding (CCA, slide 46) | `rsa_blind_decrypt(c, e, n, oracle)` |
| signing oracle that refuses a message | blinding | `rsa_blind_sign(m, e, n, oracle)` |
| oracle says “even/odd” or “valid/invalid” on the last bit | parity oracle | `lsb_oracle(c, e, n, parity)` |
| two messages with known relation `m2 = a·m1 + b` | Franklin–Reiter | `franklin_reiter(c1, c2, e, n, a, b)` |
| textbook signatures, “sign two things” | multiplicative forgery | `rsa_multiplicative_forge(sa, sb, n)` |
| e=3 signature check that only looks at the prefix | Bleichenbacher ’06 | `rsa_sig_e3_forge(digest_info, n)` |
| timing differences in decryption (slide 43) | timing attack | `Remote(...).timed(data, prompt)` and measure many times; take the median |

**Not in the toolkit (needs a lattice library such as `fpylll` or SageMath):**
- Coppersmith attacks: a known message prefix with `e = 3`, padded Håstad, and knowing half the bits of `p`.
- Boneh–Durfee: `d` slightly too large for Wiener, roughly `d < n^0.292`.
- Hidden-number attacks on DSA nonces that are biased or leak a few bits.

If you see any of those, use [SageMath online](https://sagecell.sagemath.org) and `small_roots()`.

## ElGamal / Diffie–Hellman

| You see | Attack | Call |
|---|---|---|
| same `c1` twice + one known plaintext | nonce reuse | `elgamal_known_plaintext(c2_known, m_known, c2_target, p)` |
| `c1` values related (`k+1`, `2k`, LCG…) | related nonce | see `Assymmetric encryption - ElGamal/Fresh every time/solve.py` |
| `p − 1` smooth (factor it!) | Pohlig–Hellman → private key | `dlog(g, y, p)` |
| `p − 1` has one big factor but secret `x` is small | partial Pohlig–Hellman | `dlog_partial(g, y, p)` |
| small group / small secret (< 2^40) | baby-step giant-step | `bsgs(g, h, p, order)` |
| “change the message without the key” | malleability | `elgamal_malleate(c1, c2, t, p)` → decrypts to `m·t` |
| need 1 bit of info about `m` (QR) | Legendre leak | `elgamal_qr_leak(c1, c2, g, y, p)` |
| server does DH and uses `g^ab` you can steer | send `A = 1`, `A = p−1`, `A = 0` → key becomes 1 / ±1 / 0 | by hand |
| server accepts any `A` and `p−1` has small factors | small-subgroup: send element of order `r`, brute force key mod `r`, CRT | `crt()` + `bsgs()` |

**Check the generator:** `pow(g, (p-1)//q, p) == 1` for a factor `q` means `g` lives in a small subgroup, so the key space is tiny.

## Signatures (DSA / ECDSA / ElGamal / Schnorr)

| You see | Attack | Call |
|---|---|---|
| two signatures with the same `r` | reused k | `dsa_reused_k(r, s1, h1, s2, h2, q)` → `(x, k)` |
| `k` leaked / guessable (time, counter, small) | known k | `dsa_known_k(r, s, h, k, q)` (brute force small k: check `pow(g,k,p)%q == r`) |
| `k2 = a·k1 + b` (counter, LCG) | related k | `dsa_related_k(r1,s1,h1, r2,s2,h2, q, a, b)` |
| verifier doesn't check `0 < r < q`, `0 < s < q` | `r = s = 0` or `r = q` tricks | `dsa_verify` shows what *should* be checked |
| ElGamal signature, same r | reused k mod p−1 | `elgamal_sig_reused_k(r, s1, h1, s2, h2, p)` |
| ElGamal signature on *raw* message (no hash) | existential forgery | `elgamal_sig_existential_forgery(g, y, p)` |
| hash = `int(sha256(m)) % q` | that is `H_int(m, q)` | |

## Protocols (slides part 5, “Mutual Trust”)

Expect a server you talk to over a socket or HTTP, like *Phone Book* and *Timely Database Updates*.

- **Unauthenticated public-key directory**: register your own key under the victim's name, as in *Phone Book*.
- **Diffie–Hellman with no authentication**: you are the man in the middle (slide 22). Do a separate DH exchange with each side and relay messages, decrypting and re-encrypting as they pass.
- **Merkle's simple scheme** (slide 17): A sends `PU_a`, and B replies with `E(PU_a, Ks)`. Swap `PU_a` for your own key.
- **Key distribution centre without nonces or timestamps**: replay an old message containing a session key you already know (Denning–Sacco replay). Look for a step where B can't tell whether `E(Kb, [Ks || IDa])` is fresh.
- **Nonce challenge-response**: if the server signs or encrypts any nonce you send, use it as an oracle. Reflection attack: open a second session and get the server to answer its own challenge.
- **Kerberos-style tickets**: a ticket is only bound to the fields it contains. Check what isn't covered, such as timestamps, lifetimes or the client ID.
- **Certificates** (X.509): check whether the issuer's signature is actually verified, whether the chain is checked, and whether a self-signed certificate is accepted.

## Utilities

- `Remote(host, port)`: `recvuntil`, `recvline`, `sendline`, `sendlineafter`, `recvall`, and `timed(...)` for timing attacks. A stdlib-only, pwntools-style socket wrapper.
- `ints_in(text)` pulls every number out of server output.
- `show(m)` turns a recovered integer into text and strips PKCS#1 v1.5 padding.
- `crt` (works with non-coprime moduli too), `iroot`, `egcd`, `inv`, `is_probable_prime`, `continued_fraction`, `convergents`, `sqrt_mod_prime`, `nth_roots_mod_prime`.
- Theory: `../Asymmetric encryption - Wikipedia/` (`grep -ri <term>`).
