# Optimal asymmetric encryption padding

Source: <https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding>

In cryptography, **optimal asymmetric encryption padding** (**OAEP**) is a padding scheme often used together with RSA encryption. OAEP was introduced by Bellare and Rogaway, and subsequently standardized in PKCS #1 v2 and RFC 2437.

The OAEP algorithm is a form of Feistel network which uses a pair of random oracles G and H to process the plaintext prior to asymmetric encryption. When combined with any secure trapdoor one-way permutation $f$, this processing is proved in the random oracle model to result in a combined scheme which is semantically secure under chosen-plaintext attack (IND-CPA). When implemented with certain trapdoor permutations (e.g., RSA), OAEP is also proven to be secure against chosen-ciphertext attack. OAEP can be used to build an all-or-nothing transform.

OAEP satisfies the following two goals:

1. Add an element of randomness which can be used to convert a deterministic encryption scheme (e.g., traditional RSA) into a probabilistic scheme.
2. Prevent partial decryption of ciphertexts (or other information leakage) by ensuring that an adversary cannot recover any portion of the plaintext without being able to invert the trapdoor one-way permutation $f$.

The original version of OAEP (Bellare/Rogaway, 1994) showed a form of "plaintext awareness" (which they claimed implies security against chosen-ciphertext attack) in the random oracle model when OAEP is used with any trapdoor permutation. Subsequent results contradicted this claim, showing that OAEP was only IND-CCA1 secure. However, the original scheme was proved in the random oracle model to be IND-CCA2 secure when OAEP is used with the RSA permutation using standard encryption exponents, as in the case of RSA-OAEP. An improved scheme (called OAEP+) that works with any trapdoor one-way permutation was offered by Victor Shoup to solve this problem. More recent work has shown that in the standard model (that is, when hash functions are not modeled as random oracles) it is impossible to prove the IND-CCA2 security of RSA-OAEP under the assumed hardness of the RSA problem.

## Algorithm

In the diagram,

- *MGF* is the mask generating function, usually MGF1,
- *Hash* is the chosen hash function,
- *hLen* is the length of the output of the hash function in bytes,
- *k* is the length of the RSA modulus *n* in bytes,
- *M* is the message to be padded, with length *mLen* (at most $\mathrm{mLen}= k - 2 \cdot \mathrm{hLen} - 2$ bytes),
- *L* is an optional label to be associated with the message (the label is the empty string by default and can be used to authenticate data without requiring encryption),
- *PS* is a byte string of $k - \mathrm{mLen} - 2 \cdot \mathrm{hLen} - 2$ null-bytes.
- ⊕ is an XOR-Operation.

### Encoding

RFC 8017 for PKCS#1 v2.2 specifies the OAEP scheme as follows for encoding:

1. Hash the label *L* using the chosen hash function: $\mathrm{lHash} = \mathrm{Hash}(L)$
2. Generate a padding string *PS* consisting of $k - \mathrm{mLen} - 2 \cdot \mathrm{hLen} - 2$ bytes with the value 0x00.
3. Concatenate *lHash*, *PS*, the single byte 0x01, and the message *M* to form a data block *DB*: $\mathrm{DB} = \mathrm{lHash} || \mathrm{PS} || \mathrm{0x01} || \mathrm{M}$. This data block has length $k - \mathrm{hLen} - 1$ bytes.
4. Generate a random seed of length *hLen*.
5. Use the mask generating function to generate a mask of the appropriate length for the data block: $\mathrm{dbMask} = \mathrm{MGF}(\mathrm{seed}, k - \mathrm{hLen} - 1)$
6. Mask the data block with the generated mask: $\mathrm{maskedDB} = \mathrm{DB} \oplus \mathrm{dbMask}$
7. Use the mask generating function to generate a mask of length *hLen* for the seed: $\mathrm{seedMask} = \mathrm{MGF}(\mathrm{maskedDB}, \mathrm{hLen})$
8. Mask the seed with the generated mask: $\mathrm{maskedSeed} = \mathrm{seed} \oplus \mathrm{seedMask}$
9. The encoded (padded) message is the byte 0x00 concatenated with the *maskedSeed* and *maskedDB*: $\mathrm{EM} = \mathrm{0x00} || \mathrm{maskedSeed} || \mathrm{maskedDB}$

### Decoding

Decoding works by reversing the steps taken in the encoding algorithm:

1. Hash the label *L* using the chosen hash function: $\mathrm{lHash} = \mathrm{Hash}(L)$
2. To reverse step 9, split the encoded message *EM* into the byte 0x00, the *maskedSeed* (with length *hLen*) and the *maskedDB*: $\mathrm{EM} = \mathrm{0x00} || \mathrm{maskedSeed} || \mathrm{maskedDB}$
3. Generate the *seedMask* which was used to mask the *seed*: $\mathrm{seedMask} = \mathrm{MGF}(\mathrm{maskedDB}, \mathrm{hLen})$
4. To reverse step 8, recover the *seed* with the *seedMask*: $\mathrm{seed} = \mathrm{maskedSeed} \oplus \mathrm{seedMask}$
5. Generate the *dbMask* which was used to mask the data block: $\mathrm{dbMask} = \mathrm{MGF}(\mathrm{seed}, k - \mathrm{hLen} - 1)$
6. To reverse step 6, recover the data block *DB:* $\mathrm{DB} = \mathrm{maskedDB} \oplus \mathrm{dbMask}$
7. To reverse step 3, split the data block into its parts: $\mathrm{DB} = \mathrm{lHash'} || \mathrm{PS} || \mathrm{0x01} || \mathrm{M}$.

  1. Verify that:

    - *lHash'* is equal to the computed *lHash*
    - *PS* only consists of bytes 0x00
    - *PS* and *M* are separated by the 0x01 byte and
    - the first byte of *EM* is the byte 0x00.

  2. If any of these conditions aren't met, then the padding is invalid.

Usage in RSA: The encoded message can then be encrypted with RSA. The deterministic property of RSA is now avoided by using the OAEP encoding because the *seed* is randomly generated and influences the entire encoded message.

### Security

The "all-or-nothing" security is from the fact that to recover *M*, one must recover the entire *maskedDB* and the entire *maskedSeed*; *maskedDB* is required to recover the *seed* from the *maskedSeed*, and the *seed* is required to recover the data block *DB* from *maskedDB*. Since any changed bit of a cryptographic hash completely changes the result, the entire *maskedDB*, and the entire *maskedSeed* must both be completely recovered.

### Implementation

In the PKCS#1 standard, the random oracles are identical. The PKCS#1 standard further requires that the random oracles be MGF1 with an appropriate hash function.

## See also

- Key encapsulation
