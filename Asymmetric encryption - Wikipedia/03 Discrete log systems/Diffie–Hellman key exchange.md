# Diffie–Hellman key exchange

Source: <https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange>

**Diffie–Hellman** (**DH**) **key exchange** is a mathematical method of securely generating a symmetric cryptographic key over a public channel. It is named after Whitfield Diffie and Martin Hellman who published it in 1976. DH is one of the earliest practical examples of key exchange implemented within the field of cryptography.

Traditionally, secure encrypted communication between two parties required that they first exchange keys by some secure physical means, such as paper key lists transported by a trusted courier. By contrast, the Diffie–Hellman key exchange method allows two parties that have no prior knowledge of each other to jointly establish a shared secret key over an insecure channel. This key can then be used to encrypt subsequent communications using a symmetric-key cipher.

The scheme was published by Whitfield Diffie and Martin Hellman in 1976 and named as one of Ralph Merkle's original public key protocols in 1978. The method was followed shortly after by the RSA cryptosystem, an implementation of public-key cryptography using asymmetric algorithms. In 1997 it was revealed that James H. Ellis, Clifford Cocks, and Malcolm J. Williamson of GCHQ, the British signals intelligence agency, had previously shown in 1969 how public-key cryptography could be achieved.

Diffie–Hellman is used to secure a variety of Internet services. However, research published in October 2015 suggests that the parameters in use for many DH Internet applications at that time were not strong enough to prevent compromise by very well-funded attackers, such as the security services of some countries.

Although Diffie–Hellman key exchange itself is a non-authenticated key-agreement protocol, it provides the basis for a variety of authenticated protocols, and is used to provide forward secrecy in Transport Layer Security's ephemeral modes (referred to as EDH or DHE depending on the cipher suite). Forward secrecy results from the use of ephemeral keys: the private keys are discarded once key agreement is complete, making them safe from later compromise. Ephemeral keys are practical because it is computationally cheap to create public-private key pairs suitable for use with Diffie-Hellman exchange.

Expired US patent 4200770 from 1977 describes the now public-domain algorithm. It credits Hellman, Diffie, and Merkle as inventors.

## Name

In 2006, Hellman suggested the algorithm be called **Diffie–Hellman–Merkle key exchange** in recognition of Ralph Merkle's contribution to the invention of public-key cryptography (Hellman, 2006), writing:

The system ... has since become known as Diffie–Hellman key exchange. While that system was first described in a paper by Diffie and me, it is a public key distribution system, a concept developed by Merkle, and hence should be called 'Diffie–Hellman–Merkle key exchange' if names are to be associated with it. I hope this small pulpit might help in that endeavor to recognize Merkle's equal contribution to the invention of public key cryptography.

## Description

### General overview

Diffie–Hellman key exchange establishes a shared secret between two parties that can be used for secret communication for exchanging data over a public network. An analogy illustrates the concept of public key exchange by using colors instead of very large numbers:

The process begins by having the two parties, Alice and Bob, publicly agree on an arbitrary starting color that does not need to be kept secret. In this example, the color is yellow. Each person also selects a secret color that they keep to themselves – in this case, red and cyan. The crucial part of the process is that Alice and Bob each mix their own secret color together with their mutually shared color, resulting in orange-tan and light-blue mixtures respectively, and then publicly exchange the two mixed colors. Finally, each of them mixes the color they received from the partner with their own private color. The result is a final color mixture (yellow-brown in this case) that is identical to their partner's final color mixture.

If a third party listened to the exchange, they would only know the common color (yellow) and the first mixed colors (orange-tan and light-blue), but it would be very hard for them to find out the final secret color (yellow-brown). Bringing the analogy back to a real-life exchange using large numbers rather than colors, this determination is computationally expensive; it is impossible to compute in a practical amount of time even for modern supercomputers.

### Cryptographic explanation

The simplest and the original implementation, later formalized as **Finite Field Diffie–Hellman** in RFC 7919, of the protocol uses the multiplicative group of integers modulo *p*, where *p* is prime, and *g* is a primitive root modulo *p*. To guard against potential vulnerabilities, it is recommended to use prime numbers of at least 2048 bits in length. This increases the difficulty for an adversary attempting to compute the discrete logarithm and compromise the shared secret. These two values are chosen in this way to ensure that the resulting shared secret can take on any value from 1 to *p* − 1. Here is an example of the protocol, with non-secret values in blue, and secret values in **red**.

1. Alice and Bob publicly agree to use a modulus *p* = 23 and base *g* = 5 (which is a primitive root modulo 23).
2. Alice chooses a secret integer ***a*** = 4, then sends Bob *A* = *g^(**a**)* mod *p*

  - *A* = 5^(**4**) mod 23 = 4 (in this example both *A* and ***a*** have the same value 4, but this is usually not the case)

3. Bob chooses a secret integer ***b*** = 3, then sends Alice *B* = *g^(**b**)* mod *p*

  - *B* = 5^(**3**) mod 23 = 10

4. Alice computes ***s*** = *B^(**a**)* mod *p*

  - ***s*** = 10^(**4**) mod 23 = **18**

5. Bob computes ***s*** = *A^(**b**)* mod *p*

  - ***s*** = 4^(**3**) mod 23 = **18**

6. Alice and Bob now share a secret (the number 18).

Both Alice and Bob have arrived at the same values because under mod *p*,
    ${\color{Blue}A}^{\color{Red}\boldsymbol{b}}\bmod {\color{Blue}p} = {\color{Blue}g}^{\color{Red}\boldsymbol{ab}}\bmod {\color{Blue}p} = {\color{Blue}g}^{\color{Red}\boldsymbol{ba}}\bmod {\color{Blue}p} = {\color{Blue}B}^{\color{Red}\boldsymbol{a}}\bmod {\color{Blue}p}$

More specifically,
    $({\color{Blue}g}^{\color{Red}\boldsymbol{a}}\bmod {\color{Blue}p})^{\color{Red}\boldsymbol{b}}\bmod {\color{Blue}p} = ({\color{Blue}g}^{\color{Red}\boldsymbol{b}}\bmod {\color{Blue}p})^{\color{Red}\boldsymbol{a}}\bmod {\color{Blue}p}$

Only *a* and *b* are kept secret. All the other values – *p*, *g*, *g^a* mod *p*, and *g^b* mod *p* – are sent in the clear. The strength of the scheme comes from the fact that *g^(ab)* mod *p* = *g^(ba)* mod *p* take extremely long times to compute by any known classical algorithm just from the knowledge of *p*, *g*, *g^a* mod *p*, and *g^b* mod *p*. Such a function that is easy to compute but hard to invert is called a one-way function. Once Alice and Bob compute the shared secret they can use it as an encryption key, known only to them, for sending messages across the same open communications channel.

Of course, much larger values of *a*, *b*, and *p* would be needed to make this example secure, since there are only 23 possible results of *n* mod 23. However, if *p* is a prime of at least 600 digits, then even the fastest modern computers using the fastest known algorithm cannot find *a* given only *g*, *p* and *g^a* mod *p*. Such a problem is called the discrete logarithm problem. The computation of *g^a* mod *p* is known as modular exponentiation and can be done efficiently even for large numbers. Note that *g* does not need to be large at all, and in practice is usually a small integer (like 2, 3, ...).

### Secrecy chart

The chart below depicts who knows what, again with non-secret values in blue, and secret values in **red**. Here Eve is an eavesdropper – she watches what is sent between Alice and Bob, but she does not alter the contents of their communications.

- *g*, public (primitive root) base, known to Alice, Bob, and Eve. *g* = 5
- *p*, public (prime) modulus, known to Alice, Bob, and Eve. *p* = 23
- ***a***, Alice's private key, known only to Alice. ***a*** = **6**
- ***b***, Bob's private key known only to Bob. ***b*** = **15**
- *A*, Alice's public key, known to Alice, Bob, and Eve. *A* = *g^(**a**)* mod *p* = 8
- *B*, Bob's public key, known to Alice, Bob, and Eve. *B* = *g^(**b**)* mod *p* = 19

|

Alice
|  Known |  Unknown |
|  *p* = 23 |   |
|  *g* = 5 |   |
|  ***a*** = **6** |  ***b*** |
|  *A* = 5^(***a***) mod 23 |   |
|  *A* = 5^(**6**) mod 23 = 8 |   |
|  *B* = 19 |   |
|  ***s*** = B^(***a***) mod 23 |   |
|  ***s*** = 19^(**6**) mod 23 = **2** |   |

|

Bob
|  Known |  Unknown |
|  *p* = 23 |   |
|  *g* = 5 |   |
|  ***b*** = **15** |  ***a*** |
|  *B* = 5^(***b***) mod 23 |   |
|  *B* = 5^(**15**) mod 23 = 19 |   |
|  *A* = 8 |   |
|  ***s*** = A^(***b***) mod 23 |   |
|  ***s*** = 8^(**15**) mod 23 = **2** |   |

|

Eve
|  Known |  Unknown |
|  *p* = 23 |   |
|  *g* = 5 |   |
|   |  ***a***, ***b*** |
|    |    |
|    |    |
|  *A* = 8, *B* = 19 |   |
|    |    |
|   |  ***s*** |

|

Now ***s*** is the shared secret key and it is known to both Alice and Bob, but *not* to Eve. Note that it is not helpful for Eve to compute *AB*, which equals *g*^(***a***+***b***) mod p.

Note: It should be difficult for Alice to solve for Bob's private key or for Bob to solve for Alice's private key. If it is not difficult for Alice to solve for Bob's private key (or vice versa), then an eavesdropper, Eve, may simply substitute her own private / public key pair, plug Bob's public key into her private key, produce a fake shared secret key, and solve for Bob's private key (and use that to solve for the shared secret key). Eve may attempt to choose a public / private key pair that will make it easy for her to solve for Bob's private key.

### Generalization to finite cyclic groups

Here is a more general description of the protocol:

1. Alice and Bob agree on a natural number *n* and a generating element *g* in the finite cyclic group *G* of order *n*. (This is usually done long before the rest of the protocol; *g* and *n* are assumed to be known by all attackers.) The group *G* is written multiplicatively.
2. Alice picks a random natural number *a* with 1 < *a* < *n*, and sends the element *g^a* of *G* to Bob.
3. Bob picks a random natural number *b* with 1 < *b* < *n*, and sends the element *g^b* of *G* to Alice.
4. Alice computes the element (*g^b*)^(*a*) = *g^(ba)* of G.
5. Bob computes the element (*g^a*)^(*b*) = *g^(ab)* of G.

Both Alice and Bob are now in possession of the group element *g^(ab)* = *g^(ba)*, which can serve as the shared secret key. The group *G* satisfies the requisite condition for secure communication as long as there is no efficient algorithm for determining *g^(ab)* given *g*, *g^a*, and *g^b*.

For example, the elliptic curve Diffie–Hellman protocol is a variant that represents an element of G as a point on an elliptic curve instead of as an integer modulo n. Variants using hyperelliptic curves have also been proposed. The supersingular isogeny key exchange is a Diffie–Hellman variant that was designed to be secure against quantum computers, but it was broken in July 2022.

## Ephemeral and/or static keys

The used keys can either be ephemeral or static (long term) key, but could even be mixed, so called semi-static DH. These variants have different properties and hence different use cases. An overview over many variants and some also discussions can for example be found in NIST SP 800-56A. A basic list:

1. ephemeral, ephemeral: Usually used for key agreement. Provides forward secrecy, but no authenticity.
2. static, static: Would generate a long term shared secret. Does not provide forward secrecy, but implicit authenticity. Since the keys are static it would for example not protect against replay-attacks.
3. ephemeral, static: For example, used in ElGamal encryption or Integrated Encryption Scheme (IES). If used in key agreement it could provide implicit one-sided authenticity (the ephemeral side could verify the authenticity of the static side). No forward secrecy is provided.

It is possible to use ephemeral and static keys in one key agreement to provide more security as for example shown in NIST SP 800-56A, but it is also possible to combine those in a single DH key exchange, which is then called triple DH (3-DH).

### Triple Diffie–Hellman (3-DH)

In 1997 a kind of triple DH was proposed by Simon Blake-Wilson, Don Johnson and Alfred Menezes, which was improved by C. Kudla and K. G. Paterson in 2005 and shown to be secure.

The long term secret keys of Alice and Bob are denoted by *a* and *b* respectively, with public keys *A* and *B*, as well as the ephemeral key pairs (*x*, *X*) and (*y*, *Y*). Then protocol is:

Triple Diffie–Hellman (3-DH) protocol
| Alice ($A = g^a$) |   |  Bob ($B = g^b$) |
|  $X = g^x$ |  $X \rightarrow {}$ |   |
|   |  ${} \leftarrow Y$ |  $Y = g^y$ |
|  $K = \operatorname{KDF}\left( Y^x,\, B^x,\, Y^a,\, X,\, Y,\, A,\, B \right)$ |   |  $K = \operatorname{KDF}\left( X^y,\, X^b,\, A^y,\, X,\, Y,\, A,\, B \right)$ |

The long term public keys need to be transferred somehow. That can be done beforehand in a separate, trusted channel, or the public keys can be encrypted using some partial key agreement to preserve anonymity. For more of such details as well as other improvements like side channel protection or explicit key confirmation, as well as early messages and additional password authentication, see e.g. US patent "Advanced modular handshake for key agreement and optional authentication".

### Extended Triple Diffie–Hellman (X3DH)

X3DH was initially proposed as part of the Double Ratchet Algorithm used in the Signal Protocol. The protocol offers forward secrecy and cryptographic deniability. It operates on an elliptic curve.

The protocol uses five public keys. Alice has an identity key IK_A and an ephemeral key EK_A. Bob has an identity key IK_B, a signed prekey SPK_B, and a one-time prekey OPK_B. Bob first publishes his three keys to a server, which Alice downloads and verifies the signature on. Alice then initiates the exchange to Bob. The OPK is optional.

## Operation with more than two parties

Diffie–Hellman key agreement is not limited to negotiating a key shared by only two participants. Any number of users can take part in an agreement by performing iterations of the agreement protocol and exchanging intermediate data (which does not itself need to be kept secret). For example, Alice, Bob, and Carol could participate in a Diffie–Hellman agreement as follows, with all operations taken to be modulo *p*:

1. The parties agree on the algorithm parameters *p* and *g*.
2. The parties generate their private keys, named *a*, *b*, and *c*.
3. Alice computes g^a mod p and sends it to Bob.
4. Bob computes (g^a)^b mod p = g^(ab) mod p and sends it to Carol.
5. Carol computes (g^(ab))^c mod p = g^(abc) mod p and uses it as her secret.
6. Bob computes g^b mod p and sends it to Carol.
7. Carol computes (g^b)^c mod p = g^(bc) mod p and sends it to Alice.
8. Alice computes (g^(bc))^a mod p = g^(bca) mod p = g^(abc) mod p and uses it as her secret.
9. Carol computes g^c mod p and sends it to Alice.
10. Alice computes (g^c)^a mod p = g^(ca) mod p and sends it to Bob.
11. Bob computes (g^(ca))^b mod p = g^(cab) mod p = g^(abc) mod p and uses it as his secret.

An eavesdropper has been able to see g^a mod p, g^b mod p, g^c mod p, g^(ab) mod p, g^(ac) mod p, and g^(bc) mod p, but cannot use any combination of these to efficiently reproduce g^(abc) mod p.

To extend this mechanism to larger groups, two basic principles must be followed:

- Starting with an "empty" key consisting only of *g*, the secret is made by raising the current value to every participant's private exponent once, in any order (the first such exponentiation yields the participant's own public key).
- Any intermediate value (having up to *N*−1 exponents applied, where *N* is the number of participants in the group) may be revealed publicly, but the final value (having had all *N* exponents applied) constitutes the shared secret and hence must never be revealed publicly. Thus, each user must obtain their copy of the secret by applying their own private key last (otherwise there would be no way for the last contributor to communicate the final key to its recipient, as that last contributor would have turned the key into the very secret the group wished to protect).

These principles leave open various options for choosing in which order participants contribute to keys. The simplest and most obvious solution is to arrange the *N* participants in a circle and have *N* keys rotate around the circle, until eventually every key has been contributed to by all *N* participants (ending with its owner) and each participant has contributed to *N* keys (ending with their own). However, this requires that every participant perform *N* modular exponentiations.

By choosing a more desirable order, and relying on the fact that keys can be duplicated, it is possible to reduce the number of modular exponentiations performed by each participant to log_2(*N*) + 1 using a divide-and-conquer-style approach, given here for eight participants:

1. Participants A, B, C, and D each perform one exponentiation, yielding g^(abcd); this value is sent to E, F, G, and H. In return, participants A, B, C, and D receive g^(efgh).
2. Participants A and B each perform one exponentiation, yielding g^(efghab), which they send to C and D, while C and D do the same, yielding g^(efghcd), which they send to A and B.
3. Participant A performs an exponentiation, yielding g^(efghcda), which it sends to B; similarly, B sends g^(efghcdb) to A. C and D do similarly.
4. Participant A performs one final exponentiation, yielding the secret g^(efghcdba) = g^(abcdefgh), while B does the same to get g^(efghcdab) = g^(abcdefgh); again, C and D do similarly.
5. Participants E through H simultaneously perform the same operations using g^(abcd) as their starting point.

Once this operation has been completed all participants will possess the secret g^(abcdefgh), but each participant will have performed only four modular exponentiations, rather than the eight implied by a simple circular arrangement.

## Security and practical considerations

The protocol is considered secure against eavesdroppers if *G* and *g* are chosen properly. In particular, the order of the group G must be large, particularly if the same group is used for large amounts of traffic. The eavesdropper has to solve the Diffie–Hellman problem to obtain *g*^(*ab*). This is currently considered difficult for groups whose order is large enough. An efficient algorithm to solve the discrete logarithm problem would make it easy to compute *a* or *b* and solve the Diffie–Hellman problem, making this and many other public key cryptosystems insecure. Fields of small characteristic may be less secure.

The order of *G* should have a large prime factor to prevent use of the Pohlig–Hellman algorithm to obtain *a* or *b*. For this reason, a Sophie Germain prime *q* is sometimes used to calculate *p* = 2*q* + 1, called a safe prime, since the order of *G* is then only divisible by 2 and *q*. Sometimes *g* is chosen to generate the order *q* subgroup of *G*, rather than *G*, so that the Legendre symbol of *g^a* never reveals the low order bit of *a*. A protocol using such a choice is for example IKEv2.

The generator *g* is often a small integer such as 2. Because of the random self-reducibility of the discrete logarithm problem a small *g* is equally secure as any other generator of the same group.

If Alice and Bob use random number generators whose outputs are not completely random and can be predicted to some extent, then it is much easier to eavesdrop.

In the original description, the Diffie–Hellman exchange by itself does not provide authentication of the communicating parties and can be vulnerable to a man-in-the-middle attack. Mallory (an active attacker executing the man-in-the-middle attack) may establish two distinct key exchanges, one with Alice and the other with Bob, effectively masquerading as Alice to Bob, and vice versa, allowing her to decrypt, then re-encrypt, the messages passed between them. Note that Mallory must be in the middle from the beginning and continuing to be so, actively decrypting and re-encrypting messages every time Alice and Bob communicate. If she arrives after the keys have been generated and the encrypted conversation between Alice and Bob has already begun, the attack cannot succeed. If she is ever absent, her previous presence is then revealed to Alice and Bob. They will know that all of their private conversations had been intercepted and decoded by someone in the channel. In most cases it will not help them get Mallory's private key, even if she used the same key for both exchanges.

A method to authenticate the communicating parties to each other is generally needed to prevent this type of attack. Variants of Diffie–Hellman, such as STS protocol, may be used instead to avoid these types of attacks.

### Denial-of-service attack

A CVE released in 2021 (*CVE-2002-20001*) disclosed a denial-of-service attack (DoS) against the protocol variants using ephemeral keys, called D(HE)at attack. The attack exploits that the Diffie–Hellman key exchange allows attackers to send arbitrary numbers that are actually not public keys, triggering expensive modular exponentiation calculations on the victim's side. Another CVEs release disclosed that the Diffie–Hellman key exchange implementations may use long private exponents (*CVE-2022-40735*) that arguably make modular exponentiation calculations unnecessarily expensive or may unnecessarily check a peer's public key (*CVE-2024-41996*) which has similar resource requirement as key calculation using a long exponent. An attacker can exploit both vulnerabilities together.

### Practical attacks on Internet traffic

The number field sieve algorithm, which is generally the most effective in solving the discrete logarithm problem, consists of four computational steps. The first three steps only depend on the order of the group G, not on the specific number whose finite log is desired. It turns out that much Internet traffic uses one of a handful of groups that are of order 1024 bits or less. By precomputing the first three steps of the number field sieve for the most common groups, an attacker need only carry out the last step, which is much less computationally expensive than the first three steps, to obtain a specific logarithm. The Logjam attack used this vulnerability to compromise a variety of Internet services that allowed the use of groups whose order was a 512-bit prime number, so called export grade. The authors needed several thousand CPU cores for a week to precompute data for a single 512-bit prime. Once that was done, individual logarithms could be solved in about a minute using two 18-core Intel Xeon CPUs.

As estimated by the authors behind the Logjam attack, the much more difficult precomputation needed to solve the discrete log problem for a 1024-bit prime would cost on the order of $100 million, well within the budget of a large national intelligence agency such as the U.S. National Security Agency (NSA). The Logjam authors speculate that precomputation against widely reused 1024-bit DH primes is behind claims in leaked NSA documents that NSA is able to break much of current cryptography.

To avoid these vulnerabilities, the Logjam authors recommend use of elliptic curve cryptography, for which no similar attack is known. Failing that, they recommend that the order, *p*, of the Diffie–Hellman group should be at least 2048 bits. They estimate that the pre-computation required for a 2048-bit prime is 10^9 times more difficult than for 1024-bit primes.

### Security against quantum computers

Quantum computers can break public-key cryptographic schemes, such as RSA, finite-field DH and elliptic-curve DH key-exchange protocols, using Shor's algorithm for solving the factoring problem, the discrete logarithm problem, and the period-finding problem. A post-quantum variant of Diffie-Hellman algorithm was proposed in 2023, and relies on a combination of the quantum-resistant CRYSTALS-Kyber protocol, as well as the old elliptic curve X25519 protocol.

## Other uses

### Encryption

Public key encryption schemes based on the Diffie–Hellman key exchange have been proposed. The first such scheme is the ElGamal encryption. A more modern variant is the Integrated Encryption Scheme.

### Forward secrecy

Protocols that achieve forward secrecy generate new key pairs for each session and discard them at the end of the session. The Diffie–Hellman key exchange is a frequent choice for such protocols, because of its fast key generation.

### Password-authenticated key agreement

When Alice and Bob share a password, they may use a password-authenticated key agreement (PK) form of Diffie–Hellman to prevent man-in-the-middle attacks. One simple scheme is to compare the hash of **s** concatenated with the password calculated independently on both ends of channel. A feature of these schemes is that an attacker can only test one specific password on each iteration with the other party, and so the system provides good security with relatively weak passwords. This approach is described in ITU-T Recommendation X.1035, which is used by the G.hn home networking standard.

An example of such a protocol is the Secure Remote Password protocol.

### Public key

It is also possible to use Diffie–Hellman as part of a public key infrastructure, allowing Bob to encrypt a message so that only Alice will be able to decrypt it, with no prior communication between them other than Bob having trusted knowledge of Alice's public key. Alice's public key is $(g^a \bmod{p}, g, p)$. To send her a message, Bob chooses a random *b* and then sends Alice $g^b \bmod p$ (unencrypted) together with the message encrypted with symmetric key $(g^a)^b \bmod{p}$. Only Alice can determine the symmetric key and hence decrypt the message because only she has *a* (the private key). A pre-shared public key also prevents man-in-the-middle attacks.

In practice, Diffie–Hellman is not used in this way, with RSA being the dominant public key algorithm. This is largely for historical and commercial reasons, namely that RSA Security created a certificate authority for key signing that became Verisign. Diffie–Hellman, as elaborated above, cannot directly be used to sign certificates. However, the ElGamal and DSA signature algorithms are mathematically related to it, as well as MQV, STS and the IKE component of the IPsec protocol suite for securing Internet Protocol communications.

## See also

- Elliptic-curve Diffie–Hellman key exchange
- Supersingular isogeny key exchange
- Forward secrecy
- Diffie–Hellman problem
- Modular exponentiation
- Denial-of-service attack
- Post-Quantum Extended Diffie–Hellman
- Accumulator (cryptography)
