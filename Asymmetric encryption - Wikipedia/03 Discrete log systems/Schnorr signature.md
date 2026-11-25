# Schnorr signature

Source: <https://en.wikipedia.org/wiki/Schnorr_signature>

In cryptography, a **Schnorr signature** is a digital signature produced by the **Schnorr signature algorithm** that was invented by Claus Schnorr. It is known for its simplicity, among the first whose security is based on the intractability of certain discrete logarithm problems. It is efficient and generates short signatures. It was covered by U.S. patent 4,995,082 which expired in February 2010.

## Algorithm

### Choosing parameters

- All users of the signature scheme agree on a group $G$ of prime order $q$ with generator $g$ in which the discrete log problem is assumed to be hard. Typically a Schnorr group is used.
- All users agree on a cryptographic hash function $H: \{0,1\}^* \rightarrow \mathbb Z/q\mathbb Z$.

### Notation

In the following,

- Exponentiation stands for repeated application of the group operation
- Juxtaposition stands for multiplication on the set of congruence classes or application of the group operation (as applicable)
- Subtraction stands for subtraction on the set of congruence classes
- $M \in \{0,1\}^*$, the set of finite bit strings
- $s, e, e_v, x, k \in \mathbb Z/q\mathbb Z$, the set of congruence classes modulo $q$
- $y, r, r_v \in G$.

### Key generation

- Choose a private signing key $x$ from the allowed set.
- The public verification key is $y = g^{-x}$.

### Signing

To sign a message $M$:

- Choose a random $k$ from the allowed set.
- Let $r = g^k$.
- Let $e = H(r \parallel M)$, where $\parallel$ denotes concatenation and $r$ is represented as a bit string.
- Let $s = k + xe$.

The signature is the pair, $(s, e)$.

Note that $s, e \in \mathbb Z/q\mathbb Z$; if $q < 2^{256}$, then the signature representation can fit into 64 bytes.

### Verifying

- Let $r_v = g^s y^e$
- Let $e_v = H(r_v \parallel M)$

If $e_v = e$ then the signature is verified.

### Proof of correctness

It is relatively easy to see that $e_v = e$ if the signed message equals the verified message:

$r_v = g^s y^e = g^{k + xe} g^{-xe} = g^k = r$, and hence $e_v = H(r_v \parallel M) = H(r \parallel M) = e$.

Public elements: $G$, $g$, $y$, $s$, $e$, $r$. Private elements: $k$, $x$.

This shows only that a correctly signed message will verify correctly; many other properties are required for a secure signature algorithm.

### Key leakage from nonce reuse

Just as with the closely related signature algorithms DSA, ECDSA, and ElGamal, reusing the secret nonce value $k$ on two Schnorr signatures of different messages will allow observers to recover the private key. In the case of Schnorr signatures, this simply requires subtracting $s$ values:
    $s' - s = (k' - k) + x (e' - e)$.

If $k'=k$ but $e'\ne e$ then $x$ can be simply isolated. In fact, even slight biases in the value $k$ or partial leakage of $k$ can reveal the private key, after collecting sufficiently many signatures and solving the hidden number problem.

### Security argument

The signature scheme was constructed by applying the Fiat–Shamir transformation to Schnorr's identification protocol. Therefore, (as per Fiat and Shamir's arguments), it is secure if $H$ is modeled as a random oracle.

Its security can also be argued in the generic group model, under the assumption that $H$ is "random-prefix preimage resistant" and "random-prefix second-preimage resistant". In particular, $H$ does *not* need to be collision resistant.

In 2012, Seurin provided an exact proof of the Schnorr signature scheme. In particular, Seurin shows that the security proof using the forking lemma is the best possible result for any signature schemes based on one-way group homomorphisms including Schnorr-type signatures and the Guillou–Quisquater signature schemes. Namely, under the ROMDL assumption, any algebraic reduction must lose a factor $f({\epsilon}_F)q_h$ in its time-to-success ratio, where $f \le 1$ is a function that remains close to 1 as long as "${\epsilon}_F$ is noticeably smaller than 1", where ${\epsilon}_F$ is the probability of forging an error making at most $q_h$ queries to the random oracle.

## Short Schnorr signatures

The aforementioned process achieves a *t*-bit security level with 4*t*-bit signatures. For example, a 128-bit security level would require 512-bit (64-byte) signatures. The security is limited by discrete logarithm attacks on the group, which have a complexity of the *square-root* of the group size.

In Schnorr's original 1991 paper, it was suggested that since collision resistance in the hash is not required, shorter hash functions may be just as secure, and indeed recent developments suggest that a *t*-bit security level can be achieved with 3*t*-bit signatures. Then, a 128-bit security level would require only 384-bit (48-byte) signatures, and this could be achieved by truncating the size of *e* until it is half the length of the *s* bitfield.

## Implementations

Schnorr signature is used by numerous products. A notable usage is the deterministic Schnorr's signature using the secp256k1 elliptic curve for Bitcoin transaction signature after the Taproot update.

## See also

- DSA
- EdDSA
- ElGamal signature scheme
