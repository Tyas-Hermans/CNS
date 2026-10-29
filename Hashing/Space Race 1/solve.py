"""
Solve the "Space Race 1" challenge (Mars Relay Authentication).

    cns-test.idlab.uantwerpen.be 50006

The server emits 64-hex "authentication codes" (SHA-256 digests) on a ~10s
timer and asks you to "predict the next authentication code before it is
transmitted". It reseeds every connection, so the trick is the *relation*
between successive codes, not the codes themselves.

--------------------------------------------------------------------------
How the codes are generated
--------------------------------------------------------------------------
Capturing consecutive codes and searching over
    {sha256, sha1, md5, sha512, ...} x {1,2,3 iterations}
    x {hex-string vs raw-bytes input} x {hex vs raw intermediate}
while REQUIRING one rule to explain TWO transitions (c1->c2 AND c2->c3)
yields exactly one survivor (a 2-transition match at 256 bits is certainty):

    code_{k+1} = sha256( sha256( bytes.fromhex(code_k) ).digest() ).hexdigest()

i.e. double SHA-256 over the raw bytes of the previous code. It reproduces a
whole session 10/10 transitions.

--------------------------------------------------------------------------
The protocol twist: predict the TELEMETRY, not the CODE
--------------------------------------------------------------------------
Sending the literal next code (double-sha of current) is always rejected with
"Wrong prediction." -- even though that value *does* show up as the next
transmitted code one tick later. The banner is the clue: codes are generated
"from hashed orbital telemetry". The code you see is already a hash. The chain
factors as:

    telemetry_k --sha256--> code_k
    telemetry_{k+1} = sha256( raw(code_k) )        <-- the inner value
    code_{k+1}      = sha256( telemetry_{k+1} )    == double-sha(code_k)

The server wants the *preimage* of the next code -- the telemetry -- which is
the single inner hash:

    prediction = sha256( bytes.fromhex(current_code) ).hexdigest()

Sending that on the very first code returns the flag immediately.

    Flag: cns{hash_chains_are_not_totp}

Lesson: a hash chain is deterministic and keyless -- observe any one value and
every future value is computable. It looks like a rotating one-time password
but, unlike real TOTP (which mixes in a secret key), there is no secret, so its
security is imaginary.
"""

import hashlib
import socket

HOST = "cns-test.idlab.uantwerpen.be"
PORT = 50006


def predict(code_hex):
    """The telemetry that generates the next code = single SHA-256 of raw bytes."""
    return hashlib.sha256(bytes.fromhex(code_hex)).hexdigest()


def next_code(code_hex):
    """The next transmitted code = double SHA-256 of raw bytes (for verification)."""
    return hashlib.sha256(hashlib.sha256(bytes.fromhex(code_hex)).digest()).hexdigest()


def main():
    with socket.create_connection((HOST, PORT), timeout=30) as s:
        s.settimeout(35)
        f = s.makefile("rwb", buffering=0)

        def readline():
            buf = b""
            while True:
                b = f.read(1)
                if not b:
                    return None
                buf += b
                if b == b"\n":
                    return buf.decode(errors="replace")

        while True:
            line = readline()
            if line is None:
                print("connection closed")
                return
            text = line.strip()
            if text:
                print("<<<", text)
            if text.startswith("CURRENT CODE:"):
                code = text.split(":", 1)[1].strip()
                guess = predict(code)
                f.write((guess + "\n").encode())
                print(">>>", guess)
            if "flag" in text.lower() or ("cns{" in text and "}" in text):
                return


if __name__ == "__main__":
    main()
