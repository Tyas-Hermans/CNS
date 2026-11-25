# Hash-based cryptography

Source: <https://en.wikipedia.org/wiki/Hash-based_cryptography>

**Hash-based cryptography** is the generic term for constructions of cryptographic primitives based on the security of hash functions. It is of interest as a type of post-quantum cryptography.

So far, hash-based cryptography is used to construct digital signatures schemes such as the Merkle signature scheme, zero knowledge and computationally integrity proofs, such as the zk-STARK proof system and range proofs over issued credentials via the HashWires protocol. Hash-based signature schemes combine a one-time signature scheme, such as a Lamport signature, with a Merkle tree structure. Since a one-time signature scheme key can only sign a single message securely, it is practical to combine many such keys within a single, larger structure. A Merkle tree structure is used to this end. In this hierarchical data structure, a hash function and concatenation are used repeatedly to compute tree nodes.

One consideration with hash-based signature schemes is that they can only sign a limited number of messages securely, because of their use of one-time signature schemes. The US National Institute of Standards and Technology (NIST), specified that algorithms in its post-quantum cryptography competition support a minimum of 2^(64) signatures safely.

NIST standardized stateful hash-based cryptography based on the eXtended Merkle Signature Scheme (XMSS) and Leighton–Micali Signatures (LMS), which are applicable in different circumstances, in 2020, but noted that the requirement to maintain state when using them makes them more difficult to implement in a way that avoids misuse.

In 2022, NIST announced SPHINCS+ as one of three algorithms to be standardized for digital signatures. and in 2024 NIST announced the Stateless Hash-Based Digital Signature Standard (SLH-DSA) based on SPHINCS+.

## History

Leslie Lamport invented hash-based signatures in 1979. The XMSS (eXtended Merkle Signature Scheme) and SPHINCS hash-based signature schemes were introduced in 2010 and 2015, respectively. XMSS was developed by a team of researchers under the direction of Johannes Buchmann and is based both on Merkle's seminal scheme and on the 2007 Generalized Merkle Signature Scheme (GMSS). A multi-tree variant of XMSS, XMSS^(*MT*), was described in 2013.

## One-time signature schemes

Hash-based signature schemes use one-time signature schemes as their building block. A given one-time signing key can only be used to sign a single message securely. Indeed, signatures reveal part of the signing key. The security of (hash-based) one-time signature schemes relies exclusively on the security of an underlying hash function.

Commonly used one-time signature schemes include the Lamport–Diffie scheme, the Winternitz scheme and its improvements, such as the W-OTS^(+) scheme. Unlike the seminal Lamport–Diffie scheme, the Winternitz scheme and variants can sign many bits at once. The number of bits to be signed at once is determined by a value: the Winternitz parameter. The existence of this parameter provides a trade-off between size and speed. Large values of the Winternitz parameter yield short signatures and keys, at the price of slower signing and verifying. In practice, a typical value for this parameter is 16.

In the case of stateless hash-based signatures, few-time signature schemes are used. Such schemes allow security to decrease gradually in case a few-time key is used more than once. HORST is an example of a few-time signature scheme.

## Combining many one-time key pairs into a hash-based signature scheme

The central idea of hash-based signature schemes is to combine a larger number of one-time key pairs into a single structure to obtain a practical way of signing more than once (yet a limited number of times). This is done using a Merkle tree structure, with possible variations. One public and one private key are constructed from the numerous public and private keys of the underlying one-time scheme. The global public key is the single node at the very top of the Merkle tree. Its value is an output of the selected hash function, so a typical public key size is 32 bytes. The validity of this global public key is related to the validity of a given one-time public key using a sequence of tree nodes. This sequence is called the authentication path. It is stored as part of the signature, and allows a verifier to reconstruct the node path between those two public keys.

The global private key is generally handled using a pseudo-random number generator. It is then sufficient to store a seed value. One-time secret keys are derived successively from the seed value using the generator. With this approach, the global private key is also very small, e.g. typically 32 bytes.

The problem of tree traversal is critical to signing performance. Increasingly efficient approaches have been introduced, dramatically speeding up signing time.

Some hash-based signature schemes use multiple layers of tree, offering faster signing at the price of larger signatures. In such schemes, only the lowest layer of trees is used to sign messages, while all other trees sign root values of lower trees.

The Naor–Yung work shows the pattern by which to transfer a limited time signature of the Merkle type family into an unlimited (regular) signature scheme.

## Properties of hash-based signature schemes

Hash-based signature schemes rely on security assumptions about the underlying hash function, but any hash function fulfilling these assumptions can be used. As a consequence, each adequate hash function yields a different corresponding hash-based signature scheme. Even if a given hash function becomes insecure, it is sufficient to replace it by a different, secure one to obtain a secure instantiation of the hash-based signature scheme under consideration. Some hash-based signature schemes (such as XMSS with pseudorandom key generation) are forward secure, meaning that previous signatures remain valid if a secret key is compromised.

The minimality of security assumptions is another characteristic of hash-based signature schemes. Generally, these schemes only require a secure (for instance in the sense of second preimage resistance) cryptographic hash function to guarantee the overall security of the scheme. This kind of assumption is necessary for any digital signature scheme; however, other signature schemes require additional security assumptions, which is not the case here.

Because of their reliance on an underlying one-time signature scheme, hash-based signature schemes can only sign a fixed number of messages securely. In the case of the Merkle and XMSS schemes, a maximum of $2^h$ messages can be signed securely, with $h$ the total Merkle tree height.

## Examples of hash-based signature schemes

Since Merkle's initial scheme, numerous hash-based signature schemes with performance improvements have been introduced. Recent ones include the XMSS, the Leighton–Micali (LMS), the SPHINCS and the BPQS schemes. Most hash-based signature schemes are stateful, meaning that signing requires updating the secret key, unlike conventional digital signature schemes. For stateful hash-based signature schemes, signing requires keeping state of the used one-time keys and making sure they are never reused. The XMSS, LMS and BPQS schemes are stateful, while the SPHINCS scheme is stateless. SPHINCS signatures are larger than XMSS and LMS signatures. BPQS has been designed specifically for blockchain systems. Additionally to the WOTS+ one-time signature scheme, SPHINCS also uses a few-time (hash-based) signature scheme called HORST. HORST is an improvement of an older few-time signature scheme, HORS (Hash to Obtain Random Subset).

The stateful hash-based schemes XMSS and XMSS^(*MT*) are specified in RFC 8391 (XMSS: eXtended Merkle Signature Scheme). Leighton–Micali Hash-Based Signatures are specified in RFC 8554. Practical improvements have been proposed in the literature that alleviate the concerns introduced by stateful schemes. Hash functions appropriate for these schemes include SHA-2, SHA-3 and BLAKE.

The stateless hash-based scheme SLH-DSA is specified in FIPS-205.

## Implementations

The XMSS, GMSS and SPHINCS schemes are available in the Java Bouncy Castle cryptographic APIs. LMS and XMSS schemes are available in the wolfSSL cryptographic APIs. SPHINCS is implemented in the SUPERCOP benchmarking toolkit. Optimised and unoptimised reference implementations of the XMSS RFC exist. The LMS scheme has been implemented in Python and in C following its Internet-Draft.
