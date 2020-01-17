Title: Discriminant Analysis of Several Groups
Date: 2018-08-17
Tags: R, linear algebra, matrix decomposition
Category: Linear Algebra
Slug: discriminant-analysis-several-groups
Author: Aaron Schlegel
Summary: Discriminant analysis is also applicable in the case of more than two groups. In the first post on discriminant analysis, there was only one linear discriminant function as the number of linear discriminant functions is $s = min(p, k − 1)$, where $p$ is the number of dependent variables and $k$ is the number of groups. In the case of more than two groups, there will be more than one linear discriminant function, which allows us to examine the groups' separation in more than one dimension.


Discriminant analysis is also applicable in the case of more than two groups. In the first post on [discriminant analysis](http://wp.me/p4aZEo-5Os), there was only one linear discriminant function as the number of linear discriminant functions is $s = min(p, k − 1)$, where $p$ is the number of dependent variables and $k$ is the number of groups. In the case of more than two groups, there will be more than one linear discriminant function, which allows us to examine the groups' separation in more than one dimension. Discriminant analysis of several groups also makes it possible to rank the variables regarding their relative importance to group separation.

Discriminant Analysis of Several Groups
---------------------------------------

Similar to the two-group case, the goal is to find a vector $a$ that separates the discriminant functions $\bar{z}_1, \bar{z}_2, \cdots, \bar{z}_k$ at a maximum. To extend the separation criteria to the $k > 2$ case, we take the two-group equation:

$$ \frac{(\bar{z}_1 - \bar{z}_2)}{s_z^2} = \frac{[a'(\bar{y}_1 - \bar{y}_2)]^2}{a'S_{p1}a} $$

And express it in the form:

$$ \frac{(\bar{z}_1 - \bar{z}_2)}{s_z^2} = \frac{a'(\bar{y}_1 - \bar{y}_2)(\bar{y}_1 - \bar{y}_2)'a}{a'S_{p1}a} $$

In the discriminant analysis of several groups setting, the $H$ hypothesis matrix and $E$ error matrix from MANOVA are utilized. $H$ replaces $(\bar{y}_1 - \bar{y}_2)(\bar{y}_1 - \bar{y}_2)'$ while $E$ replaces $S_{p1}$, which gives us:

$$ \lambda = \frac{a'Ha}{a'Ea} $$

Rearranging the above yields:

$$ a(Ha − \lambda Ea)=0 $$

Which can also be written as:

$$(E^{−1}H − \lambda I)a = 0 $$

The solutions of which are the eigenvalues $\lambda_1, \lambda_2, \cdots, \lambda_s$ and their corresponding eigenvectors $a_1, a_2, \cdots, a_s$ of the matrix $E^{−1}H$. Therefore, the first and largest eigenvalue $\lambda_1$ and its eigenvector $a_1$ maximally separate the groups.

The number of eigenvalues and associated eigenvectors of $E^{−1}H$, $s$, is also the number of discriminant functions that are obtained by discriminant analysis of several groups.

Discriminant Analysis of Several Groups in R
--------------------------------------------

This example will analyze the rootstock data as in the previous MANOVA post. The rootstock data were obtained from the [companion FTP site](ftp://ftp.wiley.com) of the book Methods of Multivariate Analysis by Alvin Rencher. The data contains four dependent variables as follows:

-   trunk girth at four years (mm × 100)
-   extension growth at four years (m)
-   trunk girth at 15 years (mm × 100)
-   weight of tree above ground at 15 years (lb × 1000)

``` r
root <- read.table('ROOT.DAT', col.names = c('Tree.Number', 'Trunk.Girth.4.Years', 'Ext.Growth.4.Years', 'Trunk.Girth.15.Years', 'Weight.Above.Ground.15.Years'))
```

To calculate the discriminant functions of more than two groups, the $H$ and $E$ matrices from MANOVA must be computed.

``` r
root.group <- split(root[,2:5], root$Tree.Number)
root.means <- sapply(root.group, function(x) {
  apply(x, 2, mean)
}, simplify = 'data.frame')

n <- dim(root)[1] / length(unique(root$Tree.Number))
total.means <- colMeans(root[,2:5])

H = matrix(data = 0, nrow = 4, ncol = 4)
for (i in 1:dim(H)[1]) {
  for (j in 1:i) {
    H[i,j] <- n * sum((root.means[i,] - total.means[i]) * (root.means[j,] - total.means[j]))
    H[j,i] <- n * sum((root.means[j,] - total.means[j]) * (root.means[i,] - total.means[i]))
  }
}

E = matrix(data = 0, nrow = 4, ncol = 4)
for (i in 1:dim(E)[1]) {
  for (j in 1:i) {
    b <- c() 
    for (k in root.group) {
      a <- sum((k[,i] - mean(k[,i])) * (k[,j] - mean(k[,j])))
      b <- append(b, a)
    }
    E[i,j] <- sum(b)
    E[j,i] <- sum(b)
  }
}
```

Then find the eigenvalues and eigenvectors of the matrix $E^{−1}H$.

``` r
eigens <- eigen(solve(E) %*% H)
eigens$values
```

    ## [1] 1.87567112 0.79069454 0.22904907 0.02595357

``` r
eigens$vectors
```

    ##             [,1]        [,2]       [,3]        [,4]
    ## [1,] -0.55337105  0.08340397 -0.1521720  0.97955535
    ## [2,]  0.30911038  0.08894955  0.2539187 -0.12869430
    ## [3,] -0.76855963 -0.52426558  0.4623164 -0.08413202
    ## [4,]  0.08687548  0.84277954 -0.8358424  0.12973396

Thus there are four discriminant functions. The largest eigenvalue 1.8757 and its associated eigenvector ( − 0.5534, .3091, −0.7686, 0.0868) represent the discriminant function that maximally separates the groups.

We can see the first eigenvector is the solution to the above equation $\lambda = \frac{a'Ha}{a'Ea}$.

``` r
(crossprod(eigens$vectors[,1], H) %*% eigens$vectors[,1]) /  (crossprod(eigens$vectors[,1], E) %*% eigens$vectors[,1])
```

    ##          [,1]
    ## [1,] 1.875671

The above can also be done with the `lda()` function available in the [MASS package](https://cran.r-project.org/web/packages/MASS/index.html).

``` r
library(MASS)
```

The `lda()` function takes a formula argument.

``` r
root.lda <- lda(Tree.Number ~ ., data = root)
root.lda
```

    ## Call:
    ## lda(Tree.Number ~ ., data = root)
    ## 
    ## Prior probabilities of groups:
    ##         1         2         3         4         5         6 
    ## 0.1666667 0.1666667 0.1666667 0.1666667 0.1666667 0.1666667 
    ## 
    ## Group means:
    ##   Trunk.Girth.4.Years Ext.Growth.4.Years Trunk.Girth.15.Years
    ## 1             1.13750           2.977125              3.73875
    ## 2             1.15750           3.109125              4.51500
    ## 3             1.10750           2.815250              4.45500
    ## 4             1.09750           2.879750              3.90625
    ## 5             1.08000           2.557250              4.31250
    ## 6             1.03625           2.214625              3.59625
    ##   Weight.Above.Ground.15.Years
    ## 1                     0.871125
    ## 2                     1.280500
    ## 3                     1.391375
    ## 4                     1.039000
    ## 5                     1.181000
    ## 6                     0.735000
    ## 
    ## Coefficients of linear discriminants:
    ##                                     LD1        LD2       LD3       LD4
    ## Trunk.Girth.4.Years           3.0479952  -1.140083 -1.002448 23.419063
    ## Ext.Growth.4.Years           -1.7025953  -1.215888  1.672714 -3.076804
    ## Trunk.Girth.15.Years          4.2332645   7.166403  3.045553 -2.011416
    ## Weight.Above.Ground.15.Years -0.4785144 -11.520302 -5.506192  3.101660
    ## 
    ## Proportion of trace:
    ##    LD1    LD2    LD3    LD4 
    ## 0.6421 0.2707 0.0784 0.0089

The output of the `lda()` function also shows there are four discriminant functions. The coefficients are different than what we computed; however, this is just a matter of scaling.

``` r
root.lda$scaling / eigens$vectors
```

    ##                                   LD1       LD2      LD3      LD4
    ## Trunk.Girth.4.Years          -5.50805 -13.66941 6.587596 23.90785
    ## Ext.Growth.4.Years           -5.50805 -13.66941 6.587596 23.90785
    ## Trunk.Girth.15.Years         -5.50805 -13.66941 6.587596 23.90785
    ## Weight.Above.Ground.15.Years -5.50805 -13.66941 6.587596 23.90785

Thus either set of coefficients is a solution as a multiple of an eigenvector is still the same eigenvector. The proportion of the trace output of the `lda()` function is the relative importance of each discriminant function.

Relative Importance of Discriminant Functions
---------------------------------------------

The relative importance of each discriminant function is found by finding the associated eigenvalue's proportion to the total sum of the eigenvalues.

$$ \frac{\lambda_i}{\sum^s_{j=1} \lambda_i} $$

``` r
for (i in eigens$values) {
  print(round(i / sum(eigens$values), 4))
}
```

    ## [1] 0.6421
    ## [1] 0.2707
    ## [1] 0.0784
    ## [1] 0.0089

The first and second discriminant functions account for 91% of the proportion of the total. Therefore the mean vectors lie primarily in one dimension and slightly in another dimension.

Test of Significance of Discriminant Functions
----------------------------------------------

Wilks $\LambdaΛ$-test, a common [MANOVA test statistic](http://wp.me/p4aZEo-5Pu), is also employed in the discriminant analysis for several groups setting. Wilks test is defined as:

$$ \Lambda_1 = \prod^s_{i=1} \frac{1}{1 + \lambda_i} $$

Which is distributed as $\Lambda^p_{k − 1, N − k}$. An approximate F-test is used for each $\Lambda_i$.

$$ F = \frac{1 - \Lambda_1^{(1/t)}}{\Lambda_1^{(1/t)}} \frac{df_2}{df_1} $$

Where,

$$ t = \sqrt{\frac{p^2(k-1)^2 - 4}{p^2 + (k - 1)^2 - 5}} $$
$$ w = N - 1 - \frac{1}{2}(p + k) $$
$$ df_1 = p(k − 1) $$
$$ df_2 = wt - \frac{1}{2}[p(k-1) -2] $$

Denote $\Lambda_m$ after $\Lambda_1$ for each successive value as $m = 2, 3, \cdots, s$, where $s$ is the number of non-zero eigenvalues of $E^{−1}H$.

$$ \Lambda_m = \prod_{i=m}^s \frac{1}{1 + \lambda_i} $$

The approximate F-test becomes:

$$ F = \frac{1 - \Lambda_m^{(1/t)}}{\Lambda_m^{(1/t)}} \frac{df_2}{df_1} $$

$p − m + 1$ replaces $p$ and $k − m$ replaces $k − 1$:

$$ t = \sqrt{\frac{p-m+1)^2(k-m)^2-4}{(p-m+1)^2+(k-m)^2-5}} $$
$$ w = N - 1 - \frac{1}{2}(p + k) $$
$$ df_1 = (p − m + 1)(k − m) $$
$$ df_2 = wt - \frac{1}{2}[(p - m + 1)(k - m) - 2] $$

The following function implements the above to test the significance of each discriminant function. As noted previously, the first two discriminant functions represent 91% of the proportion of the total, so it is likely at least these functions will be significant.

``` r
discriminant.significance <- function(eigenvalues, p, k, N) {
  w <- N - 1 - .5 * (p + k)
  t <- sqrt((p^2 * (k - 1)^2 - 4) / (p^2 + (k - 1)^2 - 5))
  df1 <- p * (k - 1)
  df2 <- w * t - .5 * (p * (k - 1) - 2)
  lambda1 <- prod(1 / (1 + eigenvalues))
  f1 <- (1 - lambda1^(1/t)) / (lambda1^(1/t)) * df2 / df1
  p1 <- pf(f1, df1, df2, lower.tail = FALSE)
  
  result <- NULL

  for (i in 2:p) {
    m <- i
    
    if (m == p) {
      t.i <- 1
    } else {
      t.i <- sqrt(((p - m + 1)^2 * (k - m)^2 - 4) / ((p - m + 1)^2 + (k - m)^2 - 5))
    }
    
    df1.i <- (p - m + 1) * (k - m)
    df2.i <- w * t.i - .5 * ((p - m + 1) * (k - m) - 2)
    lambda.i <- prod(1 / (1 + eigenvalues[i:p]))
    f.i <- (1 - lambda.i^(1/t.i)) / lambda.i^(1/t.i) * df2.i / df1.i
    p.i <- pf(f.i, df1.i, df2.i, lower.tail = FALSE)    
    result <- rbind(result, data.frame(lambda.i, f.i, p.i))
  }
  res <- rbind(c(lambda1, f1, p1), result)
  colnames(res) <- c('Lambda', 'Approximate F', 'p-value')
  return(res)
}

N <- dim(root)[1]
p <- dim(root)[2] - 1
k <- length(unique(root$Tree.Number))

discriminant.significance(eigens$values, p, k, N)
```

    ##      Lambda Approximate F      p-value
    ## 1 0.1540077     4.9368880 7.713766e-09
    ## 2 0.4428754     3.1879149 6.382962e-04
    ## 3 0.7930546     1.6798943 1.363020e-01
    ## 4 0.9747030     0.5450251 5.838726e-01

The first two discriminant functions are indeed significant while the remaining two can be ignored.

``` r
abs(root.lda$scaling[,1:2])
```

    ##                                    LD1       LD2
    ## Trunk.Girth.4.Years          3.0479952  1.140083
    ## Ext.Growth.4.Years           1.7025953  1.215888
    ## Trunk.Girth.15.Years         4.2332645  7.166403
    ## Weight.Above.Ground.15.Years 0.4785144 11.520302

The dependent variable trunk girth at 15 years appears to separate the groups the most in both dimensions, while trunk girth at four years and weight above ground at 15 years are the most significant variables to separating the groups in their respective discriminant functions.

References
----------

Rencher, A. (n.d.). Methods of Multivariate Analysis (2nd ed.). Brigham Young University: John Wiley & Sons, Inc.
