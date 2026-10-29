"""
SecureBank audit-fingerprint collision (cns-test.idlab.uantwerpen.be:50003).

The "audit fingerprint" is SHA-256(canonicalize(payment)) truncated to the first
4 bytes -> only 32 bits, and unkeyed (the server's value matches a local
hashlib.sha256). A 32-bit digest falls to a birthday attack: among ~2^16 inputs
a collision is likely.

We fix every field (including one fresh timestamp read from the server's clock,
since records must be stamped within the previous minute) and vary only
`reference`, hashing offline until two references share a 4-byte prefix, then
submit both valid payments in one connection.

    Flag: cns{legacy_reconciliation_collision}

Lesson: truncating a hash/MAC to save storage throws away collision resistance
proportionally -- 32 bits gives only ~16 bits of birthday security.
"""
import json
import socket
import re
import hashlib
import datetime

HOST, PORT = "cns-test.idlab.uantwerpen.be", 50003


def canonicalize(payment):
    return json.dumps(payment, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("utf-8")


def recv_until(sock, needle, t=6):
    sock.settimeout(t)
    buf = b""
    try:
        while needle not in buf:
            chunk = sock.recv(4096)
            if not chunk:
                break
            buf += chunk
    except socket.timeout:
        pass
    return buf


def recv_all(sock, t=5):
    sock.settimeout(t)
    buf = b""
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            buf += chunk
    except socket.timeout:
        pass
    return buf


def record(ref, ts):
    return {"reference": ref, "from_account": "SIM-alice", "to_account": "SIM-bob",
            "amount": 10, "currency": "EUR", "timestamp": ts}


def find_collision(ts):
    """Vary only `reference` until two payments share the 4-byte fingerprint."""
    seen = {}
    i = 0
    while True:
        ref = "r%d" % i
        fp = hashlib.sha256(canonicalize(record(ref, ts))).digest()[:4]
        if seen.get(fp, ref) != ref:
            return seen[fp], ref, fp
        seen[fp] = ref
        i += 1
        if i % 500000 == 0:
            print(f"  ...{i} candidates, no collision yet")


def main():
    sock = socket.create_connection((HOST, PORT), timeout=8)
    banner = recv_until(sock, b"Payment 1:")
    now = re.search(r"Current time:\s*([0-9T:.\-+]+)", banner.decode()).group(1)
    # Must be within the previous minute; nudge a couple of seconds into the past.
    ts = (datetime.datetime.fromisoformat(now) - datetime.timedelta(seconds=2)).isoformat()
    print("server now:", now, "| using ts:", ts)

    ref_a, ref_b, fp = find_collision(ts)
    p1 = canonicalize(record(ref_a, ts))
    p2 = canonicalize(record(ref_b, ts))
    print(f"collision on {fp.hex()}:")
    print("  P1:", p1.decode())
    print("  P2:", p2.decode())
    assert p1 != p2
    assert hashlib.sha256(p1).digest()[:4] == hashlib.sha256(p2).digest()[:4]

    sock.sendall(p1 + b"\n" + p2 + b"\n")
    print("=== RESPONSE ===")
    print(recv_all(sock).decode(errors="replace"))
    sock.close()


if __name__ == "__main__":
    main()
