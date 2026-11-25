# Carmichael function

Source: <https://en.wikipedia.org/wiki/Carmichael_function>

In number theory, a branch of mathematics, the **Carmichael function**  *λ*(*n*) of a positive integer  n is the smallest positive integer m such that

$$ a^m \equiv 1 \pmod{n} $$

holds for every integer  a coprime to  n. In algebraic terms,  *λ*(*n*) is the exponent of the multiplicative group of integers modulo  n. As this is a finite abelian group, there must exist an element whose order equals the exponent,  *λ*(*n*). Such an element is called a **primitive  *λ*-root modulo  n**.

The Carmichael function is named after the American mathematician Robert Carmichael who defined it in 1910. It is also known as **Carmichael's  λ function**, the **reduced totient function**, and the **least universal exponent function**.

The order of the multiplicative group of integers modulo  n is  *φ*(*n*), where  φ is Euler's totient function. Since the order of an element of a finite group divides the order of the group,  *λ*(*n*) divides  *φ*(*n*). The following table compares the first 36 values of  *λ*(*n*) (sequence A002322 in the OEIS) and  *φ*(*n*) (in **bold** if they are different; the values of n such that they are different are listed in (sequence A033949 in the OEIS)).

|   n |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 |  10 |  11 |  12 |  13 |  14 |  15 |  16 |  17 |  18 |  19 |  20 |  21 |  22 |  23 |  24 |  25 |  26 |  27 |  28 |  29 |  30 |  31 |  32 |  33 |  34 |  35 |  36 |
|   *λ*(*n*) |  1 | 1 | 2 | 2 | 4 | 2 | 6 | **2** | 6 | 4 | 10 | **2** | 12 | 6 | **4** | **4** | 16 | 6 | 18 | **4** | **6** | 10 | 22 | **2** | 20 | 12 | 18 | **6** | 28 | **4** | 30 | **8** | **10** | 16 | **12** | **6** |
|   *φ*(*n*) |  1 | 1 | 2 | 2 | 4 | 2 | 6 | **4** | 6 | 4 | 10 | **4** | 12 | 6 | **8** | **8** | 16 | 6 | 18 | **8** | **12** | 10 | 22 | **8** | 20 | 12 | 18 | **12** | 28 | **8** | 30 | **16** | **20** | 16 | **24** | **12** |

## Numerical examples

-  *n* = 5. The set of numbers less than and coprime to 5 is  {1,2,3,4}. Hence Euler's totient function has value  *φ*(5) = 4 and the value of Carmichael's function,  *λ*(5), must be a divisor of 4. The divisor 1 does not satisfy the definition of Carmichael's function since $a^1 \not\equiv 1\pmod{5}$ except for $a\equiv1\pmod{5}$. Neither does 2 since $2^2 \equiv 3^2 \equiv 4 \not\equiv 1\pmod{5}$. Hence  *λ*(5) = 4. Indeed, $1^4\equiv 2^4\equiv 3^4\equiv 4^4\equiv1\pmod{5}$. Both 2 and 3 are primitive  λ-roots modulo 5 and also primitive roots modulo 5.
-  *n* = 8. The set of numbers less than and coprime to 8 is  {1,3,5,7} . Hence  *φ*(8) = 4 and  *λ*(8) must be a divisor of 4. In fact  *λ*(8) = 2 since $1^2\equiv 3^2\equiv 5^2\equiv 7^2\equiv1\pmod{8}$. The primitive  λ-roots modulo 8 are 3, 5, and 7. There are no primitive roots modulo 8.

## Recurrence for  *λ*(*n*)

The Carmichael lambda function of a prime power can be expressed in terms of the Euler totient. Any number that is not 1 or a prime power can be written uniquely as the product of distinct prime powers, in which case  λ of the product is the least common multiple of the  λ of the prime power factors. Specifically,  *λ*(*n*) is given by the recurrence

$$ \lambda(n) = \begin{cases} \varphi(n) & \text{if }n\text{ is 1, 2, 4, or a power of an odd prime,}\\ \tfrac12\varphi(n) & \text{if }n=2^r,\ r\ge3,\\ \operatorname{lcm}\Bigl(\lambda(n_1),\lambda(n_2),\ldots,\lambda(n_k)\Bigr) & \text{if }n=n_1n_2\ldots n_k\text{ where }n_1,n_2,\ldots,n_k\text{ are powers of distinct primes.} \end{cases} $$

Euler's totient for a prime power, that is, a number  *p*^(*r*) with  *p* prime and  *r* ≥ 1, is given by

$$ \varphi(p^r) = p^{r-1}(p-1). $$

##  Carmichael's theorems

Carmichael proved two theorems that, together, establish that if  *λ*(*n*) is considered as defined by the recurrence of the previous section, then it satisfies the property stated in the introduction, namely that it is the smallest positive integer  m such that $a^m\equiv 1\pmod{n}$ for all  a relatively prime to  n.

**Theorem 1**—If  a is relatively prime to  n then $a^{\lambda(n)}\equiv 1\pmod{n}$.

This implies that the order of every element of the multiplicative group of integers modulo  n divides  *λ*(*n*). Carmichael calls an element  a for which $a^{\lambda(n)}$ is the least power of  a congruent to 1 (mod  n) a *primitive  λ-root modulo  n*. (This is not to be confused with a primitive root modulo  n, which Carmichael sometimes refers to as a primitive $\varphi$-root modulo  n.)

**Theorem 2**—For every positive integer  n there exists a primitive  λ-root modulo  n. Moreover, if  g is such a root, then there are $\varphi(\lambda(n))$ primitive  λ-roots that are congruent to powers of  g.

If  g is one of the primitive  λ-roots guaranteed by the theorem, then $g^m\equiv1\pmod{n}$ has no positive integer solutions  m less than  *λ*(*n*), showing that there is no positive  *m* < *λ*(*n*) such that $a^m\equiv 1\pmod{n}$ for all  a relatively prime to  n.

The second statement of Theorem 2 does not imply that all primitive  λ-roots modulo  n are congruent to powers of a single root  g. For example, if  *n* = 15, then  *λ*(*n*) = 4 while $\varphi(n)=8$ and $\varphi(\lambda(n))=2$. There are four primitive  λ-roots modulo 15, namely 2, 7, 8, and 13 as $1\equiv2^4\equiv8^4\equiv7^4\equiv13^4$. The roots 2 and 8 are congruent to powers of each other and the roots 7 and 13 are congruent to powers of each other, but neither 7 nor 13 is congruent to a power of 2 or 8 and vice versa. The other four elements of the multiplicative group modulo 15, namely 1, 4 (which satisfies $4\equiv2^2\equiv8^2\equiv7^2\equiv13^2$), 11, and 14, are not primitive  λ-roots modulo 15.

For a contrasting example, if  *n* = 9, then $\lambda(n)=\varphi(n)=6$ and $\varphi(\lambda(n))=2$. There are two primitive  λ-roots modulo 9, namely 2 and 5, each of which is congruent to the fifth power of the other. They are also both primitive $\varphi$-roots modulo 9.

The numbers of primitive  λ-roots modulo  n for $n=1,2,3,\cdots$ are 1, 1, 1, 1, 2, 1, 2, 3, 2, 2, 4, 3, 4, 2, 4, 4, 8, 2, 6, 4, 6, 4, 10, 7, 8, 4, 6, 6, 12, 4, 8, 8, 12, 8, 8, 6, 12, 6, 8, 8, 16, 6, 12, 12, 8, 10, 22, 8, 12, 8, ... (sequence A111725 in the OEIS)

## Properties of the Carmichael function

In this section, an integer $n$ is divisible by a nonzero integer $m$ if there exists an integer $k$ such that $n = km$. This is written as

$$ m \mid n. $$

### A consequence of minimality of  *λ*(*n*)

Suppose  *a^m* ≡ 1 (mod *n*) for all numbers  a coprime with  n. Then  *λ*(*n*) | *m*.

**Proof:** If  *m* = *kλ*(*n*) + *r* with  0 ≤ *r* < *λ*(*n*), then

$$ a^r = 1^k \cdot a^r \equiv \left(a^{\lambda(n)}\right)^k\cdot a^r = a^{k\lambda(n)+r} = a^m \equiv 1\pmod{n} $$

for all numbers  a coprime with  n. It follows that *r* = 0 since  *r* < *λ*(*n*) and  *λ*(*n*) is the minimal positive exponent for which the congruence holds for all  a coprime with  n.

###  *λ*(*n*) divides  *φ*(*n*)

This follows from elementary group theory, because the exponent of any finite group must divide the order of the group.  *λ*(*n*) is the exponent of the multiplicative group of integers modulo  n while  *φ*(*n*) is the order of that group. In particular, the two must be equal in the cases where the multiplicative group is cyclic due to the existence of a primitive root, which is the case for odd prime powers.

We can thus view Carmichael's theorem as a sharpening of Euler's theorem.

### Divisibility

$$ a\,|\,b \Rightarrow \lambda(a)\,|\,\lambda(b) $$

**Proof.**

By definition, for any integer $k$ with $\gcd(k,b) = 1$ (and thus also $\gcd(k,a) = 1$), we have that $b \,|\, (k^{\lambda(b)} - 1)$ , and therefore $a \,|\, (k^{\lambda(b)} - 1)$. This establishes that $k^{\lambda(b)}\equiv1\pmod{a}$ for all  k relatively prime to  a. By the consequence of minimality proved above, we have $\lambda(a)\,|\,\lambda(b)$.

### Composition

For all positive integers  a and  b it holds that

$$ \lambda(\mathrm{lcm}(a,b)) = \mathrm{lcm}(\lambda(a), \lambda(b)). $$

This is an immediate consequence of the recurrence for the Carmichael function.

### Exponential cycle length

If $r_{\mathrm{max}}=\max_i\{r_i\}$ is the biggest exponent in the prime factorization $n= p_1^{r_1}p_2^{r_2} \cdots p_{k}^{r_k}$ of  n, then for all  a (including those not coprime to  n) and all  *r* ≥ *r*_(max),

$$ a^r \equiv a^{\lambda(n)+r} \pmod n. $$

In particular, for square-free  n ( *r*_(max) = 1), for all  a we have

$$ a \equiv a^{\lambda(n)+1} \pmod n. $$

### Average value

For any  *n* ≥ 16:

$$ \frac{1}{n} \sum_{i \leq n} \lambda (i) = \frac{n}{\ln n} e^{B (1+o(1)) \ln\ln n / (\ln\ln\ln n) } $$

(called Erdős approximation in the following) with the constant

$$ B := e^{-\gamma} \prod_{p\in\mathbb P} \left({1 - \frac{1}{(p-1)^2(p+1)}}\right) \approx 0.34537 $$

and  *γ* ≈ 0.57721, the Euler–Mascheroni constant.

The following table gives some overview over the first 2^(26) – 1 = 67108863 values of the  λ function, for both, the exact average and its Erdős-approximation.

Additionally given is some overview over the more easily accessible “logarithm over logarithm” values LoL(*n*) := ln *λ*(*n*)/ln *n* with

-  LoL(*n*) > 4/5 ⇔ *λ*(*n*) > *n*^(4/5).

There, the table entry in row number 26 at column

-  % LoL > 4/5   → 60.49

indicates that 60.49% (≈ 40000000) of the integers  1 ≤ *n* ≤ 67108863 have  *λ*(*n*) > *n*^(4/5) meaning that the majority of the  λ values is exponential in the length  *l* := log_2(*n*) of the input  n, namely

$$ \left(2^\frac45\right)^l = 2^\frac{4l}{5} = \left(2^l\right)^\frac45 = n^\frac45. $$

|   ν | *n* = 2^(*ν*) – 1 | sum
$\sum_{i\le n} \lambda(i)$ | average
$\tfrac1n \sum_{i\le n} \lambda(i)$ | Erdős average | Erdős /
exact average |  LoL average | %  LoL > 4/5 | %  LoL > 7/8 |
|  5 | 31 | 270 | 8.709677 | 68.643 | 7.8813 | 0.678244 | 41.94 | 35.48 |
|  6 | 63 | 964 | 15.301587 | 61.414 | 4.0136 | 0.699891 | 38.10 | 30.16 |
|  7 | 127 | 3574 | 28.141732 | 86.605 | 3.0774 | 0.717291 | 38.58 | 27.56 |
|  8 | 255 | 12994 | 50.956863 | 138.190 | 2.7119 | 0.730331 | 38.82 | 23.53 |
|  9 | 511 | 48032 | 93.996086 | 233.149 | 2.4804 | 0.740498 | 40.90 | 25.05 |
|  10 | 1023 | 178816 | 174.795699 | 406.145 | 2.3235 | 0.748482 | 41.45 | 26.98 |
|  11 | 2047 | 662952 | 323.865169 | 722.526 | 2.2309 | 0.754886 | 42.84 | 27.70 |
|  12 | 4095 | 2490948 | 608.290110 | 1304.810 | 2.1450 | 0.761027 | 43.74 | 28.11 |
|  13 | 8191 | 9382764 | 1145.496765 | 2383.263 | 2.0806 | 0.766571 | 44.33 | 28.60 |
|  14 | 16383 | 35504586 | 2167.160227 | 4392.129 | 2.0267 | 0.771695 | 46.10 | 29.52 |
|  15 | 32767 | 134736824 | 4111.967040 | 8153.054 | 1.9828 | 0.776437 | 47.21 | 29.15 |
|  16 | 65535 | 513758796 | 7839.456718 | 15225.430 | 1.9422 | 0.781064 | 49.13 | 28.17 |
|  17 | 131071 | 1964413592 | 14987.400660 | 28576.970 | 1.9067 | 0.785401 | 50.43 | 29.55 |
|  18 | 262143 | 7529218208 | 28721.797680 | 53869.760 | 1.8756 | 0.789561 | 51.17 | 30.67 |
|  19 | 524287 | 28935644342 | 55190.466940 | 101930.900 | 1.8469 | 0.793536 | 52.62 | 31.45 |
|  20 | 1048575 | 111393101150 | 106232.840900 | 193507.100 | 1.8215 | 0.797351 | 53.74 | 31.83 |
|  21 | 2097151 | 429685077652 | 204889.909000 | 368427.600 | 1.7982 | 0.801018 | 54.97 | 32.18 |
|  22 | 4194303 | 1660388309120 | 395867.515800 | 703289.400 | 1.7766 | 0.804543 | 56.24 | 33.65 |
|  23 | 8388607 | 6425917227352 | 766029.118700 | 1345633.000 | 1.7566 | 0.807936 | 57.19 | 34.32 |
|  24 | 16777215 | 24906872655990 | 1484565.386000 | 2580070.000 | 1.7379 | 0.811204 | 58.49 | 34.43 |
|  25 | 33554431 | 96666595865430 | 2880889.140000 | 4956372.000 | 1.7204 | 0.814351 | 59.52 | 35.76 |
|  26 | 67108863 | 375619048086576 | 5597160.066000 | 9537863.000 | 1.7041 | 0.817384 | 60.49 | 36.73 |

### Prevailing interval

For all numbers  N and all but  *o*(*N*) positive integers  *n* ≤ *N* (a "prevailing" majority):

$$ \lambda(n) = \frac{n} {(\ln n)^{\ln\ln\ln n + A + o(1)}} $$

with the constant

$$ A := -1 + \sum_{p\in\mathbb P} \frac{\ln p}{(p-1)^2} \approx 0.2269688 $$

### Lower bounds

For any sufficiently large number  N and for any  Δ ≥ (ln ln *N*)^3, there are at most

$$ N\exp\left(-0.69(\Delta\ln\Delta)^\frac13\right) $$

positive integers  *n* ≤ N such that  *λ*(*n*) ≤ *ne*^(−Δ).

### Minimal order

For any sequence  *n*_1 < *n*_2 < *n*_3 < ⋯ of positive integers, any constant  0 < *c* < 1/ln 2, and any sufficiently large  i:

$$ \lambda(n_i) > \left(\ln n_i\right)^{c\ln\ln\ln n_i}. $$

### Small values

For a constant  c and any sufficiently large positive  A, there exists an integer  *n* > *A* such that

$$ \lambda(n)<\left(\ln A\right)^{c\ln\ln\ln A}. $$

Moreover,  n is of the form

$$ n=\mathop{\prod_{q \in \mathbb P}}_{(q-1)|m}q $$

for some square-free integer  *m* < (ln *A*)^(*c* ln ln ln *A*).

### Image of the function

The set of values of the Carmichael function has counting function

$$ \frac{x}{(\ln x)^{\eta+o(1)}} , $$

where

$$ \eta=1-\frac{1+\ln\ln2}{\ln2} \approx 0.08607 $$

## Use in cryptography

The Carmichael function is important in cryptography due to its use in the RSA encryption algorithm.

## Proof of Theorem 1

For  *n* = *p*, a prime, Theorem 1 is equivalent to Fermat's little theorem:

$$ a^{p-1}\equiv1\pmod{p}\qquad\text{for all }a\text{ coprime to }p. $$

For prime powers  *p*^(*r*),  *r* > 1, if

$$ a^{p^{r-1}(p-1)}=1+hp^r $$

holds for some integer  h, then raising both sides to the power  p gives

$$ a^{p^r(p-1)}=1+h'p^{r+1} $$

for some other integer $h'$. By induction it follows that $a^{\varphi(p^r)}\equiv1\pmod{p^r}$ for all  a relatively prime to  p and hence to  *p*^(*r*). This establishes the theorem for  *n* = 4 or any odd prime power.

### Sharpening the result for higher powers of two

For  a coprime to (powers of) 2 we have  *a* = 1 + 2*h*_2 for some integer  *h*_2. Then,

$$ a^2 = 1+4h_2(h_2+1) = 1+8\binom{h_2+1}{2}=:1+8h_3, $$

where $h_3$ is an integer. With *r* = 3, this is written

$$ a^{2^{r-2}} = 1+2^r h_r. $$

Squaring both sides gives

$$ a^{2^{r-1}}=\left(1+2^r h_r\right)^2=1+2^{r+1}\left(h_r+2^{r-1}h_r^2\right)=:1+2^{r+1}h_{r+1}, $$

where $h_{r+1}$ is an integer. It follows by induction that

$$ a^{2^{r-2}}=a^{\frac{1}{2}\varphi(2^r)}\equiv 1\pmod{2^r} $$

for all $r\ge3$ and all  a coprime to $2^r$.

### Integers with multiple prime factors

By the unique factorization theorem, any  *n* > 1 can be written in a unique way as

$$ n= p_1^{r_1}p_2^{r_2} \cdots p_{k}^{r_k} $$

where  *p*_1 < *p*_2 < ... < *p_k* are primes and  *r*_1, *r*_2, ..., *r_k* are positive integers. The results for prime powers establish that, for $1\le j\le k$,

$$ a^{\lambda\left(p_j^{r_j}\right)}\equiv1 \pmod{p_j^{r_j}}\qquad\text{for all }a\text{ coprime to }n\text{ and hence to }p_i^{r_i}. $$

From this it follows that

$$ a^{\lambda(n)}\equiv1 \pmod{p_j^{r_j}}\qquad\text{for all }a\text{ coprime to }n, $$

where, as given by the recurrence,

$$ \lambda(n) = \operatorname{lcm}\Bigl(\lambda\left(p_1^{r_1}\right),\lambda\left(p_2^{r_2}\right),\ldots,\lambda\left(p_k^{r_k}\right)\Bigr). $$

From the Chinese remainder theorem one concludes that

$$ a^{\lambda(n)}\equiv1 \pmod{n}\qquad\text{for all }a\text{ coprime to }n. $$

## See also

- Carmichael number
