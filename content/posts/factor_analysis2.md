Title: Factor Analysis with the Principal Component Method and R Part Two
Date: 2017-02-16
Tags: R, statistics, factor analysis, linear algebra
Category: Statistics
Slug: factor-analysis-principal-component-method-r-part-two
Author: Aaron Schlegel
Summary: In the first post on factor analysis, we examined computing the estimated covariance matrix $S$ of the rootstock data and proceeded to find two factors that fit most of the variance of the data. However, the variables in the data are not on the same scale of measurement, which can cause variables with comparatively large variances to dominate the diagonal of the covariance matrix and the resulting factors. The correlation matrix, therefore, makes more intuitive sense to employ in factor analysis.

In the [first post on factor analysis](https://aaronschlegel.me/factor-analysis-principal-component-method-r.html), we
examined computing the estimated covariance matrix $S$ of the rootstock
data and proceeded to find two factors that fit most of the variance of
the data. However, the variables in the data are not on the same scale
of measurement, which can cause variables with comparatively large
variances to dominate the diagonal of the covariance matrix and the
resulting factors. The correlation matrix, therefore, makes more
intuitive sense to employ in factor analysis. In fact, as we saw
previously, most packages available in R default to using the
correlation matrix when performing factor analysis. There are several
benefits to using $R$ over $S$, not only that it scales non-commensurate
variables, but it is also easier to calculate the factors as the matrix
does not need to be decomposed and estimated like $S$.

Factor Analysis with the Correlation Matrix
-------------------------------------------

Similar to factor analysis with the covariance matrix, we estimate
$\Lambda$ which is $p \times m$ where $D$ is a diagonal matrix of the
$m$ largest eigenvalues of $R$, and $C$ is a matrix of the corresponding
eigenvectors as columns.

$$ \hat{\Lambda} = CD^{1/2} = (\sqrt{\theta_1}c_1, \sqrt{\theta_2}c_2, \cdots, \sqrt{\theta_m}c_m) $$

Where $\theta_1, \theta_2, \cdots, \theta_m$ are the largest eigenvalues
of $R$.

Thus the correlation matrix $R$ does not require decomposition, and we
can proceed directly to finding the eigenvalues and eigenvectors of $R$.

Load the rootstock data and name the columns. From the previous post:

The rootstock data contains growth measurements of six different apple
tree rootstocks from 1918 to 1934 (Andrews and Herzberg 1985, pp.
357-360) and were obtained from the [companion FTP
site](ftp://ftp.wiley.com) of the book Methods of Multivariate Analysis
by Alvin Rencher. The data contains four dependent variables as follows:

-   trunk girth at four years (mm $\times$ 100)
-   extension growth at four years (m)
-   trunk girth at 15 years (mm $\times$ 100)
-   weight of tree above ground at 15 years (lb $\times$ 1000)

``` {.r}
root <- read.table('ROOT.DAT', col.names = c('Tree.Number', 'Trunk.Girth.4.Years', 'Ext.Growth.4.Years', 'Trunk.Girth.15.Years', 'Weight.Above.Ground.15.Years'))
```

Compute the correlation matrix of the data.

``` {.r}
R <- cor(root[,2:5])
round(R, 2)
```

    ##                              Trunk.Girth.4.Years Ext.Growth.4.Years
    ## Trunk.Girth.4.Years                         1.00               0.88
    ## Ext.Growth.4.Years                          0.88               1.00
    ## Trunk.Girth.15.Years                        0.44               0.52
    ## Weight.Above.Ground.15.Years                0.33               0.45
    ##                              Trunk.Girth.15.Years
    ## Trunk.Girth.4.Years                          0.44
    ## Ext.Growth.4.Years                           0.52
    ## Trunk.Girth.15.Years                         1.00
    ## Weight.Above.Ground.15.Years                 0.95
    ##                              Weight.Above.Ground.15.Years
    ## Trunk.Girth.4.Years                                  0.33
    ## Ext.Growth.4.Years                                   0.45
    ## Trunk.Girth.15.Years                                 0.95
    ## Weight.Above.Ground.15.Years                         1.00

Then find the eigenvalues and eigenvectors of $R$.

``` {.r}
r.eigen <- eigen(R)
r.eigen
```

    ## eigen() decomposition
    ## $values
    ## [1] 2.78462702 1.05412174 0.11733950 0.04391174
    ## 
    ## $vectors
    ##           [,1]       [,2]       [,3]       [,4]
    ## [1,] 0.4713465  0.5600120  0.6431731  0.2248274
    ## [2,] 0.5089667  0.4544775 -0.7142114 -0.1559013
    ## [3,] 0.5243109 -0.4431448  0.2413716 -0.6859012
    ## [4,] 0.4938456 -0.5324091 -0.1340527  0.6743048

We can check the proportion of each eigenvalue respective to the total
sum of the eigenvalues.

$$ \frac{\sum^p_{i=1} \hat{\lambda}^2_{ij}}{tr(R)} = \frac{\theta_j}{p} $$

Where $p$ is the number of variables. The quick and dirty loop below
finds the proportion of the total for each eigenvalue and the cumulative
proportion.

``` {.r}
cumulative.proportion <- 0
prop <- c()
cumulative <- c()
for (i in r.eigen$values) {
  proportion <- i / dim(root[,2:5])[2]
  cumulative.proportion <- cumulative.proportion + proportion
  
  prop <- append(prop, proportion)
  cumulative <- append(cumulative, cumulative.proportion)
}
data.frame(cbind(prop, cumulative))
```

    ##         prop cumulative
    ## 1 0.69615676  0.6961568
    ## 2 0.26353043  0.9596872
    ## 3 0.02933488  0.9890221
    ## 4 0.01097793  1.0000000

As in the case of the covariance matrix, the first two factors account
for nearly all of the sample variance and thus can proceed with $m = 2$
factors.

The eigenvectors corresponding to the two largest eigenvalues are
multiplied by the square roots of their respective eigenvalues as seen
earlier to obtain the factor loadings.

``` {.r}
factors <- t(t(r.eigen$vectors[,1:2]) * sqrt(r.eigen$values[1:2]))
round(factors, 2)
```

    ##      [,1]  [,2]
    ## [1,] 0.79  0.57
    ## [2,] 0.85  0.47
    ## [3,] 0.87 -0.45
    ## [4,] 0.82 -0.55

Computing the communality remains the same as in the covariance setting.

``` {.r}
h2 <- rowSums(factors^2)
```

The specific variance when factoring $R$ is $1 - \hat{h}^2_i$.

``` {.r}
u2 <- 1 - h2
```

According to the documentation of the `principal()` function (called by
\`?principal), there is another statistic called complexity, which is
the number of factors on which a variable has moderate or high loadings
(Rencher, 2002 pp. 431), that is found by:

$$ \frac{(\sum^m_{i=1} \hat{\lambda}^2_i)^2}{\sum^m_{i=1} \hat{\lambda}_i^4} $$

In the most simple structure, the complexity of all the variables is
$1$. The complexity of the variables is reduced by performing rotation
which will be seen later.

``` {.r}
com <- rowSums(factors^2)^2 / rowSums(factors^4)
com
```

    ## [1] 1.831343 1.553265 1.503984 1.737242

``` {.r}
mean(com)
```

    ## [1] 1.656459

As seen in the previous post, the `principal()` function from the [psych
package](https://cran.r-project.org/web/packages/psych/) performs factor
analysis with the principal component method.

``` {.r}
library(psych)
```

Since we are using $R$ instead of $S$, the `covar` argument remains
`FALSE` by default. No rotation is done for now, so the `rotate`
argument is set to `none`.

``` {.r}
root.fa <- principal(root[,2:5], nfactors = 2, rotate = 'none')
root.fa
```

    ## Principal Components Analysis
    ## Call: principal(r = root[, 2:5], nfactors = 2, rotate = "none")
    ## Standardized loadings (pattern matrix) based upon correlation matrix
    ##                               PC1   PC2   h2    u2 com
    ## Trunk.Girth.4.Years          0.79  0.57 0.95 0.051 1.8
    ## Ext.Growth.4.Years           0.85  0.47 0.94 0.061 1.6
    ## Trunk.Girth.15.Years         0.87 -0.45 0.97 0.027 1.5
    ## Weight.Above.Ground.15.Years 0.82 -0.55 0.98 0.022 1.7
    ## 
    ##                        PC1  PC2
    ## SS loadings           2.78 1.05
    ## Proportion Var        0.70 0.26
    ## Cumulative Var        0.70 0.96
    ## Proportion Explained  0.73 0.27
    ## Cumulative Proportion 0.73 1.00
    ## 
    ## Mean item complexity =  1.7
    ## Test of the hypothesis that 2 components are sufficient.
    ## 
    ## The root mean square of the residuals (RMSR) is  0.03 
    ##  with the empirical chi square  0.39  with prob <  NA 
    ## 
    ## Fit based upon off diagonal values = 1

The output of the `principal()` function agrees with our calculations.

Factor Rotation with Varimax Rotation
-------------------------------------

Rotation moves the axes of the loadings to produce a more simplified
structure of the factors to improve interpretation. Therefore the goal
of rotation is to find an interpretable pattern of the loadings where
variables are clustered into groups corresponding to the factors. We
will see that a successful rotation yields a complexity closer to $1$,
which denotes the variables load highly on only one factor.

One of the most common approaches to rotation is [varimax
rotation](https://en.wikipedia.org/wiki/Varimax_rotation), which is a
type of orthogonal rotation (axes remain perpendicular). The varimax
technique seeks loadings that maximize the variance of the squared
loadings in each column of the rotated matrix $\hat{\Lambda}*$.

The `varimax()` function is used to find the rotated factor loadings.
For those interested, the R code for the `varimax()` function can be
found [here](https://en.wikipedia.org/wiki/Talk:Varimax_rotation).

``` {.r}
factors.v <- varimax(factors)$loadings
round(factors.v, 2)
```

    ## 
    ## Loadings:
    ##      [,1] [,2]
    ## [1,] 0.16 0.96
    ## [2,] 0.28 0.93
    ## [3,] 0.94 0.29
    ## [4,] 0.97 0.19
    ## 
    ##                 [,1]  [,2]
    ## SS loadings    1.928 1.907
    ## Proportion Var 0.482 0.477
    ## Cumulative Var 0.482 0.959

The varimax rotation was rather successful in finding a rotation that
simplified the complexity of the variables. The first two variables now
load highly on the second factor while the remaining two variables load
primarily on the first factor.

Since we used an orthogonal rotation technique, the communalities will
not change.

``` {.r}
h2.v <- rowSums(factors.v^2)
h2.v
```

    ## [1] 0.9492403 0.9390781 0.9725050 0.9779253

``` {.r}
h2
```

    ## [1] 0.9492403 0.9390781 0.9725050 0.9779253

Thus the specific variances will also be unchanged.

``` {.r}
u2.v <- 1 - h2.v
u2.v
```

    ## [1] 0.05075965 0.06092192 0.02749496 0.02207470

``` {.r}
u2
```

    ## [1] 0.05075965 0.06092192 0.02749496 0.02207470

As stated previously, the complexity of the variables on the rotated
factors should be closer to $1$ compared to the non-rotated complexity.

``` {.r}
com.v <- rowSums(factors.v^2)^2 / rowSums(factors.v^4)
com.v
```

    ## [1] 1.054355 1.179631 1.185165 1.074226

``` {.r}
mean(com.v)
```

    ## [1] 1.123344

The complexity is rather close to $1$ which provides us further
acknowledgment the factors are now in a more simplified structure.

Setting the `rotation` argument to `varimax` in the `principal()`
function outputs the rotated factors and corresponding statistics.

``` {.r}
root.fa2 <- principal(root[,2:5], nfactors = 2, rotate = 'varimax')
root.fa2
```

    ## Principal Components Analysis
    ## Call: principal(r = root[, 2:5], nfactors = 2, rotate = "varimax")
    ## Standardized loadings (pattern matrix) based upon correlation matrix
    ##                               RC1  RC2   h2    u2 com
    ## Trunk.Girth.4.Years          0.16 0.96 0.95 0.051 1.1
    ## Ext.Growth.4.Years           0.28 0.93 0.94 0.061 1.2
    ## Trunk.Girth.15.Years         0.94 0.29 0.97 0.027 1.2
    ## Weight.Above.Ground.15.Years 0.97 0.19 0.98 0.022 1.1
    ## 
    ##                        RC1  RC2
    ## SS loadings           1.94 1.90
    ## Proportion Var        0.48 0.48
    ## Cumulative Var        0.48 0.96
    ## Proportion Explained  0.50 0.50
    ## Cumulative Proportion 0.50 1.00
    ## 
    ## Mean item complexity =  1.1
    ## Test of the hypothesis that 2 components are sufficient.
    ## 
    ## The root mean square of the residuals (RMSR) is  0.03 
    ##  with the empirical chi square  0.39  with prob <  NA 
    ## 
    ## Fit based upon off diagonal values = 1

Interpretation of Factors
-------------------------

The factor analysis performed on the rootstock data yielded two latent
variables that fit and explain the variance of the data quite
sufficiently. We see both variables relating to measurements at four
years load heavily on factor 2 while the 15-year measurements load
mainly on the first factor. Thus we could designate names for the
factors, or latent variables, such as '15 years growth' and '4 years
growth', respectively. There isn't any standard way of 'naming' factors
as the interpretation can vary widely between each case. In this
example, the factors make intuitive sense based on how they load on the
variables; however, factors resulting from a factor analysis may not
always make logic sense to the original data. If the resulting factors
do not seem logical, changes to the approach such as adjusting the
number of factors or the threshold of the loadings deemed important, or
even a different method of rotation can be done to improve
interpretation.

References
----------

[Rencher, A. C. (2002). Methods of multivariate analysis. New York: J. Wiley.](https://amzn.to/39gsldt)

<https://en.wikipedia.org/wiki/Talk:Varimax_rotation>

<https://en.wikipedia.org/wiki/Varimax_rotation>

<http://web.stanford.edu/class/psych253/tutorials/FactorAnalysis.html>
