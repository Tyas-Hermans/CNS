# Safe and Sophie Germain primes

Source: <https://en.wikipedia.org/wiki/Safe_and_Sophie_Germain_primes>

In number theory, a prime number *p* is a **Sophie Germain prime** if 2*p* + 1 is also prime. The number 2*p* + 1 associated with a Sophie Germain prime is called a **safe prime**. For example, 11 is a Sophie Germain prime and 2 × 11 + 1 = 23 is its associated safe prime. Sophie Germain primes and safe primes have applications in public key cryptography and primality testing. It has been conjectured that there are infinitely many Sophie Germain primes, but this remains unproven.

Sophie Germain primes are named after the French mathematician Sophie Germain, who used them in her investigations of Fermat's Last Theorem. One attempt by Germain to prove Fermat's Last Theorem was to let *p* be a prime number of the form 8*k* + 7 and to let *n* = *p* – 1. In this case, $x^n + y^n = z^n$ is unsolvable. Germain's proof, however, remained unfinished. Through her attempts to solve Fermat's Last Theorem, she proved a result now known as Sophie Germain's theorem, which states that if *p* is an odd prime and 2*p* + 1 is also prime, then *p* must divide *x*, *y*, or *z*. Otherwise, $x^n + y^n \neq z^n$. This case where *p* does not divide *x*, *y*, or *z* is called the first case. Sophie Germain's work was the most progress achieved on Fermat's last theorem at that time. Later work by Kummer and others always divided the problem into first and second cases.

## Individual numbers

The first few Sophie Germain primes (those less than 1000) are
    2, 3, 5, 11, 23, 29, 41, 53, 83, 89, 113, 131, 173, 179, 191, 233, 239, 251, 281, 293, 359, 419, 431, 443, 491, 509, 593, 641, 653, 659, 683, 719, 743, 761, 809, 911, 953, ... OEIS: A005384

Hence, the first few safe primes are
    5, 7, 11, 23, 47, 59, 83, 107, 167, 179, 227, 263, 347, 359, 383, 467, 479, 503, 563, 587, 719, 839, 863, 887, 983, 1019, 1187, 1283, 1307, 1319, 1367, 1439, 1487, 1523, 1619, 1823, 1907, ... OEIS: A005385

In cryptography, much larger Sophie Germain primes like 1,846,389,521,368 + 11^(600) are required.

Two distributed computing projects, PrimeGrid and Twin Prime Search, include searches for large Sophie Germain primes. Some of the largest known Sophie Germain primes are given in the following table.

|  Value | Number
of digits | Time of
discovery | Discoverer |
|  2618163402417 × 2^(1290000) − 1 | 388342 | February 2016 | Dr. James Scott Brown in a distributed PrimeGrid search using the programs TwinGen and LLR |
|  18543637900515 × 2^(666667) − 1 | 200701 | April 2012 | Philipp Bliedung in a distributed PrimeGrid search using the programs TwinGen and LLR |
|  183027 × 2^(265440) − 1 | 79911 | March 2010 | Tom Wu using LLR |
|  648621027630345 × 2^(253824) − 1 and
620366307356565 × 2^(253824) − 1 | 76424 | November 2009 | Zoltán Járai, Gábor Farkas, Tímea Csajbók, János Kasza and Antal Járai |
|  1068669447 × 2^(211088) − 1 | 63553 | May 2020 | Michael Kwok |
|  99064503957 × 2^(200008) − 1 | 60220 | April 2016 | S. Urushihata |
|  607095 × 2^(176311) − 1 | 53081 | September 2009 | Tom Wu |
|  48047305725 × 2^(172403) − 1 | 51910 | January 2007 | David Underbakke using TwinGen and LLR |
|  137211941292195 × 2^(171960) − 1 | 51780 | May 2006 | Járai et al. |
|

On 2 Dec 2019, Fabrice Boudot, Pierrick Gaudry, Aurore Guillevic, Nadia Heninger, Emmanuel Thomé, and Paul Zimmermann announced the computation of a discrete logarithm modulo the 240-digit (795 bit) prime RSA-240 + 49204 (the first safe prime above RSA-240) using a number field sieve algorithm; see Discrete logarithm records.

## Properties

There is no special primality test for safe primes, the way there is for Fermat primes and Mersenne primes. However, Pocklington's criterion can be used to prove the primality of 2*p* + 1 once one has proven the primality of *p*.

Just as every term except the last one of a Cunningham chain of the first kind is a Sophie Germain prime, so every term except the first of such a chain is a safe prime. Safe primes ending in 7, that is, of the form 10*n* + 7, are the last terms in such chains when they occur, since 2(10*n* + 7) + 1 = 20*n* + 15 is divisible by 5.

For a safe prime, every quadratic nonresidue, except −1 (if nonresidue), is a primitive root. It follows that for a safe prime, the least positive primitive root is a prime number.

### Modular restrictions

With the exception of 7, a safe prime *q* is of the form 6*k* − 1 or, equivalently, *q* ≡ 5 (mod 6) – as is *p* > 3. Similarly, with the exception of 5, a safe prime *q* is of the form 4*k* − 1 or, equivalently, *q* ≡ 3 (mod 4) — trivially true since (*q* − 1) / 2 must evaluate to an odd natural number. Combining both forms using lcm(6, 4) we determine that a safe prime *q* > 7 also must be of the form 12*k* − 1 or, equivalently, *q* ≡ 11 (mod 12).

It follows that, for any safe prime *q* > 7:

- both 3 and 12 are quadratic residues mod *q* (per law of quadratic reciprocity)

  - neither 3 nor 12 is a primitive root of *q*
  - the only safe primes that are also full reptend primes in base 12 are 5 and 7
  - *q* divides 3^((*q*−1)/2) − 1 and 12^((*q*−1)/2) − 1, same as 3^((*q*−1)/2) ≡ 1 mod *q* and 12^((*q*−1)/2) ≡ 1 mod *q* (per Euler's criterion)

- *q* − 3, *q* − 4, *q* − 9, *q* − 12 are quadratic nonresidues

  - *q* − 3, *q* − 4, *q* − 9, and, for *q* > 11, *q* − 12 are primitive roots

If *p* is a Sophie Germain prime greater than 3, then *p* must be congruent to 2 mod 3. For, if not, it would be congruent to 1 mod 3 and 2*p* + 1 would be congruent to 3 mod 3, impossible for a prime number. Similar restrictions hold for larger prime moduli, and are the basis for the choice of the "correction factor" 2*C* in the Hardy–Littlewood estimate on the density of the Sophie Germain primes.

If a Sophie Germain prime *p* is congruent to 3 (mod 4) ((sequence A002515 in the OEIS), *Lucasian primes*), then its matching safe prime 2*p* + 1 (congruent to 7 modulo 8) will be a divisor of the Mersenne number 2^(*p*) − 1. Historically, this result of Leonhard Euler was the first known criterion for a Mersenne number with a prime index to be composite. It can be used to generate the largest Mersenne numbers (with prime indices) that are known to be composite.

## Infinitude and density
Unsolved problem in mathematics Are there infinitely many Sophie Germain primes? More unsolved problems in mathematics

It is conjectured that there are infinitely many Sophie Germain primes, but this has not been proven. Several other famous conjectures in number theory generalize this and the twin prime conjecture; they include Dickson's conjecture, Schinzel's hypothesis H, and the Bateman–Horn conjecture.

A heuristic estimate for the number of Sophie Germain primes less than *n* is

$$ 2C \frac{n}{(\ln n)^2} \approx 1.32032\frac{n}{(\ln n)^2} $$

where

$$ C=\prod_{p>2} \frac{p(p-2)}{(p-1)^2}\approx 0.660161 $$

is Hardy–Littlewood's twin prime constant. For *n* = 10^4, this estimate predicts 156 Sophie Germain primes, which has a 20% error compared to the exact value of 190. For *n* = 10^7, the estimate predicts 50822, which is still 10% off from the exact value of 56032. The form of this estimate is due to G. H. Hardy and J. E. Littlewood, who applied a similar estimate to twin primes.

A sequence (*p*, 2*p* + 1, 2(2*p* + 1) + 1, ...) in which all of the numbers are prime is called a Cunningham chain of the first kind. Every term of such a sequence except the last is a Sophie Germain prime, and every term except the first is a safe prime. Extending the conjecture that there exist infinitely many Sophie Germain primes, it has also been conjectured that arbitrarily long Cunningham chains exist, although infinite chains are known to be impossible.

## Strong primes

A prime number *q* is a strong prime if *q* + 1 and *q* − 1 both have some large (around 500 digits) prime factors. For a safe prime *q* = 2*p* + 1, the number *q* − 1 naturally has a large prime factor, namely *p*, and so a safe prime *q* meets part of the criteria for being a strong prime. The running times of some methods of factoring a number with *q* as a prime factor depend partly on the size of the prime factors of *q* − 1. This is true, for instance, of the *p* − 1 method.

## Applications

### Cryptography

Safe primes are also important in cryptography because of their use in discrete logarithm-based techniques like Diffie–Hellman key exchange. If 2*p* + 1 is a safe prime, the multiplicative group of integers modulo 2*p* + 1 has a subgroup of large prime order. It is usually this prime-order subgroup that is desirable, and the reason for using safe primes is so that the modulus is as small as possible relative to *p*.

A prime number *p* = 2*q* + 1 is called a *safe prime* if *q* is prime. Thus, *p* = 2*q* + 1 is a safe prime if and only if *q* is a Sophie Germain prime, so finding safe primes and finding Sophie Germain primes are equivalent in computational difficulty. The notion of a safe prime can be strengthened to a strong prime, for which both *p* − 1 and *p* + 1 have large prime factors. Safe and strong primes were useful as the factors of secret keys in the RSA cryptosystem, because they prevent the system being broken by some factorization algorithms such as Pollard's *p* − 1 algorithm. However, with the current factorization technology, the advantage of using safe and strong primes appears to be negligible.

Similar issues apply in other cryptosystems as well, including Diffie–Hellman key exchange and similar systems that depend on the security of the discrete logarithm problem rather than on integer factorization. For this reason, key generation protocols for these methods often rely on efficient algorithms for generating strong primes, which in turn rely on the conjecture that these primes have a sufficiently high density.

In Sophie Germain Counter Mode, it was proposed to use the arithmetic in the finite field of order equal to the safe prime 2^(128) + 12451, to counter weaknesses in Galois/Counter Mode using the binary finite field GF(2^(128)). However, SGCM has been shown to be vulnerable to many of the same cryptographic attacks as GCM.

### Primality testing

In the first version of the AKS primality test paper, a conjecture about Sophie Germain primes is used to lower the worst-case complexity from O(log^(12)*n*) to O(log^6*n*). A later version of the paper is shown to have time complexity O(log^(7.5)*n*) which can also be lowered to O(log^6*n*) using the conjecture. Later variants of AKS have been proven to have complexity of O(log^6*n*) without any conjectures or use of Sophie Germain primes.

### Pseudorandom number generation

Safe primes obeying certain congruences can be used to generate pseudo-random numbers of use in Monte Carlo simulation.

Similarly, Sophie Germain primes may be used in the generation of pseudo-random numbers. The decimal expansion of 1/*q* will produce a stream of *q* − 1 pseudo-random digits, if *q* is the safe prime of a Sophie Germain prime *p*, with *p* congruent to 3, 9, or 11 modulo 20. Thus "suitable" prime numbers *q* are 7, 23, 47, 59, 167, 179, etc. ((sequence A000353 in the OEIS)) (corresponding to *p* = 3, 11, 23, 29, 83, 89, etc.) ((sequence A000355 in the OEIS)). The result is a stream of length *q* − 1 digits (including leading zeros). So, for example, using *q* = 23 generates the pseudo-random digits 0, 4, 3, 4, 7, 8, 2, 6, 0, 8, 6, 9, 5, 6, 5, 2, 1, 7, 3, 9, 1, 3. Note that these digits are not appropriate for cryptographic purposes, as the value of each can be derived from its predecessor in the digit-stream.

## In popular culture

Sophie Germain primes are mentioned in the stage play *Proof* and the subsequent film.
