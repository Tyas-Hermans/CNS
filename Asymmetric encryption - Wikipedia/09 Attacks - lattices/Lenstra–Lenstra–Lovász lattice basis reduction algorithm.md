# Lenstra–Lenstra–Lovász lattice basis reduction algorithm

Source: <https://en.wikipedia.org/wiki/Lenstra%E2%80%93Lenstra%E2%80%93Lov%C3%A1sz_lattice_basis_reduction_algorithm>

The **Lenstra–Lenstra–Lovász** (**LLL**) **lattice basis reduction algorithm** is a polynomial time lattice reduction algorithm invented by Arjen Lenstra, Hendrik Lenstra and László Lovász in 1982. Given a basis $\mathbf{B} = \{ \mathbf{b}_1,\mathbf{b}_2, \dots, \mathbf{b}_d \}$ with *n*-dimensional integer coordinates, for a lattice L (a discrete subgroup of **R**^(*n*)) with $d \leq n$, the LLL algorithm calculates an *LLL-reduced* (short, nearly orthogonal) lattice basis in time

$$ \mathcal O(d^5n\log^3 B) $$

where $B$ is the largest length of $\mathbf{b}_i$ under the Euclidean norm, that is, $B = \max\left(\|\mathbf{b}_1\|_2, \|\mathbf{b}_2\|_2, \dots, \|\mathbf{b}_d\|_2\right)$.

The original applications were to give polynomial-time algorithms for factorizing polynomials with rational coefficients, for finding simultaneous rational approximations to real numbers, and for solving the integer linear programming problem in fixed dimensions.

## LLL reduction

The precise definition of LLL-reduced is as follows: Given a basis

$$ \mathbf{B}=\{ \mathbf{b}_1,\mathbf{b}_2, \dots, \mathbf{b}_n \}, $$

define its Gram–Schmidt process orthogonal basis

$$ \mathbf{B}^*=\{ \mathbf{b}^*_1, \mathbf{b}^*_2, \dots, \mathbf{b}^*_n \}, $$

and the Gram-Schmidt coefficients

$$ \mu_{i,j}=\frac{\langle\mathbf{b}_i,\mathbf{b}^*_j\rangle}{\langle\mathbf{b}^*_j,\mathbf{b}^*_j\rangle}, $$

for any $1 \le j < i \le n$. In other words,

$$ \mathbf{b}_i = \mathbf{b}^*_i + \sum_{j=1}^{i-1} \mu_{i,j} \mathbf{b}^*_j $$

for all $1 \leq i \leq n$. Note that the Gram–Schmidt process, as understood here, does not include normalisation of the orthogonal basis.

Then the basis $\mathbf{B}$ is LLL-reduced if there exists a parameter $\delta$ in (0.25, 1] such that the following holds:

1. (size-reduced) For $1 \leq j < i \leq n$, we have $\left|\mu_{i,j}\right|\leq 0.5$. By definition, this property guarantees the length reduction of the ordered basis.
2. (Lovász condition) For $2 \leq k \leq n$, we have $\delta \Vert \mathbf{b}^*_{k-1}\Vert^2 \leq \Vert \mathbf{b}^*_k\Vert^2+ \mu_{k,k-1}^2\Vert \mathbf{b}^*_{k-1}\Vert^2$.

Here, estimating the value of the $\delta$ parameter, we can conclude how well the basis is reduced. Greater values of $\delta$ lead to stronger reductions of the basis. Initially, A. Lenstra, H. Lenstra and L. Lovász demonstrated the LLL-reduction algorithm for $\delta = 3/4$. Note that although LLL-reduction is well-defined for $\delta = 1$, the polynomial-time complexity is guaranteed only for $\delta$ in $(0.25,1)$.

The LLL algorithm computes LLL-reduced bases. There is no known efficient algorithm to compute a basis in which the basis vectors are as short as possible for lattices of dimensions greater than 4. However, an LLL-reduced basis is nearly as short as possible, in the sense that there are absolute bounds $c_i > 1$ such that the first basis vector is no more than $c_1$ times as long as a shortest vector in the lattice, the second basis vector is likewise within $c_2$ of the second successive minimum, and so on.

## Applications

An early successful application of the LLL algorithm was its use by Andrew Odlyzko and Herman te Riele in disproving the Mertens conjecture.

The LLL algorithm has found numerous other applications in MIMO detection algorithms and cryptanalysis of public-key encryption schemes: knapsack cryptosystems, RSA with particular settings, NTRUEncrypt, and so forth. The algorithm can be used to find integer solutions to many problems.

In particular, the LLL algorithm forms a core of one of the integer relation algorithms. For example, if it is believed that *r*=1.618034 is a (slightly rounded) root to an unknown quadratic equation with integer coefficients, one may apply LLL reduction to the lattice in $\mathbf{R}^4$ spanned by $[1,0,0,10000r^2], [0,1,0,10000r],$ and $[0,0,1,10000]$. The first vector in the reduced basis will be an integer linear combination of these three, thus necessarily of the form $[a,b,c,10000(ar^2+br+c)]$; but such a vector is "short" only if *a*, *b*, *c* are small and $ar^2+br+c$ is even smaller. Thus the first three entries of this short vector are likely to be the coefficients of the integral quadratic polynomial which has *r* as a root. In this example the LLL algorithm finds the shortest vector to be [1, -1, -1, 0.00025] and indeed $x^2-x-1$ has a root equal to the golden ratio, 1.6180339887....

## Properties of LLL-reduced basis

Let $\mathbf{B}=\{ \mathbf{b}_1,\mathbf{b}_2, \dots, \mathbf{b}_n \}$ be a $\delta$-LLL-reduced basis of a lattice $\mathcal L$. From the definition of LLL-reduced basis, we can derive several other useful properties about $\mathbf{B}$.

1. The first vector in the basis cannot be much larger than the shortest non-zero vector: $\Vert\mathbf{b}_1 \Vert \le (2 / (\sqrt{4\delta - 1}))^{n-1} \cdot \lambda_1(\mathcal L)$. In particular, for $\delta = 3/4$, this gives $\Vert\mathbf{b}_1 \Vert \le 2^{(n-1)/2} \cdot \lambda_1(\mathcal L)$.
2. The first vector in the basis is also bounded by the determinant of the lattice: $\Vert\mathbf{b}_1 \Vert \le (2 / (\sqrt{4\delta - 1}))^{(n-1)/2} \cdot (\det(\mathcal L))^{1/n}$. In particular, for $\delta = 3/4$, this gives $\Vert\mathbf{b}_1 \Vert \le 2^{(n-1)/4} \cdot (\det(\mathcal L))^{1/n}$.
3. The product of the norms of the vectors in the basis cannot be much larger than the determinant of the lattice: let $\delta = 3/4$, then $\prod_{i=1}^n \Vert\mathbf{b}_i \Vert \le 2^{n(n-1)/4} \cdot \det(\mathcal L)$.

## LLL algorithm pseudocode

The following description is based on (Hoffstein, Pipher & Silverman 2008, Theorem 6.68), with the corrections from the errata.

```
**INPUT**
a lattice basis **b**_1, **b**_2, ..., **b**_(*n*) in **Z**^(*m*)
a parameter *δ* with 1/4 < *δ* < 1, most commonly *δ* = 3/4
**PROCEDUREB^(*)** <- GramSchmidt({**b**_1, ..., **b**_(*n*)}) = {**b**_1^(*), ..., **b**_(*n*)^(*)};  *and do not normalize*
*μ*_(*i*,*j*) <- InnerProduct(**b**_(*i*), **b**_(*j*)^(*))/InnerProduct(**b**_j^(*), **b**_(*j*)^(*));   *using the most current values of* **b**_(*i*) and **b**_(*j*)^(*)
*k* <- 2;
**while** *k* <= *n* **dofor** *j* **from** *k*−1 **to** 1 **doif** |*μ*_(*k*,*j*)| > 1/2 **thenb**_(*k*) <- **b**_(*k*) − ⌊*μ*_(*k*,*j*)⌉**b**_(*j*);
*Update* **B^(*)** *and the related* *μ*_(*i*,*j*)*'s as needed.*
*(The naive method is to recompute* **B^(*)** *whenever* **b_(*i*)** *changes:*
**B^(*)** <- GramSchmidt({**b**_1, ..., **b**_(*n*)}) = {**b**_1^(*), ..., **b**_(*n*)^(*)})
**end ifend forif** InnerProduct(**b**_(*k*)^(*), **b**_(*k*)^(*)) > (*δ − μ^2*_(*k*,*k*−1)) InnerProduct(**b**_(*k*−1)^(*), **b**_(*k*−1)^(*)) **then**
*k* <- *k* + 1;
**else**
Swap **b**_(*k*) and  **b**_(*k*−1);
*Update* **B^(*)** *and the related* *μ*_(*i*,*j*)*'s as needed.*
*k* <- max(*k*−1, 2);
**end ifend whilereturnB** the LLL reduced basis of {b_1, ..., b_(*n*)}
**OUTPUT**
the reduced basis **b**_1, **b**_2, ..., **b**_(*n*) in **Z**^(*m*)
```

## Examples

### Example from Z^3

Let a lattice basis $\mathbf{b}_1,\mathbf{b}_2, \mathbf{b}_3 \in \mathbf{Z}^{3}$, be given by the columns of

$$ \begin{bmatrix} 1 & -1& 3\\ 1 & 0 & 5\\ 1 & 2 & 6 \end{bmatrix} $$

then the reduced basis is

$$ \begin{bmatrix} 0 & 1& -1\\ 1 & 0 & 0\\ 0 & 1 & 2 \end{bmatrix}, $$

which is size-reduced, satisfies the Lovász condition, and is hence LLL-reduced, as described above. See W. Bosma. for details of the reduction process.

### Example from Z[*i*]^4

Likewise, for the basis over the complex integers given by the columns of the matrix below,

$$ \begin{bmatrix} -2+2i & 7+3i & 7+3i & -5+4i\\ 3+3i & -2+4i & 6+2i & -1+4i\\ 2+2i & -8+0i & -9+1i & -7+5i\\ 8+2i & -9+0i & 6+3i & -4+4i \end{bmatrix}, $$

then the columns of the matrix below give an LLL-reduced basis.

$$ \begin{bmatrix} -6+3i & -2+2i & 2-2i & -3+6i \\ 6-1i & 3+3i & 5-5i & 2+1i \\ 2-2i & 2+2i & -3-1i & -5+3i \\ -2+1i & 8+2i & 7+1i & -2-4i \\ \end{bmatrix}. $$

## Implementations

LLL is implemented in

- Arageli as the function `lll_reduction_int`
- fpLLL as a stand-alone implementation
- FLINT as the function `fmpz_lll`
- GAP as the function `LLLReducedBasis`
- Macaulay2 as the function `LLL` in the package `LLLBases`
- Magma as the functions `LLL` and `LLLGram` (taking a gram matrix)
- Maple as the function `IntegerRelations[LLL]`
- Mathematica as the function `LatticeReduce`
- Number Theory Library (NTL) as the function `LLL`
- PARI/GP as the function `qflll`
- Pymatgen as the function `analysis.get_lll_reduced_lattice`
- SageMath as the method `LLL` driven by fpLLL and NTL
- Isabelle/HOL in the 'archive of formal proofs' entry `LLL_Basis_Reduction`. This code exports to efficiently executable Haskell.

## See also

- Coppersmith method
