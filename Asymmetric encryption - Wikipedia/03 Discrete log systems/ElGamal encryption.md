# ElGamal encryption

Source: <https://en.wikipedia.org/wiki/ElGamal_encryption>

In cryptography, the **ElGamal encryption system** is a public-key encryption algorithm based on the Diffie–Hellman key exchange. It was described by Taher Elgamal in 1985. ElGamal encryption is used in the free GNU Privacy Guard software, recent versions of PGP, and other cryptosystems. The Digital Signature Algorithm (DSA) is a variant of the ElGamal signature scheme, which should not be confused with ElGamal encryption.

ElGamal encryption can be defined over any cyclic group $G$, like multiplicative group of integers modulo *n* if and only if *n* is 1, 2, 4, *p*^(*k*) or 2*p*^(*k*), where *p* is an odd prime and *k* > 0. Its security depends upon the difficulty of the Decisional Diffie Hellman Problem in $G$.

## Algorithm

The algorithm first performs Diffie–Hellman key agreement to establish a shared secret $s$, then uses this as a one-time pad for encrypting the message. ElGamal encryption is performed in three phases: the key generation, the encryption, and the decryption. The first is purely key exchange, whereas the latter two mix key exchange computations with message computations.

### Key generation

The first party, Alice, generates a key pair as follows:

- Generate an efficient description of a cyclic group $G\,$ of order $q\,$ with generator $g$. Let $e$ represent the identity element of $G$.
It is not necessary to come up with a group and generator for each new key. Indeed, one may expect a specific implementation of ElGamal to be hardcoded to use a specific group, or a group from a specific suite. The choice of group is mostly about choosing the size of the keys used.
- Choose an integer $x$ randomly from $\{1, \ldots, q-1\}$.
- Compute $h := g^x$.
- The public key consists of the values $(G,q,g,h)$. Alice publishes this public key and retains $x$ as her private key, which must be kept secret.

### Encryption

A second party, Bob, encrypts a message $M$ to Alice under her public key $(G,q,g,h)$ as follows:

- Map the message $M$ to an element $m$ of $G$ using a reversible mapping function.
- Choose an integer $y$ randomly from $\{1, \ldots, q-1\}$.
- Compute $s := h^y$. This is called the *shared secret*.
- Compute $c_1 := g^y$.
- Compute $c_2 := m \cdot s$.
- Bob sends the ciphertext $(c_1,c_2)$ to Alice.

Note that if one knows both the ciphertext $(c_1,c_2)$ and the plaintext $m$, one can easily find the shared secret $s$, since $c_2 \cdot m^{-1} = s$. Therefore, a new $y$ and hence a new $s$ is generated for every message to improve security. For this reason, $y$ is also called an ephemeral key.

### Decryption

Alice decrypts a ciphertext $(c_1, c_2)$ with her private key $x$ as follows:

- Compute $s := c_1^x$. Since $c_1 = g^y$, $c_1^x = g^{xy} = h^y$, and thus it is the same shared secret that was used by Bob in encryption.
- Compute $s^{-1}$, the inverse of $s$ in the group $G$. This can be computed in one of several ways. If $G$ is a subgroup of a multiplicative group of integers modulo $n$, where $n$ is prime, the modular multiplicative inverse can be computed using the extended Euclidean algorithm. An alternative is to compute $s^{-1}$ as $c_1^{q-x}$. This is the inverse of $s$ because of Lagrange's theorem, since $s \cdot c_1^{q-x} = g^{xy} \cdot g^{(q-x)y} = (g^{q})^y = e^y = e$.
- Compute $m := c_2 \cdot s^{-1}$. This calculation produces the original message $m$, because $c_2 = m \cdot s$; hence $c_2 \cdot s^{-1} = (m \cdot s) \cdot s^{-1} = m \cdot e = m$.
- Map $m$ back to the plaintext message $M$.

### Practical use

Like most public key systems, the ElGamal cryptosystem is usually used as part of a hybrid cryptosystem, where the message itself is encrypted using a symmetric cryptosystem, and ElGamal is then used to encrypt only the symmetric key. This is because asymmetric cryptosystems like ElGamal are usually slower than symmetric ones for the same level of security, so it is faster to encrypt the message, which can be arbitrarily large, with a symmetric cipher, and then use ElGamal only to encrypt the symmetric key, which usually is quite small compared to the size of the message.

## Security

The security of the ElGamal scheme depends on the properties of the underlying group $G$ as well as any padding scheme used on the messages. If the computational Diffie–Hellman assumption (CDH) holds in the underlying cyclic group $G$, then the encryption function is one-way.

If the decisional Diffie–Hellman assumption (DDH) holds in $G$, then ElGamal achieves semantic security. Semantic security is not implied by the computational Diffie–Hellman assumption alone. See Decisional Diffie–Hellman assumption for a discussion of groups where the assumption is believed to hold.

ElGamal encryption is unconditionally malleable, and therefore is not secure under chosen ciphertext attack. For example, given an encryption $(c_1, c_2)$ of some (possibly unknown) message $m$, one can easily construct a valid encryption $(c_1, 2 c_2)$ of the message $2m$.

To achieve chosen-ciphertext security, the scheme must be further modified, or an appropriate padding scheme must be used. Depending on the modification, the DDH assumption may or may not be necessary.

Other schemes related to ElGamal which achieve security against chosen ciphertext attacks have also been proposed. The Cramer–Shoup cryptosystem is secure under chosen ciphertext attack assuming DDH holds for $G$. Its proof does not use the random oracle model. Another proposed scheme is DHIES, whose proof requires an assumption that is stronger than the DDH assumption.

## Efficiency

ElGamal encryption is probabilistic, meaning that a single plaintext can be encrypted to many possible ciphertexts, with the consequence that a general ElGamal encryption produces a 1:2 expansion in size from plaintext to ciphertext.

Encryption under ElGamal requires two exponentiations; however, these exponentiations are independent of the message and can be computed ahead of time if needed. Decryption requires one exponentiation and one computation of a group inverse, which can, however, be easily combined into just one exponentiation.

## See also

- Taher Elgamal, designer of this and other cryptosystems
- ElGamal signature scheme
- Homomorphic encryption
