# Secure Bank 2

**Course:** Cryptography & Network Security — Hashing chapter
**Category:** Hash collision / truncated-digest birthday attack
**Target:** `cns-test.idlab.uantwerpen.be:50003`
**Flag:** `cns{legacy_reconciliation_collision}`

---

## 1. Challenge

After the first Secure Bank hack, the bank "can no longer afford to store the full
fingerprint." It now keeps only a **truncated** audit fingerprint of each payment. The
server takes two JSON payment records (one per line), validates both, and returns their
audit fingerprints. The hint — *they don't store the full fingerprint anymore, you might be
able to make use of that* — points straight at the shortened digest.

Each record must contain exactly these fields:

| Field | Type | Requirement |
|---|---|---|
| `reference` | String | 1–128 chars |
| `from_account` | String | starts with `SIM-` |
| `to_account` | String | starts with `SIM-`, different from source |
| `amount` | Number | must equal `10` |
| `currency` | String | must be `EUR` |
| `timestamp` | String | valid ISO 8601, recent |

Records are serialised with a fixed canonical form before hashing:

```python
def canonicalize(payment):
    return json.dumps(payment, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("utf-8")
```

## 2. Reconnaissance — what the fingerprint actually is

Hash one canonicalised record locally with plain `hashlib.sha256` and compare the first
bytes to the server's returned fingerprint. They match, and the server's value is only
**4 bytes long**. Two facts fall out:

- The fingerprint is **unkeyed** — it is just `SHA-256(canonicalize(payment))`, which we
  can reproduce offline. No secret is involved.
- It is **truncated to 32 bits** (4 bytes). That is the "we can't afford the full
  fingerprint" hint made literal.

## 3. Root cause — truncation destroys collision resistance

SHA-256's collision resistance comes from its 256-bit output: a birthday collision needs
~2¹²⁸ work, which is infeasible. Truncate the digest to `n` bits and the birthday bound
drops to ~2^(n/2):

| Digest kept | Birthday work for a collision |
|---|---|
| 256 bits (full) | ~2¹²⁸ — infeasible |
| **32 bits (this challenge)** | **~2¹⁶ ≈ 65k hashes — milliseconds** |

So we don't attack SHA-256 at all; we attack the **4-byte cut**. Among roughly 2¹⁶ inputs,
two are overwhelmingly likely to share the same 4-byte prefix (the birthday paradox).

## 4. The attack

We need **two different valid payments with the same fingerprint**. Every field is pinned
to a value the validator accepts, and we vary only the one free-text field, `reference`:

```python
def record(ref, ts):
    return {"reference": ref, "from_account": "SIM-alice", "to_account": "SIM-bob",
            "amount": 10, "currency": "EUR", "timestamp": ts}
```

Then hash offline, storing each 4-byte prefix in a dict, until one repeats:

```python
def find_collision(ts):
    seen = {}
    i = 0
    while True:
        ref = "r%d" % i
        fp = hashlib.sha256(canonicalize(record(ref, ts))).digest()[:4]
        if seen.get(fp, ref) != ref:     # this prefix seen before with a different ref
            return seen[fp], ref, fp
        seen[fp] = ref
        i += 1
```

This is a textbook birthday search: keep a table of seen prefixes and stop at the first
repeat. It returns after ~2¹⁶ tries on average.

## 5. The timestamp gotcha

Records must be stamped within the previous minute, so the collision has to be found
*against a timestamp the server will still accept*. The script reads the server's own
clock from the banner and nudges it two seconds into the past, then uses that single fixed
`ts` for **both** records so they stay collidable and valid:

```python
now = re.search(r"Current time:\s*([0-9T:.\-+]+)", banner.decode()).group(1)
ts = (datetime.datetime.fromisoformat(now) - datetime.timedelta(seconds=2)).isoformat()
```

Because `ts` is identical in both records, it is part of the shared canonical structure —
only `reference` differs — so the collision search is clean and both payments validate.

## 6. Exploit — one connection

```python
ref_a, ref_b, fp = find_collision(ts)
p1 = canonicalize(record(ref_a, ts))
p2 = canonicalize(record(ref_b, ts))
assert p1 != p2
assert hashlib.sha256(p1).digest()[:4] == hashlib.sha256(p2).digest()[:4]
sock.sendall(p1 + b"\n" + p2 + b"\n")      # two records, one per line
```

Two distinct valid payments that hash to the same 4-byte audit fingerprint → the server
reconciles them as the same record → flag.

```
=> cns{legacy_reconciliation_collision}
```

## 7. Step-by-step reproduction

1. **Connect** to `cns-test.idlab.uantwerpen.be:50003` and read the banner (it prints the
   current server time and prompts for `Payment 1:`).
2. **Identify the fingerprint.** Hash one canonicalised record with `hashlib.sha256` and
   confirm the server returns only its first 4 bytes — unkeyed and truncated.
3. **Pin every validated field** to an accepted value; leave only `reference` free.
4. **Grab a fresh timestamp** from the banner, back-date it a couple of seconds, and reuse
   it for both records.
5. **Birthday-search** over `reference` values, storing 4-byte prefixes until one repeats
   (~2¹⁶ hashes, well under a second).
6. **Submit both colliding records** in one connection, `\n`-separated.
7. **Collect the flag:** `cns{legacy_reconciliation_collision}`.

## 8. Why it works / lessons

Truncating a hash or MAC to save storage throws away collision resistance **in proportion
to the bits removed** — and because of the birthday bound you lose it *twice as fast* as
intuition suggests: cutting to 32 bits leaves only ~16 bits of real collision security.

**Mitigations**

- **Don't truncate below the security you need.** For collision resistance keep at least
  2× the target security level in bits (≥256 bits for 128-bit collision security).
- If short identifiers are genuinely required, make them **keyed** (HMAC) *and* tie the
  decision to the full digest, so an attacker can't precompute collisions offline.
- Treat an "audit fingerprint" as security-relevant: enforce uniqueness on the **full**
  hash, not on a storage-optimised prefix.
