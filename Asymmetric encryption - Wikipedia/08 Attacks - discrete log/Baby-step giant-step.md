# Baby-step giant-step

Source: <https://en.wikipedia.org/wiki/Baby-step_giant-step>

In group theory, a branch of mathematics, the **baby-step giant-step** is a meet-in-the-middle algorithm for computing the discrete logarithm or order of an element in a finite abelian group by Daniel Shanks. The discrete log problem is of fundamental importance to the area of public key cryptography.

Many of the most commonly used cryptography systems are based on the assumption that the discrete log is extremely difficult to compute; the more difficult it is, the more security it provides a data transfer. One way to increase the difficulty of the discrete log problem is to base the cryptosystem on a larger group.

## Theory

The algorithm is based on a space–time tradeoff. It is a fairly simple modification of trial multiplication, the naive method of finding discrete logarithms.

Given a cyclic group $G$ of order $n$, a generator $\alpha$ of the group and a group element $\beta$, the problem is to find an integer $x$ such that
    $\alpha^x = \beta\,.$

The baby-step giant-step algorithm is based on rewriting $x$:
    $x = im + j$
    $m = \left\lceil \sqrt{n} \right\rceil$
    $0 \leq i < m$
    $0 \leq j < m$

Therefore, we have:
    $\alpha^x = \beta\,$
    $\alpha^{im + j} = \beta\,$
    $\alpha^j = \beta\left(\alpha^{-m}\right)^i\,$

The algorithm precomputes $\alpha^j$ for several values of $j$. Then it fixes an $m$ and tries values of $i$ in the right-hand side of the congruence above, in the manner of trial multiplication. It tests to see if the congruence is satisfied for any value of $j$, using the precomputed values of $\alpha^j$.

## The algorithm

**Input**: A cyclic group *G* of order *n*, having a generator *α* and an element *β*.

**Output**: A value *x* satisfying $\alpha^x = \beta$.

1. *m* ← Ceiling(√*n*)
2. For all *j* where 0 ≤ *j* < *m*:

  1. Compute *α*^(*j*) and store the pair (*j*, *α*^(*j*)) in a table. (See § In practice)

3. Compute *α*^(−*m*).
4. *γ* ← *β*. (set *γ* = *β*)
5. For all *i* where 0 ≤ *i* < *m*:

  1. Check to see if γ is the second component (*α*^(*j*)) of any pair in the table.
  2. If so, return *im* + *j*.
  3. If not, *γ* ← *γ* • *α*^(−*m*).

## In practice

The best way to speed up the baby-step giant-step algorithm is to use an efficient table lookup scheme. The best in this case is a hash table. The hashing is done on the second component, and to perform the check in step 1 of the main loop, γ is hashed and the resulting memory address checked. Since hash tables can retrieve and add elements in $O(1)$ time (constant time), this does not slow down the overall baby-step giant-step algorithm.

The space complexity of the algorithm is $O(\sqrt n)$, while the time complexity of the algorithm is $O(\sqrt n)$. This running time is better than the $O(n)$ running time of the naive brute force calculation.

The baby-step giant-step algorithm could be used by an eavesdropper to derive the private key generated in the Diffie Hellman key exchange, when the modulus is a prime number that is not too large. If the modulus is not prime, the Pohlig–Hellman algorithm has a smaller algorithmic complexity, and potentially solves the same problem.
