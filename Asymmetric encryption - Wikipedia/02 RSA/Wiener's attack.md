# Wiener's attack

Source: <https://en.wikipedia.org/wiki/Wiener%27s_attack>

**Wiener's attack**, named after cryptologist Michael J. Wiener, is a type of cryptographic attack against the RSA cryptosystem. The attack uses continued fraction representation to expose the private key $d$ when $d$ is small.

## Background on RSA

The RSA system is a public key cryptosystem, described as follows. Two large primes $p, q$ are chosen and the product $N = pq$, known as the modulus, is computed. The Euler totient of $N$ is calculated as $\varphi(N) = (p-1)(q-1)$. An integer $e$, called the public exponent, is chosen, and an integer $d$ satisfying $ed \equiv 1 \ (\text{mod }\varphi(N))$ is found by use of the Euclidean algorithm.

The public key consists of the pair $\langle N,e\rangle$, while the private key is the integer $d$. Encryption of a message, encoded as an integer $m$, is performed by taking $c \equiv m^e \ (\text{mod }N)$, while decryption of ciphertext $c$ is performed by taking $m \equiv c^d \ (\text{mod }N)$. The prime factorization of $N$ is also private and may be included in the private key for a more efficient decryption algorithm.

A possible attack on this system involves either directly finding $d$ given $N$, or factorizing $N$ first and then computing $d$ as before using the Euclidean algorithm. Note that it is possible to factorize $N$ with the knowledge of any one of $p, q$ or $\varphi(N)$.

## Small private key

For performance reasons, one might decide to use a small value of $d$ in order to speed up decryption. However, Wiener's attack shows that choosing a small value for $d$ will result in an insecure system in which an attacker can recover all secret information, i.e., break the RSA system. This break is based on Wiener's theorem, which holds for small values of $d$. Wiener has proved that the attacker may efficiently find $d$ when $d< \frac{1}{3}N^{1/4}$.

Wiener's paper also presented some countermeasures against his attack that allow fast decryption. Two techniques are described as follows.

**Choosing large public key**: Replace $e$ by $e'$, where $e' = e + k \varphi(N)$ for some large integer $k$. When $e'$ is large enough, for example $e' > N^{3/2}$, Wiener's attack cannot be applied regardless of how small $d$ is.

**Using the Chinese remainder theorem**: A more efficient decryption algorithm, known as CRT-RSA, may be performed by using the primes $p, q$ as the moduli during decryption instead of $N$.

Suppose one chooses $d$ such that both $d_p \equiv d \ (\text{mod }p-1)$ and $d_q \equiv d \ (\text{mod }q-1)$ are small but $d$ itself is not, then a fast decryption of the ciphertext $c$ is performed as follows:

1. First compute $m_p = c^{d_p} \ (\text{mod }p), m_q \equiv c^{d_q} \ (\text{mod }q)$.
2. Use the Chinese remainder theorem to compute the unique value of $0 \leq m < N$ that satisfies $m \equiv m_p \ (\text{mod }p)$ and $m \equiv m_q \ (\text{mod }q)$. The resulting $m$ satisfies $m \equiv c^d \ (\text{mod }N)$. The point is that Wiener's attack does not apply here because the value of $d\text{ mod }\varphi(N)$ can be large.

## How the attack works

Since $ed \equiv 1 \ (\text{mod }\varphi(N))$, there exists an integer $k$ such that
    $ed = k(p-1)(q-1)+1.$

Dividing by $Nd = pqd$ gives
    $\frac{e}{N} = \frac{k}{d} (1- \delta)$, where $\delta = \frac {p+q-1- \frac {1}{k}}{pq}$ is small.

Importantly, the fraction $e/N$ consists of public data and is approximated by the fraction $k/d$ consisting of private data. Wiener's attack exploits this fact by using the continued fraction expansion of $e/N$ to generate fractions close to $e/N$, known as convergents, and guessing $k$ and $d$ to be the numerator and denominator of these approximating fractions. Note that the continued fraction for a rational number appears as a byproduct of the Euclidean algorithm and may be computed quickly. When the denominator $d$ is small enough relative to $N$, the fraction $k/d$ is guaranteed to be one of these convergents.

The guess can be checked by using $k$ and $d$ to compute $\varphi(N) = (ed-1)/k$ and then checking if this guess for $\varphi(N)$ factorizes $N$ by solving the quadratic equation
    $x^2 - (N - \varphi(N)+1)x + N = 0.$

## Wiener's theorem

Let $N=pq$ with $q < p < 2q$, and let $d < \frac{1}{3}N^{1/4}$.

Given $\langle N,e\rangle$ with $ed \equiv 1 \ (\text{mod }\varphi(N))$, the attacker can efficiently recover $d$.

## Example

Suppose that the public keys are $\langle N, e \rangle = \langle 90581, 17993\rangle$. The attack should determine $d$. By using Wiener's theorem and continued fractions to approximate $d$, first we try to find the continued fractions expansion of $\frac{e}{N}$. Note that this algorithm finds fractions in their lowest terms. We know that
    $\frac{e}{N} = \frac{17993}{90581} = \cfrac{1}{5 + \cfrac{1}{29 +\dots + \cfrac{1}{3}}} = \left [0,5,29,4,1,3,2,4,3 \right ]$

According to the continued fractions expansion of $\frac{e}{N}$, all convergents $\frac{k}{d}$ are
    $\frac{k}{d} = 0, \frac{1}{5}, \frac{29}{146}, \frac{117}{589}, \frac{146}{735}, \frac{555}{2794}, \frac{1256}{6323}, \frac{5579}{28086}, \frac{17993}{90581}.$

We can verify that the first convergent does not produce a factorization of *N*. However, the convergent $\frac{1}{5}$ yields
    $\varphi (N) = \frac{ed - 1}{k} = \frac{17993\times5 - 1}{1} = 89964$

Now, if we solve the equation
    $x^2 - \left ( N - \varphi(N) + 1 \right )x + N = 0$
    $x^2 - 618x + 90581 = 0,$

then we find the roots which are $x=379;\ 239$. Therefore we have found the factorization
    $N = 90581 = 379 \times 239 = p \times q$.

Notice that, for the modulus $N = 90581$, Wiener's theorem will work if
    $d < \frac{1}{3}N^{1/4} \approx 5.7828$.

## Proof of Wiener's theorem

The proof is based on approximations using continued fractions.

Since $ed \equiv 1 \ (\text{mod }\varphi(N))$ there exists a $k$ such that $ed = k\varphi(N)+1$. Therefore
    $\left | \frac {e}{\varphi (N)}- \frac {k}{d} \right \vert = \left|\frac{ed - k\varphi(N)}{d\varphi(N)} \right| = \frac{1}{d \varphi (N)}$.

Hence, $k/d$ is an approximation of $e/\varphi(N)$. Although the attacker does not know $\varphi(N)$, they may use $N$ to approximate it.

To see this, note the hypothesis $q < p < 2q$ implies $N = pq > q^2$, and so
    $N-\varphi (N)= p+q-1 < 3q -1 < 3 \sqrt{N}$.

Also, $N - \varphi(N) > 0$ for $N > 1$.

The above estimate lets us approximate $ed = k\varphi(N) + 1$ by $kN+1$ (relative to $k$):
    $|ed - (kN+1)| = |(k\varphi(N) + 1)- (kN+1)| = |k(\varphi(N) - N)| < 3k\sqrt{N}$.

In fact, because $N - \varphi(N) \geq 1$, we can approximate $ed$ by $kN$ (relative to $k$):
    $|ed - kN| = |1 - k(N - \varphi(N))| = k(N - \varphi(N)) - 1 < k(N - \varphi(N)) < 3k \sqrt{N}$.

Therefore,
    $\begin{align} \left \vert \frac{e}{N}- \frac{k}{d} \right \vert &= \left \vert \frac{ed-kN}{Nd} \right \vert \\ &< \frac{3k \sqrt{N}}{Nd} = \frac {3k}{d \sqrt{N}} \end{align}$

Now, since $e < \varphi(N)$,
    $k = \frac{ed - 1}{\varphi(N)} < \frac{ed}{\varphi(N)} < d < \frac{1}{3}N^{1/4}.$

Therefore,
    $\left \vert \frac{e}{N}- \frac{k}{d} \right \vert < \frac{3k}{d\sqrt{N}} < \frac{1}{dN^{1/4}} < \frac{1}{2d^2}$

where the last inequality uses $2d < N^{1/4}$ from the assumption on $d$.

Now in general, if $|x - \frac{a}{b}| < \frac{1}{2b^2}$, then $\frac{a}{b}$ is a convergent of $x$, so $k/d$ appears among the convergents of $e/N$. We may guess $k$ and $d$ to be the numerator and denominator of these convergents respectively, and verify if they are correct by computing $\varphi(N)$ and attempting to factorize $N$ with these guesses. Eventually one such guess (of which there are $O(\log N)$ of them ) will be correct.

## Python implementation

The following is a minimal implementation of Wiener's attack in Python, given a vulnerable system with public key $\langle N, e\rangle$, based on an online implementation.

```
import math

# Convergents of num/den as fractions
def convergents(num, den):
# The Euclidean algorithm gives the denominators, then compute convergents
ni, di = (0, 1), (1, 0)
while den != 0:
div = num // den
num, den = den, num % den
ni = (ni[1], div * ni[1] + ni[0])
di = (di[1], div * di[1] + di[0])
yield (ni[1], di[1])

# Factorizes N when successful
def wiener(N, e):
for k_guess, d_guess in convergents(e, N):
if k_guess == 0:
continue
phi_guess = (e * d_guess - 1) // k_guess
# Solve the quadratic
coeff = N - phi_guess + 1
disc = coeff * coeff - 4 * N
if coeff <= 0 or coeff >= N + 1 or disc < 0:
continue
root_disc = math.isqrt(disc)
if root_disc * root_disc != disc:
continue
return ((coeff + root_disc) // 2, (coeff - root_disc) // 2)
return None

```
