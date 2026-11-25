# Trapdoor function

Source: <https://en.wikipedia.org/wiki/Trapdoor_function>

In theoretical computer science and cryptography, a **trapdoor function** is a function that is easy to compute in one direction, yet difficult to compute in the opposite direction (finding its inverse) without special information, called the "trapdoor". Trapdoor functions are a special case of one-way functions and are widely used in public-key cryptography.

In mathematical terms, if *f* is a trapdoor function, then there exists some secret information *t*, such that given *f*(*x*) and *t*, it is easy to compute *x*. Consider a padlock and its key. It is trivial to change the padlock from open to closed without using the key, by pushing the shackle into the lock mechanism. Opening the padlock easily, however, requires the key to be used. Here the key *t* is the trapdoor and the padlock is the trapdoor function.

An example of a simple mathematical trapdoor is "6895601 is the product of two prime numbers. What are those numbers?" A typical "brute-force" solution would be to try dividing 6895601 by many prime numbers until finding the answer. However, if one is told that 1931 is one of the numbers, one can find the answer by entering "6895601 ÷ 1931" into any calculator. This example is not a sturdy trapdoor function – modern computers can guess all of the possible answers within a second – but this sample problem could be improved by using the product of two much larger primes.

Trapdoor functions came to prominence in cryptography in the mid-1970s with the publication of asymmetric (or public-key) encryption techniques by Diffie, Hellman, and Merkle. Indeed, Diffie & Hellman (1976) coined the term. Several function classes had been proposed, and it soon became obvious that trapdoor functions are harder to find than was initially thought. For example, an early suggestion was to use schemes based on the subset sum problem. This turned out rather quickly to be unsuitable.

As of 2004, the best known trapdoor function (family) candidates are the RSA and Rabin families of functions. Both are written as exponentiation modulo a composite number, and both are related to the problem of prime factorization.

Functions related to the hardness of the discrete logarithm problem (either modulo a prime or in a group defined over an elliptic curve) are *not* known to be trapdoor functions, because there is no known "trapdoor" information about the group that enables the efficient computation of discrete logarithms.

A trapdoor in cryptography has the very specific aforementioned meaning and is not to be confused with a backdoor (these are frequently used interchangeably, which is incorrect). A backdoor is a deliberate mechanism that is added to a cryptographic algorithm (e.g., a key pair generation algorithm, digital signing algorithm, etc.) or operating system, for example, that permits one or more unauthorized parties to bypass or subvert the security of the system in some fashion.

## Definition

A **trapdoor function** is a collection of one-way functions { *f*_(*k*) : *D*_(*k*) → *R*_(*k*) } (*k* ∈ *K*), in which all of *K*, *D*_(*k*), *R*_(*k*) are subsets of binary strings {0, 1}^(*), satisfying the following conditions:

- There exists a probabilistic polynomial time (PPT) *sampling* algorithm Gen s.t. Gen(1^(*n*)) = (*k*, *t*_(*k*)) with *k* ∈ *K* ∩ {0, 1}^(*n*) and *t*_(*k*) ∈ {0, 1}^(*) satisfies | *t*_(*k*) | < *p* (*n*), in which *p* is some polynomial. Each *t*_(*k*) is called the *trapdoor* corresponding to *k*. Each trapdoor can be efficiently sampled.
- Given input *k*, there also exists a PPT algorithm that outputs *x* ∈ *D*_(*k*). That is, each *D*_(*k*) can be efficiently sampled.
- For any *k* ∈ *K*, there exists a PPT algorithm that correctly computes *f*_(*k*).
- For any *k* ∈ *K*, there exists a PPT algorithm *A* s.t. for any *x* ∈ *D*_(*k*), let *y* = *A* ( *k*, *f*_(*k*)(*x*), *t*_(*k*) ), and then we have *f*_(*k*)(*y*) = *f*_(*k*)(*x*). That is, given trapdoor, it is easy to invert.
- For any *k* ∈ *K*, without trapdoor *t*_(*k*), for any PPT algorithm, the probability to correctly invert *f*_(*k*) (i.e., given *f*_(*k*)(*x*), find a pre-image *x' * such that *f*_(*k*)(*x' *) = *f*_(*k*)(*x*)) is negligible.

If each function in the collection above is a one-way permutation, then the collection is also called a **trapdoor permutation**.

## Examples

In the following two examples, we always assume that it is difficult to factorize a large composite number (see Integer factorization).

### RSA assumption

In this example, the inverse $d$ of $e$ modulo $\phi(n)$ (Euler's totient function of $n$) is the trapdoor:
    $f(x) = x^e \mod n.$

If the factorization of $n=pq$ is known, then $\phi(n)=(p-1)(q-1)$ can be computed. With this the inverse $d$ of $e$ can be computed $d = e^{-1} \mod{\phi(n)}$, and then given $y = f(x)$, we can find $x = y^d \mod n = x^{ed} \mod n = x \mod n$. Its hardness follows from the RSA assumption.

### Rabin's quadratic residue assumption

Let $n$ be a large composite number such that $n = pq$, where $p$ and $q$ are large primes such that $p \equiv 3 \pmod{4}, q \equiv 3 \pmod{4}$, and kept confidential to the adversary. The problem is to compute $z$ given $a$ such that $a \equiv z^2 \pmod{n}$. The trapdoor is the factorization of $n$. With the trapdoor, the solutions of *z* can be given as $cx + dy, cx - dy, -cx + dy, -cx - dy$, where $a \equiv x^2 \pmod{p}, a \equiv y^2 \pmod{q}, c \equiv 1 \pmod{p}, c \equiv 0 \pmod{q}, d \equiv 0 \pmod{p}, d \equiv 1 \pmod{q}$. See Chinese remainder theorem for more details. Note that given primes $p$ and $q$, we can find $x \equiv a^{\frac{p+1}{4}} \pmod{p}$ and $y \equiv a^{\frac{q+1}{4}} \pmod{q}$. Here the conditions $p \equiv 3 \pmod{4}$ and $q \equiv 3 \pmod{4}$ guarantee that the solutions $x$ and $y$ can be well defined.

## See also

- One-way function
