# Integer factorization

Source: <https://en.wikipedia.org/wiki/Integer_factorization>

Unsolved problem in computer science Can integer factorization be solved in polynomial time on a classical computer? More unsolved problems in computer science

In mathematics, **integer factorization** is the decomposition of a positive integer into a product of integers. Every positive integer greater than 1 is either the product of two or more integer factors greater than 1, in which case it is a composite number, or it is not, in which case it is a prime number. For example, 15 is a composite number because 15 = 3 · 5, but 7 is a prime number because it cannot be decomposed in this way. If one of the factors is composite, it can in turn be written as a product of smaller factors, for example 60 = 3 · 20 = 3 · (5 · 4). Continuing this process until every factor is prime is called **prime factorization**; the result is always unique up to the order of the factors by the prime factorization theorem.

To factorize a small integer n using mental or pen-and-paper arithmetic, the simplest method is trial division: checking if the number is divisible by prime numbers 2, 3, 5, and so on, up to the square root of n. For larger numbers, especially when using a computer, various more sophisticated factorization algorithms are more efficient. A prime factorization algorithm typically involves testing whether each factor is prime each time a factor is found.

When the numbers are sufficiently large, no efficient non-quantum integer factorization algorithm is known. However, it has not been proven that such an algorithm does not exist. The presumed difficulty of this problem is important for the algorithms used in cryptography such as RSA public-key encryption and the RSA digital signature. Many areas of mathematics and computer science have been brought to bear on this problem, including elliptic curves, algebraic number theory, and quantum computing.

Not all numbers of a given length are equally hard to factor. The hardest instances of these problems (for currently known techniques) are semiprimes, the product of two prime numbers. When they are both large, for instance more than two thousand bits long, randomly chosen, and about the same size (but not too close, for example, to avoid efficient factorization by Fermat's factorization method), even the fastest prime factorization algorithms on the fastest classical computers can take enough time to make the search impractical; that is, as the number of digits of the integer being factored increases, the number of operations required to perform the factorization on any classical computer increases drastically.

Many cryptographic protocols are based on the presumed difficulty of factoring large composite integers or a related problem – for example, the RSA problem. An algorithm that efficiently factors an arbitrary integer would render RSA-based public-key cryptography insecure.

## Prime decomposition

By the fundamental theorem of arithmetic, every positive integer has a unique prime factorization. (By convention, 1 is the empty product.) Testing whether the integer is prime can be done in polynomial time, for example, by the AKS primality test. If composite, however, the polynomial time tests give no insight into how to obtain the factors.

Given a general algorithm for integer factorization, any integer can be factored into its constituent prime factors by repeated application of this algorithm. The situation is more complicated with special-purpose factorization algorithms, whose benefits may not be realized as well or even at all with the factors produced during decomposition. For example, if *n* = 171 × *p* × *q* where *p* < *q* are very large primes, trial division will quickly produce the factors 3 and 19 but will take *p* divisions to find the next factor. As a contrasting example, if *n* is the product of the primes 13729, 1372933, and 18848997161, where 13729 × 1372933 = 18848997157, Fermat's factorization method will begin with ⌈√*n*⌉ = 18848997159 which immediately yields *b* = √*a*^2 − *n* = √4 = 2 and hence the factors *a* − *b* = 18848997157 and *a* + *b* = 18848997161. While these are easily recognized as composite and prime respectively, Fermat's method will take much longer to factor the composite number because the starting value of ⌈√18848997157⌉ = 137292 for *a* is a factor of 10 from 1372933.

## Current state of the art

Among the *b*-bit numbers, the most difficult to factor in practice using existing algorithms are those semiprimes whose factors are of similar size. For this reason, these are the integers used in cryptographic applications.

In 2019, a 240-digit (795-bit) number (RSA-240) was factored by a team of researchers including Paul Zimmermann, utilizing approximately 900 core-years of computing power. These researchers estimated that a 1024-bit RSA modulus would take about 500 times as long.

The largest such semiprime yet factored was RSA-260, an 862-bit number with 260 decimal digits, in September 2026. The total computation time was roughly 4,900 GPU-days using a GPU-accelerated implementation of the general number field sieve. Like all recent factorization records, this factorization was completed with a highly optimized implementation of the general number field sieve run on hundreds of machines.

### Time complexity

No algorithm has been published that can factor all integers in polynomial time, that is, that can factor a *b*-bit number *n* in time O(*b*^(*k*)) for some constant *k*. Neither the existence nor non-existence of such algorithms has been proved, but it is generally suspected that they do not exist.

There are published algorithms that are faster than O((1 + *ε*)^(*b*)) for all positive *ε*, that is, sub-exponential. As of 2022, the algorithm with best theoretical asymptotic running time is the general number field sieve (GNFS), first published in 1993, running on a *b*-bit number *n* in time

$$ \exp\left( \left(\left(\tfrac83\right)^\frac23 + o(1)\right)\left(\log n\right)^\frac13\left(\log \log n\right)^\frac23\right). $$

For current computers, GNFS is the best published algorithm for large *n* (more than about 400 bits). For a quantum computer, however, Peter Shor discovered an algorithm in 1994 that solves it in polynomial time. Shor's algorithm takes only O(*b*^3) time and O(*b*) space on *b*-bit number inputs. In 2001, Shor's algorithm was implemented for the first time, by using NMR techniques on molecules that provide seven qubits.

In order to talk about complexity classes such as P, NP, and co-NP, the problem has to be stated as a decision problem.

**Decision problem** (Integer factorization)—For every natural numbers $n$ and $k$, does *n* have a factor smaller than *k* besides 1?

It is known to be in both NP and co-NP, meaning that both "yes" and "no" answers can be verified in polynomial time. An answer of "yes" can be certified by exhibiting a factorization *n* = *d*(*n*/*d*) with *d* ≤ *k*. An answer of "no" can be certified by exhibiting the factorization of *n* into distinct primes, all larger than *k*; one can verify their primality using the AKS primality test, and then multiply them to obtain *n*. The fundamental theorem of arithmetic guarantees that there is only one possible string of increasing primes that will be accepted, which shows that the problem is in both UP and co-UP. It is known to be in BQP because of Shor's algorithm.

The problem is suspected to be outside all three of the complexity classes P, NP-complete, and co-NP-complete. It is therefore a candidate for the NP-intermediate complexity class.

In contrast, the decision problem "Is *n* a composite number?" (or equivalently: "Is *n* a prime number?") appears to be much easier than the problem of specifying factors of *n*. The composite/prime problem can be solved in polynomial time (in the number *b* of digits of *n*) with the AKS primality test. In addition, there are several probabilistic algorithms that can test primality very quickly in practice if one is willing to accept a vanishingly small possibility of error. The ease of primality testing is a crucial part of the RSA algorithm, as it is necessary to find large prime numbers to start with.

## Factoring algorithms

### Special-purpose

A special-purpose factoring algorithm's running time depends on the properties of the number to be factored or on one of its unknown factors: size, special form, etc. The parameters which determine the running time vary among algorithms.

An important subclass of special-purpose factoring algorithms is the *Category 1* or *First Category* algorithms, whose running time depends on the size of smallest prime factor. Given an integer of unknown form, these methods are usually applied before general-purpose methods to remove small factors. For example, naive trial division is a Category 1 algorithm.

- Trial division (TD)
- Wheel factorization
- Pollard's rho algorithm, which has two common flavors to identify group cycles: one by Floyd and one by Brent.
- Algebraic-group factorization algorithms, among which are Pollard's *p* − 1 algorithm, Williams's *p* + 1 algorithm, and Lenstra elliptic curve factorization (ECM)
- Fermat's factorization method
- Euler's factorization method
- Special number field sieve (SNFS)
- Algebraic factorization (which includes difference of two squares, sum of two cubes, Aurifeuillean factorization, etc.)

### General-purpose

A general-purpose factoring algorithm, also known as a *Category 2*, *Second Category*, or *Kraitchik* *family* algorithm, has a running time which depends solely on the size of the integer to be factored. This is the type of algorithm used to factor RSA numbers. Most general-purpose factoring algorithms are based on the congruence of squares method.

- Dixon's factorization method
- Continued fraction factorization (CFRAC)
- Quadratic sieve (QS)
- Rational sieve
- General number field sieve (GNFS)
- Shanks's square forms factorization (SQUFOF)

### Other notable algorithms

- Shor's algorithm, for quantum computers

## Heuristic running time

In number theory, there are many integer factoring algorithms that heuristically have expected running time

$$ L_n\left[\tfrac12,1+o(1)\right]=e^{(1+o(1))\sqrt{(\log n)(\log \log n)}} $$

in little-o and L-notation. Some examples of those algorithms are the elliptic curve method and the quadratic sieve. Another such algorithm is the **class group relations method** proposed by Schnorr, Seysen, and Lenstra, which they proved while assuming the unproved generalized Riemann hypothesis.

## Rigorous running time

The Schnorr–Seysen–Lenstra probabilistic algorithm has been rigorously proven by Lenstra and Pomerance to have expected running time *L_n*[1/2, 1+*o*(1)] by replacing the GRH assumption with the use of multipliers. The algorithm uses the class group of positive binary quadratic forms of discriminant Δ denoted by *G*_Δ. *G*_Δ is the set of triples of integers (*a*, *b*, *c*) in which those integers are relative prime.

### Schnorr–Seysen–Lenstra algorithm

Given an integer n that will be factored, where n is an odd positive integer greater than a certain constant. In this factoring algorithm the discriminant Δ is chosen as a multiple of n, Δ = −*dn*, where d is some positive multiplier. The algorithm expects that for one d there exist enough smooth forms in *G*_Δ. Lenstra and Pomerance show that the choice of d can be restricted to a small set to guarantee the smoothness result.

Denote by *P*_Δ the set of all primes q with Kronecker symbol (Δ/*q*) = 1. By constructing a set of generators of *G*_Δ and prime forms *f*_(*q*) of *G*_Δ with q in *P*_Δ a sequence of relations between the set of generators and *f*_(*q*) are produced. The size of q can be bounded by *c*_0(log|Δ|)^2 for some constant *c*_0.

The relation that will be used is a relation between the product of powers that is equal to the neutral element of *G*_Δ. These relations will be used to construct a so-called ambiguous form of *G*_Δ, which is an element of *G*_Δ of order dividing 2. By calculating the corresponding factorization of Δ and by taking a gcd, this ambiguous form provides the complete prime factorization of n. This algorithm has these main steps:

Let n be the number to be factored.

1. Let Δ be a negative integer with Δ = −*dn*, where d is a multiplier and Δ is the negative discriminant of some quadratic form.
2. Take the t first primes *p*_1 = 2, *p*_2 = 3, *p*_3 = 5, ..., *p*_(*t*), for some *t* ∈ **N**.
3. Let *f*_(*q*) be a random prime form of *G*_Δ with (Δ/*q*) = 1.
4. Find a generating set X of *G*_Δ.
5. Collect a sequence of relations between set X and {*f*_(*q*) : *q* ∈ *P*_Δ} satisfying

$$ \left(\prod_{x \in X_{}} x^{r(x)}\right).\left(\prod_{q \in P_\Delta} f^{t(q)}_{q}\right) = 1. $$

6. Construct an ambiguous form (*a*, *b*, *c*) that is an element *f* ∈ *G*_Δ of order dividing 2 to obtain a coprime factorization of the largest odd divisor of Δ in which Δ = −4*ac* or Δ = *a*(*a* − 4*c*) or Δ = (*b* − 2*a*)(*b* + 2*a*).
7. If the ambiguous form provides a factorization of n then stop, otherwise find another ambiguous form until the factorization of n is found. In order to prevent useless ambiguous forms from generating, build up the 2-Sylow group Sll_2(Δ) of *G*(Δ).

To obtain an algorithm for factoring any positive integer, it is necessary to add a few steps to this algorithm such as trial division, and the Jacobi sum test.

### Expected running time

The algorithm as stated is a probabilistic algorithm as it makes random choices. Its expected running time is at most *L_n*[1/2, 1+*o*(1)].

## See also

- Algebraic factorization
- Aurifeuillean factorization
- Bach's algorithm – For generation of random factorized numbers
- Canonical representation of a positive integer
- Factorization
- Multiplicative partition – Way to write a number as a product of other numbers
- p-adic valuation
- Integer partition – Decomposition of an integer as a sum of positive integers
- Jevon's number
