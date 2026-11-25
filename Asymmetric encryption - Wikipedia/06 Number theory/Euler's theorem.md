# Euler's theorem

Source: <https://en.wikipedia.org/wiki/Euler%27s_theorem>

In number theory, **Euler's theorem** (also known as the **Fermat–Euler theorem** or **Euler's totient theorem**) states that, if *n* and *a* are coprime positive integers, then $a^{\varphi(n)}$ is congruent to $1$ modulo *n*, where $\varphi$ denotes Euler's totient function; that is
    $a^{\varphi (n)} \equiv 1 \pmod{n}.$

In 1736, Leonhard Euler published a proof of Fermat's little theorem (stated by Fermat without proof), which is the restriction of Euler's theorem to the case where n is a prime number. Subsequently, Euler presented other proofs of the theorem, culminating with his paper of 1763, in which he proved a generalization to the case where n is not prime.

The converse of Euler's theorem is also true: if the above congruence is true, then $a$ and $n$ must be coprime.

The theorem is further generalized by some of Carmichael's theorems.

The theorem may be used to easily reduce large powers modulo $n$. For example, consider finding the ones place decimal digit of $7^{222}$, i.e. $7^{222} \pmod{10}$. The integers 7 and 10 are coprime, and $\varphi(10) = 4$. So Euler's theorem yields $7^4 \equiv 1 \pmod{10}$, and we get $7^{222} \equiv 7^{4 \times 55 + 2} \equiv (7^4)^{55} \times 7^2 \equiv 1^{55} \times 7^2 \equiv 49 \equiv 9 \pmod{10}$.

In general, when reducing a power of $a$ modulo $n$ (where $a$ and $n$ are coprime), one needs to work modulo $\varphi(n)$ in the exponent of $a$:
if $x \equiv y \pmod{\varphi(n)}$, then $a^x \equiv a^y \pmod{n}$.

Euler's theorem underlies the RSA cryptosystem, which is widely used in Internet communications. In this cryptosystem, Euler's theorem is used with n being a product of two large prime numbers, and the security of the system is based on the difficulty of factoring such an integer.

## Proofs

1. Euler's theorem can be proven using concepts from the theory of groups: The residue classes modulo n that are coprime to n form a group under multiplication (see the article Multiplicative group of integers modulo *n* for details). The order of that group is *φ*(*n*). Lagrange's theorem states that the order of any subgroup of a finite group divides the order of the entire group, in this case *φ*(*n*). If a is any number coprime to n then a is in one of these residue classes, and its powers *a*, *a*^2, ... , *a*^(*k*) modulo n form a subgroup of the group of residue classes, with *a*^(*k*) ≡ 1 (mod *n*). Lagrange's theorem says k must divide *φ*(*n*), i.e. there is an integer M such that *kM* = *φ*(*n*). This then implies,
    $a^{\varphi(n)} = a^{kM} = (a^{k})^M \equiv 1^M =1 \pmod{n}.$

2. There is also a direct proof: Let *R* = {*x*_1, *x*_2, ... , *x*_(*φ*(*n*))} be a reduced residue system (mod *n*) and let a be any integer coprime to n. The proof hinges on the fundamental fact that multiplication by a permutes the x_i: in other words if *ax_j* ≡ *ax_k* (mod *n*) then *j* = *k*. (This law of cancellation is proved in the article Multiplicative group of integers modulo *n*.) That is, the sets R and *aR* = {*ax*_1, *ax*_2, ... , *ax*_(*φ*(*n*))}, considered as sets of congruence classes (mod *n*), are identical (as sets—they may be listed in different orders), so the product of all the numbers in R is congruent (mod *n*) to the product of all the numbers in aR:
    $\prod_{i=1}^{\varphi(n)} x_i \equiv \prod_{i=1}^{\varphi(n)} ax_i = a^{\varphi(n)}\prod_{i=1}^{\varphi(n)} x_i \pmod{n},$ and using the cancellation law to cancel each x_i gives Euler's theorem:
    $a^{\varphi(n)}\equiv 1 \pmod{n}.$

## See also

- Carmichael number
- Euler's criterion
- Wilson's theorem
- List of topics named after Leonhard Euler
