"""
C_1 = M³ mod n_1
C_2 = M³ mod n_2
C_3 = M³ mod n_3
trying to find M
example:
n_1 = 55
n_2 = 77
n_3 = 91
M =13
C_1 = 52
C_2 = 41
C_3 = 13
"""
import math

from sympy import integer_nthroot
c1 = 4850370392558546246514347977200533994365629758026446799011726901926708724622211014226334371049610550361890519867189929979584471402256962154336291435115051
c2 = 925617903172905686269738952522261745702184896278505458752644606331005606645434745821220926157589689810610208801632143105341568799172893809891456144217115
c3 = 2994423788477786683957292040074194773241360803967764595369415279413166689378856118141236282313151996675193996235975547015423084485479505234160311764632711


#--- KEY 1 ---
n1 = 6601514513649518920279892901564780522279009526315196379648408183598423266464743370237155844444550168426968544125632903695330764069391957257462703561896377
e = 3

#--- KEY 2 ---
n2 = 4758647878178723152629896429350683984908320113752214897868471446510112022142441754789895950762103788607490506293471670252683896806829881757270373888385173
e = 3

#--- KEY 3 ---
n3 = 6213681056262749062269306419456728479083164147822700073811694198951746102333940461427250166224159413319657684140862766752983555691560924447981288319056509
e = 3
def crt(remainders, moduli):
    N = math.prod(moduli)
    x = 0
    for c, n in zip(remainders, moduli):
        Ni = N // n
        x += c * Ni * pow(Ni, -1, n)
    return x % N


def solve():
    # Hastad's broadcast attack: same M, e=3, three different moduli.
    # CRT gives X = M^3 mod n1*n2*n3, and since M^3 < n1*n2*n3, X == M^3 exactly.
    X = crt([c1, c2, c3], [n1, n2, n3])
    M, exact = integer_nthroot(X, 3)
    assert exact, "cube root not exact"
    print(M)
    print(M.to_bytes((M.bit_length() + 7) // 8, "big"))

def solve2():
    X,exact = integer_nthroot(c1,3)
    print(X.to_bytes((X.bit_length() + 7) // 8))

def to_text(m):
    return m.to_bytes((m.bit_length() + 7) // 8, "big")


def shared_factor_attack(cs, ns, e):
    """Side case: two moduli share a prime -> gcd factors them -> real RSA decryption.
    Gives M mod n for that key (only the full M if M < n)."""
    for i in range(len(ns)):
        for j in range(i + 1, len(ns)):
            p = math.gcd(ns[i], ns[j])
            if p == 1:
                continue
            for k in (i, j):               # either key of the pair is now factored
                q = ns[k] // p
                if q == 1:
                    continue
                try:
                    d = pow(e, -1, (p - 1) * (q - 1))
                except ValueError:         # e not invertible for this key, try the other
                    continue
                return pow(cs[k], d, ns[k])
    return None


def coprime_subset(cs, ns):
    """CRT needs pairwise coprime moduli: drop any modulus sharing a factor with one we kept."""
    keep_c, keep_n = [], []
    for c, n in zip(cs, ns):
        if all(math.gcd(n, m) == 1 for m in keep_n):
            keep_c.append(c)
            keep_n.append(n)
    return keep_c, keep_n


def hastad(cs, ns, e=3, max_k=100_000):
    """General Hastad broadcast attack.
    Works for any e, any number of ciphertexts, and when M^e wraps around N a few times."""
    # moduli must be pairwise coprime for CRT; if not, that's an even easier break
    m = shared_factor_attack(cs, ns, e)
    if m is not None:
        return m

    cs, ns = coprime_subset(cs, ns)
    N = math.prod(ns)
    X = crt(cs, ns)                        # X = M^e mod N
    # M^e = X + k*N for some k >= 0; k = 0 is the normal case
    for k in range(max_k):
        M, exact = integer_nthroot(X + k * N, e)
        if exact:
            return M
    raise ValueError(f"no exact {e}-th root for k < {max_k}: need more ciphertexts")


def solve3():
    M = hastad([c1, c2, c3], [n1, n2, n3], e)
    print(M)
    print(to_text(M))


if __name__ == "__main__":
    solve3()
