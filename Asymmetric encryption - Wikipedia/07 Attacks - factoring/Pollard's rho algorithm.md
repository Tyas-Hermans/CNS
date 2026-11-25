# Pollard's rho algorithm

Source: <https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm>

**Pollard's rho algorithm** is an algorithm for integer factorization. It was invented by John Pollard in 1975. It uses only a small amount of space, and its expected running time is proportional to the square root of the smallest prime factor of the composite number being factorized.

## Core ideas

The algorithm is used to factorize a number $n = pq$, where $p$ is a non-trivial factor. A polynomial modulo $n$, called $g(x)$ (e.g., $g(x) = (x^2 + 1) \bmod n$), is used to generate a pseudorandom sequence. $g(x)$ must be a polynomial. A starting value, say 2, is chosen, and the sequence continues as $x_1 = g(2)$, $x_2 = g(g(2))$, $x_3 = g(g(g(2)))$, etc. The sequence is related to another sequence $\{x_k \bmod p\}$. Since $p$ is not known beforehand, this sequence cannot be explicitly computed in the algorithm. Yet in it lies the core idea of the algorithm.

Because the number of possible values for these sequences is finite, both the $\{x_k\}$ sequence, which is mod $n$, and $\{x_k \bmod p\}$ sequence will eventually repeat, even though these values are unknown. If the sequences were to behave like random numbers, the birthday paradox implies that the number of $x_k$ before a repetition occurs would be expected to be $O(\sqrt N)$, where $N$ is the number of possible values. So the sequence $\{x_k \bmod p\}$ will likely repeat much earlier than the sequence $\{x_k\}$. When one has found a $k_1,k_2$ such that $x_{k_1}\neq x_{k_2}$ but $x_{k_1}\equiv x_{k_2}\bmod p$, the number $|x_{k_1}-x_{k_2}|$ is a multiple of $p$, so a non-trivial divisor has been found.

Once a sequence has a repeated value, the sequence will cycle, because each value depends only on the one before it. This structure of eventual cycling gives rise to the name "rho algorithm", owing to similarity to the shape of the Greek letter *ρ* when the values $x_1 \bmod p$, $x_2 \bmod p$, etc. are represented as nodes in a directed graph.

This is detected by Floyd's cycle-finding algorithm: two nodes $i$ and $j$ (i.e., $x_i$ and $x_j$) are kept. In each step, one moves to the next node in the sequence and the other moves forward by two nodes. After that, it is checked whether $\gcd(x_i - x_j, n) \ne 1$. If it is not 1, then this implies that there is a repetition in the $\{x_k \bmod p\}$ sequence (i.e. $x_i \bmod p = x_j \bmod p)$. This works because if the $x_i \bmod p$ is the same as $x_j \bmod p$, the difference between $x_i$ and $x_j$ is necessarily a multiple of $p$. Although this always happens eventually, the resulting greatest common divisor (GCD) is a divisor of $n$ other than 1. This may be $n$ itself (if $x_i \bmod n$ equals $x_j \bmod n$) since the two sequences might repeat at the same time. In this (uncommon) case that the algorithm fails, it can be repeated with a different starting parameter $x_0$.

## Algorithm

The algorithm takes as its inputs n, the integer to be factored; and $g(x)$, a polynomial in x computed modulo n. In the original algorithm, $g(x) = (x^2 - 1) \bmod n$, but nowadays it is more common to use $g(x) = (x^2 + 1) \bmod n$. The output is either a non-trivial factor of n, or failure.

It performs the following steps:

Pseudocode for Pollard's rho algorithm

```
x ← 2 // starting value
y ← x
d ← 1

**while** d = 1:
x ← g(x)
y ← g(g(y))
d ← gcd(|x - y|, n)

**if** d = n:
**return failureelse**:
**return** d
```

Here x and y corresponds to $x_i$ and $x_j$ in the previous section. Note that this algorithm may fail to find a nontrivial factor even when n is composite. In that case, the method can be tried again, using a starting value of *x* other than 2 ($0 \leq x < n$) or a different $g(x)$, such as $g(x) = (x^2 + b) \bmod n$, with $1 \leq b < n$.

## Example factorization

Let $n = 8051$ and $g(x) = (x^2 + 1) \bmod{8051}$.

| i | x | y | gcd(|*x* − *y*|, 8051) |
|  1 | 5 | 26 | 1 |
|  2 | 26 | 7474 | 1 |
|  3 | 677 | 871 | 97 |
|  4 | 7474 | 1481 | 1 |

Now 97 is a non-trivial factor of 8051. Starting values other than *x* = *y* = 2 may give the cofactor (83) instead of 97. One extra iteration is shown above to make it clear that y moves twice as fast as x. Note that even after a repetition, the GCD can return to 1.

## Variants

In 1980, Richard Brent published a faster variant of the rho algorithm. He used the same core ideas as Pollard but a different method of cycle detection, replacing Floyd's cycle-finding algorithm with the related Brent's cycle finding method. CLRS (Cormen et Al. Introduction to Algorithms book) gives a heuristic analysis and failure conditions (the trivial divisor $n$ is found).

A further improvement was made by Pollard and Brent. They observed that if $\gcd(a,n) > 1$, then also $\gcd(ab,n) > 1$ for any positive integer $b$. In particular, instead of computing $\gcd (|x-y|,n)$ at every step, it suffices to define $z$ as the product of 100 consecutive $|x-y|$ terms modulo $n$, and then compute a single $\gcd(z,n)$. A major speed up results as 100 gcd steps are replaced with 99 multiplications modulo $n$ and a single gcd. Occasionally it may cause the algorithm to fail by introducing a repeated factor, for instance when $n$ is a square. But it then suffices to go back to the previous gcd term, where $\gcd(z,n)=1$, and use the regular *ρ* algorithm from there.

## Application

The algorithm is very fast for numbers with small factors, but slower in cases where all factors are large. The *ρ* algorithm's most remarkable success was the 1980 factorization of the Fermat number *F*_8 = 1238926361552897 × 93461639715357977769163558199606896584051237541638188580280321. The *ρ* algorithm was a good choice for *F*_8 because the prime factor *p* = 1238926361552897 is much smaller than the other factor. The factorization took 2 hours on a UNIVAC 1100/42.

## Example: factoring n = 10403 = 101 · 103

The following table shows numbers produced by the algorithm, starting with $x=2$ and using the polynomial $g(x) = (x^2 + 1) \bmod{10403}$. The third and fourth columns of the table contain additional information not known by the algorithm. They are included to show how the algorithm works.

| $x$ | $y$ | $x \bmod{101}$ | $y \bmod{101}$ | step |
|  2 | 2 | 2 | 2 | 0 |
|  5 | 2 | 5 | 2 | 1 |
|  26 | 2 | 26 | 2 | 2 |
|  677 | 26 | 71 | 26 | 3 |
|  598 | 26 | 93 | 26 | 4 |
|  3903 | 26 | 65 | 26 | 5 |
|  3418 | 26 | 85 | 26 | 6 |
|  156 | 3418 | 55 | 85 | 7 |
|  3531 | 3418 | 97 | 85 | 8 |
|  5168 | 3418 | 17 | 85 | 9 |
|  3724 | 3418 | 88 | 85 | 10 |
|  978 | 3418 | 69 | 85 | 11 |
|  9812 | 3418 | 15 | 85 | 12 |
|  5983 | 3418 | 24 | 85 | 13 |
|  9970 | 3418 | 72 | 85 | 14 |
|  236 | 9970 | 34 | 72 | 15 |
|  3682 | 9970 | 46 | 72 | 16 |
|  2016 | 9970 | 97 | 72 | 17 |
|  7087 | 9970 | 17 | 72 | 18 |
|  10289 | 9970 | 88 | 72 | 19 |
|  2594 | 9970 | 69 | 72 | 20 |
|  8499 | 9970 | 15 | 72 | 21 |
|  4973 | 9970 | 24 | 72 | 22 |
|  2799 | 9970 | 72 | **72** | 23 |

The first repetition modulo 101 is 97 which occurs in step 17. The repetition is not detected until step 23, when $x \equiv y \pmod{101}$. This causes $\gcd (x - y, n) = \gcd (2799 - 9970, n)$ to be $p = 101$, and a factor is found.

## Complexity

If the pseudorandom number $x = g(x)$ occurring in the Pollard *ρ* algorithm were an actual random number, it would follow that success would be achieved half the time, by the birthday paradox in $O(\sqrt p)\le O(n^{1/4})$ iterations. It is believed that the same analysis applies as well to the actual rho algorithm, but this is a heuristic claim, and rigorous analysis of the algorithm remains open.

## See also

- Pollard's rho algorithm for logarithms
- Pollard's kangaroo algorithm
