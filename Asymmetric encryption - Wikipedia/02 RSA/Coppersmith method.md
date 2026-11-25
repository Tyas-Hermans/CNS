# Coppersmith method

Source: <https://en.wikipedia.org/wiki/Coppersmith_method>

The **Coppersmith method**, proposed by Don Coppersmith, is a method to find small integer zeroes of univariate or bivariate polynomials, or their small zeroes modulo a given integer. The method uses the Lenstra–Lenstra–Lovász lattice basis reduction algorithm (LLL) to find a polynomial that has the same zeroes as the target polynomial but smaller coefficients.

In cryptography, the Coppersmith method is mainly used in attacks on RSA when parts of the secret key are known and forms a base for Coppersmith's attack.

## Approach

Coppersmith's approach is a reduction of solving modular polynomial equations to solving polynomials over the integers.

Let $F(x) = x^n+a_{n-1}x^{n-1}+\ldots +a_1x+a_0$ and assume that $F(x_0)\equiv 0 \pmod{M}$ for some integer $|x_0|< M^{1/n}$. Coppersmith’s algorithm can be used to find this integer solution $x_0$.

Finding roots over the rationals **Q** is easy using, e.g., Newton's method, but such an algorithm does not work modulo a composite number M. The idea behind Coppersmith’s method is to find a different polynomial f related to F that has the same root $x_0$ modulo M, but has only small coefficients. If the coefficients and $x_0$ are small enough that $|f(x_0)| < M$ over the integers, then we have $f(x_0) = 0$, so that $x_0$ is a root of f over **Q** and can be found easily. More generally, we can find a polynomial $f(x)$ with the same root $x_0$ modulo some power $M^a$ of M, satisfying $|f(x_0)| < M^a$, and solve for $x_0$ as above.

Coppersmith's algorithm uses the Lenstra–Lenstra–Lovász lattice basis reduction algorithm (LLL) to construct the polynomial f with small coefficients. Given F, the algorithm constructs polynomials $p_1(x), p_2(x), \dots, p_n(x)$ that all have the same root $x_0$ modulo $M^a$, where a is some integer chosen based on the degree of F and the size of $x_0$. Any linear combination of these polynomials also has $x_0$ as a root modulo $M^a$.

The next step is to use the LLL algorithm to construct a linear combination $f(x)=\sum c_ip_i(x)$ of the $p_i(x)$ so that the inequality $|f(x_0)| < M^a$ holds. Now standard factorization methods can calculate the zeroes of $f(x)$ over the integers.

## Implementations

Coppersmith's method for univariate polynomials is implemented in

- Magma as the function `SmallRoots`;
- PARI/GP as the function `zncoppersmith`;
- SageMath as the method `small_roots`.
