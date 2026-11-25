# Quadratic residue

Source: <https://en.wikipedia.org/wiki/Quadratic_residue>

In number theory, an integer q is a **quadratic residue** modulo n if it is congruent to a perfect square modulo n; that is, if there exists an integer x such that

$$ x^2\equiv q \pmod{n}. $$

Otherwise, q is a **quadratic nonresidue** modulo n.

Quadratic residues are used in applications ranging from acoustical engineering to cryptography and the factoring of large numbers.

## History, conventions, and elementary facts

Fermat, Euler, Lagrange, Legendre, and other number theorists of the 17th and 18th centuries established theorems and formed conjectures about quadratic residues, but the first systematic treatment is § IV of Gauss's *Disquisitiones Arithmeticae* (1801). Article 95 introduces the terminology "quadratic residue" and "quadratic nonresidue", and says that if the context makes it clear, the adjective "quadratic" may be dropped.

For a given n, a list of the quadratic residues modulo n may be obtained by simply squaring all the numbers 0, 1, ..., *n* − 1. Since *a* ≡ *b* (mod *n*) implies *a*^2 ≡ *b*^2 (mod *n*), any other quadratic residue is congruent (mod n) to some in the obtained list. But the obtained list is not composed of mutually incongruent quadratic residues (mod n) only. Since *a*^2 ≡ (*n*−*a*)^2 (mod *n*), the list obtained by squaring all numbers in the list 1, 2, ..., *n* − 1 (or in the list 0, 1, ..., n) is symmetric (mod n) around its midpoint, hence it is actually only needed to square all the numbers in the list $0, 1, ..., \lfloor n/2 \rfloor$. The list so obtained may still contain mutually congruent numbers (mod n). Thus, the number of mutually noncongruent quadratic residues modulo n cannot exceed *n*/2 + 1 (n even) or (*n* + 1)/2 (n odd).

The product of two residues is always a residue.

### Prime modulus

Modulo an odd prime number p there are (*p* + 1)/2 residues (including 0) and (*p* − 1)/2 nonresidues, by Euler's criterion. In this case, it is customary to consider 0 as a special case and work within the multiplicative group of nonzero elements of the field $(\mathbb{Z}/p\mathbb{Z})$. In other words, every congruence class except zero modulo p has a multiplicative inverse. This is not true for composite moduli.

Following this convention, the multiplicative inverse of a residue is a residue, and the inverse of a nonresidue is a nonresidue.

Following this convention, modulo an odd prime number there is an equal number of residues and nonresidues.

Modulo a prime, the product of two nonresidues is a residue and the product of a nonresidue and a (nonzero) residue is a nonresidue.

The first supplement to the law of quadratic reciprocity is that if *p* ≡ 1 (mod 4) then −1 is a quadratic residue modulo p, and if *p* ≡ 3 (mod 4) then −1 is a nonresidue modulo p. This implies the following:

If *p* ≡ 1 (mod 4) the negative of a residue modulo p is a residue and the negative of a nonresidue is a nonresidue.

If *p* ≡ 3 (mod 4) the negative of a residue modulo p is a nonresidue and the negative of a nonresidue is a residue.

### Prime power modulus

All odd squares are ≡ 1 (mod 8) and thus also ≡ 1 (mod 4). If a is an odd number and *m* = 8, 16, or some higher power of 2, then a is a residue modulo m if and only if *a* ≡ 1 (mod 8).

For example, mod (32) the odd squares are

- 1^2 ≡ 15^2 ≡ 1
- 3^2 ≡ 13^2 ≡ 9
- 5^2 ≡ 11^2 ≡ 25
- 7^2 ≡ 9^2 ≡ 49 ≡ 17

and the even ones are

- 0^2 ≡ 8^2 ≡ 16^2 ≡ 0
- 2^2 ≡ 6^2≡ 10^2 ≡ 14^2≡ 4
- 4^2 ≡ 12^2 ≡ 16.

So a nonzero number is a residue mod 8, 16, etc., if and only if it is of the form 4^(*k*)(8*n* + 1).

A number a relatively prime to an odd prime p is a residue modulo any power of p if and only if it is a residue modulo p.

If the modulus is *p*^(*n*), then *p*^(*k*)*a*

- is a residue modulo *p*^(*n*) if *k* ≥ *n*
- is a nonresidue modulo *p*^(*n*) if *k* < *n* is odd
- is a residue modulo *p*^(*n*) if *k* < *n* is even and a is a residue
- is a nonresidue modulo *p*^(*n*) if *k* < *n* is even and a is a nonresidue.

Notice that the rules are different for powers of two and powers of odd primes.

Modulo an odd prime power *n* = *p*^(*k*), the products of residues and nonresidues relatively prime to p obey the same rules as they do mod p; p is a nonresidue, and in general all the residues and nonresidues obey the same rules, except that the products will be zero if the power of p in the product ≥ *n*.

Modulo 8, the product of the nonresidues 3 and 5 is the nonresidue 7, and likewise for permutations of 3, 5 and 7. In fact, the multiplicative group of the non-residues and 1 form the Klein four-group.

### Composite modulus not a prime power

The basic fact in this case is

- if a is a residue modulo n, then a is a residue modulo *p*^(*k*) for *every* prime power dividing n.
- if a is a nonresidue modulo n, then a is a nonresidue modulo *p*^(*k*) for *at least one* prime power dividing n.

Modulo a composite number, the product of two residues is a residue. The product of a residue and a nonresidue may be a residue, a nonresidue, or zero.

For example, from the table for modulus 6   **1**, 2, **3**, **4**, 5 (residues in **bold**).

The product of the residue 3 and the nonresidue 5 is the residue 3, whereas the product of the residue 4 and the nonresidue 2 is the nonresidue 2.

Also, the product of two nonresidues may be either a residue, a nonresidue, or zero.

For example, from the table for modulus 15   **1**, 2, 3, **4**, 5, **6**, 7, 8, **9**, **10**, 11, 12, 13, 14 (residues in **bold**).

The product of the nonresidues 2 and 8 is the residue 1, whereas the product of the nonresidues 2 and 7 is the nonresidue 14.

This phenomenon can best be described using the vocabulary of abstract algebra. The congruence classes relatively prime to the modulus are a group under multiplication, called the group of units of the ring $(\mathbb{Z}/n\mathbb{Z})$, and the squares are a subgroup of it. Different nonresidues may belong to different cosets, and there is no simple rule that predicts which one their product will be in. Modulo a prime, there is only the subgroup of squares and a single coset.

The fact that, e.g., modulo 15 the product of the nonresidues 3 and 5, or of the nonresidue 5 and the residue 9, or the two residues 9 and 10 are all zero comes from working in the full ring $(\mathbb{Z}/n\mathbb{Z})$, which has zero divisors for composite n.

For this reason some authors add to the definition that a quadratic residue a must not only be a square but must also be relatively prime to the modulus n. (a is coprime to n if and only if *a*^2 is coprime to n.)

Although it makes things tidier, this article does not insist that residues must be coprime to the modulus.

## Notations

Gauss used R and N to denote residuosity and non-residuosity, respectively; for example, 2 R 7 and 5 N 7, or 1 R 8 and 3 N 8.

Although this notation is compact and convenient for some purposes, a more useful notation is the Legendre symbol, also called the quadratic character, which is defined for all integers a and positive odd prime numbers p as

$$ \left(\frac{a}{p}\right) = \begin{cases}\;\;\,0&\text{ if }p \text { divides } a\\+1&\text{ if } a \operatorname{R} p \text{ and }p \text { does not divide } a\\-1&\text{ if }a \operatorname{N} p \text{ and }p \text{ does not divide } a\end{cases} $$

There are two reasons why numbers ≡ 0 (mod p) are treated specially. As we have seen, it makes many formulas and theorems easier to state. The other (related) reason is that the quadratic character is a homomorphism from the multiplicative group of nonzero congruence classes modulo p to the complex numbers under multiplication. Setting $(\tfrac{np}{p}) = 0$ allows its domain to be extended to the multiplicative semigroup of all the integers.

One advantage of this notation over Gauss's is that the Legendre symbol is a function that can be used in formulas. It can also easily be generalized to cubic, quartic and higher power residues.

There is a generalization of the Legendre symbol for composite values of p, the Jacobi symbol, but its properties are not as simple: if m is composite and the Jacobi symbol $(\tfrac{a}{m}) = -1,$ then *a* N *m*, and if *a* R *m* then $(\tfrac{a}{m}) = 1,$ but if $(\tfrac{a}{m}) = 1$ we do not know whether *a* R *m* or *a* N *m*. For example: $(\tfrac{2}{15}) = 1$ and $(\tfrac{4}{15}) = 1$, but 2 N 15 and 4 R 15. If m is prime, the Jacobi and Legendre symbols agree.

## Distribution of quadratic residues

Although quadratic residues appear to occur in a rather random pattern modulo n, and this has been exploited in such applications as acoustics and cryptography, their distribution also exhibits some striking regularities.

Using Dirichlet's theorem on primes in arithmetic progressions, the law of quadratic reciprocity, and the Chinese remainder theorem (CRT) it is easy to see that for any *M* > 0 there are primes p such that the numbers 1, 2, ..., M are all residues modulo p.

For example, if *p* ≡ 1 (mod 8), (mod 12), (mod 5) and (mod 28), then by the law of quadratic reciprocity 2, 3, 5, and 7 will all be residues modulo p, and thus all numbers 1–10 will be. The CRT says that this is the same as *p* ≡ 1 (mod 840), and Dirichlet's theorem says there are an infinite number of primes of this form. 2521 is the smallest, and indeed 1^2 ≡ 1, 1046^2 ≡ 2, 123^2 ≡ 3, 2^2 ≡ 4, 643^2 ≡ 5, 87^2 ≡ 6, 668^2 ≡ 7, 429^2 ≡ 8, 3^2 ≡ 9, and 529^2 ≡ 10 (mod 2521).

### Dirichlet's formulas

The first of these regularities stems from Peter Gustav Lejeune Dirichlet's work (in the 1830s) on the analytic formula for the class number of binary quadratic forms. Let q be a prime number, s a complex variable, and define a Dirichlet L-function as

$$ L(s) = \sum_{n=1}^\infty\left(\frac{n}{q}\right)n^{-s}. $$

Dirichlet showed that if *q* ≡ 3 (mod 4), then

$$ L(1) = -\frac{\pi}{\sqrt q}\sum_{n=1}^{q-1} \frac{n}{q} \left(\frac{n}{q}\right) > 0. $$

Therefore, in this case (prime *q* ≡ 3 (mod 4)), the sum of the quadratic residues minus the sum of the nonresidues in the range 1, 2, ..., *q* − 1 is a negative number.

For example, modulo 11,

- **1**, 2, **3**, **4**, **5**, 6, 7, 8, **9**, 10 (residues in **bold**)
- 1 + 4 + 9 + 5 + 3 = 22, 2 + 6 + 7 + 8 + 10 = 33, and the difference is −11.

In fact the difference will always be an odd multiple of q if *q* > 3. In contrast, for prime *q* ≡ 1 (mod 4), the sum of the quadratic residues minus the sum of the nonresidues in the range 1, 2, ..., *q* − 1 is zero, implying that both sums equal $\frac{q(q-1)}{4}$.

Dirichlet also proved that for prime *q* ≡ 3 (mod 4),

$$ L(1) = \frac{\pi}{\left(2-\left(\frac{2}{q}\right)\right)\!\sqrt q}\sum_{n=1}^\frac{q-1}{2}\left(\frac{n}{q}\right) > 0. $$

This implies that there are more quadratic residues than nonresidues among the numbers 1, 2, ..., (*q* − 1)/2.

For example, modulo 11 there are four residues less than 6 (namely 1, 3, 4, and 5), but only one nonresidue (2).

An intriguing fact about these two theorems is that all known proofs rely on analysis; no-one has ever published a simple or direct proof of either statement.

### Law of quadratic reciprocity

If p and q are odd primes, then:

((p is a quadratic residue mod q) if and only if (q is a quadratic residue mod p)) if and only if (at least one of p and q is congruent to 1 mod 4).

That is:

$$ \left(\frac{p}{q}\right) \left(\frac{q}{p}\right) = (-1)^{\frac{p-1}{2} \cdot \frac{q-1}{2}} $$

where $\left(\frac{p}{q}\right)$ is the Legendre symbol.

Thus, for numbers a and odd primes p that don't divide a:

| a |  a is a quadratic residue mod p if and only if |  a |  a is a quadratic residue mod p if and only if |
|  1 |  (every prime p) |  −1 |  *p* ≡ 1 (mod 4) |
|  2 |  *p* ≡ 1, 7 (mod 8) |  −2 |  *p* ≡ 1, 3 (mod 8) |
|  3 |  *p* ≡ 1, 11 (mod 12) |  −3 |  *p* ≡ 1 (mod 3) |
|  4 |  (every prime p) |  −4 |  *p* ≡ 1 (mod 4) |
|  5 |  *p* ≡ 1, 4 (mod 5) |  −5 |  *p* ≡ 1, 3, 7, 9 (mod 20) |
|  6 |  *p* ≡ 1, 5, 19, 23 (mod 24) |  −6 |  *p* ≡ 1, 5, 7, 11 (mod 24) |
|  7 |  *p* ≡ 1, 3, 9, 19, 25, 27 (mod 28) |  −7 |  *p* ≡ 1, 2, 4 (mod 7) |
|  8 |  *p* ≡ 1, 7 (mod 8) |  −8 |  *p* ≡ 1, 3 (mod 8) |
|  9 |  (every prime p) |  −9 |  *p* ≡ 1 (mod 4) |
|  10 |  *p* ≡ 1, 3, 9, 13, 27, 31, 37, 39 (mod 40) |  −10 |  *p* ≡ 1, 7, 9, 11, 13, 19, 23, 37 (mod 40) |
|  11 |  *p* ≡ 1, 5, 7, 9, 19, 25, 35, 37, 39, 43 (mod 44) |  −11 |  *p* ≡ 1, 3, 4, 5, 9 (mod 11) |
|  12 |  *p* ≡ 1, 11 (mod 12) |  −12 |  *p* ≡ 1 (mod 3) |

### Pairs of residues and nonresidues

Modulo a prime p, the number of pairs n, *n* + 1 where *n* R *p* and *n* + 1 R *p*, or *n* N *p* and *n* + 1 R *p*, etc., are almost equal. More precisely, let p be an odd prime. For *i*, *j* = 0, 1 define the sets

$$ A_{ij}=\left\{k\in\{1,2,\dots,p-2\}: \left(\frac{k}{p}\right)=(-1)^i\land\left(\frac{k+1}{p}\right)=(-1)^j\right\}, $$

and let

$$ \alpha_{ij} = |A_{ij}|. $$

That is,

- *α*_(00) is the number of residues that are followed by a residue,
- *α*_(01) is the number of residues that are followed by a nonresidue,
- *α*_(10) is the number of nonresidues that are followed by a residue, and
- *α*_(11) is the number of nonresidues that are followed by a nonresidue.

Then if *p* ≡ 1 (mod 4)

$$ \alpha_{00} = \frac{p-5}{4},\;\alpha_{01} =\alpha_{10} =\alpha_{11} = \frac{p-1}{4} $$

and if *p* ≡ 3 (mod 4)

$$ \alpha_{01} = \frac{p+1}{4},\;\alpha_{00} =\alpha_{10} =\alpha_{11} = \frac{p-3}{4}. $$

For example: (residues in **bold**)

Modulo 17

- **1**, **2**, 3, **4**, 5, 6, 7, **8**, **9**, 10, 11, 12, **13**, 14, **15**, **16**

  - *A*_(00) = {1,8,15},
  - *A*_(01) = {2,4,9,13},
  - *A*_(10) = {3,7,12,14},
  - *A*_(11) = {5,6,10,11}.

Modulo 19

- **1**, 2, 3, **4**, **5**, **6**, **7**, 8, **9**, 10, **11**, 12, 13, 14, 15, **16**, **17**, 18

  - *A*_(00) = {4,5,6,16},
  - *A*_(01) = {1,7,9,11,17},
  - *A*_(10) = {3,8,10,15},
  - *A*_(11) = {2,12,13,14}.

Gauss (1828) introduced this sort of counting when he proved that if *p* ≡ 1 (mod 4) then *x*^4 ≡ 2 (mod *p*) can be solved if and only if *p* = *a*^2 + 64 *b*^2.

### Pólya–Vinogradov inequality

The values of $(\tfrac{a}{p})$ for consecutive values of a mimic a random variable like a coin flip. Specifically, Pólya and Vinogradov proved (independently) in 1918 that for any nonprincipal Dirichlet character *χ*(*n*) modulo q and any integers M and N,

$$ \left|\sum_{n=M+1}^{M+N}\chi(n)\right| =O\left( \sqrt q \log q\right), $$

in big O notation. Setting

$$ \chi(n) = \left(\frac{n}{q}\right), $$

this shows that the number of quadratic residues modulo q in any interval of length N is

$$ \frac{1}{2}N + O(\sqrt q\log q). $$

It is easy to prove that

$$ \left| \sum_{n=M+1}^{M+N} \left( \frac{n}{q} \right) \right| < \sqrt q \log q. $$

In fact,

$$ \left| \sum_{n=M+1}^{M+N} \left( \frac{n}{q} \right) \right| < \frac{4}{\pi^2} \sqrt q \log q+0.41\sqrt q +0.61. $$

Montgomery and Vaughan improved this in 1977, showing that, if the generalized Riemann hypothesis is true then

$$ \left|\sum_{n=M+1}^{M+N}\chi(n)\right|=O\left(\sqrt q \log \log q\right). $$

This result cannot be substantially improved, for Schur had proved in 1918 that

$$ \max_N \left|\sum_{n=1}^{N}\left(\frac{n}{q}\right)\right|>\frac{1}{2\pi}\sqrt q $$

and Paley had proved in 1932 that

$$ \max_N \left|\sum_{n=1}^{N}\left(\frac{d}{n}\right)\right|>\frac{1}{7}\sqrt d \log \log d $$

for infinitely many *d* > 0.

### Least quadratic non-residue

The least quadratic residue mod p is clearly 1. The question of the magnitude of the least quadratic non-residue *n*(*p*) is more subtle, but it is always prime, with 7 appearing for the first time at 71.

The Pólya–Vinogradov inequality above gives O(√*p* log *p*).

The best unconditional estimate is *n*(*p*) ≪ *p*^(*θ*) for any *θ* > 1/4√e, obtained by estimates of Burgess on character sums.

Assuming the Generalised Riemann hypothesis, Ankeny obtained *n*(*p*) ≪ (log *p*)^2.

Linnik showed that the number of p less than X such that *n*(*p*) > *X*^(*ε*) is bounded by a constant depending on ε.

The least quadratic non-residues mod p for odd primes p are: 2, 2, 3, 2, 2, 3, 2, 5, 2, 3, 2, ... (sequence A053760 in the OEIS)

### Quadratic excess

Let p be an odd prime. The **quadratic excess** *E*(*p*) is the number of quadratic residues on the range (0, *p*/2) minus the number in the range (*p*/2, *p*) (sequence A178153 in the OEIS). For p congruent to 1 mod 4, the excess is zero, since −1 is a quadratic residue and the residues are symmetric under *r* ↔ *p*−*r*. For p congruent to 3 mod 4, the excess E is always positive.

## Computational complexity

Two natural computational problems are:

1. Given a number a and a modulus n, determine whether a is a quadratic residue.
2. Calculate a square root of a (that is, a solution to *x*^2 ≡ *a* (mod *n*)), assuming one exists.

For prime moduli, both problems can be solved efficiently using the Tonelli–Shanks algorithm; the same is true for composite moduli whose prime factorization is known. In the case of a composite modulus with unknown prime factorization, the problem of identifying quadratic residues is known as the quadratic residuosity problem and is believed to be computationally difficult.

Modulo a prime p, a quadratic residue a has 1 + (*a*|*p*) roots (i.e. zero if *a* N *p*, one if *a* ≡ 0 (mod *p*), or two if *a* R *p* and gcd(*a*, *p*) = 1.)

In general, if a composite modulus n is written as a product of powers of distinct primes, and there are *n*_1 roots modulo the first one, *n*_2 mod the second, ..., there will be *n*_1*n*_2... roots modulo n.

The theoretical way solutions modulo the prime powers are combined to make solutions modulo n is called the Chinese remainder theorem; it can be implemented with an efficient algorithm.

For example:

- Solve *x*^2 ≡ 6 (mod 15).

  - *x*^2 ≡ 6 (mod 3) has one solution, 0; *x*^2 ≡ 6 (mod 5) has two, 1 and 4.
  - and there are two solutions modulo 15, namely 6 and 9.

-
- Solve *x*^2 ≡ 4 (mod 15).

  - *x*^2 ≡ 4 (mod 3) has two solutions, 1 and 2; *x*^2 ≡ 4 (mod 5) has two, 2 and 3.
  - and there are four solutions modulo 15, namely 2, 7, 8, and 13.

-
- Solve *x*^2 ≡ 7 (mod 15).

  - *x*^2 ≡ 7 (mod 3) has two solutions, 1 and 2; *x*^2 ≡ 7 (mod 5) has no solutions.
  - and there are no solutions modulo 15.

### Prime or prime power modulus

First off, if the modulus n is prime, the Legendre symbol $\left(\frac{a}{n}\right)$ can be quickly computed using a variation of Euclid's algorithm or the Euler's criterion. If it is −1, there is no solution. Secondly, assuming that $\left(\frac{a}{n}\right)=1$, if *n* ≡ 3 (mod 4), Lagrange found that the solutions are given by

$$ x \equiv \pm a^{(n+1)/4} \pmod{n}, $$

and Legendre found a similar solution if *n* ≡ 5 (mod 8):

$$ x \equiv \begin{cases} \pm a^{(n+3)/8} \pmod{n}& \text{ if } a \text{ is a quartic residue modulo } n, \\ \pm a^{(n+3)/8}2^{(n-1)/4} \pmod{n}& \text{ if } a \text{ is a quartic non-residue modulo } n. \end{cases} $$

For prime *n* ≡ 1 (mod 8), however, there is no known formula. Tonelli (in 1891) and Cipolla found efficient algorithms that work for all prime moduli. Both algorithms require finding a quadratic nonresidue modulo n, and there is no efficient deterministic algorithm known for doing that. But since half the numbers between 1 and n are nonresidues, picking numbers x at random and calculating the Legendre symbol $\left(\frac{x}{n}\right)$ until a nonresidue is found will quickly produce one. A slight variant of this algorithm is the Tonelli–Shanks algorithm.

If the modulus n is a prime power *n* = *p*^(*e*), a solution may be found modulo p and "lifted" to a solution modulo n using Hensel's lemma or an algorithm of Gauss.

### Composite modulus

If the modulus n has been factored into prime powers, the solution was discussed above.

If n is not congruent to 2 modulo 4 and the Kronecker symbol $\left(\tfrac{a}{n}\right)=-1,$ then there is no solution; if n is congruent to 2 modulo 4 and $\left(\tfrac{a}{n/2}\right)=-1$, then there is also no solution. If n is not congruent to 2 modulo 4 and $\left(\tfrac{a}{n}\right)=1$, or n is congruent to 2 modulo 4 and $\left(\tfrac{a}{n/2}\right)=1$, there may or may not be one.

If the complete factorization of n is not known, and $\left(\tfrac{a}{n}\right)=1$ and n is not congruent to 2 modulo 4, or n is congruent to 2 modulo 4 and $\left(\tfrac{a}{n/2}\right)=1$, the problem is known to be equivalent to integer factorization of n (i.e. an efficient solution to either problem could be used to solve the other efficiently).

The above discussion indicates how knowing the factors of n allows us to find the roots efficiently. Say there were an efficient algorithm for finding square roots modulo a composite number. The article congruence of squares discusses how finding two numbers x and y where *x*^2 ≡ *y*^2 (mod *n*) and *x* ≠ ±*y* suffices to factorize n efficiently. Generate a random number, square it modulo n, and have the efficient square root algorithm find a root. Repeat until it returns a number not equal to the one we originally squared (or its negative modulo n), then follow the algorithm described in congruence of squares. The efficiency of the factoring algorithm depends on the exact characteristics of the root-finder (e.g. does it return all roots? just the smallest one? a random one?), but it will be efficient.

Determining whether a is a quadratic residue or nonresidue modulo n (denoted *a* R *n* or *a* N *n*) can be done efficiently for prime n by computing the Legendre symbol. However, for composite n, this forms the quadratic residuosity problem, which is not known to be as hard as factorization, but is assumed to be quite hard.

On the other hand, if we want to know whether there is a solution for x less than some given limit c, this problem is NP-complete; however, this is a fixed-parameter tractable problem, where c is the parameter.

In general, to determine whether a is a quadratic residue modulo composite n, one can use the following theorem:

Let *n* > 1, and gcd(*a*, *n*) = 1. Then *x*^2 ≡ *a* (mod *n*) is solvable if and only if:

- The Legendre symbol $\left(\tfrac{a}{p}\right)=1$ for all odd prime divisors p of n.
- *a* ≡ 1 (mod 4) if n is divisible by 4 but not 8; or *a* ≡ 1 (mod 8) if n is divisible by 8.

Note: This theorem essentially requires that the factorization of n is known. Also notice that if gcd(*a*, *n*) = *m*, then the congruence can be reduced to *a*/*m* ≡ *x*^2/*m* (mod *n*/*m*), but then this takes the problem away from quadratic residues (unless m is a square).

## Number of quadratic residues

The list of the number of quadratic residues modulo n, for *n* = 1, 2, 3 ..., looks like: 1, 2, 2, 2, 3, 4, 4, 3, 4, 6, 6, 4, 7, 8, 6, ... (sequence A000224 in the OEIS)

Formulas to count the number of squares modulo $n$ are given by Stangl. Let $s(n)$ give the number of squares modulo $n$. This is a multiplicative function, so it is completely characterized by its values at prime powers.

### Modulo powers of 2

- $s(2^n) = \frac{2^{n-1}+4}{3}$ for even $n$
- $s(2^n) = \frac{2^{n-1}+5}{3}$ for odd $n$

### Modulo powers of odd primes

- $s(p) = \frac{p+1}{2}$
- $s(p^2) = \frac{p^2-p+2}{2}$
- $s(p^n) = \frac{p^{n+1}+p+2}{2(p+1)}$ for even $n \geq 3$
- $s(p^n) = \frac{p^{n+1}+2p+1}{2(p+1)}$ for odd $n \geq 3$

## Applications of quadratic residues

### Acoustics

Sound diffusers have been based on number-theoretic concepts such as primitive roots and quadratic residues.

### Graph theory

Paley graphs are dense undirected graphs, one for each prime *p* ≡ 1 (mod 4), that form an infinite family of conference graphs, which yield an infinite family of symmetric conference matrices.

Paley digraphs are directed analogs of Paley graphs, one for each *p* ≡ 3 (mod 4), that yield antisymmetric conference matrices.

The construction of these graphs uses quadratic residues.

### Cryptography

The fact that finding a square root of a number modulo a large composite n is equivalent to factoring (which is widely believed to be a hard problem) has been used for constructing cryptographic schemes such as the Rabin signature and the oblivious transfer. The quadratic residuosity problem is the basis for the Goldwasser–Micali cryptosystem.

The discrete logarithm is a similar problem that is also used in cryptography.

### Primality testing

Euler's criterion is a formula for the Legendre symbol (*a*|*p*) where p is prime. If p is composite the formula may or may not compute (*a*|*p*) correctly. The Solovay–Strassen primality test for whether a given number n is prime or composite picks a random a and computes (*a*|*n*) using a modification of Euclid's algorithm, and also using Euler's criterion. If the results disagree, n is composite; if they agree, n may be composite or prime. For a composite n at least 1/2 the values of a in the range 2, 3, ..., *n* − 1 will return "n is composite"; for prime n none will. If, after using many different values of a, n has not been proved composite it is called a "probable prime".

The Miller–Rabin primality test is based on the same principles. There is a deterministic version of it, but the proof that it works depends on the generalized Riemann hypothesis; the output from this test is "n is definitely composite" or "either n is prime or the GRH is false". If the second output ever occurs for a composite n, then the GRH would be false, which would have implications through many branches of mathematics.

### Integer factorization

In § VI of the *Disquisitiones Arithmeticae* Gauss discusses two factoring algorithms that use quadratic residues and the law of quadratic reciprocity.

Several modern factorization algorithms (including Dixon's algorithm, the continued fraction method, the quadratic sieve, and the number field sieve) generate small quadratic residues (modulo the number being factorized) in an attempt to find a congruence of squares which will yield a factorization. The number field sieve is the fastest general-purpose factorization algorithm known.

## Table of quadratic residues

The following table (sequence A096008 in the OEIS) lists the quadratic residues mod 1 to 75 (a red number means it is not coprime to n). (For the quadratic residues coprime to n, see (sequence A096103 in the OEIS), and for nonzero quadratic residues, see (sequence A046071 in the OEIS).)

| n |  quadratic residues mod n |  n |  quadratic residues mod n |  n |  quadratic residues mod n |
|  1 |  0 |  26 |  0, 1, 3, 4, 9, 10, 12, 13, 14, 16, 17, 22, 23, 25 |  51 |  0, 1, 4, 9, 13, 15, 16, 18, 19, 21, 25, 30, 33, 34, 36, 42, 43, 49 |
|  2 |  0, 1 |  27 |  0, 1, 4, 7, 9, 10, 13, 16, 19, 22, 25 |  52 |  0, 1, 4, 9, 12, 13, 16, 17, 25, 29, 36, 40, 48, 49 |
|  3 |  0, 1 |  28 |  0, 1, 4, 8, 9, 16, 21, 25 |  53 |  0, 1, 4, 6, 7, 9, 10, 11, 13, 15, 16, 17, 24, 25, 28, 29, 36, 37, 38, 40, 42, 43, 44, 46, 47, 49, 52 |
|  4 |  0, 1 |  29 |  0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28 |  54 |  0, 1, 4, 7, 9, 10, 13, 16, 19, 22, 25, 27, 28, 31, 34, 36, 37, 40, 43, 46, 49, 52 |
|  5 |  0, 1, 4 |  30 |  0, 1, 4, 6, 9, 10, 15, 16, 19, 21, 24, 25 |  55 |  0, 1, 4, 5, 9, 11, 14, 15, 16, 20, 25, 26, 31, 34, 36, 44, 45, 49 |
|  6 |  0, 1, 3, 4 |  31 |  0, 1, 2, 4, 5, 7, 8, 9, 10, 14, 16, 18, 19, 20, 25, 28 |  56 |  0, 1, 4, 8, 9, 16, 25, 28, 32, 36, 44, 49 |
|  7 |  0, 1, 2, 4 |  32 |  0, 1, 4, 9, 16, 17, 25 |  57 |  0, 1, 4, 6, 7, 9, 16, 19, 24, 25, 28, 30, 36, 39, 42, 43, 45, 49, 54, 55 |
|  8 |  0, 1, 4 |  33 |  0, 1, 3, 4, 9, 12, 15, 16, 22, 25, 27, 31 |  58 |  0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28, 29, 30, 33, 34, 35, 36, 38, 42, 45, 49, 51, 52, 53, 54, 57 |
|  9 |  0, 1, 4, 7 |  34 |  0, 1, 2, 4, 8, 9, 13, 15, 16, 17, 18, 19, 21, 25, 26, 30, 32, 33 |  59 |  0, 1, 3, 4, 5, 7, 9, 12, 15, 16, 17, 19, 20, 21, 22, 25, 26, 27, 28, 29, 35, 36, 41, 45, 46, 48, 49, 51, 53, 57 |
|  10 |  0, 1, 4, 5, 6, 9 |  35 |  0, 1, 4, 9, 11, 14, 15, 16, 21, 25, 29, 30 |  60 |  0, 1, 4, 9, 16, 21, 24, 25, 36, 40, 45, 49 |
|  11 |  0, 1, 3, 4, 5, 9 |  36 |  0, 1, 4, 9, 13, 16, 25, 28 |  61 |  0, 1, 3, 4, 5, 9, 12, 13, 14, 15, 16, 19, 20, 22, 25, 27, 34, 36, 39, 41, 42, 45, 46, 47, 48, 49, 52, 56, 57, 58, 60 |
|  12 |  0, 1, 4, 9 |  37 |  0, 1, 3, 4, 7, 9, 10, 11, 12, 16, 21, 25, 26, 27, 28, 30, 33, 34, 36 |  62 |  0, 1, 2, 4, 5, 7, 8, 9, 10, 14, 16, 18, 19, 20, 25, 28, 31, 32, 33, 35, 36, 38, 39, 40, 41, 45, 47, 49, 50, 51, 56, 59 |
|  13 |  0, 1, 3, 4, 9, 10, 12 |  38 |  0, 1, 4, 5, 6, 7, 9, 11, 16, 17, 19, 20, 23, 24, 25, 26, 28, 30, 35, 36 |  63 |  0, 1, 4, 7, 9, 16, 18, 22, 25, 28, 36, 37, 43, 46, 49, 58 |
|  14 |  0, 1, 2, 4, 7, 8, 9, 11 |  39 |  0, 1, 3, 4, 9, 10, 12, 13, 16, 22, 25, 27, 30, 36 |  64 |  0, 1, 4, 9, 16, 17, 25, 33, 36, 41, 49, 57 |
|  15 |  0, 1, 4, 6, 9, 10 |  40 |  0, 1, 4, 9, 16, 20, 24, 25, 36 |  65 |  0, 1, 4, 9, 10, 14, 16, 25, 26, 29, 30, 35, 36, 39, 40, 49, 51, 55, 56, 61, 64 |
|  16 |  0, 1, 4, 9 |  41 |  0, 1, 2, 4, 5, 8, 9, 10, 16, 18, 20, 21, 23, 25, 31, 32, 33, 36, 37, 39, 40 |  66 |  0, 1, 3, 4, 9, 12, 15, 16, 22, 25, 27, 31, 33, 34, 36, 37, 42, 45, 48, 49, 55, 58, 60, 64 |
|  17 |  0, 1, 2, 4, 8, 9, 13, 15, 16 |  42 |  0, 1, 4, 7, 9, 15, 16, 18, 21, 22, 25, 28, 30, 36, 37, 39 |  67 |  0, 1, 4, 6, 9, 10, 14, 15, 16, 17, 19, 21, 22, 23, 24, 25, 26, 29, 33, 35, 36, 37, 39, 40, 47, 49, 54, 55, 56, 59, 60, 62, 64, 65 |
|  18 |  0, 1, 4, 7, 9, 10, 13, 16 |  43 |  0, 1, 4, 6, 9, 10, 11, 13, 14, 15, 16, 17, 21, 23, 24, 25, 31, 35, 36, 38, 40, 41 |  68 |  0, 1, 4, 8, 9, 13, 16, 17, 21, 25, 32, 33, 36, 49, 52, 53, 60, 64 |
|  19 |  0, 1, 4, 5, 6, 7, 9, 11, 16, 17 |  44 |  0, 1, 4, 5, 9, 12, 16, 20, 25, 33, 36, 37 |  69 |  0, 1, 3, 4, 6, 9, 12, 13, 16, 18, 24, 25, 27, 31, 36, 39, 46, 48, 49, 52, 54, 55, 58, 64 |
|  20 |  0, 1, 4, 5, 9, 16 |  45 |  0, 1, 4, 9, 10, 16, 19, 25, 31, 34, 36, 40 |  70 |  0, 1, 4, 9, 11, 14, 15, 16, 21, 25, 29, 30, 35, 36, 39, 44, 46, 49, 50, 51, 56, 60, 64, 65 |
|  21 |  0, 1, 4, 7, 9, 15, 16, 18 |  46 |  0, 1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18, 23, 24, 25, 26, 27, 29, 31, 32, 35, 36, 39, 41 |  71 |  0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 19, 20, 24, 25, 27, 29, 30, 32, 36, 37, 38, 40, 43, 45, 48, 49, 50, 54, 57, 58, 60, 64 |
|  22 |  0, 1, 3, 4, 5, 9, 11, 12, 14, 15, 16, 20 |  47 |  0, 1, 2, 3, 4, 6, 7, 8, 9, 12, 14, 16, 17, 18, 21, 24, 25, 27, 28, 32, 34, 36, 37, 42 |  72 |  0, 1, 4, 9, 16, 25, 28, 36, 40, 49, 52, 64 |
|  23 |  0, 1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18 |  48 |  0, 1, 4, 9, 16, 25, 33, 36 |  73 |  0, 1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 19, 23, 24, 25, 27, 32, 35, 36, 37, 38, 41, 46, 48, 49, 50, 54, 55, 57, 61, 64, 65, 67, 69, 70, 71, 72 |
|  24 |  0, 1, 4, 9, 12, 16 |  49 |  0, 1, 2, 4, 8, 9, 11, 15, 16, 18, 22, 23, 25, 29, 30, 32, 36, 37, 39, 43, 44, 46 |  74 |  0, 1, 3, 4, 7, 9, 10, 11, 12, 16, 21, 25, 26, 27, 28, 30, 33, 34, 36, 37, 38, 40, 41, 44, 46, 47, 48, 49, 53, 58, 62, 63, 64, 65, 67, 70, 71, 73 |
|  25 |  0, 1, 4, 6, 9, 11, 14, 16, 19, 21, 24 |  50 |  0, 1, 4, 6, 9, 11, 14, 16, 19, 21, 24, 25, 26, 29, 31, 34, 36, 39, 41, 44, 46, 49 |  75 |  0, 1, 4, 6, 9, 16, 19, 21, 24, 25, 31, 34, 36, 39, 46, 49, 51, 54, 61, 64, 66, 69 |

Quadratic residues (see also A048152, A343720)
|  x | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
|  *x*^2 |  001 |  004 |  009 |  016 |  025 |  036 |  049 |  064 |  081 |  100 | 121 | 144 | 169 | 196 | 225 | 256 | 289 | 324 | 361 | 400 | 441 | 484 | 529 | 576 | 625 |
|  mod 1 |  0 | 0 | 0 | 0 | 0 |  0 | 0 | 0 | 0 | 0 |  0 | 0 | 0 | 0 | 0 |  0 | 0 | 0 | 0 | 0 |  0 | 0 | 0 | 0 | 0 |
|  mod 2 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 |
|  mod 3 |  1 | 1 | 0 |  1 | 1 | 0 |  1 | 1 | 0 |  1 | 1 | 0 |  1 | 1 | 0 |  1 | 1 | 0 |  1 | 1 | 0 |  1 | 1 | 0 |  1 |
|  mod 4 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 | 0 |  1 |
|  mod 5 |  1 | 4 | 4 | 1 | 0 |  1 | 4 | 4 | 1 | 0 |  1 | 4 | 4 | 1 | 0 |  1 | 4 | 4 | 1 | 0 |  1 | 4 | 4 | 1 | 0 |
|  mod 6 |  1 | 4 | 3 | 4 | 1 | 0 |  1 | 4 | 3 | 4 | 1 | 0 |  1 | 4 | 3 | 4 | 1 | 0 |  1 | 4 | 3 | 4 | 1 | 0 |  1 |
|  mod 7 |  1 | 4 | 2 | 2 | 4 | 1 | 0 |  1 | 4 | 2 | 2 | 4 | 1 | 0 |  1 | 4 | 2 | 2 | 4 | 1 | 0 |  1 | 4 | 2 | 2 |
|  mod 8 |  1 | 4 | 1 | 0 |  1 | 4 | 1 | 0 |  1 | 4 | 1 | 0 |  1 | 4 | 1 | 0 |  1 | 4 | 1 | 0 |  1 | 4 | 1 | 0 |  1 |
|  mod 9 |  1 | 4 | 0 | 7 | 7 | 0 | 4 | 1 | 0 |  1 | 4 | 0 | 7 | 7 | 0 | 4 | 1 | 0 |  1 | 4 | 0 | 7 | 7 | 0 | 4 |
|  mod 10 |  1 | 4 | 9 | 6 | 5 | 6 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 6 | 5 | 6 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 6 | 5 |
|  mod 11 |  1 | 4 | 9 | 5 | 3 | 3 | 5 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 5 | 3 | 3 | 5 | 9 | 4 | 1 | 0 |  1 | 4 | 9 |
|  mod 12 |  1 | 4 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 4 | 1 | 0 |  1 |
|  mod 13 |  1 | 4 | 9 | 3 | 12 | 10 | 10 | 12 | 3 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 3 | 12 | 10 | 10 | 12 | 3 | 9 | 4 | 1 |
|  mod 14 |  1 | 4 | 9 | 2 | 11 | 8 | 7 | 8 | 11 | 2 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 2 | 11 | 8 | 7 | 8 | 11 | 2 | 9 |
|  mod 15 |  1 | 4 | 9 | 1 | 10 | 6 | 4 | 4 | 6 | 10 | 1 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 1 | 10 | 6 | 4 | 4 | 6 | 10 |
|  mod 16 |  1 | 4 | 9 | 0 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 0 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 0 | 9 | 4 | 1 | 0 |  1 |
|  mod 17 |  1 | 4 | 9 | 16 | 8 | 2 | 15 | 13 | 13 | 15 | 2 | 8 | 16 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 16 | 8 | 2 | 15 | 13 |
|  mod 18 |  1 | 4 | 9 | 16 | 7 | 0 | 13 | 10 | 9 | 10 | 13 | 0 | 7 | 16 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 16 | 7 | 0 | 13 |
|  mod 19 |  1 | 4 | 9 | 16 | 6 | 17 | 11 | 7 | 5 | 5 | 7 | 11 | 17 | 6 | 16 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 16 | 6 | 17 |
|  mod 20 |  1 | 4 | 9 | 16 | 5 | 16 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 16 | 5 | 16 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 16 | 5 |
|  mod 21 |  1 | 4 | 9 | 16 | 4 | 15 | 7 | 1 | 18 | 16 | 16 | 18 | 1 | 7 | 15 | 4 | 16 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 16 |
|  mod 22 |  1 | 4 | 9 | 16 | 3 | 14 | 5 | 20 | 15 | 12 | 11 | 12 | 15 | 20 | 5 | 14 | 3 | 16 | 9 | 4 | 1 | 0 |  1 | 4 | 9 |
|  mod 23 |  1 | 4 | 9 | 16 | 2 | 13 | 3 | 18 | 12 | 8 | 6 | 6 | 8 | 12 | 18 | 3 | 13 | 2 | 16 | 9 | 4 | 1 | 0 |  1 | 4 |
|  mod 24 |  1 | 4 | 9 | 16 | 1 | 12 | 1 | 16 | 9 | 4 | 1 | 0 |  1 | 4 | 9 | 16 | 1 | 12 | 1 | 16 | 9 | 4 | 1 | 0 |  1 |
|  mod 25 |  1 | 4 | 9 | 16 | 0 | 11 | 24 | 14 | 6 | 0 | 21 | 19 | 19 | 21 | 0 | 6 | 14 | 24 | 11 | 0 | 16 | 9 | 4 | 1 | 0 |

## See also

- Euler's criterion
- Gauss's lemma
- Zolotarev's lemma
- Character sum
- Law of quadratic reciprocity
- Quadratic residue code
