# Elliptic-curve cryptography

Source: <https://en.wikipedia.org/wiki/Elliptic-curve_cryptography>

**Elliptic-curve cryptography** (**ECC**) is an approach to public-key cryptography based on the algebraic structure of elliptic curves over finite fields. ECC allows smaller keys to provide equivalent security, compared to cryptosystems based on modular exponentiation in finite fields, such as the RSA cryptosystem and  ElGamal cryptosystem.

Elliptic curves are applicable for key agreement, digital signatures, pseudo-random generators and other tasks. Indirectly, they can be used for encryption by combining the key agreement with a symmetric encryption scheme. They are also used in several integer factorization algorithms that have applications in cryptography, such as Lenstra elliptic-curve factorization.

## History

The use of elliptic curves in cryptography was suggested independently by Neal Koblitz and Victor S. Miller in 1985. Elliptic curve cryptography algorithms entered wide use starting in 2004.

In 1999, U.S. NIST recommended fifteen elliptic curves for use in the Digital Signature Standard. These curves were later specified in FIPS 186-4, which was superseded by FIPS 186-5 in 2023 and withdrawn in 2024. NIST moved its recommended elliptic-curve domain parameters to Special Publication 800-186. SP 800-186 includes previously recommended Weierstrass curves and two Edwards curves for EdDSA; it also deprecates binary-field curves and strongly recommends use of prime curves.

At the RSA Conference 2005, the National Security Agency (NSA) announced Suite B, which used ECC for digital signature generation and key exchange. Suite B was later superseded by the Commercial National Security Algorithm Suite (CNSA), and NSA announced CNSA 2.0 as a quantum-resistant transition suite for national security systems.

Since the early 2000s, cryptographic primitives based on bilinear mappings on various elliptic curve groups, such as the Weil and Tate pairings, have been studied. Schemes based on these primitives include identity-based encryption as well as pairing-based signatures, signcryption, key agreement, and proxy re-encryption.

Elliptic curve cryptography is used successfully in numerous popular protocols, such as Transport Layer Security and Bitcoin.

### Security concerns

In 2013, *The New York Times* stated that Dual Elliptic Curve Deterministic Random Bit Generation (or Dual_EC_DRBG) had been included as a NIST national standard due to the influence of NSA, which had included a deliberate weakness in the algorithm and the recommended elliptic curve. RSA Security in September 2013 issued an advisory recommending that its customers discontinue using any software based on Dual_EC_DRBG. In the wake of the exposure of Dual_EC_DRBG as "an NSA undercover operation", cryptography experts have also expressed concern over the security of the NIST recommended elliptic curves, suggesting a return to encryption based on non-elliptic-curve groups.

Additionally, in August 2015, the NSA announced that it planned to replace Suite B with a new cipher suite due to concerns about quantum computing attacks on ECC. NSA later published CNSA 2.0 guidance for a transition to quantum-resistant algorithms for national security systems.

### Patents

While the RSA patent expired in 2000, there may be patents in force covering certain aspects of ECC technology, including at least one ECC scheme (ECMQV). However, RSA Laboratories and Daniel J. Bernstein have argued that the US government elliptic curve digital signature standard (ECDSA; NIST FIPS 186-3) and certain practical ECC-based key exchange schemes (including ECDH) can be implemented without infringing those patents.

## Elliptic curve theory

For the purposes of this article, an *elliptic curve* is a plane curve over a finite field (rather than the real numbers). A common form for curves over finite fields of characteristic not equal to 2 or 3 consists of the points satisfying the equation
    $y^2 = x^3 + ax + b,$

along with a distinguished point at infinity, denoted $\infty$. Curves over fields of characteristic 2 or 3, and curves used in other representations such as Montgomery or Edwards form, are written differently.

This set of points, together with the group operation of elliptic curves, is an abelian group, with the point at infinity as an identity element. The structure of the group is inherited from the divisor group of the underlying algebraic variety:
    $\operatorname{Div}^0(E) \to \operatorname{Pic}^0(E) \simeq E.$

### Application to cryptography

Public-key cryptography is based on the intractability of certain mathematical problems. Early public-key systems, such as RSA's 1983 patent, based their security on the assumption that it is difficult to factor a large integer composed of two or more large prime factors which are far apart. For elliptic-curve protocols, a central hardness assumption is the elliptic curve discrete logarithm problem (ECDLP): given a public base point $P$ and another point $Q=kP$, it should be infeasible to recover $k$. Key-agreement protocols such as ECDH rely on related Diffie–Hellman assumptions, such as the difficulty of computing $abP$ from $P$, $aP$, and $bP$. The security of elliptic curve cryptography depends on the ability to compute point multiplication efficiently and the apparent inability to reverse it for properly chosen curves and key sizes. The size and structure of the curve group, rather than only the total number of coordinate pairs satisfying the curve equation, determine the difficulty of the problem.

The primary benefit promised by elliptic curve cryptography over alternatives such as RSA is a smaller key size, reducing storage and transmission requirements. For example, a 256-bit elliptic curve public key should provide comparable security to a 3072-bit RSA public key.

### Cryptographic schemes

Several discrete logarithm-based protocols have been adapted to elliptic curves, replacing the group $(\mathbb{Z}_{p})^\times$ with an elliptic-curve group:

- The Elliptic-curve Diffie–Hellman (ECDH) key agreement scheme is based on the Diffie–Hellman scheme,
- X25519 and X448 are Diffie–Hellman functions specified by the IRTF for use with Montgomery-form curves,
- The Elliptic Curve Integrated Encryption Scheme (ECIES), also known as Elliptic Curve Augmented Encryption Scheme or simply the Elliptic Curve Encryption Scheme,
- The Elliptic Curve Digital Signature Algorithm (ECDSA) is based on the Digital Signature Algorithm,
- The Edwards-curve Digital Signature Algorithm (EdDSA) is based on Schnorr signature and uses twisted Edwards curves,
- The ECMQV key agreement scheme is based on the MQV key agreement scheme,
- The ECQV implicit certificate scheme.

## Implementation

Some common implementation considerations include:

### Domain parameters

To use ECC, all parties must agree on all the elements defining the elliptic curve, that is, the *domain parameters* of the scheme. The underlying finite field is typically either a prime field, denoted $\mathbb{F}_p$, or a binary field, denoted $\mathbb{F}_{2^m}$. In the binary case, $m$ and an irreducible reduction polynomial $f$ specify the field representation; $f$ is not an auxiliary curve. The elliptic curve is defined by the coefficients in its defining equation. Finally, the cyclic subgroup is defined by its generator (a.k.a. *base point*) *G*. For cryptographic application, the order of *G*, that is the smallest positive number *n* such that $n G = \mathcal{O}$ (the point at infinity of the curve, and the identity element), is normally prime. Since *n* is the size of a subgroup of $E(\mathbb{F}_q)$, it follows from Lagrange's theorem that the number $h = \frac{1}{n}|E(\mathbb{F}_q)|$ is an integer. In cryptographic applications, this number *h*, called the *cofactor*, is usually small, ideally 1. Protocols using curves with cofactors greater than 1 must handle the cofactor appropriately. To summarize: in the prime case, the domain parameters are $(p,a,b,G,n,h)$; in the binary case, they are $(m,f,a,b,G,n,h)$.

Unless there is an assurance that domain parameters were generated by a party trusted with respect to their use, the domain parameters *must* be validated before use.

The generation of domain parameters is not usually done by each participant because this involves computing the number of points on a curve which is time-consuming and troublesome to implement. As a result, several standard bodies published domain parameters of elliptic curves for several common field sizes. Such domain parameters are commonly known as "standard curves" or "named curves"; a named curve can be referenced either by name or by the unique object identifier defined in the standard documents:

- NIST, SP 800-186: Recommendations for Discrete Logarithm-Based Cryptography: Elliptic Curve Domain Parameters
- SECG, SEC 2: Recommended Elliptic Curve Domain Parameters

- ECC Brainpool (RFC 5639), ECC Brainpool Standard Curves and Curve Generation Archived 2018-04-17 at the Wayback Machine

SECG test vectors are also available. NIST has approved many SECG curves, so there is a significant overlap between the specifications published by NIST and SECG. EC domain parameters may be specified either by value or by name.

If, despite the preceding admonition, one decides to construct one's own domain parameters, one should select the underlying field and then use one of the following strategies to find a curve with appropriate (i.e., near prime) number of points using one of the following methods:

- Select a random curve and use a general point-counting algorithm, for example, Schoof's algorithm or the Schoof–Elkies–Atkin algorithm,
- Select a random curve from a family which allows easy calculation of the number of points (e.g., Koblitz curves), or
- Select the number of points and generate a curve with this number of points using the *complex multiplication* technique.

Several classes of curves are weak and should be avoided:

- Curves over $\mathbb{F}_{2^m}$ with non-prime *m* are vulnerable to Weil descent attacks.
- Curves such that *n* divides $p^B-1$ (where *p* is the characteristic of the field: *q* for a prime field, or $2$ for a binary field) for sufficiently small *B* are vulnerable to Menezes–Okamoto–Vanstone (MOV) attack which applies usual discrete logarithm problem (DLP) in a small-degree extension field of $\mathbb{F}_p$ to solve ECDLP. The bound *B* should be chosen so that discrete logarithms in the field $\mathbb{F}_{p^B}$ are at least as difficult to compute as discrete logs on the elliptic curve $E(\mathbb{F}_q)$.
- Curves such that $|E(\mathbb{F}_q)| = q$ are vulnerable to the attack that maps the points on the curve to the additive group of $\mathbb{F}_q$.

### Key sizes

Because all the fastest known algorithms that allow one to solve the ECDLP (baby-step giant-step, Pollard's rho, etc.), need $O(\sqrt{n})$ steps, it follows that the size of the underlying field should be roughly twice the security parameter. For example, for 128-bit security one needs a curve over $\mathbb{F}_q$, where $q \approx 2^{256}$. This can be contrasted with finite-field cryptography (e.g., DSA) which requires 3072-bit public keys and 256-bit private keys, and integer factorization cryptography (e.g., RSA) which requires a 3072-bit value of *n*, where the private key should be just as large. However, the public key may be smaller to accommodate efficient encryption, especially when processing power is limited.

Historic public ECDLP challenge records include a 112-bit key for the prime field case and a 109-bit key for the binary field case. For the prime field case, this was broken in July 2009 using a cluster of over 200 PlayStation 3 game consoles and could have been finished in 3.5 months using this cluster when running continuously. The binary field case was broken in April 2004 using 2600 computers over 17 months. The binary-field ECC2K-130 challenge has also been targeted by distributed computation using CPUs, GPUs, and FPGAs.

### Projective coordinates

A close examination of the addition rules shows that in order to add two points, one needs not only several additions and multiplications in $\mathbb{F}_q$ but also an inversion operation. The inversion (for given $x \in \mathbb{F}_q$ find $y \in \mathbb{F}_q$ such that $x y = 1$) is one to two orders of magnitude slower than multiplication. However, points on a curve can be represented in different coordinate systems which do not require an inversion operation to add two points. Several such systems were proposed: in the *projective* system each point is represented by three coordinates $(X,Y,Z)$ using the following relation: $x = \frac{X}{Z}$, $y = \frac{Y}{Z}$; in the *Jacobian system* a point is also represented with three coordinates $(X,Y,Z)$, but a different relation is used: $x = \frac{X}{Z^2}$, $y = \frac{Y}{Z^3}$; in the *López–Dahab system* the relation is $x = \frac{X}{Z}$, $y = \frac{Y}{Z^2}$; in the *modified Jacobian* system the same relations are used but four coordinates are stored and used for calculations $(X,Y,Z,aZ^4)$; and in the *Chudnovsky Jacobian* system five coordinates are used $(X,Y,Z,Z^2,Z^3)$. Note that there may be different naming conventions, for example, IEEE P1363-2000 standard uses "projective coordinates" to refer to what is commonly called Jacobian coordinates. An additional speed-up is possible if mixed coordinates are used.

### Fast reduction

Reduction modulo *p* (which is needed for addition and multiplication) can be executed much faster if the prime *p* is a pseudo-Mersenne prime (Solinas prime), that is $p \approx 2^d$; for example, $p = 2^{521} - 1$ (P-521) or $p = 2^{256} - 2^{32} - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1.$ Compared to Barrett reduction, there can be an order of magnitude speed-up. The speed-up here is a practical rather than theoretical one, and derives from the fact that the moduli of numbers against numbers near powers of two can be performed efficiently by computers operating on binary numbers with bitwise operations.

The curves over $\mathbb{F}_p$ with pseudo-Mersenne P-256 and P-384 are recommended by NIST in SP 800-186. The NIST curves also use *a* = −3, which improves addition in Jacobian coordinates. Bernstein and Lange have criticized some design choices of the NIST curves and list alternative criteria for curve selection in the SafeCurves project.

Other widely deployed curves also use primes with special forms that allow efficient reduction, such as $p = 2^{255} - 19$ for Curve25519 and $2^{448} - 2^{224} - 1$ for Curve448.

## Security

### Side-channel attacks

Unlike most other discrete logarithm problem (DLP) systems (where it is possible to use the same procedure for squaring and multiplication), the EC addition is significantly different for doubling (*P* = *Q*) and general addition (*P* ≠ *Q*) depending on the coordinate system used. Consequently, it is important to counteract side-channel attacks (e.g., timing or simple/differential power analysis attacks) using, for example, fixed pattern window (a.k.a. comb) methods (note that this does not increase computation time). Alternatively one can use an Edwards curve; this is a special family of elliptic curves for which doubling and addition can be done with the same operation. Another concern for ECC-systems is the danger of fault attacks, especially when running on smart cards.

### Backdoors

Cryptographic experts have expressed concerns that the National Security Agency has inserted a kleptographic backdoor into at least one elliptic curve-based pseudo random generator. Internal memos leaked by former NSA contractor Edward Snowden suggest that the NSA put a backdoor in the Dual EC DRBG standard. One analysis of the possible backdoor concluded that an adversary in possession of the algorithm's secret key could obtain encryption keys given only 32 bytes of PRNG output.

The SafeCurves project catalogs curves that are easy to implement securely and are designed in a fully publicly verifiable way to minimize the chance of a backdoor.

### Quantum computing attack

Shor's algorithm can be used to break elliptic curve cryptography by computing discrete logarithms on a sufficiently large fault-tolerant quantum computer. Published quantum resource estimates for breaking a curve with a 256-bit modulus (128-bit security level) include 2330 logical qubits and 126 billion Toffoli gates. For the binary elliptic curve case, 906 logical qubits are necessary to break 128 bits of security. These estimates do not imply that current quantum computers can break deployed ECC systems, but they are a reason for migration planning.

In August 2024, NIST approved the first three Federal Information Processing Standards for post-quantum cryptography: FIPS 203 for ML-KEM, FIPS 204 for ML-DSA, and FIPS 205 for SLH-DSA. NIST describes these standards as principal post-quantum standards for key establishment and digital signatures. NSA's CNSA 2.0 guidance similarly identifies quantum-resistant algorithms for national security systems and states that CNSA 1.0 compliance remains required during the transition.

Supersingular Isogeny Diffie–Hellman Key Exchange was proposed as a post-quantum form of elliptic-curve-based key exchange using isogenies. However, new classical attacks undermined the security of this protocol.

In August 2015, the NSA announced that it planned to transition "in the not distant future" to a new cipher suite that is resistant to quantum attacks. "Unfortunately, the growth of elliptic curve use has bumped up against the fact of continued progress in the research on quantum computing, necessitating a re-evaluation of our cryptographic strategy."

### Invalid curve attack

ECC implementations can be susceptible to invalid-curve attacks if they multiply a secret scalar by attacker-supplied points without verifying that the points lie on the intended curve and in the correct subgroup. In such attacks, repeated operations on invalid or small-order points can leak information about the private scalar. In 2019, an invalid-curve attack against AMD Secure Encrypted Virtualization was reported to recover a Platform Diffie–Hellman (PDH) private key.

## Alternative representations

Alternative representations of elliptic curves include:

- Hessian curves
- Edwards curves
- Twisted curves
- Twisted Hessian curves
- Twisted Edwards curve
- Doubling-oriented Doche–Icart–Kohel curve
- Tripling-oriented Doche–Icart–Kohel curve
- Jacobian curve
- Montgomery curves

## See also

- BLS digital signature
- Curve25519
- DNSCurve
- ECC patents
- ECMQV
- EdDSA
- Elliptic Curve Digital Signature Algorithm (ECDSA)
- Elliptic curve point multiplication
- Elliptic-curve Diffie–Hellman (ECDH)
- FourQ
- Homomorphic signatures for network coding
- Hyperelliptic curve cryptography
- Pairing-based cryptography
- Public-key cryptography
- Quantum cryptography
- RSA (cryptosystem)
- Supersingular isogeny key exchange
