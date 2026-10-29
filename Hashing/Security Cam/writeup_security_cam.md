# Security Cam

**Course:** Cryptography & Network Security — Hashing chapter
**Category:** RTSP Digest authentication / offline MD5 dictionary attack
**Target:** `rtsp://cns-test.idlab.uantwerpen.be:50002/video`
**Recovered password:** `camera123456789`

---

## 1. Challenge

We intercepted network traffic from a security camera (`security-cam.pcapng`) and must
recover the password to "see into their facility." The attached screenshot is a Wireshark
hint: it shows the **RTSP protocol preferences** with the TCP port list set to
`554,8554,7236,50002`. The takeaway is that the camera speaks **RTSP on the non-standard
port 50002**, so Wireshark won't decode it as RTSP until you add that port (or you just
read it as text, since RTSP is a cleartext, HTTP-like protocol).

## 2. Reconnaissance — read the RTSP exchange

RTSP messages are plain ASCII, so the whole handshake is visible in the capture
(`strings security-cam.pcapng | grep -iE 'RTSP|Authorize|Digest'`):

```
DESCRIBE rtsp://cns-test.idlab.uantwerpen.be:50002/video RTSP/1.0
→ RTSP/1.0 401 Unauthorized
  WWW-Authenticate: Digest realm="PythonRTSP",
      nonce="4874a055c3f4390506d99e6c51a9e3e360cbef8a62abd7079e11faddcb70a38c",
      algorithm=MD5

DESCRIBE rtsp://.../video RTSP/1.0
  Authorization: Digest username="user", realm="PythonRTSP",
      nonce="4874a055...a38c", uri="rtsp://.../video",
      response="b3539154c5b784bba2c47a1a6c7c4ab0", algorithm="MD5"
→ RTSP/1.0 200 OK
```

The server challenges with a `nonce`; the client answers with a `response`. No password is
ever transmitted — that is the point of Digest auth. But **every input to the response
except the password sits in the capture in cleartext.**

## 3. How RTSP Digest auth works (RFC 2617)

RTSP reuses HTTP Digest. The `response` is a chain of MD5 hashes:

```
HA1      = MD5(username : realm : password)
HA2      = MD5(method : uri)
response = MD5(HA1 : nonce : HA2)
```

From the capture we know **all** of these except `password`:

| Term | Value from capture |
|---|---|
| `username` | `user` |
| `realm` | `PythonRTSP` |
| `nonce` | `4874a055c3f4390506d99e6c51a9e3e360cbef8a62abd7079e11faddcb70a38c` |
| `method` | `DESCRIBE` |
| `uri` | `rtsp://cns-test.idlab.uantwerpen.be:50002/video` |
| `response` | `b3539154c5b784bba2c47a1a6c7c4ab0` |

## 4. Root cause — Digest is an offline-crackable MD5 chain

Digest never sends the password, but the `response` is a **deterministic, unkeyed,
unsalted MD5 function of the password plus public values**. So an attacker who captured one
exchange can test password guesses entirely **offline**: recompute `response` for each
candidate and compare. MD5 is extremely fast (tens of millions of hashes/second), so any
password in a wordlist like rockyou falls in seconds.

## 5. The attack (`solve.py`)

`HA2` is constant (no password), so compute it once; only `HA1` varies per guess:

```python
ha2 = md5(f"{METHOD}:{URI}")
for raw in open("rockyou.txt", "rb"):
    pw  = raw.rstrip(b"\r\n").decode("latin-1")
    ha1 = md5(f"{USERNAME}:{REALM}:{pw}")
    if md5(f"{ha1}:{NONCE}:{ha2}") == RESPONSE:
        print("password:", pw); break
```

Running it:

```
[+] password found after 9326363 tries: 'camera123456789'
real 0m18s
```

**Verification.** The same password reproduces the `response` of every authenticated
request in the capture, not just the DESCRIBE — confirming it is correct:

| Request | method : uri | captured response | matches? |
|---|---|---|---|
| DESCRIBE | `DESCRIBE : .../video` | `b3539154…4ab0` | ✅ |
| SETUP | `SETUP : .../video/trackID=0` | `083ae471…1893` | ✅ |
| PLAY | `PLAY : .../video/` | `be8c3203…4562` | ✅ |

With `user:camera123456789` you can now authenticate to
`rtsp://cns-test.idlab.uantwerpen.be:50002/video` and pull the live stream (e.g.
`ffplay rtsp://user:camera123456789@cns-test.idlab.uantwerpen.be:50002/video`) to "see into
the facility."

## 6. Step-by-step reproduction

1. **Spot the port.** The Wireshark hint adds `50002` to the RTSP port list — the camera
   speaks RTSP on a non-standard port. Decode-as RTSP, or just read the packets as text.
2. **Pull the Digest challenge/response.** Find the `WWW-Authenticate` (nonce, realm) and
   the client's `Authorization` header (username, uri, response, method).
3. **Recall the Digest formula:** `response = MD5(MD5(user:realm:pw) : nonce :
   MD5(method:uri))`. Everything but `pw` is known.
4. **Dictionary-attack offline** with rockyou: recompute `response` per candidate, compare.
5. **Crack:** `camera123456789` (≈9.3M guesses, ~18 s).
6. **Verify** against the SETUP/PLAY responses, then connect to the stream with the
   recovered credentials.

## 7. Why it works / lessons

Digest auth keeps the password off the wire, but it provides **no protection once a single
exchange is captured**: the verifier is an unsalted MD5 chain over mostly-public values, so
password guessing happens offline at full MD5 speed. A short/weak password (`camera` + a
digit run) makes this trivial.

**Mitigations**

- **Run RTSP over TLS (RTSPS) / a VPN** so the handshake can't be sniffed at all.
- **Use strong, high-entropy passwords** — Digest's only remaining security *is* the
  password's guessing resistance.
- Prefer modern password-authenticated schemes with **salting and slow KDFs** (or mutual
  TLS / client certs) instead of raw MD5 Digest, which has no salt and no work factor.
- Change default/weak camera credentials; `camera123456789` is exactly the kind of
  predictable password a wordlist contains.
