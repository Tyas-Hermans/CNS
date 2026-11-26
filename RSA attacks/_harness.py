"""Shared setup for the RSA-attack demos.

Each demo file does `from _harness import *`, defines functions named demo_*,
and the runner at the bottom builds a vulnerable instance, runs the attack and
checks the flag comes back.  Run a file directly to see every attack in it:

    python3 "01_factoring.py"
"""
import math
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "hacking session 2"))
from cryptokit import *  # noqa: F401,F403  (the whole toolkit)

from sympy import nextprime, primerange, primitive_root, randprime  # noqa: F401

random.seed(0xC0FFEE)
FLAG = b"cns{this_is_the_secret_flag}"
M = b2i(FLAG)


def prime(bits: int) -> int:
    return int(randprime(1 << (bits - 1), 1 << bits))


def _squarefree_smooth(bits: int, B: int) -> int:
    """Product of 2 and DISTINCT odd primes < B, ~`bits` long (square-free, so the
    largest prime power equals the largest prime -> a bound of B really covers it)."""
    pool = list(primerange(3, B))
    while True:
        random.shuffle(pool)
        n, i = 2, 0
        while n.bit_length() < bits and i < len(pool):
            n *= pool[i]
            i += 1
        if n.bit_length() >= bits:
            return n


def smooth_prime(bits: int, B: int = 1 << 16) -> int:
    """A prime p where p-1 is B-smooth (vulnerable to Pollard p-1)."""
    while True:
        n = _squarefree_smooth(bits, B)
        if is_probable_prime(n + 1):
            return n + 1


def smooth_plus_prime(bits: int, B: int = 1 << 13) -> int:
    """A prime p where p+1 is B-smooth (vulnerable to Williams p+1)."""
    while True:
        n = _squarefree_smooth(bits, B)
        if is_probable_prime(n - 1):
            return n - 1


def run(namespace):
    """Run every demo_* in a module namespace, printing pass/fail."""
    demos = [(k, v) for k, v in sorted(namespace.items())
             if k.startswith("demo_") and callable(v)]
    print(f"\n=== {namespace['__file__'].split('/')[-1]} : {len(demos)} attacks ===")
    bad = 0
    for name, fn in demos:
        t = time.perf_counter()
        try:
            info = fn() or ""
            print(f"[ok]   {name[5:]:30} {time.perf_counter() - t:5.1f}s  {info}")
        except Exception as e:  # noqa: BLE001
            bad += 1
            print(f"[FAIL] {name[5:]:30} {time.perf_counter() - t:5.1f}s  {e!r}")
    if bad:
        print(f"\n{bad} FAILED")
        sys.exit(1)
