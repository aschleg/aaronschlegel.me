Title: Factor Analysis with Principal Factor Method and R
Date: 2017-02-23
Tags: R, factor analysis
Category: R
Slug: factor-analysis-principal-factor-r
Author: Aaron Schlegel
Summary: As discussed in a previous post on the principal component method of factor analysis, the $\hat{\Psi}$ term in the estimated covariance matrix $S$, $S = \hat{\Lambda} \hat{\Lambda}' + \hat{\Psi}$, was excluded and we proceeded directly to factoring $S$ and $R$. The principal factor method of factor analysis (also called the principal axis method) finds an initial estimate of $\hat{\Psi}$ and factors $S - \hat{\Psi}$, or $R - \hat{\Psi}$ for the correlation matrix.


As discussed in a previous post on the [principal component method of
factor analysis](https://aaronschlegel.me/factor-analysis-principal-component-method-r.html), the $\hat{\Psi}$ term in the
estimated covariance matrix $S$,
$S = \hat{\Lambda} \hat{\Lambda}' + \hat{\Psi}$, was excluded and we
proceeded directly to factoring $S$ and $R$. The principal factor method
of factor analysis (also called the principal axis method) finds an
initial estimate of $\hat{\Psi}$ and factors $S - \hat{\Psi}$, or
$R - \hat{\Psi}$ for the correlation matrix. Rearranging the estimated
covariance and correlation matrices with the estimated $p \times m$
$\hat{\Lambda}$ matrix yields:

$$ S - \hat{\Psi} = \hat{\Lambda} \hat{\Lambda}^\prime $$
$$ R - \hat{\Psi} = \hat{\Lambda} \hat{\Lambda}^\prime $$

Therefore the principal factor method begins with eigenvalues and
eigenvectors of $S - \hat{\Psi}$ or $R - \hat{\Psi}$. $\hat{\Psi}$ is a
diagonal matrix of the $i$th communality. As in the principal component
method, the $i$th communality, $\hat{h}^2_i$, is equal to
$s_{ii} - \hat{\psi}_i$ for $S - \hat{\Psi}$ and $1 - \hat{\psi}_i$ for
$R - \hat{\Psi}$. The diagonal of $S$ or $R$ is replaced by their
respective communalities in $\hat{\psi}_i$ which gives us the following
forms:

$$ S - \hat{\Psi} = 
\begin{bmatrix}
  \hat{h}^2_1 & s_{12} & \cdots & s_{1p} \\
  s_{21} & \hat{h}^2_2 & \cdots & s_{2p} \\
  \vdots & \vdots & & \vdots \\
  s_{p1} & s_{p2} & \cdots & \hat{h}^2_p \\
\end{bmatrix}$$

$$ R - \hat{\Psi} = 
\begin{bmatrix}
  \hat{h}^2_1 & r_{12} & \cdots & r_{1p} \\
  r_{21} & \hat{h}^2_2 & \cdots & r_{2p} \\
  \vdots & \vdots & & \vdots \\
  r_{p1} & r_{p2} & \cdots & \hat{h}^2_p \\
\end{bmatrix}$$

An initial estimate of the communalities is made using the squared
multiple correlation between the observation vector $y_i$ and the other
$p - 1$ variables. The squared multiple correlation in the case of
$R - \hat{\Psi}$ is equivalent to the following:

$$ \hat{h}^2_i = 1 - \frac{1}{r^{ii}} $$

Where $r^{ii}$ is the $i$th diagonal element of $R^{-1}$. In the case of
$S - \hat{\Psi}$, the above is multiplied by the variance of the
respective variable.

The factor loadings are then calculated by finding the eigenvalues and
eigenvectors of the $R - \hat{\Psi}$ or $S - \hat{\Psi}$ matrix.

Factor Analysis with the Principal Factor Method in R
-----------------------------------------------------

We will perform factor analysis using the principal factor method on the
rootstock data as done previously with the principal component method to
see if the approaches differ significantly. The data were obtained from
the [companion FTP site](ftp://ftp.wiley.com) of the book Methods of
Multivariate Analysis by Alvin Rencher. The data contains four dependent
variables as follows:

-   trunk girth at four years (mm $\times$ 100)
-   extension growth at four years (m)
-   trunk girth at 15 years (mm $\times$ 100)
-   weight of tree above ground at 15 years (lb $\times$ 1000)

Load the data and name the columns

``` {.r}
root <- read.table('ROOT.DAT', col.names = c('Tree.Number', 'Trunk.Girth.4.Years', 'Ext.Growth.4.Years', 'Trunk.Girth.15.Years', 'Weight.Above.Ground.15.Years'))
```

Since the variables of the rootstock data were measured on different
scales, we will proceed with using the correlation matrix $R$ to perform
factor analysis.

Find the correlation matrix.

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

Calculate and replace the diagonal of $R$ with the estimated
communalities.

``` {.r}
R.smc <- (1 - 1 / diag(solve(R)))
diag(R) <- R.smc
round(R, 2)
```

    ##                              Trunk.Girth.4.Years Ext.Growth.4.Years
    ## Trunk.Girth.4.Years                         0.80               0.88
    ## Ext.Growth.4.Years                          0.88               0.81
    ## Trunk.Girth.15.Years                        0.44               0.52
    ## Weight.Above.Ground.15.Years                0.33               0.45
    ##                              Trunk.Girth.15.Years
    ## Trunk.Girth.4.Years                          0.44
    ## Ext.Growth.4.Years                           0.52
    ## Trunk.Girth.15.Years                         0.91
    ## Weight.Above.Ground.15.Years                 0.95
    ##                              Weight.Above.Ground.15.Years
    ## Trunk.Girth.4.Years                                  0.33
    ## Ext.Growth.4.Years                                   0.45
    ## Trunk.Girth.15.Years                                 0.95
    ## Weight.Above.Ground.15.Years                         0.91

Now that we have an initial estimate of the communalities, we can find
the eigenvalues and eigenvectors of the $R - \hat{\Psi}$ matrix.

``` {.r}
r.eigen <- eigen(R)
r.eigen$values
```

    ## [1]  2.64598796  0.90756969 -0.03306996 -0.09008523

The $R$ matrix is no longer positive semidefinite due to replacing the
diagonal with the communalities. Thus there are a few small negative
eigenvalues. Since negative eigenvalues cannot be used to estimate
$\hat{\Lambda}$ (due to taking the square root of the $D$ matrix), we
can proceed with $m = 2$.

An interesting note is when negative eigenvalues exist, the cumulative
proportion of variance calculated from the eigenvalues will exceed $1$
and then decline back to $1$ after considering the negative eigenvalues.
The following loop demonstrates this phenomenon:

``` {.r}
tot.prop <- 0
for (i in r.eigen$values) {
  tot.prop <- tot.prop + i / sum(r.eigen$values)
  print(tot.prop)
}
```

    ## [1] 0.7713346
    ## [1] 1.035901
    ## [1] 1.026261
    ## [1] 1

Obtain the factor loadings as before by multiplying the square root of
the first two eigenvalues by their respective eigenvectors.

``` {.r}
r.lambda <- as.matrix(r.eigen$vectors[,1:2]) %*% diag(sqrt(r.eigen$values[1:2]))
r.lambda
```

    ##            [,1]       [,2]
    ## [1,] -0.7402973  0.5421762
    ## [2,] -0.8034091  0.4520610
    ## [3,] -0.8770380 -0.4050851
    ## [4,] -0.8266112 -0.4951379

The communalities, specific variances and complexity of the factor
loadings can then be calculated.

``` {.r}
r.h2 <- rowSums(r.lambda^2)
r.u2 <- 1 - r.h2
com <- rowSums(r.lambda^2)^2 / rowSums(r.lambda^4)
```

Collect the results into a `data.frame`.

``` {.r}
cor.pa <- data.frame(cbind(round(r.lambda, 2), round(r.h2, 2), round(r.u2, 3), round(com, 1)))
colnames(cor.pa) <- c('PA1', 'PA2', 'h2', 'u2', 'com')
cor.pa
```

    ##     PA1   PA2   h2    u2 com
    ## 1 -0.74  0.54 0.84 0.158 1.8
    ## 2 -0.80  0.45 0.85 0.150 1.6
    ## 3 -0.88 -0.41 0.93 0.067 1.4
    ## 4 -0.83 -0.50 0.93 0.072 1.6

Principal Factor Method with the `psych` Package
------------------------------------------------

The [psych package](https://cran.r-project.org/web/packages/psych/) also
performs factor analysis using the principal method with the `fa()`
function.

``` {.r}
library(psych)
```

The `fa()` function performs the iterated principal factor method by
default, which, as the name implies, iterates the initial communality
estimates with those of the resulting $\hat{\Lambda}$ matrix until they
converge. This approach to factor analysis will be demonstrated in a
future post. Setting the `max.iter` argument to 1 will output the
non-iterated principal factor method results.

``` {.r}
root.cor.fa <- fa(root[,2:5], nfactors = 2, rotate = 'none', fm = 'pa', max.iter = 1)
root.cor.fa
```

    ## Factor Analysis using method =  pa
    ## Call: fa(r = root[, 2:5], nfactors = 2, rotate = "none", max.iter = 1, 
    ##     fm = "pa")
    ## Standardized loadings (pattern matrix) based upon correlation matrix
    ##                               PA1   PA2   h2    u2 com
    ## Trunk.Girth.4.Years          0.74  0.54 0.84 0.158 1.8
    ## Ext.Growth.4.Years           0.80  0.45 0.85 0.150 1.6
    ## Trunk.Girth.15.Years         0.88 -0.41 0.93 0.067 1.4
    ## Weight.Above.Ground.15.Years 0.83 -0.50 0.93 0.072 1.6
    ## 
    ##                        PA1  PA2
    ## SS loadings           2.65 0.91
    ## Proportion Var        0.66 0.23
    ## Cumulative Var        0.66 0.89
    ## Proportion Explained  0.74 0.26
    ## Cumulative Proportion 0.74 1.00
    ## 
    ## Mean item complexity =  1.6
    ## Test of the hypothesis that 2 factors are sufficient.
    ## 
    ## The degrees of freedom for the null model are  6  and the objective function was  4.19 with Chi Square of  187.92
    ## The degrees of freedom for the model are -1  and the objective function was  0.17 
    ## 
    ## The root mean square of the residuals (RMSR) is  0.02 
    ## The df corrected root mean square of the residuals is  NA 
    ## 
    ## The harmonic number of observations is  48 with the empirical chi square  0.24  with prob <  NA 
    ## The total number of observations was  48  with Likelihood Chi Square =  7.26  with prob <  NA 
    ## 
    ## Tucker Lewis Index of factoring reliability =  1.281
    ## Fit based upon off diagonal values = 1
    ## Measures of factor score adequacy             
    ##                                                    PA1  PA2
    ## Correlation of (regression) scores with factors   0.98 0.93
    ## Multiple R square of scores with factors          0.95 0.86
    ## Minimum correlation of possible factor scores     0.90 0.72

The results of the `fa()` function align to our own other than an
arbitrary scaling of the first factor by $-1$.

Rotation of Factor Loadings
---------------------------

Rotate the factors using [varimax
rotation](https://en.wikipedia.org/wiki/Varimax_rotation) to improve
interpretation. Varimax rotation of the loadings can be done with the
`varimax()` function, or in the `fa()` function by setting the `rotate`
argument to `varimax`.

``` {.r}
root.cor.fa.v <- fa(root[,2:5], nfactors = 2, rotate = 'varimax', fm = 'pa', max.iter = 1)
root.cor.fa.v
```

    ## Factor Analysis using method =  pa
    ## Call: fa(r = root[, 2:5], nfactors = 2, rotate = "varimax", max.iter = 1, 
    ##     fm = "pa")
    ## Standardized loadings (pattern matrix) based upon correlation matrix
    ##                               PA1  PA2   h2    u2 com
    ## Trunk.Girth.4.Years          0.19 0.90 0.84 0.158 1.1
    ## Ext.Growth.4.Years           0.30 0.87 0.85 0.150 1.2
    ## Trunk.Girth.15.Years         0.92 0.29 0.93 0.067 1.2
    ## Weight.Above.Ground.15.Years 0.95 0.18 0.93 0.072 1.1
    ## 
    ##                        PA1  PA2
    ## SS loadings           1.87 1.68
    ## Proportion Var        0.47 0.42
    ## Cumulative Var        0.47 0.89
    ## Proportion Explained  0.53 0.47
    ## Cumulative Proportion 0.53 1.00
    ## 
    ## Mean item complexity =  1.1
    ## Test of the hypothesis that 2 factors are sufficient.
    ## 
    ## The degrees of freedom for the null model are  6  and the objective function was  4.19 with Chi Square of  187.92
    ## The degrees of freedom for the model are -1  and the objective function was  0.17 
    ## 
    ## The root mean square of the residuals (RMSR) is  0.02 
    ## The df corrected root mean square of the residuals is  NA 
    ## 
    ## The harmonic number of observations is  48 with the empirical chi square  0.24  with prob <  NA 
    ## The total number of observations was  48  with Likelihood Chi Square =  7.26  with prob <  NA 
    ## 
    ## Tucker Lewis Index of factoring reliability =  1.281
    ## Fit based upon off diagonal values = 1
    ## Measures of factor score adequacy             
    ##                                                    PA1  PA2
    ## Correlation of (regression) scores with factors   0.97 0.94
    ## Multiple R square of scores with factors          0.94 0.87
    ## Minimum correlation of possible factor scores     0.88 0.75

Principal Component and Principal Factor Methods Comparison
-----------------------------------------------------------

The principal factor method (and iterated principal factor method) will
usually yield results close to the principal component method if either
the correlations or the number of variables is large (Rencher, 2002, pp.
424).

Perform the principal component method of factor analysis and compare
with the principal factor method.

``` {.r}
root.cor.pa <- principal(root[,2:5], nfactors = 2, rotate = 'varimax')
root.cor.pa
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

Both methods achieved a simple structure of the loadings following
rotation. The loadings from each method are rather similar and don't
differ significantly, though the principal component method yielded
factors that load more heavily on the variables which the factors
hypothetically represent. However, the factors resulting from the
principal component method explain 96% of the cumulative variance
compared to 89% from the principal factor method. Though not a drastic
difference, one is inclined to proceed with the principal component
method in this case as the factors account for almost all of the
variance in the variables.

References
----------

Rencher, A. (2002). Methods of Multivariate Analysis (2nd ed.). Brigham
Young University: John Wiley & Sons, Inc.
