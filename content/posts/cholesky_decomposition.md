Title: Cholesky Decomposition with R Example
Date: 2016-10-06
Tags: R, linear algebra, matrix decomposition
Category: Linear Algebra
Slug: cholesky-decomposition-r-example
Author: Aaron Schlegel
Summary: Cholesky decomposition, also known as Cholesky factorization, is a
method of decomposing a positive-definite matrix. A positive-definite matrix 
is defined as a symmetric matrix where for all possible vectors $x$, $x'Ax > 0$. 
Cholesky decomposition and other decomposition methods are important as it is 
not often feasible to perform matrix computations explicitly.


Cholesky decomposition, also known as Cholesky factorization, is a
method of decomposing a [positive-definite
matrix](https://en.wikipedia.org/wiki/Positive-definite_matrix). A
positive-definite matrix is defined as a symmetric matrix where for all
possible vectors $x$, $x'Ax > 0$. Cholesky decomposition and other
decomposition methods are important as it is not often feasible to
perform matrix computations explicitly. Some [applications of Cholesky
decomposition](https://en.wikipedia.org/wiki/Cholesky_decomposition#Applications)
include solving systems of linear equations, Monte Carlo simulation, and
Kalman filters.

Cholesky decomposition factors a positive-definite matrix $A$ into:

$$ A = LL^T$$

Where $L$ is a [lower triangular
matrix](https://en.wikipedia.org/wiki/Triangular_matrix#lower_triangular).
$L$ is known as the Cholesky factor of $A$ and can be interpreted as the
square root of a positive-definite matrix.

How to Decompose a Matrix with Cholesky Decomposition
-----------------------------------------------------

There are many methods for computing a matrix decomposition with the
Cholesky approach. This post takes a similar approach to [this
implementation](http://www.math.sjsu.edu/~foster/m143m/cholesky.pdf).

We define the decomposed matrix as $L$. Thus $L_{k-1}$ represents the
$k-1 \times k-1$ upper left corner of $L$. $a_k$ and $l_k$ denote the
first $k - 1$ entries in column $k$ of $A$ and $L$, respectively.
$a_{kk}$ and $l_{kk}$ are defined as the entries of $A$ and $L$.

The steps in factoring the matrix are as follows:

1.  Compute $L_1 = \sqrt{a_{11}}$
2.  For $k = 2, \dots, n$:

-   Find $L_{k-1} l_k = a_k$ for $l_k$
-   $l_{kk} = \sqrt{a_{kk} - l_k^T l_k}$
-   $L_k = \begin{bmatrix} L_{k-1} & 0 \\ l_k^T & l_{kk}\end{bmatrix}$

An Example of Cholesky Decomposition
------------------------------------

Consider the following matrix $A$.

$$A = 
\begin{bmatrix}
  3 & 4 & 3 \\
  4 & 8 & 6 \\
  3 & 6 & 9
\end{bmatrix}$$

The matrix $A$ above is taken from Exercise 2.16 in the book Methods of
Multivariate Analysis by Alvin Rencher.

Begin by finding $L_1$.

$$ L_1 = \sqrt{a_{11}} = \sqrt{3} = 1.732051 $$

Next we find $l_2$

$$ l_2 = \frac{a_{21}}{L_1} = \frac{4}{\sqrt{3}} = 2.309401 $$

Then $l_{22}$ can be computed.

$$ l_{22} = \sqrt{a_{22} - l_2^T l_2} = \sqrt{8 - 2.309401^2} = 1.632993 $$

We now have the $L_2$ matrix:

$$L_2 = 
\begin{bmatrix}
  L_1 & 0 \\
  l_2^T & l_{22}
\end{bmatrix} = 
\begin{bmatrix}
  1.732051 & 0 \\
  2.309401 & 1.632993
\end{bmatrix}$$

Since the matrix is $3 \times 3$, we only require one more iteration.

With $L_2$ computed, $l_3$ can be found:

$$ l_3 = \frac{a_3}{L_2} = a_3 L_2^{-1} = 
\begin{bmatrix}
  1.732051 & 0 \\
  2.309401 & 1.632993
\end{bmatrix}^{-1} 
\begin{bmatrix}
  3 \\
  6
\end{bmatrix}$$

$$l_3 = 
\begin{bmatrix}
  1.7320508 \\
  1.224745 
\end{bmatrix}$$

$l_{33}$ is then found:

$$ l_{33} = \sqrt{a_{33} - l_3^T l_3} = \sqrt{9 - \begin{bmatrix}1.7320508 & 1.224745\end{bmatrix} \begin{bmatrix}1.7320508 \\ 1.224745\end{bmatrix}} = 2.12132 $$

Which gives us the $L_3$ matrix:

$$L_3 = 
\begin{bmatrix}
  1.7320508 & 0 & 0 \\
  2.309401 & 1.632993 & 0 \\
  1.7320508 & 1.224745 & 2.12132
\end{bmatrix}$$

The $L_3$ matrix can then be taken as the solution. Transposing the
decomposition changes the matrix into an upper triangular matrix.

Cholesky Decomposition in R
---------------------------

The function `chol()` performs Cholesky decomposition on a
positive-definite matrix. We define the matrix $A$ as follows.

``` {.r}
A = as.matrix(data.frame(c(3,4,3),c(4,8,6),c(3,6,9)))
colnames(A) <- NULL
A
```

    ##      [,1] [,2] [,3]
    ## [1,]    3    4    3
    ## [2,]    4    8    6
    ## [3,]    3    6    9

Then factor the matrix with the `chol()` function.

``` {.r}
A.chol <- chol(A)
A.chol
```

    ##          [,1]     [,2]     [,3]
    ## [1,] 1.732051 2.309401 1.732051
    ## [2,] 0.000000 1.632993 1.224745
    ## [3,] 0.000000 0.000000 2.121320

The `chol()` function returns an upper triangular matrix. Transposing
the decomposed matrix yields a lower triangular matrix as in our result
above.

``` {.r}
t(A.chol)
```

    ##          [,1]     [,2]    [,3]
    ## [1,] 1.732051 0.000000 0.00000
    ## [2,] 2.309401 1.632993 0.00000
    ## [3,] 1.732051 1.224745 2.12132

Our result above matches the output of the `chol()` function.

We can also show the identity $A = LL^T$ with the result.

``` {.r}
t(A.chol) %*% A.chol
```

    ##      [,1] [,2] [,3]
    ## [1,]    3    4    3
    ## [2,]    4    8    6
    ## [3,]    3    6    9

Summary
-------

Cholesky decomposition is frequently utilized when direct computation of
a matrix is not optimal. The method is employed in a variety of
applications such as multivariate analysis due to its relatively
efficient nature and stability.

References
----------

(2011). Retrieved from
<http://www.seas.ucla.edu/~vandenbe/103/lectures/chol.pdf>

Algorithm for Cholesky decomposition. Retrieved from
<http://www.math.sjsu.edu/~foster/m143m/cholesky.pdf>

Cholesky decomposition (2016). In Wikipedia. Retrieved from
<https://en.wikipedia.org/wiki/Cholesky_decomposition>

Rencher, A. (2002). Methods of Multivariate Analysis (Second Edition
ed.)
