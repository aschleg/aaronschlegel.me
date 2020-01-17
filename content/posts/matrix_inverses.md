Title: How to Calculate the Inverse Matrix for 2×2 and 3×3 Matrices
Date: 2016-08-18
Tags: R, linear algebra, matrices
Category: Linear Algebra
Slug: calculate-matrix-inverse-2x2-3x3
Author: Aaron Schlegel
Summary: The inverse of a number is its reciprocal. For example, the inverse of 8
is $\frac{1}{8}$, the inverse of 20 is $\frac{1}{20}$ and so on.
Therefore, a number multiplied by its inverse will always equal 1. An
inverse of a number is denoted with a $-1$ superscript.

Inverses of Numbers and Matrices
--------------------------------

The inverse of a number is its reciprocal. For example, the inverse of 8
is $\frac{1}{8}$, the inverse of 20 is $\frac{1}{20}$ and so on.
Therefore, a number multiplied by its inverse will always equal 1. An
inverse of a number is denoted with a $-1$ superscript.

$$ x \cdot \frac{1}{x} = x \cdot x^{-1} = x^{-1} \cdot x = 1 $$

The inverse of a matrix $A$ is another matrix denoted by $A^{-1}$ and is
defined as:

$$ A^{-1}A = AA^{-1} = I $$

Where $I$ is the [identity
matrix](https://en.wikipedia.org/wiki/Identity_matrix). Thus, similar to
a number and its inverse always equaling 1, a matrix multiplied by its
inverse equals the identity.

This post will explore several concepts related to the inverse of a
matrix, including linear dependence and the rank of a matrix. Afterward,
the method of computing an inverse (if one exists) of a $2 \times 2$ or
$3 \times 3$ matrix shall be demonstrated. Finding the inverse of a
square matrix with $\geq 4$ columns is computationally intensive and
best left to R's built-in linear algebra routines which are built on
[LINPACK](https://en.wikipedia.org/wiki/LINPACK) and
[LAPACK](https://en.wikipedia.org/wiki/LAPACK). Here is an excellent
resource that lists the [linear algebra
operations](http://www.statmethods.net/advstats/matrix.html) available
in R. Here is a good resource on how to compute a [4x4 inverse
matrix](http://www.cg.info.hiroshima-cu.ac.jp/~miyazaki/knowledge/teche23.html)
manually for those interested.

The example inverse matrix problems used in the post are from Jim
Hefferon's excellent book [Linear
Algebra](http://joshua.smcvt.edu/linearalgebra) on page 249. I highly
recommend the book to those learning more about linear algebra. The book
is free to download and comes with many exercises and other features.

Linear Dependence of a Matrix
-----------------------------

The following matrix A has three column vectors.

$$A = 
\begin{bmatrix}
  2 & 2 & 3 \\
  1 & -2 & -3 \\
  4 & -2 & - 3
\end{bmatrix}$$

Notice the second column vector is a multiple of the third column. The
matrix is therefore linearly dependent as the matrix contains a column
vector that is a multiple of another. The matrix is linearly independent
when no column vector can be expressed as a multiple of another vector
in the matrix.

$$\begin{bmatrix}
  2 \\
  -2 \\
  -2
\end{bmatrix}
=
\frac{3}{2}
\begin{bmatrix}
  3 \\
  -3 \\
  -3
\end{bmatrix}$$

Rank of a Matrix
----------------

The rank of a matrix is the maximum number of linearly independent
columns or linearly independent rows in the matrix. Therefore, the rank
of a $row \times column$ matrix is the minimum of the two values. For
example, the above matrix would have a rank of 1. Inverses only exist
for a square $r \times r$ matrix with rank $r$, which is called a full
rank or nonsingular matrix.

Computing an inverse matrix
---------------------------

Consider a 2x2 matrix:

$$\underset{2 \times 2}{A} = 
\begin{bmatrix}
  a & b \\
  c & d
\end{bmatrix}$$

The $2 \times 2$ inverse matrix is then:

$$\underset{2 \times 2}{A^{-1}} = 
\begin{bmatrix}
  a & b \\
  c & d
\end{bmatrix}^{-1} = 
\frac{1}{D}
\begin{bmatrix}
  d & -b \\
  -c & a
\end{bmatrix}$$

Where $D = ad - bc$. $D$ is called the determinant of the matrix.

The $3 \times 3$ matrix can be defined as:

$$\underset{3 \times 3}{B} = 
\begin{bmatrix}
  a & b & c \\
  d & e & f \\
  g & h & k
\end{bmatrix}$$

Then the inverse matrix is:

$$\underset{3 \times 3}{B^{-1}} = 
\begin{bmatrix}
  a & b & c \\
  d & e & f \\
  g & h & k
\end{bmatrix}^{-1} = 
\frac{1}{det(B)}
\begin{bmatrix}
  (ek - fh) & -(bk - ch) & (bf - ce) \\
  -(dk - fg) & (ak - cg) & -(af - cd) \\
  (dh - eg) & -(ah - bg) & (ae - bd)
\end{bmatrix}$$

Where $det(B)$ is equal to:

$$ det(B) = a(ek - fh) - b(dk -fg) + c(dh - eg) $$

The following function implements a quick and rough routine to find the
inverse of a $2 \times 2$ or $3 \times 3$ matrix should one exist.

``` {.r}
matrix.inverse <- function(mat) {
  A <- as.matrix(mat)

  # If there are more than four columns in the supplied matrix, stop routine
  if ((ncol(A) >= 4) | (nrow(A) >= 4)) {
    stop('Matrix is not 2x2 or 3x3')
  }
  
  # Stop if matrix is a single column vector
  if (ncol(A) == 1) {
    stop('Matrix is a vector')
  }
  
  # 2x2 inverse matrix
  if(ncol(A) == 2) {
    # Determinant
    a <- A[1]
    b <- A[3]
    c <- A[2]
    d <- A[4]
    det <- a * d - b * c
    # Check to see if matrix is singular
    if (det == 0) {
      stop('Determinant of matrix equals 0, no inverse exists')
    }
    # Compute inverse matrix elements
    a.inv <- d / det
    b.inv <- -b / det
    c.inv <- -c / det
    d.inv <- a / det
    # Collect the results into a new matrix
    inv.mat <- as.matrix(cbind(c(a.inv,c.inv), c(b.inv,d.inv)))
  }
  
  # 3x3 inverse matrix
  if (ncol(A) == 3) {
    # Extract the entries from the matrix
    a <- A[1]
    b <- A[4]
    c <- A[7]
    d <- A[2]
    e <- A[5]
    f <- A[8]
    g <- A[3]
    h <- A[6]
    k <- A[9]
    
    # Compute the determinant and check that it is not 0
    det <- a * (e * k - f * h) - b * (d * k - f * g) + c * (d * h - e * g)
    if (det == 0) {
      stop('Determinant of matrix equals 0, no inverse exists')
    }
    
    # Using the equations defined above, calculate the inverse matrix entries.
    A.inv <- (e * k - f * h) / det
    B.inv <- -(b * k - c * h) / det
    C.inv <- (b * f - c * e) / det
    D.inv <- -(d * k - f * g) / det
    E.inv <- (a * k - c * g) / det
    F.inv <- -(a * f - c * d) / det
    G.inv <- (d * h - e * g) / det
    H.inv <- -(a * h - b * g) / det
    K.inv <- (a * e - b * d) / det
    
    # Collect the results into a new matrix
    inv.mat <- as.matrix(cbind(c(A.inv,D.inv,G.inv), c(B.inv,E.inv,H.inv), c(C.inv,F.inv,K.inv)))
  }
  
return(inv.mat)
}
```

The results from the above function can be used to verify the
definitions and equations of the inverse matrix above in conjunction
with R's built-in methods.

``` {.r}
A <- as.matrix(cbind(c(3,0),c(1,2)))
A
```

    ##      [,1] [,2]
    ## [1,]    3    1
    ## [2,]    0    2

``` {.r}
A1 <- matrix.inverse(A)
A1
```

    ##           [,1]       [,2]
    ## [1,] 0.3333333 -0.1666667
    ## [2,] 0.0000000  0.5000000

``` {.r}
solve(A)
```

    ##           [,1]       [,2]
    ## [1,] 0.3333333 -0.1666667
    ## [2,] 0.0000000  0.5000000

``` {.r}
B <- as.matrix(cbind(c(1,0,-1), c(1,2,1), c(3,4,0)))
B
```

    ##      [,1] [,2] [,3]
    ## [1,]    1    1    3
    ## [2,]    0    2    4
    ## [3,]   -1    1    0

``` {.r}
B1 <- matrix.inverse(B)
B1
```

    ##      [,1] [,2] [,3]
    ## [1,]    2 -1.5    1
    ## [2,]    2 -1.5    2
    ## [3,]   -1  1.0   -1

``` {.r}
solve(B)
```

    ##      [,1] [,2] [,3]
    ## [1,]    2 -1.5    1
    ## [2,]    2 -1.5    2
    ## [3,]   -1  1.0   -1

Recall the product of the matrix and its inverse will always equal the
identity matrix.

``` {.r}
A %*% A1
```

    ##      [,1] [,2]
    ## [1,]    1    0
    ## [2,]    0    1

``` {.r}
B %*% B1
```

    ##      [,1] [,2] [,3]
    ## [1,]    1    0    0
    ## [2,]    0    1    0
    ## [3,]    0    0    1

Matrices that are singular or not of full rank will have a determinant
of 0, and thus no inverse exists.

``` {.r}
C <- as.matrix(cbind(c(2,-1),c(-4,2)))
C
```

    ##      [,1] [,2]
    ## [1,]    2   -4
    ## [2,]   -1    2

``` {.r}
solve(C)
```

    ## Error in solve.default(C): Lapack routine dgesv: system is exactly singular: U[2,2] = 0

``` {.r}
D <- as.matrix(cbind(c(2,1,4),c(2,-2,-2),c(3,-3,-3)))
D
```

    ##      [,1] [,2] [,3]
    ## [1,]    2    2    3
    ## [2,]    1   -2   -3
    ## [3,]    4   -2   -3

``` {.r}
solve(D)
```

    ## Error in solve.default(D): Lapack routine dgesv: system is exactly singular: U[3,3] = 0

Summary
-------

The inverse matrix was explored by examining several concepts such as
linear dependency and the rank of a matrix. The method of calculating an
inverse of a $2 \times 2$ and $3 \times 3$ matrix (if one exists) was
also demonstrated. As stated earlier, finding an inverse matrix is best
left to a computer, especially when dealing with matrices of
$4 \times 4$ or above.

References
----------

Hefferon, J. (n.d.). Linear Algebra

Inverse matrix of 2x2 matrix, 3x3 matrix, 4x4 matrix. Retrieved August
10, 2016, from
<http://www.cg.info.hiroshima-cu.ac.jp/~miyazaki/knowledge/teche23.html>

Kutner, M. H., Nachtsheim, C. J., Neter, J., Li, W., & Wasserman, W.
(2004). Applied linear statistical models (5th ed.). Boston, MA:
McGraw-Hill Higher Education.
