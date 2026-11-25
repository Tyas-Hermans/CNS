# ElGamal signature scheme

Source: <https://en.wikipedia.org/wiki/ElGamal_signature_scheme>

The **ElGamal signature scheme** is a digital signature scheme which is based on the difficulty of computing discrete logarithms. It was described by Taher Elgamal in 1985.

The ElGamal signature algorithm is rarely used in practice. A variant developed at the NSA and known as the Digital Signature Algorithm is much more widely used. There are several other variants. The ElGamal signature scheme must not be confused with ElGamal encryption which was also invented by Taher Elgamal.

## Overview

The ElGamal signature scheme is a digital signature scheme based on the algebraic properties of modular exponentiation, together with the discrete logarithm problem. The algorithm uses a **key pair** consisting of a **public key** and a **private key**. The private key is used to generate a **digital signature** for a message, and such a signature can be **verified** by using the signer's corresponding public key. The digital signature provides message authentication (the receiver can verify the origin of the message), integrity (the receiver can verify that the message has not been modified since it was signed) and non-repudiation (the sender cannot falsely claim that they have not signed the message).

## History

The ElGamal signature scheme was described by Taher Elgamal in 1985. It is based on the Diffie–Hellman problem.

## Operation

The scheme involves four operations: key generation (which creates the key pair), key distribution, signing and signature verification.

### Key generation

Key generation has two phases. The first phase is a choice of algorithm parameters which may be shared between different users of the system, while the second phase computes a single key pair for one user.

#### Parameter generation

- Choose a key length $N$.
- Choose a $N$-bit prime number $p$
- Choose a cryptographic hash function $H$ with output length $L$ bits. If $L > N$, only the leftmost $N$ bits of the hash output are used.
- Choose a generator $g < p$ of the multiplicative group of integers modulo *p*, $Z_p^*$.

The algorithm parameters are $(p, g)$. These parameters may be shared between users of the system.

#### Per-user keys

Given a set of parameters, the second phase computes the key pair for a single user:

- Choose an integer $x$ randomly from $\{ 1 \ldots p-2 \}$.
- Compute $y := g^x \bmod p$.

$x$ is the private key and $y$ is the public key.

### Key distribution

The signer should send the public key $y$ to the receiver via a reliable, but not necessarily secret, mechanism. The signer should keep the private key $x$ secret.

### Signing

A message $m$ is signed as follows:

- Choose an integer $k$ randomly from $\{ 2 \ldots p-2 \}$ with $k$ relatively prime to $p-1$.
- Compute $r := g^k \bmod p$.
- Compute $s := (H(m)-x r)k^{-1} \bmod (p-1)$.
- In the unlikely event that $s=0$ start again with a different random $k$.

The signature is $(r,s)$.

### Verifying a signature

One can verify that a signature $(r,s)$ is a valid signature for a message $m$ as follows:

- Verify that $0<r<p$ and $0<s<p-1$.
- The signature is valid if and only if $g^{H(m)} \equiv y^r r^s \pmod p.$

## Correctness

The algorithm is correct in the sense that a signature generated with the signing algorithm will always be accepted by the verifier.

The computation of $s$ during signature generation implies
    $H(m) \, \equiv \, x r + s k \pmod{p-1}.$

Since $g$ is relatively prime to $p$,
    $\begin{align} g^{H(m)} & \equiv g^{xr+sk} \pmod p\\ & \equiv (g^{x})^r (g^{k})^s \pmod p\\ & \equiv (y)^r (r)^s \pmod p.\\ \end{align}$

## Security

A third party can forge signatures either by finding the signer's secret key *x* or by finding collisions in the hash function $H(m) \equiv H(M) \pmod{p-1}$. Both problems are believed to be difficult. However, as of 2011 no tight reduction to a computational hardness assumption is known.

The signer must be careful to choose a different *k* uniformly at random for each signature and to be certain that *k*, or even partial information about *k*, is not leaked. Otherwise, an attacker may be able to deduce the secret key *x* with reduced difficulty, perhaps enough to allow a practical attack. In particular, if two messages are sent using the same value of *k* and the same key, then an attacker can compute *x* directly.

### Existential forgery

The original paper did not include a hash function as a system parameter. The message *m* was used directly in the algorithm instead of *H(m)*. This enables an attack called existential forgery, as described in section IV of the paper. Pointcheval and Stern generalized that case and described two levels of forgeries:

1. **The one-parameter forgery.** Select an $e$ such that $1 < e < p-1$. Set $r := g^e y \bmod{p}$ and $s := -r \bmod{(p-1)}$. Then the tuple $(r,s)$ is a valid signature for the message $m = es \bmod{(p-1)}$.
2. **The two-parameters forgery.** Select $1 < e,v < p-1$, and $\gcd (v,p-1)=1$. Set $r := g^e y^v \bmod{p}$ and $s := -rv^{-1} \bmod{(p-1)}$. Then the tuple $(r,s)$ is a valid signature for the message $m = es \bmod{(p-1)}$. The one-parameter forgery is a special case of the two-parameter forgery, when $v = 1$.

## See also

- Modular arithmetic
- Digital Signature Algorithm
- Elliptic Curve Digital Signature Algorithm
- ElGamal encryption
- Schnorr signature
- Pointcheval–Stern signature algorithm
