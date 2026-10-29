"""
Security Cam (cns-test.idlab.uantwerpen.be:50002) -- crack the RTSP Digest password.

The capture (security-cam.pcapng) contains an RTSP session on non-standard TCP port
50002. RTSP authentication is HTTP Digest (RFC 2617) over MD5, so the client proves it
knows the password without sending it -- but every input to that proof except the
password is in the cleartext capture:

    HA1      = MD5(username : realm : password)
    HA2      = MD5(method : uri)
    response = MD5(HA1 : nonce : HA2)

Only `password` is unknown, and MD5 is unkeyed and fast, so we dictionary-attack it with
rockyou: for each candidate, recompute `response` and compare to the captured value.
"""
import hashlib

# --- values lifted straight from the DESCRIBE (CSeq 3) request in the pcap ---
USERNAME = "user"
REALM    = "PythonRTSP"
NONCE    = "4874a055c3f4390506d99e6c51a9e3e360cbef8a62abd7079e11faddcb70a38c"
METHOD   = "DESCRIBE"
URI      = "rtsp://cns-test.idlab.uantwerpen.be:50002/video"
RESPONSE = "b3539154c5b784bba2c47a1a6c7c4ab0"

WORDLIST = "rockyou.txt"


def md5(s):
    return hashlib.md5(s.encode()).hexdigest()


def main():
    # HA1 depends on the password; HA2 is constant, so compute it once.
    ha2 = md5(f"{METHOD}:{URI}")
    with open(WORDLIST, "rb") as f:
        for i, raw in enumerate(f):
            pw = raw.rstrip(b"\r\n").decode("latin-1")
            ha1 = md5(f"{USERNAME}:{REALM}:{pw}")
            if md5(f"{ha1}:{NONCE}:{ha2}") == RESPONSE:
                print(f"[+] password found after {i} tries: {pw!r}")
                return
    print("[-] password not found in wordlist")


if __name__ == "__main__":
    main()
