# Modular multiplicative inverse

Source: <https://en.wikipedia.org/wiki/Modular_multiplicative_inverse>

In mathematics, particularly in the area of arithmetic, a **modular multiplicative inverse** of an integer a is an integer x such that the product ax is congruent to 1 with respect to the modulus m. In the standard notation of modular arithmetic this congruence is written as
    $ax \equiv 1 \pmod{m},$

which is the shorthand way of writing the statement that m divides (evenly) the quantity *ax* − 1, or, put another way, the remainder after dividing ax by the integer m is 1. If a does have an inverse modulo m, then there is an infinite number of solutions of this congruence, which form a congruence class with respect to this modulus. Furthermore, any integer that is congruent to a (i.e., in a's congruence class) has any element of x's congruence class as a modular multiplicative inverse. Using the notation of $\overline{w}$ to indicate the congruence class containing w, this can be expressed by saying that the *modulo multiplicative inverse* of the congruence class $\overline{a}$ is the congruence class $\overline{x}$ such that:
    $\overline{a} \cdot \overline{x} = \overline{1},$

where the symbol $\cdot$ denotes the multiplication of equivalence classes modulo m. Written in this way, the analogy with the usual concept of a multiplicative inverse in the set of rational or real numbers is clearly represented, replacing the numbers by congruence classes and altering the binary operation appropriately.

As with the analogous operation on the real numbers, a fundamental use of this operation is in solving, when possible, linear congruences of the form
    $ax \equiv b \pmod{m}.$

Finding modular multiplicative inverses also has practical applications in the field of cryptography, e.g. public-key cryptography and the RSA algorithm. A benefit for the computer implementation of these applications is that there exists a very fast algorithm (the extended Euclidean algorithm) that can be used for the calculation of modular multiplicative inverses.

## Modular arithmetic

For a given positive integer m, two integers, a and b, are said to be **congruent modulo m** if m divides their difference. This binary relation is denoted by,
    $a \equiv b \pmod{m}.$

This is an equivalence relation on the set of integers, $\mathbb{Z}$, and the equivalence classes are called **congruence classes modulo m** or **residue classes modulo m**. Let $\overline{a}$ denote the congruence class containing the integer a, then
    $\overline{a} = \{b \in \mathbb{Z} \mid a \equiv b \pmod{m} \}.$

A **linear congruence** is a modular congruence of the form
    $ax \equiv b \pmod{m}.$

Unlike linear equations over the reals, linear congruences may have zero, one or several solutions. If x is a solution of a linear congruence then every element in $\overline{x}$ is also a solution, so, when speaking of the number of solutions of a linear congruence we are referring to the number of different congruence classes that contain solutions.

If d is the greatest common divisor of a and m then the linear congruence *ax* ≡ *b* (mod *m*) has solutions if and only if d divides b. If d divides b, then there are exactly d solutions.

A modular multiplicative inverse of an integer a with respect to the modulus m is a solution of the linear congruence
    $ax \equiv 1 \pmod{m}.$

The previous result says that a solution exists if and only if gcd(*a*, *m*) = 1, that is, a and m must be relatively prime (i.e. coprime). Furthermore, when this condition holds, there is exactly one solution, i.e., when it exists, a modular multiplicative inverse is unique: If b and b' are both modular multiplicative inverses of a respect to the modulus m, then
    $ab \equiv ab' \equiv 1 \pmod{m} ,$

therefore
    $a(b-b') \equiv 0 \pmod{m}.$

If *a* ≡ 0 (mod *m*), then gcd(*a*, *m*) = *m*, and a won't even have a modular multiplicative inverse. Therefore, *b ≡ b'* (mod *m*).

When *ax* ≡ 1 (mod *m*) has a solution it is often denoted in this way −
    $x \equiv a^{-1} \pmod{m},$

but this can be considered an abuse of notation since it could be misinterpreted as the reciprocal of $a$ (which, contrary to the modular multiplicative inverse, is not an integer except when a is 1 or −1). The notation would be proper if a is interpreted as a token standing for the congruence class $\overline{a}$, as the multiplicative inverse of a congruence class is a congruence class with the multiplication defined in the next section.

### Integers modulo m

The congruence relation, modulo m, partitions the set of integers into m congruence classes. Operations of addition and multiplication can be defined on these m objects in the following way: To either add or multiply two congruence classes, first pick a representative (in any way) from each class, then perform the usual operation for integers on the two representatives and finally take the congruence class that the result of the integer operation lies in as the result of the operation on the congruence classes. In symbols, these definitions are
    $\overline{a} + \overline{b} = \overline{a + b}$

and
    $\overline{a} \cdot \overline{b} = \overline{ab},$

where $+$ and $\,\!\cdot$ on the left denote addition and multiplication of congruence classes modulo m. These operations are well-defined, meaning that the end result does not depend on the choices of representatives that were made to obtain the result.

The m congruence classes with these two defined operations form a commutative ring, called the **ring of integers modulo m**. There are several notations used for these algebraic objects, most often $\mathbb{Z}/m\mathbb{Z}$ or $\mathbb{Z}/m$, but several elementary texts and application areas use a simplified notation $\mathbb{Z}_m$ when confusion with other algebraic objects is unlikely.

The congruence classes of the integers modulo m were traditionally known as *residue classes modulo m*, reflecting the fact that all the elements of a congruence class have the same remainder (i.e., "residue") upon being divided by m. Any set of m integers selected so that each comes from a different congruence class modulo m is called a **complete system of residues modulo m**. The division algorithm shows that the set of integers, {0, 1, 2, ..., *m* − 1}  form a complete system of residues modulo m, known as the **least residue system modulo m**. In working with arithmetic problems it is sometimes more convenient to work with a complete system of residues and use the language of congruences while at other times the point of view of the congruence classes of the ring $\mathbb{Z}/m\mathbb{Z}$ is more useful.

### Multiplicative group of integers modulo m

Not every element of a complete residue system modulo m has a modular multiplicative inverse, for instance, zero does not have one if *m* > 1. After removing the elements of a complete residue system that are not relatively prime to m, what is left is called a **reduced residue system**, all of whose elements have modular multiplicative inverses. The number of elements in a reduced residue system is $\phi(m)$, where $\phi$ is the Euler totient function, i.e., the number of positive integers less than m that are relatively prime to m.

In a general ring with unity not every element has a multiplicative inverse and those that do are called **units**. As the product of two units is a unit, the units of a ring form a group, the **group of units of the ring** and often denoted by *R*^(×) if R is the name of the ring. The group of units of the ring of integers modulo m is called the **multiplicative group of integers modulo m**, and it is isomorphic to a reduced residue system. In particular, it has order (size), $\phi(m)$.

In the case that m is a prime, say p, then $\phi(p) = p-1$ and all the non-zero elements of $\mathbb{Z}/p\mathbb{Z}$ have multiplicative inverses, thus $\mathbb{Z}/p\mathbb{Z}$ is a finite field. In this case, the multiplicative group of integers modulo p form a cyclic group of order *p* − 1.

## Example

For any integer $n>1$, it's always the case that $n^2-n+1$ is the modular multiplicative inverse of $n+1$ with respect to the modulus $n^2$, since $(n+1)(n^2-n+1)=n^3+1$. Examples are $3\times3 \equiv 1 \pmod{4}$, $4\times7 \equiv 1 \pmod{9}$, $5\times13 \equiv 1 \pmod{16}$ and so on.

The following example uses the modulus 10: Two integers are congruent mod 10 if and only if their difference is divisible by 10, for instance
    $32 \equiv 2 \pmod{10}$ since 10 divides 32 − 2 = 30, and
    $111 \equiv 1 \pmod{10}$ since 10 divides 111 − 1 = 110.

Some of the ten congruence classes with respect to this modulus are:
    $\overline{0} = \{ \cdots, -20, -10, 0, 10, 20, \cdots \}$
    $\overline{1} = \{ \cdots, -19, -9, 1, 11, 21, \cdots \}$
    $\overline{5} = \{ \cdots, -15, -5, 5, 15, 25, \cdots \}$ and
    $\overline{9} = \{ \cdots, -11, -1, 9, 19, 29, \cdots \}.$

The linear congruence 4*x* ≡ 5 (mod 10) has no solutions since the integers that are congruent to 5 (i.e., those in $\overline{5}$) are all odd while 4*x* is always even. However, the linear congruence 4*x* ≡ 6 (mod 10) has two solutions, namely, *x* = 4 and *x* = 9. The gcd(4, 10) = 2 and 2 does not divide 5, but does divide 6.

Since gcd(3, 10) = 1, the linear congruence 3*x* ≡ 1 (mod 10) will have solutions, that is, modular multiplicative inverses of 3 modulo 10 will exist. In fact, 7 satisfies this congruence (i.e., 21 − 1 = 20). However, other integers also satisfy the congruence, for instance 17 and −3 (i.e., 3(17) − 1 = 50 and 3(−3) − 1 = −10). In particular, every integer in $\overline{7}$ will satisfy the congruence since these integers have the form 7 + 10*r* for some integer r and
    $3(7 + 10 r) - 1 = 21 + 30 r -1 = 20 + 30 r = 10(2 + 3r),$

is divisible by 10. This congruence has only this one congruence class of solutions. The solution in this case could have been obtained by checking all possible cases, but systematic algorithms would be needed for larger moduli and these will be given in the next section.

The product of congruence classes $\overline{5}$ and $\overline{8}$ can be obtained by selecting an element of $\overline{5}$, say 25, and an element of $\overline{8}$, say −2, and observing that their product (25)(−2) = −50 is in the congruence class $\overline{0}$. Thus, $\overline{5} \cdot \overline{8} = \overline{0}$. Addition is defined in a similar way. The ten congruence classes together with these operations of addition and multiplication of congruence classes form the ring of integers modulo 10, i.e., $\mathbb{Z}/10\mathbb{Z}$.

A complete residue system modulo 10 can be the set {10, −9, 2, 13, 24, −15, 26, 37, 8, 9} where each integer is in a different congruence class modulo 10. The unique least residue system modulo 10 is {0, 1, 2, ..., 9}. A reduced residue system modulo 10 could be {1, 3, 7, 9}. The product of any two congruence classes represented by these numbers is again one of these four congruence classes. This implies that these four congruence classes form a group, in this case the cyclic group of order four, having either 3 or 7 as a (multiplicative) generator. The represented congruence classes form the group of units of the ring $\mathbb{Z}/10\mathbb{Z}$. These congruence classes are precisely the ones which have modular multiplicative inverses.

## Computation

### Extended Euclidean algorithm

A modular multiplicative inverse of a modulo m can be found by using the extended Euclidean algorithm.

The Euclidean algorithm determines the greatest common divisor (gcd) of two integers, say a and m. If a has a multiplicative inverse modulo m, this gcd must be 1. The last of several equations produced by the algorithm may be solved for this gcd. Then, using a method called "back substitution", an expression connecting the original parameters and this gcd can be obtained. In other words, integers x and y can be found to satisfy Bézout's identity,
    $ax + my = \gcd(a, m)= 1.$

Rewritten, this is
    $ax - 1 = (-y)m,$

that is,
    $ax \equiv 1 \pmod{m},$

so, a modular multiplicative inverse of a has been calculated. A more efficient version of the algorithm is the extended Euclidean algorithm, which, by using auxiliary equations, reduces two passes through the algorithm (back substitution can be thought of as passing through the algorithm in reverse) to just one. In big O notation, this algorithm runs in time O(log^2(*m*)), assuming |*a*| < *m*, and is considered to be very fast and generally more efficient than its alternative, exponentiation.

For example, a modular multiplicative inverse of $a = 15$ with respect to the modulus $m = 34$ is $-9$ but also $-9 + 34 = 25,$ i.e., in the ring $\Z/34\Z,$ the residue class $\overline{15}$ is invertible with the inverse
    $\overline{15}^{\!\ -1} = \overline{-9} = \overline{25}.$

Because
    $g = \mathrm{gcd}(m,a) = 1 = 4m - 9a,$

according to the adjacent calculation. In the first step, corresponding to the Euclidean division "$\;\! 34 \div 15$ is $2$ with remainder $4\!\$", $-2$ times equation $15 = 0m + 1a$ is added to equation $34 = 1m + 0a$, which leads to $4 = 1m - 2a.$ As soon as a remainder on the left is $0,$ $g$ stands above it (or generally $\pm g$ if negative remainders are also allowed). In the corresponding table far right with the analogous row operations, one could apparently omit the $m$-column. Finally, $\overline{15}{}^{\!\ -1} = \overline{-9}$ can be checked directly:
    $\overline{15}\cdot\overline{-9} = \overline{-135} = \overline{-135 + 4\cdot 34} = \overline{1}$

in $\Z/34\Z.$

### Using Euler's theorem

As an alternative to the extended Euclidean algorithm, Euler's theorem may be used to compute modular inverses.

According to Euler's theorem, if a is coprime to m, that is, gcd(*a*, *m*) = 1, then
    $a^{\phi(m)} \equiv 1 \pmod{m},$

where $\phi$ is Euler's totient function. This follows from the fact that a belongs to the multiplicative group $(\mathbb{Z}/m\mathbb{Z})$^(×) if and only if a is coprime to m. Therefore, a modular multiplicative inverse can be found directly:
    $a^{\phi(m)-1} \equiv a^{-1} \pmod{m}.$

In the special case where m is a prime, $\phi (m) = m - 1$ and a modular inverse is given by
    $a^{-1} \equiv a^{m-2} \pmod{m}.$

This method is generally slower than the extended Euclidean algorithm, but is sometimes used when an implementation for modular exponentiation is already available. Some disadvantages of this method include:

- The value $\phi (m)$ must be known and the most efficient known computation requires m's factorization. Factorization is widely believed to be a computationally hard problem. However, calculating $\phi (m)$ is straightforward when the prime factorization of m is known.
- The relative cost of exponentiation. Though it can be implemented more efficiently using modular exponentiation, when large values of m are involved this is most efficiently computed with the Montgomery reduction method, that method, itself, requiring a modular inverse mod m, which is what was to be calculated in the first place. Without the Montgomery method, the standard binary exponentiation, which requires division mod m at every step, is a slow operation when m is large.

One notable *advantage* of this technique is that there are no conditional branches which depend on the value of a, and thus the value of a, which may be an important secret in public-key cryptography, can be protected from side-channel attacks. For this reason, the standard implementation of Curve25519 uses this technique to compute an inverse.

### Multiple inverses

It is possible to compute the inverse of multiple numbers a_i, modulo a common m, with a single invocation of the Euclidean algorithm and three multiplications per additional input. The basic idea is to form the product of all the a_i, invert that, then multiply by a_j for all *j* ≠ *i* to leave only the desired *a*^(−1)
_(*i*).

More specifically, the algorithm is (all arithmetic performed modulo m):

1. Compute the prefix products $b_i = \prod_{j=1}^i a_j = a_i b_{i-1}$ for all *i* ≤ *n*.
2. Compute *b*^(−1)
_(*n*) using any available algorithm.
3. For i from n down to 2, compute

  - *a*^(−1)
_(*i*) = *b*^(−1)
_(*i*)*b*_(*i*−1) and
  - *b*^(−1)
_(*i*−1) = *b*^(−1)
_(*i*)*a_i*.

4. Finally, *a*^(−1)
_1 = *b*^(−1)
_1.

It is possible to perform the multiplications in a tree structure rather than linearly to exploit parallel computing.

### Inverses modulo prime powers (including powers of 2)

In the case where the modulus M is on the form $p^{m}$ for some prime number p and positive integer m, it is possible to compute modular multiplicative inverses efficiently by using the Newton-Raphson iteration, allowing the inverse to be computed with $O(\log m)$ multiplications. It can be shown that if
    $ax\equiv 1\pmod{p^{k}}$

(that is, x is a modular multiplicative inverse of a modulo some prime power $p^{k}$), then
    $ax\left(2-ax\right)\equiv 1\pmod{p^{2k}}$

which means that it is possible to perform a modular-inverse calculation by first computing a modular multiplicative inverse of a modulo the prime number p or a small power thereof, then performing a series of Newton-Raphson iterations to compute the inverse modulo progressively larger prime powers $p^{2^{n} * k}$ for progressively larger values of n.

A practical use of this method is to efficiently compute modular multiplicative inverses modulo powers of 2. For such a calculation, one could start with noting that all odd integers are their own modular multiplicative inverses modulo $2^{3}$, as can be shown by inspection:

$1*1=1\equiv 1\pmod{8}$,
$3*3=9\equiv 1\pmod{8}$,
$5*5=25\equiv 1\pmod{8}$,
$7*7=49\equiv 1\pmod{8}$,

and then iteratively use Newton-Raphson iterations to compute the modular inverse modulo $2^{6}$, $2^{12}$, $2^{24}$ and so on.

For example, in the C programming language, where additions, subtractions and multiplications on the `uint64_t` data type are all done modulo $2^{64}$, one could compute the modular multiplicative inverse of an odd integer a modulo $2^{64}$ using the following function that performs five Newton-Raphson iterations:

```
#include <stdint.h>
uint64_t modinv64(uint64_t a) {
uint64_t x = a;
for (int i = 0; i < 5; i++) x *= 2 - a*x;
return x;
}

```

Depending on application and platform, it may make sense to optimize this routine further — e.g. the first few iterations can be skipped by using a lookup table to provide an inverse modulo a larger power-of-2; also, on some systems, 32-bit multiplications may be faster than 64-bit multiplications, in which case some speedup can be obtained by only using 32-bit multiplications until an inverse modulo $2^{32}$ has been obtained and then switch to 64-bit multiplications only after that. Applying such optimizations, a C routine that computes a modular multiplicative inverse modulo $2^{64}$ becomes:

```
#include <stdint.h>
uint64_t modinv64(uint64_t a) {
static const uint8_t tbl[256] = {
        0,1,0,171,0,205,0,183,0,57,0,163,0,197,0,239,
        0,241,0,27,0,61,0,167,0,41,0,19,0,53,0,223,
        0,225,0,139,0,173,0,151,0,25,0,131,0,165,0,207,
        0,209,0,251,0,29,0,135,0,9,0,243,0,21,0,191,
        0,193,0,107,0,141,0,119,0,249,0,99,0,133,0,175,
        0,177,0,219,0,253,0,103,0,233,0,211,0,245,0,159,
        0,161,0,75,0,109,0,87,0,217,0,67,0,101,0,143,
        0,145,0,187,0,221,0,71,0,201,0,179,0,213,0,127,
        0,129,0,43,0,77,0,55,0,185,0,35,0,69,0,111,
        0,113,0,155,0,189,0,39,0,169,0,147,0,181,0,95,
        0,97,0,11,0,45,0,23,0,153,0,3,0,37,0,79,
        0,81,0,123,0,157,0,7,0,137,0,115,0,149,0,63,
        0,65,0,235,0,13,0,247,0,121,0,227,0,5,0,47,
        0,49,0,91,0,125,0,231,0,105,0,83,0,117,0,31,
        0,33,0,203,0,237,0,215,0,89,0,195,0,229,0,15,
        0,17,0,59,0,93,0,199,0,73,0,51,0,85,0,255 };
uint32_t a32 = (uint32_t)a;
uint32_t x = tbl[a & 0xFF];  // inverse modulo 2^8
x *= 2 - a32*x;        // 32-bit multiplications
x *= 2 - a32*x;        // 32-bit multiplications
return x * (2 - a*x);  // 64-bit multiplications
}

```

## Applications

Finding a modular multiplicative inverse has many applications in algorithms that rely on the theory of modular arithmetic. For instance, in cryptography the use of modular arithmetic permits some operations to be carried out more quickly and with fewer storage requirements, while other operations become more difficult. Both of these features can be used to advantage. In particular, in the RSA algorithm, encrypting and decrypting a message is done using a pair of numbers that are multiplicative inverses with respect to a carefully selected modulus. One of these numbers is made public and can be used in a rapid encryption procedure, while the other, used in the decryption procedure, is kept hidden. Determining the hidden number from the public number is considered to be computationally infeasible and this is what makes the system work to ensure privacy.

As another example in a different context, consider the exact division problem in computer science where you have a list of odd word-sized numbers each divisible by *k* and you wish to divide them all by *k*. One solution is as follows:

1. Use the extended Euclidean algorithm to compute *k*^(−1), the modular multiplicative inverse of *k* mod 2^(*w*), where *w* is the number of bits in a word. This inverse will exist since the numbers are odd and the modulus has no odd factors.
2. For each number in the list, multiply it by *k*^(−1) and take the least significant word of the result.

On many machines, particularly those without hardware support for division, division is a slower operation than multiplication, so this approach can yield a considerable speedup. The first step is relatively slow but only needs to be done once.

Modular multiplicative inverses are used to obtain a solution of a system of linear congruences that is guaranteed by the Chinese Remainder Theorem.

For example, the system

X ≡ 4 (mod 5)
X ≡ 4 (mod 7)
X ≡ 6 (mod 11)

has common solutions since 5,7 and 11 are pairwise coprime. A solution is given by
X = *t*_1 (7 × 11) × 4 + *t*_2 (5 × 11) × 4 + *t*_3 (5 × 7) × 6

where
*t*_1 = 3 is the modular multiplicative inverse of 7 × 11 (mod 5),
*t*_2 = 6 is the modular multiplicative inverse of 5 × 11 (mod 7) and
*t*_3 = 6 is the modular multiplicative inverse of 5 × 7 (mod 11).

Thus,
X = 3 × (7 × 11) × 4 + 6 × (5 × 11) × 4 + 6 × (5 × 7) × 6 = 3504

and in its unique reduced form
X ≡ 3504 ≡ 39 (mod 385)

since 385 is the LCM of 5,7 and 11.

Also, the modular multiplicative inverse figures prominently in the definition of the Kloosterman sum.

## See also

- Inversive congruential generator – a pseudo-random number generator that uses modular multiplicative inverses
- Rational reconstruction (mathematics)
