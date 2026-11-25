# Pollard's p − 1 algorithm

Source: <https://en.wikipedia.org/wiki/Pollard%27s_p_%E2%88%92_1_algorithm>

**Pollard's *p* − 1 algorithm** is a number theoretic integer factorization algorithm, invented by John Pollard in 1974. It is a special-purpose algorithm, meaning that it is only suitable for integers with specific types of factors; it is the simplest example of an algebraic-group factorisation algorithm.

The factors it finds are ones for which the number preceding the factor, *p* − 1, is powersmooth; the essential observation is that, by working in the multiplicative group modulo a composite number *N*, we are also working in the multiplicative groups modulo all of *N'*s factors.

The existence of this algorithm leads to the concept of safe primes, being primes for which *p* − 1 is two times a Sophie Germain prime *q* and thus minimally smooth. These primes are sometimes construed as "safe for cryptographic purposes", but they might be *unsafe* — in current recommendations for cryptographic strong primes (*e.g.* ANSI X9.31), it is necessary but not sufficient that *p* − 1 has at least one large prime factor. Most sufficiently large primes are strong; if a prime used for cryptographic purposes turns out to be non-strong, it is much more likely to be through malice than through an accident of random number generation. This terminology is considered obsolete by the cryptography industry: the ECM factorization method is more efficient than Pollard's algorithm and finds safe prime factors just as quickly as it finds non-safe prime factors of similar size, thus the size of *p* is the key security parameter, not the smoothness of *p* − 1.

## Base concepts

Let *n* be a composite integer with prime factor *p*. By Fermat's little theorem, we know that for all integers *a* coprime to *p* and for all positive integers *K*:
    $a^{K(p-1)} \equiv 1\pmod{p}$

If a number *x* is congruent to 1 modulo a factor of *n*, then the gcd(*x* − 1, *n*) will be divisible by that factor.

The idea is to make the exponent a large multiple of *p* − 1 by making it a number with very many prime factors; generally, we take the product of all prime powers less than some limit *B*. Start with a random *x*, and repeatedly replace it by $x^w \bmod n$ as *w* runs through those prime powers. Check at each stage, or once at the end if you prefer, whether gcd(*x* − 1, *n*) is not equal to 1.

## Algorithm and running time

The basic algorithm can be written as follows:
**Inputs**: *n*: a (possibly) composite number
**Output**: a nontrivial factor of *n* or failure

1. select a smoothness bound *B* (not necessarily prime)
2. define $M = \prod_{\text{primes}~q \le B} q^{ \lfloor \log_q{B} \rfloor }$ (note: $M=\operatorname{lcm}(1,2,...,B)$ is the largest *B*-powersmooth number; explicitly evaluating *M* may not be necessary)
3. randomly pick a positive integer, *a*, which is coprime to *n* (note: we can actually fix *a*, e.g. if *n* is odd, then we can always select *a* = 2, random selection here is not imperative)
4. compute *g* = gcd(*a*^(*M*) − 1, *n*) (note: exponentiation can be done modulo *n*)
5. if 1 < *g* < *n* then return *g*
6. if *g* = 1 then select a larger *B* and go to step 2 or return failure
7. if *g* = *n* then select a smaller *B* and go to step 2 or return failure

If *g* = 1 in step 6, this indicates there are no prime factors *p* for which *p* − 1 is *B*-powersmooth. If *g* = *n* in step 7, this usually indicates that all factors were *B*-powersmooth, but in rare cases it could indicate that *a* had a small order modulo *n*. Additionally, when the maximum prime factors of *p* − 1 for each prime factors *p* of *n* are all the same in some rare cases, this algorithm will fail.

The running time of this algorithm is O(*B* × log *B* × log^2 *n*); larger values of *B* make it run slower, but are more likely to produce a factor.

### Example

If we want to factor the number *n* = 299.

1. We select *B* = 5.
2. Thus *M* = 2^2 × 3^1 × 5^1.
3. We select *a* = 2.
4. *g* = gcd(*a*^(*M*) − 1, *n*) = 13.
5. Since 1 < 13 < 299, thus return 13.
6. 299 / 13 = 23 is prime, thus it is fully factored: 299 = 13 × 23.

## Methods of choosing *B*

Since the algorithm is incremental, it is able to keep running with the bound constantly increasing.

Assume that *p* − 1, where *p* is the smallest prime factor of *n*, can be modelled as a random number of size less than √*n*. By the Dickman function, the probability that the largest factor of such a number is less than (*p* − 1)^(*1/ε*) is roughly *ε*^(−*ε*); so there is a probability of about 3^(−3) = 1/27 that a *B* value of *n*^(1/6) will yield a factorisation.

An improved method to estimate the probability of success given *B*_1, *B*_2 is found in Kruppa (2010).

In practice, the elliptic curve method is faster than the Pollard *p* − 1 method once the factors are at all large; running the *p* − 1 method up to *B* = 2^(32) will find a quarter of all 64-bit factors and 1/27 of all 96-bit factors.

## Two-stage variant

A variant of the basic algorithm is used in practice; instead of requiring that *p* − 1 has all its factors less than *B*, we require it to have all but one of its factors less than some *B*_1, and the remaining factor less than some *B*_2 ≫ *B*_1.

### Pollard's stage 2 and Montgomery's prime-pairing

After completing the first stage, which is the same as the basic algorithm, instead of computing a new
    $M' = \prod_{\text{primes }q \le B_2} q^{ \lfloor \log_q B_2 \rfloor }$

for *B*_2 and checking gcd(*a*^(*M'*) − 1, *n*), we compute
    $Q = \prod_{\text{primes } q \in (B_1, B_2]} (H^q - 1)$

where *H* = *a*^(*M*) and check if gcd(*Q*, *n*) produces a nontrivial factor of *n*. As before, exponentiations can be done modulo *n*.

Let {*q*_1, *q*_2, …} be successive prime numbers in the interval (*B*_1, *B*_2] and *d*_(*n*) = *q*_(*n*) − *q*_(*n*−1) the difference between consecutive prime numbers. Since typically *B*_1 > 2, *d*_(*n*) are even numbers. The distribution of prime numbers is such that the *d*_(*n*) will all be relatively small. It is suggested that *d*_(*n*) ≤ ln^2 *B*_2. Hence, the values of *H*^2, *H*^4, *H*^6, … (mod *n*) can be stored in a table, and *H*^(*q*_(*n*)) be computed from *H*^(*q*_(*n*−1))⋅*H*^(*d*_(*n*)), saving the need for exponentiations.

This above method is found in Pollard (1974). For each "outlying" prime *q* in the range, it requires two modular multiplications, the main time-cost in this algorithm. An improved method in Montgomery  (1978) implements "prime-pairing" and halves the number of modular multiplications required. Nevertheless, there remains a need to do O(π(*B*_2)−π(*B*_1)) operations modulo N, so O(*B*_2/log *B*_2) operations assuming *B*_2 is much larger than *B*_1.

There is also a Brent-Suyama extension that allows numbers beyond the two bounds to be retrieved and factored, improving the probability of finding factors. However, it is much more efficient (in terms of amount of computation required for a given probability of success) to instead use the polynomial stage 2 (below) with a larger *B*_2.

### Crandall's n^K stage 2

Richard Crandall describes a more efficient stage 2 in *Topics in Advanced Scientific Computation* (1996). The underlying idea is that for some carefully chosen fixed power *K*, one accumulates the power $c = \prod_{i,j} (H^{i^K} - H^{j^K})$ over unequal *i, j*. If there is a congruence $i^K=j^K \pmod q$ for the outlying prime *q*, then GCD(*c*, *n*) may produce the factor. Therefore it is beneficial to evaluate quickly numbers of the form $x^{n^K}$ for given *x* and *K*, with *n* = 1,2,3...

### Montgomery and Kruppa's polynomial stage 2

A more efficient continuation can be done using a polynomial multiplication implemented via fast Fourier transform, taking O(√*B*_2 log *B*_2) operations, which is much more efficient for large *B*_2. This new algorithm runs even faster if more memory is allocated for convolution: with convolution size increased by a factor of *n*, the memory usage as well as run time per convolution is increased by a factor of *n*, but the amount of advancement of *B*_2 in each step is increased by a factor of *n*^2.

Montgomery and Silverman also published an earlier polynomial evaluation scheme in 1990–1992.

## Implementations

- The GMP-ECM package includes an efficient implementation of the *p* − 1 method. It implements both prime-pairing and polynomial stage 2.
- Prime95 and MPrime, the official clients of the Great Internet Mersenne Prime Search, implements *p* − 1 for numbers of the form $(kb^n+c)/d$, though it mainly focuses on using *p* − 1 to prove Mersenne numbers composite. It implements both prime-pairing and polynomial stage 2.

## See also

- Williams's *p* + 1 algorithm
