Title: Singular Value Decomposition and R Example
Date: 2016-11-03
Tags: R, singular value decomposition, linear algebra, matrices
Category: R
Slug: singular-value-decomposition-r
Author: Aaron Schlegel
Summary: SVD underpins many statistical and real-world
applications principal component analysis, image compression, noise
reduction of an image, and even climate studies. Singular value
decomposition was also a primary technique used in the winning solution
of Netflix's \$1 million recommendation system improvement contest.


Following from a previous post on the [Cholesky
decomposition](http://www.aaronschlegel.com/cholesky-decomposition-r-example.html) of
a matrix, I wanted to explore another often used decomposition method
known as [Singular Value
Decomposition](https://en.wikipedia.org/wiki/Singular_value_decomposition),
also called SVD. SVD underpins many statistical and real-world
applications principal component analysis, image compression, noise
reduction of an image, and even climate studies. Singular value
decomposition was also a primary technique used in the winning solution
of Netflix's \$1 million recommendation system improvement contest. The
method of SVD works by reducing a matrix $A$ of rank $R$ to a matrix of
rank $k$ and is applicable for both square and rectangular matrices.

Singular value decomposition can be thought of as a method that
transforms correlated variables into a set of uncorrelated variables,
enabling one to better analyze the relationships of the original data
(Baker, 2005). Similar to Cholesky decomposition, SVD factors a matrix
$A$ into a product of three matrices:

$$ A = U\Sigma V^T $$

Where the columns of matrices $U$ and $V$ are orthonormal (orthogonal
unit vectors) and $\Sigma$ is a diagonal matrix. The columns of $U$ and
$V$ are the eigenvectors of $AA^T$ and $A^T A$, respectively. The
entries in the diagonal matrix $\Sigma$ are the singular values $r$,
which are the square roots of the non-zero eigenvalues of $AA^T$ and
$A^T A$.

Singular Value Decomposition in R
---------------------------------

Base R provides the function `svd()` for performing SVD. The following
matrix was taken from Problem 2.23 in the book Methods of Multivariate
Analysis by Alvin Rencher.

$$A = 
\begin{bmatrix}
  4 & -5 & -1 \\
  7 & -2 & 3 \\
  -1 & 4 & -3 \\
  8 & 2 & 6 \\
\end{bmatrix}$$

``` {.r}
A = as.matrix(data.frame(c(4,7,-1,8), c(-5,-2,4,2), c(-1,3,-3,6)))
A
```

    ##      c.4..7...1..8. c..5...2..4..2. c..1..3...3..6.
    ## [1,]              4              -5              -1
    ## [2,]              7              -2               3
    ## [3,]             -1               4              -3
    ## [4,]              8               2               6

The singular value decomposition of the matrix is computed using the
`svd()` function.

``` {.r}
A.svd <- svd(A)
A.svd
```

    ## $d
    ## [1] 13.161210  6.999892  3.432793
    ## 
    ## $u
    ##            [,1]       [,2]        [,3]
    ## [1,] -0.2816569  0.7303849 -0.42412326
    ## [2,] -0.5912537  0.1463017 -0.18371213
    ## [3,]  0.2247823 -0.4040717 -0.88586638
    ## [4,] -0.7214994 -0.5309048  0.04012567
    ## 
    ## $v
    ##            [,1]        [,2]       [,3]
    ## [1,] -0.8557101  0.01464091 -0.5172483
    ## [2,]  0.1555269 -0.94610374 -0.2840759
    ## [3,] -0.4935297 -0.32353262  0.8073135

Thus the above matrix $A$ can be factorized as the following:

$$\begin{bmatrix}
 0.281657 & -0.730385 & -0.424123 & 0.455332 \\
 0.591254 & -0.146302 & -0.183712 & -0.771534 \\
 -0.224782 & 0.404072 & -0.885866 & -0.0379443 \\
 0.721499 & 0.530905 & 0.0401257 & 0.442683 \\
\end{bmatrix}\begin{bmatrix}
 13.1612 & 0 & 0 \\
 0 & 6.99989 & 0 \\
 0 & 0 & 3.43279 \\
 0 & 0 & 0 \\
\end{bmatrix}\begin{bmatrix}
 0.85571 & -0.0146409 & -0.517248 \\
 -0.155527 & 0.946104 & -0.284076 \\
 0.49353 & 0.323533 & 0.807314 \\
\end{bmatrix}$$

Singular Value Decomposition Step-by-Step
-----------------------------------------

SVD can be performed step-by-step with R by calculating $A^TA$ and
$AA^T$ then finding the eigenvalues and eigenvectors of the matrices.
However, it should be noted this is only for demonstration and not
recommended in practice as the results can be slightly different than
the output of the `svd()`. This is due to somewhat random changes in
signs of the eigenvectors from the `eigen()` function as the
eigenvectors can be scaled by $-1$. [This question on
Stackoverflow](http://stackoverflow.com/questions/17998228/sign-of-eigenvectors-change-depending-on-specification-of-the-symmetric-argument)
contains more information for those curious.

First, find $A^TA$ and $AA^T$.

$$A^TA = 
\begin{bmatrix}
  4 & 7 & -1 & 8 \\
  -5 & -2 & 4 & 2 \\
  -1 & 3 & -3 & 6
\end{bmatrix}
\begin{bmatrix}
  4 & -5 & -1 \\
  7 & -2 & 3 \\
  -1 & 4 & -3 \\
  8 & 2 & 6 
\end{bmatrix} = 
\begin{bmatrix}
  130 & -22 & 68 \\
  -22 & 49 & -1 \\
  68 & -1 & 55
\end{bmatrix}$$

``` {.r}
ATA <- t(A) %*% A
ATA
```

    ##                 c.4..7...1..8. c..5...2..4..2. c..1..3...3..6.
    ## c.4..7...1..8.             130             -22              68
    ## c..5...2..4..2.            -22              49              -1
    ## c..1..3...3..6.             68              -1              55

The $V$ component of the singular value decomposition is then found by
calculating the eigenvectors of the resultant $A^TA$ matrix.

``` {.r}
ATA.e <- eigen(ATA)
v.mat <- ATA.e$vectors
v.mat
```

    ##            [,1]        [,2]       [,3]
    ## [1,]  0.8557101 -0.01464091 -0.5172483
    ## [2,] -0.1555269  0.94610374 -0.2840759
    ## [3,]  0.4935297  0.32353262  0.8073135

Here we see the $V$ matrix is the same as the output of the `svd()` but
with some sign changes. These sign changes can happen, as mentioned
earlier, as the eigenvector scaled by $-1$ is still the same
eigenvector, just scaled. We will alter the signs of our calculated $V$
to match the output of the `svd()` function.

``` {.r}
v.mat[,1:2] <- v.mat[,1:2] * -1
v.mat
```

    ##            [,1]        [,2]       [,3]
    ## [1,] -0.8557101  0.01464091 -0.5172483
    ## [2,]  0.1555269 -0.94610374 -0.2840759
    ## [3,] -0.4935297 -0.32353262  0.8073135

The same routine is done for the $AA^T$ matrix.

$$AA^T = 
\begin{bmatrix}
  4 & -5 & -1 \\
  7 & -2 & 3 \\
  -1 & 4 & -3 \\
  8 & 2 & 6 
\end{bmatrix}
\begin{bmatrix}
  4 & 7 & -1 & 8 \\
  -5 & -2 & 4 & 2 \\
  -1 & 3 & -3 & 6
\end{bmatrix} = 
\begin{bmatrix}
  42 & 35 & -21 & 16 \\
  35 & 62 & -24 & 70 \\
  -21 & -24 & 26 & -18 \\
  16 & 70 & -17 & 104
\end{bmatrix}$$

``` {.r}
AAT <- A %*% t(A)
AAT
```

    ##      [,1] [,2] [,3] [,4]
    ## [1,]   42   35  -21   16
    ## [2,]   35   62  -24   70
    ## [3,]  -21  -24   26  -18
    ## [4,]   16   70  -18  104

The eigenvectors are again found for the computed $AA^T$ matrix.

``` {.r}
AAT.e <- eigen(AAT)
u.mat <- AAT.e$vectors
u.mat
```

    ##            [,1]       [,2]        [,3]       [,4]
    ## [1,] -0.2816569  0.7303849 -0.42412326 -0.4553316
    ## [2,] -0.5912537  0.1463017 -0.18371213  0.7715340
    ## [3,]  0.2247823 -0.4040717 -0.88586638  0.0379443
    ## [4,] -0.7214994 -0.5309048  0.04012567 -0.4426835

There are four eigenvectors in the resulting matrix; however, we are
only interested in the non-zero eigenvalues and their respective
eigenvectors. Therefore, we can remove the last eigenvector from the
matrix which gives us the $U$ matrix. Note the eigenvalues of $AA^T$ and
$A^TA$ are the same except the $0$ eigenvalue in the $AA^T$ matrix.

``` {.r}
u.mat <- u.mat[,1:3]
```

As mentioned earlier, the singular values $r$ are the square roots of
the non-zero eigenvalues of the $AA^T$ and $A^TA$ matrices.

``` {.r}
r <- sqrt(ATA.e$values)
r <- r * diag(length(r))[,1:3]
r
```

    ##          [,1]     [,2]     [,3]
    ## [1,] 13.16121 0.000000 0.000000
    ## [2,]  0.00000 6.999892 0.000000
    ## [3,]  0.00000 0.000000 3.432793

Our answers align with the output of the `svd()` function. We can also
show that the matrix $A$ is indeed equal to the components resulting
from singular value decomposition.

``` {.r}
svd.matrix <- u.mat %*% r %*% t(v.mat)
svd.matrix
```

    ##      [,1] [,2] [,3]
    ## [1,]    4   -5   -1
    ## [2,]    7   -2    3
    ## [3,]   -1    4   -3
    ## [4,]    8    2    6

``` {.r}
A == round(svd.matrix, 0)
```

    ##      c.4..7...1..8. c..5...2..4..2. c..1..3...3..6.
    ## [1,]           TRUE            TRUE            TRUE
    ## [2,]           TRUE            TRUE            TRUE
    ## [3,]           TRUE            TRUE            TRUE
    ## [4,]           TRUE            TRUE            TRUE

Summary
-------

This post explored the very useful and frequently appearing matrix
decomposition method known as singular value decomposition. The method
is worthwhile to review as SVD is an essential technique in many
statistical methods such as principal component analysis and factor
analysis. I plan on writing more posts that explore practical
applications of SVD such as compressing an image to provide more
real-world examples.

References
----------

Austin, D. Feature column from the AMS. Retrieved from
<http://www.ams.org/samplings/feature-column/fcarc-svd>

Baker, K. (2005, March). Singular value decomposition Tutorial.
Retrieved from
<https://www.ling.ohio-state.edu/~kbaker/pubs/Singular_Value_Decomposition_Tutorial.pdf>

[Enderton, H. (1977). Elements of set theory (1st ed.). New York:
Academic Press.](https://amzn.to/2SsiA5g)

Singular value decomposition (SVD). Retrieved from
<https://www.cs.cmu.edu/~venkatg/teaching/CStheory-infoage/book-chapter-4.pdf>

SVD computation example. Retrieved from
<http://www.d.umn.edu/~mhampton/m4326svd_example.pdf>
