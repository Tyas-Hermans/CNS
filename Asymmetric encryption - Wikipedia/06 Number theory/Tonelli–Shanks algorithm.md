# Tonelli–Shanks algorithm

Source: <https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm>

The **Tonelli–Shanks** algorithm (referred to by Shanks as the RESSOL algorithm) is used in modular arithmetic to solve for *r* in a congruence of the form *r*^2 ≡ *n* (mod *p*), where *p* is a prime: that is, to find a square root of *n* modulo *p*.

The Tonelli–Shanks algorithm cannot be used for composite moduli: finding square roots modulo composite numbers is a computational problem equivalent to integer factorization.

An equivalent, but slightly more redundant version of this algorithm was developed by Alberto Tonelli in 1891. The version discussed here was developed independently by Daniel Shanks in 1973, who explained:

My tardiness in learning of these historical references was because I had lent Volume 1 of Dickson's History to a friend and it was never returned.

According to Dickson, Tonelli's algorithm can take square roots of *x* modulo prime powers *p^λ* apart from primes.

## Core ideas

Given a non-zero $n$ and a prime $p > 2$ (which will always be odd), Euler's criterion tells us that $n$ has a square root (i.e., $n$ is a quadratic residue) if and only if:
    $n^{\frac{p-1}{2}} \equiv 1 \pmod p$.

In contrast, if a number $z$ has no square root (is a non-residue), Euler's criterion tells us that:
    $z^{\frac{p-1}{2}} \equiv -1 \pmod p$.

It is not hard to find such $z$, because half of the integers between 1 and $p-1$ have this property. So we assume that we have access to such a non-residue.

By (normally) dividing by 2 repeatedly, we can write $p-1$ as $Q 2^S$, where $Q$ is odd. Note that if we try
    $R \equiv n^{\frac{Q+1}{2}} \pmod p$,

then $R^2 \equiv n^{Q+1} = (n)(n^Q) \pmod p$. If $t \equiv n^Q \equiv 1 \pmod p$, then $R$ is a square root of $n$. Otherwise, for $M = S$, we have $R$ and $t$ satisfying:

- $R^2 \equiv nt \pmod p$; and
- $t$ is a $2^{M-1}$-th root of 1 (because $t^{2^{M-1}} = t^{2^{S-1}} \equiv n^{Q 2^{S-1}} = n^{\frac{p-1}{2}}$).

If, given a choice of $R$ and $t$ for a particular $M$ satisfying the above (where $R$ is not a square root of $n$), we can easily calculate another $R$ and $t$ for $M - 1$ such that the above relations hold, then we can repeat this until $t$ becomes a $2^0$-th root of 1, i.e., $t = 1$. At that point $R$ is a square root of $n$.

We can check whether $t$ is a $2^{M-2}$-th root of 1 by squaring it $M-2$ times and check whether it is 1. If it is, then we do not need to do anything, as the same choice of $R$ and $t$ works. But if it is not, $t^{2^{M-2}}$ must be -1 (because squaring it gives 1, and there can only be two square roots 1 and -1 of 1 modulo $p$).

To find a new pair of $R$ and $t$, we can multiply $R$ by a factor $b$, to be determined. Then $t$ must be multiplied by a factor $b^2$ to keep $R^2 \equiv nt \pmod p$. So, when $t^{2^{M-2}}$ is -1, we need to find a factor $b^2$ so that $tb^2$ is a $2^{M-2}$-th root of 1, or equivalently $b^2$ is a $2^{M-2}$-th root of -1.

The trick here is to make use of $z$, the known non-residue. The Euler's criterion applied to $z$ shown above says that $z^Q$ is a $2^{S-1}$-th root of -1. So by squaring $z^Q$ repeatedly, we have access to a sequence of $2^i$-th roots of -1. We can select the right one to serve as $b$. With a little bit of variable maintenance and trivial case compression, the algorithm below emerges naturally.

## The algorithm

Operations and comparisons on elements of the multiplicative group of integers modulo p $\mathbb{Z}/p\mathbb{Z}$ are implicitly mod *p*.

**Inputs**:

- *p*, a prime
- *n*, an element of $\mathbb{Z}/p\mathbb{Z}$ such that solutions to the congruence *r*^2 = *n* exist; when this is so we say that *n* is a quadratic residue mod *p*.

**Outputs**:

- *r* in $\mathbb{Z}/p\mathbb{Z}$ such that *r*^2 = *n*

**Algorithm**:

1. By factoring out powers of 2, find *Q* and *S* such that $p-1=Q 2^S$ with *Q* odd
2. Search for a *z* in $\mathbb{Z}/p\mathbb{Z}$ which is a quadratic non-residue

  - Half of the elements in the set will be quadratic non-residues
  - Candidates can be tested with Euler's criterion or by finding the Jacobi symbol

3. Let
    $\begin{align} M &\leftarrow S \\ c &\leftarrow z^Q \\ t &\leftarrow n^Q \\ R &\leftarrow n^\frac{Q+1}{2} \end{align}$
4. Loop:

  - If *t* = 0, return *r* = *0*
  - If *t* = 1, return *r* = *R*
  - Otherwise, use repeated squaring to find the least *i*, 0 < *i* < *M*, such that $t^{2^i} = 1$
  - Let $b \leftarrow c^{2^{M-i-1}}$, and set
    $\begin{align} M &\leftarrow i \\ c &\leftarrow b^2 \\ t &\leftarrow tb^2 \\ R &\leftarrow Rb \end{align}$

Once you have solved the congruence with *r* the second solution is $-r \pmod p$. If the least *i* such that $t^{2^i} = 1$ is *M*, then no solution to the congruence exists, i.e. *n* is not a quadratic residue.

This is most useful when *p* ≡ 1 (mod 4).

For primes such that *p* ≡ 3 (mod 4), this problem has possible solutions $r = \pm n^{\frac{p+1}{4}}\pmod p$. If these satisfy $r^2 \equiv n \pmod p$, they are the only solutions. If not, $r^2 \equiv -n \pmod p$, *n* is a quadratic non-residue, and there are no solutions.

## Proof

We can show that at the start of each iteration of the loop the following loop invariants hold:

- $c^{2^{M-1}} = -1$
- $t^{2^{M-1}} = 1$
- $R^2 = tn$

Initially:

- $c^{2^{M-1}} = z^{Q2^{S-1}} = z^\frac{p-1}{2} = -1$ (since *z* is a quadratic nonresidue, per Euler's criterion)
- $t^{2^{M-1}} = n^{Q2^{S-1}} = n^\frac{p-1}{2} = 1$ (since *n* is a quadratic residue)
- $R^2 = n^{Q+1} = tn$

At each iteration, with *M' *, *c' *, *t' *, *R' * the new values replacing *M*, *c*, *t*, *R*:

- $c'^{2^{M'-1}} = (b^2)^{2^{i-1}} = c^{2^{M-i}2^{i-1}} = c^{2^{M-1}} = -1$
- $t'^{2^{M'-1}} = (tb^2)^{2^{i-1}} = t^{2^{i-1}}b^{2^i} = -1 \cdot -1 = 1$

  - $t^{2^{i-1}} = -1$ since we have that $t^{2^i} = 1$ but $t^{2^{i-1}} \neq 1$ (*i* is the least value such that $t^{2^i} = 1$)
  - $b^{2^i} = c^{2^{M-i-1}2^i}= c^{2^{M-1}} = -1$

- $R'^2 = R^2b^2 = tnb^2 = t'n$

From $t^{2^{M-1}} = 1$ and the test against *t* = 1 at the start of the loop, we see that we will always find an *i* in 0 < *i* < *M* such that $t^{2^i} = 1$. *M* is strictly smaller on each iteration, and thus the algorithm is guaranteed to halt. When we hit the condition *t* = 1 and halt, the last loop invariant implies that *R*^2 = *n*.

### Order of *t*

We can alternately express the loop invariants using the order of the elements:

- $\operatorname{ord}(c) = 2^M$
- $\operatorname{ord}(t) | 2^{M-1}$
- $R^2 = tn$ as before

Each step of the algorithm moves *t* into a smaller subgroup by measuring the exact order of *t* and multiplying it by an element of the same order.

## Example

Solving the congruence *r*^2 ≡ 5 (mod 41). 41 is prime as required and 41 ≡ 1 (mod 4). 5 is a quadratic residue by Euler's criterion: $5^{\frac{41-1}{2}} = 5^{20} = 1$ (as before, operations in $(\mathbb{Z}/41\mathbb{Z})^\times$ are implicitly mod 41).

1. $p-1 = 40 = 5 \cdot 2^3$ so $Q \leftarrow 5$, $S \leftarrow 3$
2. Find a value for z:

  - $2^{\frac{41-1}{2}} = 1$, so 2 is a quadratic residue by Euler's criterion.
  - $3^{\frac{41-1}{2}} = 40 = -1$, so 3 is a quadratic nonresidue: set $z \leftarrow 3$

3. Set

  - $M \leftarrow S = 3$
  - $c \leftarrow z^Q = 3^5 = 38$
  - $t \leftarrow n^Q = 5^5 = 9$
  - $R \leftarrow n^{\frac{Q+1}{2}} = 5^{\frac{5+1}{2}} = 2$

4. Loop:

  - First iteration:

    - $t \neq 1$, so we're not finished
    - $t^{2^1} = 40$, $t^{2^2} = 1$ so $i \leftarrow 2$
    - $b \leftarrow c^{2^{M-i-1}} = 38^{2^{3-2-1}} = 38$
    - $M \leftarrow i = 2$
    - $c \leftarrow b^2 = 38^2 = 9$
    - $t \leftarrow tb^2 = 9 \cdot 9 = 40$
    - $R \leftarrow Rb = 2 \cdot 38 = 35$

  - Second iteration:

    - $t \neq 1$, so we're still not finished
    - $t^{2^1} = 1$ so $i \leftarrow 1$
    - $b \leftarrow c^{2^{M-i-1}} = 9^{2^{2-1-1}} = 9$
    - $M \leftarrow i = 1$
    - $c \leftarrow b^2 = 9^2 = 40$
    - $t \leftarrow tb^2 = 40 \cdot 40 = 1$
    - $R \leftarrow Rb = 35 \cdot 9 = 28$

  - Third iteration:

    - $t = 1$, and we are finished; return $r = R = 28$

Indeed, 28^2 ≡ 5 (mod 41) and (−28)^2 ≡ 13^2 ≡ 5 (mod 41). So the algorithm yields the two solutions to our congruence.

## Speed of the algorithm

The Tonelli–Shanks algorithm requires (on average over all possible input (quadratic residues and quadratic nonresidues))
    $2m+2k+\frac{S(S-1)}{4} +\frac{1}{2^{S-1}} - 9$

modular multiplications, where $m$ is the number of digits in the binary representation of $p$ and $k$ is the number of ones in the binary representation of $p$. If the required quadratic nonresidue $z$ is to be found by checking if a randomly taken number $y$ is a quadratic nonresidue, it requires (on average) $2$ computations of the Legendre symbol. The average of two computations of the Legendre symbol are explained as follows: $y$ is a quadratic residue with chance $\tfrac{\tfrac{p+1}{2}}{p} = \tfrac{1 + \tfrac{1}{p}}{2}$, which is smaller than $1$ but $\geq \tfrac{1}{2}$, so we will on average need to check if a $y$ is a quadratic residue two times.

This shows essentially that the Tonelli–Shanks algorithm works very well if the modulus $p$ is random, that is, if $S$ is not particularly large with respect to the number of digits in the binary representation of $p$. As written above, Cipolla's algorithm works better than Tonelli–Shanks if (and only if) $S(S-1) > 8m + 20$. However, if one instead uses Sutherland's algorithm to perform the discrete logarithm computation in the 2-Sylow subgroup of $\mathbb{F}_p^{\ast}$, one may replace $S(S-1)$ with an expression that is asymptotically bounded by $O(S\log S/\log\log S)$. Explicitly, one computes $e$ such that $c^e\equiv n^Q$ and then $R\equiv c^{-e/2} n^{(Q+1)/2}$ satisfies $R^2\equiv n$ (note that $e$ is a multiple of 2 because $n$ is a quadratic residue).

The algorithm requires us to find a quadratic nonresidue $z$. There is no known deterministic algorithm that runs in polynomial time for finding such a $z$. However, if the generalized Riemann hypothesis is true, there exists a quadratic nonresidue $z < 2\ln^2{p}$, making it possible to check every $z$ up to that limit and find a suitable $z$ within polynomial time. Keep in mind, however, that this is a worst-case scenario; in general, $z$ is found in on average 2 trials as stated above.

## Uses

The Tonelli–Shanks algorithm can (naturally) be used for any process in which square roots modulo a prime are necessary. For example, it can be used for finding points on elliptic curves. It is also useful for the computations in the Rabin signature algorithm and in the sieving step of the quadratic sieve.

## Generalizations

Tonelli–Shanks can be generalized to any cyclic group (instead of $(\mathbb{Z}/p\mathbb{Z})^\times$) and to *k*th roots for arbitrary integer *k*, in particular to taking the *k*th root of an element of a finite field.

If many square-roots must be done in the same cyclic group and S is not too large, a table of square-roots of the elements of 2-power order can be prepared in advance and the algorithm simplified and sped up as follows.

1. Factor out powers of 2 from *p* − 1, defining *Q* and *S* as: $p-1 = Q2^S$ with *Q* odd.
2. Let $R \leftarrow n^{\frac{Q+1}{2}}, t\leftarrow n^Q \equiv R^2/n$
3. Find $b$ from the table such that $b^2 \equiv t$ and set $R \equiv R/b$
4. return *R*.

### Tonelli's algorithm will work on mod *p^λ*

According to Dickson's "Theory of Numbers"

A. Tonelli gave an explicit formula for the roots of $x^{2}=c \pmod{ p^{\lambda}}$

The Dickson reference shows the following formula for the square root of $x^{2}\bmod{p^{\lambda}}$.
when $p=4\cdot7+1$, or $s=2$ (s must be 2 for this equation) and $a=7$ such that $29=2^{2}\cdot7+1$
for $x^{2}\bmod{p^{\lambda}}\equiv c$ then
    $x \bmod{p^{\lambda}}\equiv \pm (c^{a}+3)^{\beta}\cdot c^{(\beta+1)/2}$ where $\beta \equiv a\cdot p^{\lambda-1}$

Noting that $23^{2} \bmod{ 29^{3}}\equiv 529$ and noting that $\beta = 7\cdot29^{2}$ then
    $(529^{7} + 3)^{7\cdot 29^{2}}\cdot 529^{(7\cdot29^{2} + 1)/2}\bmod{ 29^{3}}\equiv 24366 \equiv -23$

To take another example: $2333^{2} \bmod{ 29^{3}}\equiv 4142$ and

    $(4142^{7} + 3)^{7 \cdot29^{2}}\cdot 4142^{(7\cdot29^{2} + 1)/2}\bmod{ 29^{3}}\equiv 2333$

Dickson also attributes the following equation to Tonelli:
    $X\bmod{p^{\lambda}}\equiv x^{p^{\lambda-1}}\cdot c^{(p^{\lambda}-2p^{\lambda-1}+1)/2}$ where $X^{2}\bmod{p^{\lambda}}\equiv c$ and $x^{2}\bmod{p}\equiv c$;

Using $p=23$ and using the modulus of $p^{3}$ the math follows:
    $1115^{2}\bmod{ 23^{3}}=2191$

First, find the modular square root mod $p$ which can be done by the regular Tonelli algorithm for one or the other roots:
    $1115^{2}\bmod{ 23}\equiv 6$ and thus $\sqrt{6}\bmod{23}\equiv 11$

And applying Tonelli's equation (see above):
    $11^{23^{2}}\cdot 2191^{(23^{3} - 2 \cdot23^{2} + 1)/2}\bmod {23^{3}} \equiv 1115$

Dickson's reference clearly shows that Tonelli's algorithm works on moduli of $p^{\lambda}$.
