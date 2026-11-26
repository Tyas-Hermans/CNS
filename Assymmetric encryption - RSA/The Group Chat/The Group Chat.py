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
c1 = 1148176102467930159856714719821330971449602527964126426770344293712866719611027934580388248910690062744474773139786182084511607713966499366265508001141309234043702051769340910511513570512371901969864293
c2 = 1148176102467930159856714719821330971449602527964126426770344293712866719611027934580388248910690062744474773139786182084511607713966499366265508001141309234043702051769340910511513570512371901969864293
c3 = 1148176102467930159856714719821330971449602527964126426770344293712866719611027934580388248910690062744474773139786182084511607713966499366265508001141309234043702051769340910511513570512371901969864293

#--- KEY 1 ---
n1 = 83070775017400312771924958652523550174876970032198824894485803990647401326585645419168010276752754281220521091737241531623587366614877536741795974783883608947001667394720201384646684654209380451903193093145030177252481951786407944077748350388257188686591610624482542959686201501255221078521538009830962618753
e = 3

#--- KEY 2 ---
n2 = 150281049452833163414676521365443769534455880917643097125467205272749283575397502132863296737671457109187189280454100313560318164728893957751223512692402291792323386675113985678324707971053577149714912827633977748863015476137652321053272742506434168409775625868658936959522748452272869276834462936165344214919
e = 3

#--- KEY 3 ---
n3 = 142793526151862431310863906542217659425794538950981572220028937673486533383057457140011539163560175713697971765243495540422602160407278278703849242289259417644426609582853106553025365180014326710780218382841842232920966129203055420461028783405765818154164441559622923542133125850962571489621615236301580233409
e = 3
def crt(remainders, moduli):
    N = math.prod(moduli)
    x = 0
    for c, n in zip(remainders, moduli):
        Ni = N // n
        x += c * Ni * pow(Ni, -1, n)
    return x % N


def solve():
    # Hastad's broadcast attack: , e=3, three different moduli.
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
