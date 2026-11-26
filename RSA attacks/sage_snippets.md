# Lattice attacks at real sizes — Sage / fpylll snippets

The pure-Python Coppersmith in `cryptokit` (used by the `*DEMO size*` demos) is
only fast for small moduli, because exact-integer LLL blows up on 1024-bit
lattices. For a real challenge, paste these into **https://sagecell.sagemath.org**
(free, nothing to install) or run locally if you have SageMath / `fpylll`.

`beta` = the size of the divisor you target, as a power of `N`
(`beta = 1.0` → modulo N itself; `beta = 0.5` → a prime factor p ≈ √N).
`epsilon` trades lattice size for how large a root you can reach; shrink it
(e.g. `1/30`) and raise `m` if `small_roots` returns `[]`.

## 1. Stereotyped message / known prefix, small e

`c = m^e mod n`, and you know all of `m` except a short unknown chunk.

```python
# Sage
n = 0x...        # modulus
e = 3
c = 0x...        # ciphertext
known = bytes.fromhex("...")      # the part of the padded message you know
unknown_len = 16                  # unknown bytes, at the END (low bytes)

P.<x> = PolynomialRing(Zmod(n))
m0 = int.from_bytes(known + b"\x00"*unknown_len, "big")
f = (m0 + x)^e - c
X = 256^unknown_len
roots = f.monic().small_roots(X=X, beta=1.0, epsilon=1/20)
for r in roots:
    m = m0 + int(r)
    print(int(m).to_bytes((int(m).bit_length()+7)//8, "big"))
```

Coppersmith works here while `unknown_len < bits(n)/(8*e)` (for 1024-bit n, e=3:
about 42 unknown bytes).

## 2. Known high bits of p (partial key exposure) → factor n

You know the top bits of a prime factor `p` (e.g. from a side channel or a
truncated key print).

```python
# Sage
n = 0x...
p_high = 0x...          # known high part, low `unknown_bits` bits zeroed
unknown_bits = 400      # must be < bits(p)/2  (for a 1024-bit n: < 256)

P.<x> = PolynomialRing(Zmod(n))
f = p_high + x
X = 2^unknown_bits
r = f.small_roots(X=X, beta=0.5, epsilon=1/30)
if r:
    p = p_high + int(r[0]); print("p =", p, "  n % p == 0:", n % p == 0)
```

## 3. Boneh–Durfee: d a bit too large for Wiener (d < n^0.292)

Wiener needs `d < n^0.25`; Boneh–Durfee reaches `d < n^0.292`. Use a maintained
implementation rather than writing it from scratch — the well-known one is
David Wong's `boneh_durfee.sage`
(https://github.com/mimoo/RSA-and-LLL-attacks). Set `delta = 0.28` and grow `m`.

## 4. Håstad with *padding* (linear padding, same small e)

If each recipient got `a_i*m + b_i` encrypted with the same small `e`, plain
Håstad fails. Combine the `e` polynomials `(a_i*m + b_i)^e - c_i` with CRT into
one polynomial mod `∏ n_i` and run `small_roots` on it (this is the generalized
Håstad / Coppersmith broadcast attack).

## When to reach for this

If `cryptokit`'s `small_e_root`, `hastad`, `wiener` or `factor` all fail and the
challenge hints that you know *part* of the message or key, it is almost
certainly a Coppersmith problem — switch to Sage here.
