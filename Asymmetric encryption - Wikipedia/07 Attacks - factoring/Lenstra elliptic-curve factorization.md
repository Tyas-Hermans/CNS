# Lenstra elliptic-curve factorization

Source: <https://en.wikipedia.org/wiki/Lenstra_elliptic-curve_factorization>

The **Lenstra elliptic-curve factorization** or the **elliptic-curve factorization method** (**ECM**) is a fast, sub-exponential running time, algorithm for integer factorization, which employs elliptic curves. For general-purpose factoring, ECM is the third-fastest known factoring method. The second-fastest is the multiple polynomial quadratic sieve, and the fastest is the general number field sieve. The Lenstra elliptic-curve factorization is named after Hendrik Lenstra. It is an algebraic-group factorisation algorithm.

Practically speaking, ECM is considered a special-purpose factoring algorithm, as it is most suitable for finding small factors. Currently, it is still the best algorithm for divisors not exceeding 50 to 60 digits, as its running time is dominated by the size of the smallest factor *p* rather than by the size of the number *n* to be factored. Frequently, ECM is used to remove small factors from a very large integer with many factors; if the remaining integer is still composite, then it has only large factors and is factored using general-purpose techniques. The largest factor found using ECM so far has 83 decimal digits and was discovered on 7 September 2013 by R. Propper. Increasing the number of curves tested improves the chances of finding a factor, but they are not linear with the increase in the number of digits.

## Algorithm

### Background

Lenstra elliptic-curve factorization method uses a elliptic curve mod *n* (i.e. the number to be factored) and multiplies a random point *P* on it. The multiplication is based on elliptic curve point multiplication, which in turn is just the repeated addition of elliptic curve points, described in the article on elliptic curves. This addition would form a group in the non-modular case and in the case when *n* is prime, because $\mathbb{Z}/n\mathbb{Z}$ (the integers modulo $n$) forms a group when *n* is prime.

When modular numbers are used instead of the whole range of integers, the addition of two points on the same elliptic curve would involve taking the modular slope of a chord joining $P$ and $Q$, and thus division between residue classes modulo $n$, performed using the extended Euclidean algorithm. In particular, division by some $v \bmod n$ includes calculation of the $\gcd(v,n)$. Assuming we calculate a slope of the form $u/v$ with $\gcd(u,v)=1$, then if $v = 0 \bmod n$, the result of the point addition will be $\infty$, the point "at infinity" corresponding to the intersection of the "vertical" line joining $P(x,y), P'(x,-y)$ and the curve. However, if $\gcd(v,n) \neq 1, n$, then the point addition will not produce a meaningful point on the curve; but, more importantly, $\gcd(v,n)$ is a non-trivial factor of $n$: meaning that we have successfully factored the number.

The usual multiplication methods such as multiplication by doubling still apply. Naive successive addition is not required.

### Process

The Lenstra elliptic-curve factorization method to find a factor of a given natural number $n$ works as follows:

1. Pick a random elliptic curve over $\mathbb{Z}/n\mathbb{Z}$ (the integers modulo $n$), with equation of the form $y^2 = x^3 + ax + b \pmod n$ together with a non-trivial point $P(x_0,y_0)$ on it.
This can be done by first picking random $x_0,y_0,a \in \mathbb{Z}/n\mathbb{Z}$, and then setting $b = y_0^2 - x_0^3 - ax_0\pmod n$ to ensure the point is on the curve.
2. As discussed above, we have defined *addition* and *multiplication* of a point on the curve. With enough repeated additions, we should be able to cause a failure to add, thus finding us a factor. As a result, we compute $[k]P$ on the elliptic curve ($\bmod n$), where $k$ is a product of many small numbers.

  - k can be a product of small primes raised to small powers, as in the p-1 algorithm, or the factorial $B!$ for some not too large $B$. This can be done efficiently, one small factor at a time. Say, to get $[B!]P$, first compute $[2]P$, then $[3]([2]P)$, then $[4]([3!]P)$, and so on. $B$ is picked to be small enough so that $B$-wise point addition can be performed in reasonable time.

3. Check the result of the addition.

  - If we finish all the calculations above without encountering non-invertible elements ($\bmod n$), it means that the elliptic curves' (modulo primes) order is not smooth enough, so we need to try again with a different curve and starting point.
  - If we encounter a $p = \gcd(v,n) \neq 1$ we are done: it is a non-trivial factor of $n$.

The time complexity depends on the size of the number's smallest prime factor and can be represented by exp[(√2 + o(1)) √ln *p* ln ln *p*], where *p* is the smallest factor of *n*, or $L_p\left[\frac{1}{2},\sqrt{2}\right]$, in L-notation.

## Explanation

If *p* and *q* are two prime divisors of *n*, then *y*^2 = *x*^3 + *ax* + *b* (mod *n*) implies the same equation also modulo *p* and modulo *q*. These two smaller elliptic curves with the $\boxplus$-addition are now genuine groups. If these groups have *N*_(*p*) and *N_q* elements, respectively, then for any point *P* on the original curve, by Lagrange's theorem, *k* > 0 is minimal such that $kP=\infty$ on the curve modulo *p* implies that *k* divides *N*_(*p*); moreover, $N_p P=\infty$. The analogous statement holds for the curve modulo *q*. When the elliptic curve is chosen randomly, then *N*_(*p*) and *N*_(*q*) are random numbers close to *p* + 1 and *q* + 1, respectively (see below). Hence it is unlikely that most of the prime factors of *N*_(*p*) and *N*_(*q*) are the same, and it is quite likely that while computing *eP*, we will encounter some *kP* that is ∞ modulo *p* but not modulo *q*, or vice versa. When this is the case, *kP* does not exist on the original curve, and in the computations we found some *v* with either gcd(*v*,*p*) = *p* or gcd(*v*, *q*) = *q*, but not both. That is, gcd(*v*, *n*) gave a non-trivial factor of *n*.

ECM is at its core an improvement of the older *p* − 1 algorithm. The *p* − 1 algorithm finds prime factors *p* such that *p* − 1 is b-powersmooth for small values of *b*. For any *e*, a multiple of *p* − 1, and any *a* relatively prime to *p*, by Fermat's little theorem we have *a*^(*e*) ≡ 1 (mod *p*). Then gcd(*a*^(*e*) − 1, *n*) is likely to produce a factor of *n*. However, the algorithm fails when *p* − 1 has large prime factors, as is the case for numbers containing strong primes, for example.

ECM gets around this obstacle by considering the group of a random elliptic curve over the finite field **Z**_(*p*), rather than considering the multiplicative group of **Z**_(*p*) which always has order *p* − 1.

The order of the group of an elliptic curve over **Z**_(*p*) varies (quite randomly) between *p* + 1 − 2√*p* and *p* + 1 + 2√*p* by Hasse's theorem, and is likely to be smooth for some elliptic curves. Although there is no proof that a smooth group order will be found in the Hasse-interval, by using heuristic probabilistic methods, the Canfield–Erdős–Pomerance theorem with suitably optimized parameter choices, and the L-notation, we can expect to try **L**[√2/2, √2] curves before getting a smooth group order. This heuristic estimate is very reliable in practice.

## Example usage

The following example is from Trappe & Washington (2006), with some details added.

We want to factor $n = 455839$. Let's choose the elliptic curve $y^2 = x^3 + 5x - 5$, with the point $P=(1,1)$ on it, and let's try to compute the point $(10!)P$.

The slope of the tangent line at some point $A=(x,y)$ on the curve is $\lambda=\frac{3x^2+5}{2y}\ (\mathrm{mod}\ n)$. Using $\lambda$, we can compute point $2A$. If the value of $\lambda$ does not exist, as a result of $y$ not having a modular inverse, then $\gcd(n,y)$ is a non-trivial factor of $n$.

First, we compute $2!P$. Using point doubling, we have $\lambda(P)=\lambda(1,1)=4$, so the coordinates of point $2P=(x',y')$ are
    $x'=4^2-2(1)=14$
    $y'=4(1-14)-1=-53$

yielding the point $2P=(14,-53)$.

Next, we compute $3!P$. We have $\lambda(2P)=\lambda(14,-53)=-593/106\ (\mathrm{mod}\ n)$. Since $\gcd(106,455839)=1$, the modular inverse of 106 exists. Using the extended Euclidean algorithm, we can obtain that $\lambda=-593/106=322522\ (\mathrm{mod}\ 455839)$.

Given this, we can compute the coordinates of $2(2P)$, just as we did above. The coordinates of point $4P=(x',y')$ are
    $x'=322522^2-2(14)=259851\pmod{455839}$
    $y'=322522(14-259851)-(-53)=116255\pmod{455839}$

This yields $4P=(259851,116255)$.

After this, we can compute $3(2P) = 4P + 2P$ using point addition. The line joining $4P$ and $2P$ has slope $\lambda=116308/259837=206097\ (\mathrm{mod}\ n)$, so the coordinates of $6P=(x',y')$ are
    $x'=206097^2-14-259851=179685\pmod{455839}$
    $y'=206097(14-179685)-(-53)=427131\pmod{455839}$

yielding the point $6P=(179685,427131)$

We can similarly compute points $4!P$, $5!P$, and so on, but computing $8!P$ requires inverting 599 (mod 455839), which is not possible because $\gcd(599,455839)=599\ne1$. Thus 599 is a divisor of 455839. After a quick division, we have 455839 = 599×761.

The reason this works is that the curve (mod 599) has 640 = 2^7·5 points, while (mod 761) it has 777 = 3·7·37 points. Moreover, 640 and 777 are the smallest positive integers *k* such that *kP* = ∞ on the curve (mod 599) and (mod 761), respectively. Since 8! is a multiple of 640 but not a multiple of 777, we have 8!*P* = ∞ on the curve (mod 599), but not on the curve (mod 761), hence the repeated addition broke down here, yielding the factorization.

## The algorithm, with projective coordinates

Before considering the projective plane over $(\Z/n\Z)/\sim,$ first consider a 'normal' projective space over $\mathbb{R}$: Instead of points, lines through the origin are studied. A line may be represented as a non-zero point $(x,y,z)$, under an equivalence relation ~ given by: $(x,y,z)\sim(x',y',z')$ ⇔ ∃ ***c*** ≠ 0 such that *x' = **c**x*, *y' = **c**y* and *z' = **c**z*. Under this equivalence relation, the space is called **the projective plane** $\mathbb{P}^2$; points, denoted by $(x:y:z)$, correspond to lines in a three-dimensional space that pass through the origin. Note that the point $(0:0:0)$ does not exist in this space since to draw a line in any possible direction requires at least one of x',y' or z' ≠ 0. Now observe that almost all lines go through any given reference plane - such as the (*X*,*Y*,1)-plane, whilst the lines precisely parallel to this plane, having coordinates (*X,Y*,0), specify directions uniquely, as 'points at infinity' that are used in the affine (*X,Y*)-plane it lies above.

The coordinate $(x:y:z)$ corresponds to $(x/z:y/z)$ in affine space.

In the algorithm, only the group structure of an elliptic curve over the field $\mathbb{R}$ is used. Since we do not necessarily need the field $\mathbb{R}$, a finite field will also provide a group structure on an elliptic curve. However, considering the same curve and operation over $(\Z/n\Z)/\sim$ with n not a prime does not give a group. The Elliptic Curve Method makes use of the failure cases of the addition law.

We now state the algorithm in projective coordinates. The neutral element is then given by the point at infinity $(0:1:0)$. Let n be a (positive) integer to be factored and consider the elliptic curve (a set of points with some structure on it) $E(\Z/n\Z)=\{(x:y:z) \in \mathbb{P}^2\ |\ y^2z=x^3+axz^2+bz^3\}$.

1. Pick $x_P,y_P,a \in \Z/n\Z$ with a ≠ 0.
2. Calculate $b = y_P^2 - x_P^3 - ax_P$. The elliptic curve E is then in Weierstrass form given by $y^2 = x^3 + ax + b$ and by using projective coordinates the elliptic curve is given by the homogeneous equation $ZY^2=X^3+aZ^2X+bZ^3$. It has the point $P=(x_P:y_P:1)$.
3. Choose an upperbound $B \in \Z$ for this elliptic curve.

  - Remark: You will only find factors p if the group order g of the elliptic curve E over $\Z/p\Z$ (denoted by $\#E(\Z/p\Z)$) is B-smooth, which means that all prime factors of $n$ have to be less or equal to B.

4. Calculate $k={\rm lcm}(1,\dots ,B)$.
5. Calculate $kP := P + P + \cdots + P$ (multiplication is repeated addition) in the ring $E(\Z/n\Z)$.

  - If the calculation successfully returns $kP = (0:1:0)$, it means g is not B-smooth or n is prime. Go back to step 2 to pick another curve.
  - If the calculation fails at some point, it means a non-trivial divisor can be found. It can fail because addition and multiplication are not well-defined if n is not prime, but this only occurs when a inversion of a particular residue v is tried. In this case the factor is found as $\gcd(v,n)$ as above.

In point 5 it is said that under the right circumstances a non-trivial divisor can be found. As pointed out in Lenstra's article (Factoring Integers with Elliptic Curves) the addition needs the assumption $\gcd(x_1-x_2,n)=1$. If $P,Q$ are not $(0:1:0)$ and distinct (otherwise addition works similarly, but is a little different), then addition works as follows:

- To calculate: $R = P + Q;$ $P = (x_1:y_1:1), Q = (x_2:y_2:1)$,
- $\lambda =(y_1-y_2) (x_1-x_2)^{-1}$,
- $x_3 = \lambda^2 - x_1 - x_2$,
- $y_3 = \lambda(x_1-x_3) - y_1$,
- $R = P + Q = (x_3:y_3:1)$.

If addition fails, this will be due to a failure calculating $\lambda.$ In particular, because $(x_1-x_2)^{-1}$ can not always be calculated if n is not prime (and therefore $\Z/n\Z$ is not a field). Without making use of $\Z/n\Z$ being a field, one could calculate:

- $\lambda'=y_1-y_2$,
- $x_3' = {\lambda'}^2 - x_1(x_1-x_2)^2 - x_2(x_1-x_2)^2$,
- $y_3' = \lambda'(x_1(x_1-x_2)^2-x_3') - y_1(x_1-x_2)^3$,
- $R = P + Q = (x_3'(x_1-x_2):y_3':(x_1-x_2)^3)$, and simplify if possible.

This calculation is always legal and if the gcd of the Z-coordinate with n ≠ (1 or n), so when simplifying fails, a non-trivial divisor of n is found.

### Two-stage variant

Analogous to the two-stage variant of Pollard's p − 1 algorithm, Lenstra ECM can too be done in two stages. This allows one to save a time factor of O(log *p*).

**Algorithm Two-Stage ECM.**

- Input: number to be factored *n*, integer bounds $B_1 \leq B_2$.
- Output: a factor of *n* or failure.

Preparation.

1. Choose a random elliptic curve E mod *n*.
2. Pick a point $P = (x_0:y_0:z_0)$ on the curve.

(A convenient choice is Suyama's $\sigma$ parametrization, which only requires one random number to be drawn.)

Stages.

1. Compute a point $Q := \prod_{p \leq B_1} p^{\left\lfloor\log B_1 / \log p \right\rfloor} P$ on the E. The product means that one loops over every prime $p \leq B_1$; it plays the same role as the large $k$ seen in the algorithms above.

  - Using the product of all prime powers less than $B_1$ instead of $B_1!$ reduces the asymptotic complexity by $O(\log B_1)$.

2. For each prime p, $B_1 \leq p \leq B_2$,

  - Compute a point $(x_p:y_p:z_p) = pQ$ on E.
  - Compute $g := \operatorname{gcd}\left(n, z_p\right)$. If $g \neq 1$, output $g$ and exit.

3. If all primes in range are tried without producing a factor, report failure.

It is possible for stage 1 to yield a factor like previously discussed: a non-invertible denominator implies a factor. $B_1$ is functionally the same as $B$ from the standard version, so it too happens when the group order g is B-smooth. In other words, one looks for a prime divisor p such that $sP$ is the neutral element of $E(\mathbb{Z}/p\mathbb{Z})$ in stage 1.

The second stage is very similar to the second stage of p-1 and p+1. It is a continuation of the work in stage 1 and can be described using very similar mathematical terms. It relaxes the condition such that one can find a factor when g is $(B_1, B_2)$-smooth, or in other words the largest prime factor of g is at most $B_2$ and the second-smallest is at most $B_1$.

To achieve stage 2, one hopes there is a prime p between $B_1$ and $B_2$ such that $pQ = (0:1:0) \mod p$; looking for a failed inversion would produce it after a gcd. Equivalently, one is looking for a prime divisor q such that $sP$ has small prime order in $E(\mathbb{Z}/q\mathbb{Z})$. Checking for a small order of $sP$ is done in stage 2 by computing $(ls)P$ modulo n for each prime l.

The above describe the "naive" approach, which is amenable to prime-pairing optimization and Brent-Suyama extension. However, a much faster polynomial-multiplication stage 2 is also available from Peter Montgomery's 1992 thesis. This new approach is found in GMP-ECM and Prime95. This approach was later extended to p-1 and p+1.(Montgomery and Kruppa 2008).

## Twisted Edwards curves

The use of Edwards curves needs fewer modular multiplications and less time than the use of Montgomery curves or Weierstrass curves (other used methods). Using Edwards curves you can also find more primes.

**Definition.** Let $k$ be a field in which $2 \neq 0$, and let $a,d \in k\setminus\{0\}$ with $a\neq d$. Then the twisted Edwards curve $E_{E,a,d}$ is given by $ax^2+y^2=1+dx^2y^2.$ An Edwards curve is a twisted Edwards curve in which $a=1$.

There are five known ways to build a set of points on an Edwards curve: the set of affine points, the set of projective points, the set of inverted points, the set of extended points and the set of completed points.

The set of affine points is given by:
    $\{(x,y)\in \mathbb{A}^2 : ax^2+y^2=1+dx^2y^2\}$.

The addition law is given by
    $(e,f),(g,h) \mapsto \left(\frac{eh+fg}{1+ degfh},\frac{fh-aeg}{1-degfh}\right).$

The point (0,1) is its neutral element and the inverse of $(e,f)$ is $(-e,f)$.

The other representations are defined similar to how the projective Weierstrass curve follows from the affine.

Any elliptic curve in Edwards form has a point of order 4. So the torsion group of an Edwards curve over $\Q$ is isomorphic to either $\Z/4\Z, \Z/8\Z, \Z/12\Z,\Z/2\Z \times \Z/4\Z$ or $\Z/2\Z\times \Z/8\Z$.

The most interesting cases for ECM are $\Z/12\Z$ and $\Z/2\Z\times \Z/8\Z$, since they force the group orders of the curve modulo primes to be divisible by 12 and 16 respectively. The following curves have a torsion group isomorphic to $\Z/12\Z$:

- $x^2+y^2=1+dx^2y^2$ with point $(a,b)$ where $b \notin\{-2,-1/2,0,\pm1\}, a^2=-(b^2+2b)$ and $d=-(2b+1)/(a^2b^2)$
- $x^2+y^2=1+dx^2y^2$ with point $(a,b)$ where $a=\frac{u^2-1}{u^2+1}, b=-\frac{(u-1)^2}{u^2+1}$ and $d=\frac{(u^2+1)^3(u^2-4u+1)}{(u-1)^6(u+1)^2}, u\notin\{0,\pm1\}.$

Every Edwards curve with a point of order 3 can be written in the ways shown above. Curves with torsion group isomorphic to $\Z/2\Z\times \Z/8\Z$ and $\Z/2\Z\times \Z/4\Z$ may be more efficient at finding primes.

## Software implementations

GMP-ECM of Paul Zimmerman is a general-purpose implementation of the Lenstra algorithm based on the GNU Multiple Precision Arithmetic Library. It has been continually updated, with the latest version as of September 2025 being 7.0.6 from July 2024. It allows Montgomery, Weierstrass, and (twisted) Hessian curves. It can run stage 1 for a subset of Montgomery curves on a CUDA GPU, with the earlier implementation by Cyril Bouvier in 2012 having been replaced by Seth Troisi's newer implementation in 2021. Version 7.0.6 also includes an implementation of the HECM method, (described below), the p-1 and p+1 methods, and primality proving using APRCL. GMP-ECM is used in SageMath.

Daniel J. Bernstein and coworkers have published a series of implementations based on Twisted Edwards elliptic curves between 2008 and 2010. They all claim to outperform the contemporary version of GMP-ECM, with the latest being EECM-MPFQ of 2008. Two GPU implementations are also available from Bernstein, the newer and faster one being CUDA-EECM of 2009.

Prime95 includes an implementation of Lenstra ECM for Montgomery and Edwards curves. It is used for the ECM subproject of Great Internet Mersenne Prime Search, which seeks to factor composite Mersenne numbers no smaller than 2^(1213). It can produce stage 1 output compatible with GMP-ECM as well as consume stage 1 output from GMP-ECM. It is faster than GMP-ECM at stage 1.

John Wloka and coworkers published ecmongpu, an implementation of both stage 1 and stage 2 of Lenstra ECM based on Twisted Edwards elliptic curves, in 2020. Their paper report on performance for factoring moduli up to 448 bits long (between 2^(447) and 2^(448)-1).

All software listed above are open-source. In addition, the open-source PARI/GP and proprietary Magma (computer algebra system) also contain "good ECM implementations" according to Paul Zimmerman. An earlier 16-bit software implementation is giantint by Richard Crandall.

## Hyperelliptic-curve method (HECM)

There are recent developments in using hyperelliptic curves to factor integers. Cosset shows in his article (of 2010) that one can build a hyperelliptic curve with genus two (so a curve $y^2 = f(x)$ with f of degree 5), which gives the same result as using two "normal" elliptic curves at the same time. By making use of the Kummer surface, calculation is more efficient. The disadvantages of the hyperelliptic curve (versus an elliptic curve) are compensated by this alternative way of calculating. Therefore, Cosset roughly claims that using hyperelliptic curves for factorization is no worse than using elliptic curves.

## Quantum version (GEECM)

Bernstein, Heninger, Lou, and Valenta suggest GEECM, a quantum version of ECM with Edwards curves. It uses Grover's algorithm to roughly double the length of the primes found compared to standard EECM, assuming a quantum computer with sufficiently many qubits and of comparable speed to the classical computer running EECM.
