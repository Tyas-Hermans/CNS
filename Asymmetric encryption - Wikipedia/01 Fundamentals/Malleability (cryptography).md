# Malleability (cryptography)

Source: <https://en.wikipedia.org/wiki/Malleability_%28cryptography%29>

**Malleability** is a property of some cryptographic algorithms. An encryption algorithm is said to be malleable if it is possible to transform a ciphertext into another ciphertext which decrypts to a related plaintext. That is, given an encryption of a plaintext $m$, it is possible to generate another ciphertext which decrypts to $f(m)$, for a known function $f$, without necessarily knowing or learning $m$.

Malleability is often an undesirable property in a general-purpose cryptosystem, since it allows an attacker to modify the contents of a message. For example, suppose that a bank uses a stream cipher to hide its financial information, and a user sends an encrypted message containing, say, "TRANSFER $0000100.00 TO ACCOUNT #199." If an attacker can modify the message on the wire, and can guess the format of the unencrypted message, the attacker could change the amount of the transaction, or the recipient of the funds, e.g. "TRANSFER $0100000.00 TO ACCOUNT #227". Malleability does not refer to the attacker's ability to read the encrypted message. Both before and after tampering, the attacker cannot read the encrypted message.

On the other hand, some cryptosystems are malleable by design. In other words, in some circumstances it may be viewed as a feature that anyone can transform an encryption of $m$ into a valid encryption of $f(m)$ (for some restricted class of functions $f$) without necessarily learning $m$. Such schemes are known as homomorphic encryption schemes.

A cryptosystem may be semantically secure against chosen-plaintext attacks or even non-adaptive chosen-ciphertext attacks (CCA1) while still being malleable. However, security against adaptive chosen-ciphertext attacks (CCA2) is equivalent to non-malleability.

## Example malleable cryptosystems

In a stream cipher, the ciphertext is produced by taking the exclusive or of the plaintext and a pseudorandom stream based on a secret key $k$, as $E(m) = m \oplus S(k)$. An adversary can construct an encryption of $m \oplus t$ for any $t$, as $E(m) \oplus t = m \oplus t \oplus S(k) = E(m \oplus t)$.

In the RSA cryptosystem, a plaintext $m$ is encrypted as $E(m) = m^e \bmod n$, where $(e,n)$ is the public key. Given such a ciphertext, an adversary can construct an encryption of $mt$ for any $t$, as $E(m) \cdot t^e \bmod n = (mt)^e \bmod n = E(mt)$. For this reason, RSA is commonly used together with padding methods such as OAEP or PKCS1.

In the ElGamal cryptosystem, a plaintext $m$ is encrypted as $E(m) = (g^b, m A^b)$, where $(g,A)$ is the public key. Given such a ciphertext $(c_1, c_2)$, an adversary can compute $(c_1, t \cdot c_2)$, which is a valid encryption of $tm$, for any $t$. In contrast, the Cramer-Shoup system (which is based on ElGamal) is not malleable.

In the Paillier, ElGamal, and RSA cryptosystems, it is also possible to combine *several* ciphertexts together in a useful way to produce a related ciphertext. In Paillier, given only the public key and an encryption of $m_1$ and $m_2$, one can compute a valid encryption of their sum $m_1+m_2$. In ElGamal and in RSA, one can combine encryptions of $m_1$ and $m_2$ to obtain a valid encryption of their product $m_1 m_2$.

Block ciphers in the cipher block chaining mode of operation, for example, are partly malleable: flipping a bit in a ciphertext block will completely mangle the plaintext it decrypts to, but will result in the same bit being flipped in the plaintext of the next block. This allows an attacker to 'sacrifice' one block of plaintext in order to change some data in the next one, possibly managing to maliciously alter the message. This is essentially the core idea of the padding oracle attack on CBC, which allows the attacker to decrypt almost an entire ciphertext without knowing the key. For this and many other reasons, a message authentication code is required to guard against any method of tampering.

## Complete non-malleability

Fischlin, in 2005, defined the notion of complete non-malleability as the ability of the system to remain non-malleable while giving the adversary additional power to choose a new public key which could be a function of the original public key. In other words, the adversary shouldn't be able to come up with a ciphertext whose underlying plaintext is related to the original message through a relation that also takes public keys into account.

## See also

- Homomorphic encryption
