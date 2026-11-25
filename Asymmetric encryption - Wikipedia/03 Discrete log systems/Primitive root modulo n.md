# Primitive root modulo n

Source: <https://en.wikipedia.org/wiki/Primitive_root_modulo_n>

In number theory, a number g is a **primitive root modulo n** if every number a coprime to n is congruent to a power of g modulo n. In symbols, g is a primitive root modulo n if for every integer a coprime to n, there is some integer k for which *g*^(*k*) ≡ *a* (mod *n*).

Primitive roots only exist for some integers n. Specifically, a primitive root exists modulo n if and only if n is 4, *p*^(*k*) or 2*p*^(*k*) for some odd prime number p and some *k* ≥ 0. This was first proved by Carl Friedrich Gauss. Gauss defined primitive roots in Article 57 of his *Disquisitiones Arithmeticae* (1801), where he credited Leonhard Euler with coining the term. In Article 56 he stated that Johann Heinrich Lambert and Euler knew of them, but he was the first to rigorously demonstrate that primitive roots exist for a prime number n. In fact, the *Disquisitiones* contains two proofs: The one in Article 54 is a nonconstructive existence proof, while the proof in Article 55 is constructive.

An equivalent characterization is that g is a primitive root modulo n if and only if g is a generator of the multiplicative group of integers modulo n. Thus, primitive roots exist if and only if this group is a cyclic group.

If g is a primitive root modulo n and *g*^(*k*) ≡ *a* (mod *n*), then the value k is called the *index* or *discrete logarithm* of a to the base g modulo n.

## Elementary example

The number 3 is a primitive root modulo 7 because

$$ \begin{array}{rcrcrcrcrcr} 3^1 &=& 3^0 \times 3 &\equiv& 1 \times 3 &=& 3 &\equiv& 3 \pmod 7 \\ 3^2 &=& 3^1 \times 3 &\equiv& 3 \times 3 &=& 9 &\equiv& 2 \pmod 7 \\ 3^3 &=& 3^2 \times 3 &\equiv& 2 \times 3 &=& 6 &\equiv& 6 \pmod 7 \\ 3^4 &=& 3^3 \times 3 &\equiv& 6 \times 3 &=& 18 &\equiv& 4 \pmod 7 \\ 3^5 &=& 3^4 \times 3 &\equiv& 4 \times 3 &=& 12 &\equiv& 5 \pmod 7 \\ 3^6 &=& 3^5 \times 3 &\equiv& 5 \times 3 &=& 15 &\equiv& 1 \pmod 7 \end{array} $$

The remainders 3, 2, 6, 4, 5, 1 include each congruence class relatively prime to 7. Higher powers repeat the same pattern periodically.

The number of congruence classes relatively prime to the modulus n is given by Euler's totient function φ applied to n. In this case, that is *φ*(7) = 6. For a prime modulus n, this period is always equal to *n* − 1, but this is not true for composite n.

## Definition

If n is a positive integer, the integers from 1 to n − 1 that are coprime to n (or equivalently, the congruence classes coprime to n) form a group, with multiplication modulo n as the operation; it is denoted by $\mathbb{Z}_n^\times$, and is called the group of units modulo n, or the group of primitive classes modulo n. As explained in the article multiplicative group of integers modulo n, this multiplicative group $\mathbb{Z}_n^\times$ is cyclic if and only if n is equal to 2, 4, p^k, or 2*p^k* where p^k is a power of an odd prime number. When (and only when) this group $\mathbb{Z}_n^\times$ is cyclic, a generator of this cyclic group is called a *primitive root modulo* n (or in fuller language *primitive root of unity modulo n*, emphasizing its role as a fundamental solution of the **roots of unity** polynomial equations X^m
_() − 1 in the ring $\mathbb{Z}_n$), or simply a **primitive element of** $\mathbb{Z}_n^\times$.

When $\mathbb{Z}_n^\times$ is non-cyclic, such primitive elements mod n do not exist. Instead, each prime component of n has its own sub-primitive roots (see 15 in the examples below).

For any n (whether or not $\mathbb{Z}_n^\times$ is cyclic), the order of $\mathbb{Z}_n^\times$ is given by Euler's totient function φ(n) (sequence A000010 in the OEIS). And then, Euler's theorem says that a^(φ(n)) ≡ 1 (mod n) for every a coprime to n; the lowest power of a that is congruent to 1 modulo n is called the multiplicative order of a modulo n. In particular, for a to be a primitive root modulo n, φ(n) has to be the smallest power of a satisfying a^x ≡ 1 (mod n) .

## Examples

For example, if n = 14 then the elements of $\mathbb{Z}$^(×)
_n are the congruence classes {1, 3, 5, 9, 11, 13}; there are φ(14) = 6 of them. Here is a table of their powers modulo 14:

```
x     x, x^2, x^3, ... (mod 14)
 1 :   1
 3 :   3,  9, 13, 11,  5,  1
 5 :   5, 11, 13,  9,  3,  1
 9 :   9, 11,  1
11 :  11,  9,  1
13 :  13,  1
```

The order of 1 is 1, the orders of 3 and 5 are 6, the orders of 9 and 11 are 3, and the order of 13 is 2. Thus, 3 and 5 are the primitive roots modulo 14.

For a second example let n = 15 . The elements of $\mathbb{Z}$^(×)
_(15) are the congruence classes {1, 2, 4, 7, 8, 11, 13, 14}; there are φ(15) = 8 of them.

```
x     x, x^2, x^3, ... (mod 15)
 1 :   1
 2 :   2,  4,  8, 1
 4 :   4,  1
 7 :   7,  4, 13, 1
 8 :   8,  4,  2, 1
11 :  11,  1
13 :  13,  4,  7, 1
14 :  14,  1
```

Since there is no number whose order is 8, there are no primitive roots modulo 15. Indeed, λ(15) = 4, where λ is the Carmichael function. (sequence A002322 in the OEIS)

## Table of primitive roots

Numbers $n$ that have a primitive root are of the form
    $n \in \{1, 2, 4, p^k, 2 \cdot p^k \; \; | \; \; 2 < p \text{ prime}; \; k \in \mathbb{N}\} ,$
= {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 17, 18, 19, ...}.

These are the numbers $n$ with $\varphi(n) = \lambda(n),$ kept also in the sequence A033948 in the OEIS.

The following table lists the primitive roots modulo n up to $n=31$:

| $n$ |  primitive roots modulo $n$ |  order $\varphi(n),$
((sequence A000010 in the OEIS)) |  exponent $\lambda(n),$
((sequence A002322 in the OEIS)) |
|  1 | 0 | 1 | 1 |
|  2 | 1 | 1 | 1 |
|  3 | 2 | 2 | 2 |
|  4 | 3 | 2 | 2 |
|  5 | 2, 3 | 4 | 4 |
|  6 | 5 | 2 | 2 |
|  7 | 3, 5 | 6 | 6 |
|  8 |  | 4 | 2 |
|  9 | 2, 5 | 6 | 6 |
|  10 | 3, 7 | 4 | 4 |
|  11 | 2, 6, 7, 8 | 10 | 10 |
|  12 |  | 4 | 2 |
|  13 | 2, 6, 7, 11 | 12 | 12 |
|  14 | 3, 5 | 6 | 6 |
|  15 |  | 8 | 4 |
|  16 |  | 8 | 4 |
|  17 | 3, 5, 6, 7, 10, 11, 12, 14 | 16 | 16 |
|  18 | 5, 11 | 6 | 6 |
|  19 | 2, 3, 10, 13, 14, 15 | 18 | 18 |
|  20 |  | 8 | 4 |
|  21 |  | 12 | 6 |
|  22 | 7, 13, 17, 19 | 10 | 10 |
|  23 | 5, 7, 10, 11, 14, 15, 17, 19, 20, 21 | 22 | 22 |
|  24 |  | 8 | 2 |
|  25 | 2, 3, 8, 12, 13, 17, 22, 23 | 20 | 20 |
|  26 | 7, 11, 15, 19 | 12 | 12 |
|  27 | 2, 5, 11, 14, 20, 23 | 18 | 18 |
|  28 |  | 12 | 6 |
|  29 | 2, 3, 8, 10, 11, 14, 15, 18, 19, 21, 26, 27 | 28 | 28 |
|  30 |  | 8 | 4 |
|  31 | 3, 11, 12, 13, 17, 21, 22, 24 | 30 | 30 |

## Properties

Gauss proved that for any prime number p (with the sole exception of p = 3), the product of its primitive roots is congruent to 1 modulo p.

He also proved that for any prime number p, the sum of its primitive roots is congruent to μ(p − 1) modulo p, where μ is the Möbius function.

For example,

|  p = 3, | μ(2) = −1. | The primitive root is 2. |
|  p = 5, | μ(4) = 0. | The primitive roots are 2 and 3. |
|  p = 7, | μ(6) = 1. | The primitive roots are 3 and 5. |
|  p = 31, | μ(30) = −1. | The primitive roots are 3, 11, 12, 13, 17, 21, 22 and 24. |

E.g., the product of the latter primitive roots is $2^6\cdot 3^4\cdot 7\cdot 11^2\cdot 13\cdot 17 = 970377408 \equiv 1 \pmod{31}$, and their sum is $123 \equiv -1 \equiv \mu(31-1) \pmod{31}$.

If $a$ is a primitive root modulo the prime $p$, then $a^\frac{p-1}{2}\equiv -1 \pmod p$.

Artin's conjecture on primitive roots states that a given integer a that is neither a perfect square nor −1 is a primitive root modulo infinitely many primes.

## Finding primitive roots

No simple general formula to compute primitive roots modulo n is known. There are however methods to locate a primitive root that are faster than simply trying out all candidates. If the multiplicative order (its exponent) of a number m modulo n is equal to $\varphi(n)$ (the order of $\mathbb{Z}$^(×)
_n), then it is a primitive root. In fact the converse is true: If m is a primitive root modulo n, then the multiplicative order of m is $\varphi(n) = \lambda(n)~.$ We can use this to test a candidate m to see if it is primitive.

For $n > 1$ first, compute $\varphi(n)~.$ Then determine the different prime factors of $\varphi(n)$, say p_1, ..., p_k. Finally, compute
    $g^{\varphi(n)/p_i}\bmod n \qquad\mbox{ for } i=1,\ldots,k$

using a fast algorithm for modular exponentiation such as exponentiation by squaring. A number g for which these k results are all different from 1 is a primitive root.

The number of primitive roots modulo n, if there are any, is equal to
    $\varphi\left(\varphi(n)\right)$

since, in general, a cyclic group with r elements has $\varphi(r)$ generators.

For prime n, this equals $\varphi(n-1)$, and since $n / \varphi(n-1) \in O(\log\log n)$ the generators are very common among {2, ..., n−1} and thus it is relatively easy to find one.

If g is a primitive root modulo p, then g is also a primitive root modulo all powers p^k unless g^(p−1) ≡ 1 (mod p^2); in that case, g + p is.

If g is a primitive root modulo p^k, then g is also a primitive root modulo all smaller powers of p.

If g is a primitive root modulo p^k, then either g or g + p^k (whichever one is odd) is a primitive root modulo 2p^k.

Finding primitive roots modulo p is also equivalent to finding the roots of the (p − 1)st cyclotomic polynomial modulo p.

## Order of magnitude of primitive roots

The least primitive root g_p modulo p (in the range 1, 2, ..., p − 1) is generally small.

### Upper bounds

Burgess (1962) proved that for every *ε* > 0 there is a C such that $g_p \leq C\,p^{\frac{1}{4}+\varepsilon}.$

Grosswald (1981) proved that if $p > e^{e^{24}} \approx 10^{11504079571}$, then $g_p < p^{0.499}.$

Shoup (1990, 1992) proved, assuming the generalized Riemann hypothesis, that g_p = O(log^6 p).

### Lower bounds

Fridlander (1949) and Salié (1950) proved that there is a positive constant C such that for infinitely many primes g_p > C log p.

It can be proved in an elementary manner that for any positive integer M there are infinitely many primes such that M < g_p < p − M.

## Applications

A primitive root modulo n is often used in pseudorandom number generators and cryptography, including the Diffie–Hellman key exchange scheme. Sound diffusers have been based on number-theoretic concepts such as primitive roots and quadratic residues.

## See also

- Artin's conjecture on primitive roots
- Dirichlet character
- Full reptend prime
- Multiplicative order
- Quadratic residue
- Root of unity modulo n
- Welch–Costas array
- Gauss's generalization of Wilson's theorem
