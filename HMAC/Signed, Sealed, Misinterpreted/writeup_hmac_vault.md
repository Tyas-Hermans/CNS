# Signed, Sealed, Misinterpreted

**Course:** Cryptography & Network Security — HMAC chapter
**Category:** Message authentication / parser differential
**Target:** `http://cns-test.idlab.uantwerpen.be:50007`
**Flag:** `cns{canonicalization_is_critical}`

---

## 1. Challenge

The vault authenticates JSON requests with HMAC-SHA256. The signature travels in the
`X-Signature` header, and `/challenge` hands out one legitimate signed request. The goal
is to reach the administrator vault **without knowing the secret key**, and we are told we
*may reuse* the signature from `/challenge`.

## 2. Reconnaissance

`GET /challenge` returns a signed message:

```json
{
  "instructions": "POST JSON to /vault with X-Signature",
  "message": { "action": "view", "role": "user" },
  "signature": "817e86132b480782043d61602c1843100dc8002186502619e802913d918a0f69"
}
```

So the authenticated payload is `{"action":"view","role":"user"}` and we need `role` to
become `admin` while keeping a signature that still verifies.

## 3. Probing the verifier

| # | Body sent (with the original signature) | Response |
|---|---|---|
| 1 | `{"action":"view","role":"user"}` (exact) | `403 Access denied` |
| 2 | `{"action":"view","role":"admin"}` | `Invalid signature` |
| 3 | `{"action": "view", "role": "user"}` (extra whitespace) | `403 Access denied` |
| 4 | `{"role":"user","action":"view"}` (reordered) | `403 Access denied` |
| 5 | `{"action":"view","role":"user","role":"admin"}` | `Invalid signature` |
| 6 | `{"action":"view","role":"admin","role":"user"}` | **`cns{canonicalization_is_critical}`** |

Two facts fall out of this:

- **The signature is not computed over the raw bytes.** Adding whitespace (#3) and
  reordering keys (#4) both still verify. The server therefore *parses the JSON and
  re-serialises it into a canonical form*, then HMACs that canonical form.
- **Duplicate keys behave asymmetrically** (#5 vs #6). The only difference between the two
  is the *order* of the two `role` entries, yet one is rejected as a bad signature and the
  other is accepted **and** treated as admin.

## 4. Root cause — a JSON parser differential

The server parses the same body twice, with two parsers that resolve duplicate keys
**differently**:

| Component | Duplicate-key rule | Sees `role` = | Effect for body #6 |
|---|---|---|---|
| Signature canonicaliser | **last** value wins (standard `json.loads`) | `user` | canonical form == originally signed message ⇒ **signature valid** |
| Authorisation check | **first** value wins | `admin` | **admin access granted** |

For body #6, `{"action":"view","role":"admin","role":"user"}`:

- The signature path collapses the duplicate to `role=user`, reproducing the exact message
  that `817e86…` was computed over, so the reused signature matches.
- The authorisation path reads the *first* `role`, `admin`, and unlocks the vault.

Body #5 is the mirror image (`user` first, `admin` last): now the signature path collapses
to `role=admin`, which no longer matches the signed message, so it is rejected before
authorisation is ever reached. This confirms the last-wins / first-wins split.

## 5. Exploit

```bash
curl -X POST http://cns-test.idlab.uantwerpen.be:50007/vault \
  -H "Content-Type: application/json" \
  -H "X-Signature: 817e86132b480782043d61602c1843100dc8002186502619e802913d918a0f69" \
  --data '{"action":"view","role":"admin","role":"user"}'
# => {"flag":"cns{canonicalization_is_critical}"}
```

No knowledge of the HMAC key is required — the attack lives entirely in the mismatch
between what is signed and what is interpreted.

## 6. Step-by-step reproduction

1. **Get the signed sample.** `GET /challenge` and note the `message`
   (`{"action":"view","role":"user"}`) and its `signature` (`817e86…`).

   ```bash
   curl -s http://cns-test.idlab.uantwerpen.be:50007/challenge
   ```

2. **Confirm the signature is valid by replaying it verbatim.** POST the exact message with
   the given signature. You get `403 Access denied` — not "Invalid signature". This proves
   the signature *verifies*; you are only blocked by `role=user`.

   ```bash
   curl -s -X POST .../vault -H "X-Signature: 817e86…" \
        --data '{"action":"view","role":"user"}'      # -> Access denied
   ```

3. **Confirm the naive forgery fails.** Change `role` to `admin` with the same signature →
   `Invalid signature`. So `role` *is* covered by the MAC; you cannot just edit the value.

   ```bash
   curl ... --data '{"action":"view","role":"admin"}'  # -> Invalid signature
   ```

4. **Test whether the MAC is over raw bytes or over canonical JSON.** Re-send the original
   message but add whitespace, then reorder the keys. Both still return `Access denied`
   (signature still valid) → the server **parses and re-serialises** the JSON before
   hashing. This is the opening: you can restructure the body without breaking the MAC.

   ```bash
   curl ... --data '{"action": "view", "role": "user"}'   # whitespace  -> Access denied
   curl ... --data '{"role":"user","action":"view"}'      # reordered   -> Access denied
   ```

5. **Attack the canonicalisation with a duplicate key.** Send `role` twice and vary the
   order to find the parser split:
   - `…,"role":"user","role":"admin"` → `Invalid signature`
   - `…,"role":"admin","role":"user"` → **flag**

   The working order puts `admin` first and `user` last. The signer keeps the *last* value
   (`user`, matching the signed message → valid MAC); the authoriser keeps the *first*
   value (`admin` → access granted).

   ```bash
   curl -s -X POST http://cns-test.idlab.uantwerpen.be:50007/vault \
     -H "Content-Type: application/json" \
     -H "X-Signature: 817e86132b480782043d61602c1843100dc8002186502619e802913d918a0f69" \
     --data '{"action":"view","role":"admin","role":"user"}'
   ```

6. **Collect the flag:** `cns{canonicalization_is_critical}`.

### Mental model for the probe order
- First establish a **valid baseline** (step 2) so every later response is interpreted
  against "signature OK, authz denied".
- Then separate the two failure modes: `Access denied` (sig valid, not authorised) vs
  `Invalid signature` (sig rejected). Every probe is just moving a body between those two
  buckets until you find one that is *sig-valid* **and** *authorised*.

## 7. Why it works / lessons

HMAC did its job perfectly: it guaranteed integrity of *the canonical string the verifier
chose to sign*. The vulnerability is that **that string is not the same object the
authorisation logic acts on.** Authenticating one representation while making decisions on
another breaks the entire guarantee.

**Mitigations**

- Authenticate the **exact bytes** that are consumed — compute and verify the HMAC over the
  raw request body, and feed those same bytes to exactly one parser.
- **Reject duplicate keys** (RFC 8259 permits either resolution, so treat duplicates as
  malformed) rather than silently picking one.
- If canonicalisation is needed, canonicalise **once** and derive both the signature check
  and every authorisation decision from that single parsed object.
- Keep the key unknown and the algorithm strong — it changes nothing here. A correct
  primitive used around an ambiguous data model is still exploitable.
