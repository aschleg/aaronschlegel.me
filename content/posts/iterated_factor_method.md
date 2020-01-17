Title: Factor Analysis with the Iterated Factor Method and R
Date: 2017-03-03
Tags: R, factor analysis, linear algebra
Category: Statistics
Slug: factor-analysis-iterated-factor-method-r
Author: Aaron Schlegel
Summary: The iterated principal factor method is an extension of the principal
factor method that seeks improved estimates of the communality. In the iterated 
principal factor method, the initial estimates of the communality are used to 
find new communality estimates from the loadings. The iterated principal factor method is demonstrated on the rootstock
data as in the previous posts on factor analysis for consistency and
comparison of the various approaches.

The iterated principal factor method is an extension of the [principal
factor method](https://aaronschlegel.me/factor-analysis-principal-factor-r.html) 
that seeks improved estimates of the communality. As seen in the previous post on the principal factor
method, initial estimates of $R - \hat{\Psi}$ or $S - \hat{\Psi}$ are
found to obtain $\hat{\Lambda}$ from which the factors are computed. In
the iterated principal factor method, the initial estimates of the
communality are used to find new communality estimates from the loadings
in $\hat{\Lambda}$ with the following:

$$ \hat{h}^2_i = \sum^m_{j=1} \hat{\lambda}^2_{ij} $$

The values of $\hat{h}^2_i$ are then substituted into the diagonal of
$R - \hat{\Psi}$ or $S - \hat{\Psi}$ and a new value of $\hat{\Lambda}$
is found. This iteration continues until the communality estimates
converge, though sometimes convergence does not occur. Once the
estimates converge, the eigenvalues and eigenvectors are calculated from
the iterated $R - \hat{\Psi}$ or $S - \hat{\Psi}$ matrix to arrive at
the factor loadings.

The Iterated Principal Factor Method in R
-----------------------------------------

The iterated principal factor method is demonstrated on the rootstock
data as in the previous posts on factor analysis for consistency and
comparison of the various approaches. The rootstock data contain four
variables representing measurements in different units taken at four and
fifteen years growth of six different rootstocks. The data were obtained
from the [companion FTP site](ftp://ftp.wiley.com) of the book Methods
of Multivariate Analysis by Alvin Rencher. The data contains four
dependent variables as follows:

-   trunk girth at four years (mm $\times$ 100)
-   extension growth at four years (m)
-   trunk girth at 15 years (mm $\times$ 100)
-   weight of tree above ground at 15 years (lb $\times$ 1000)

Load the data and name the columns.

``` {.r}
root <- read.table('ROOT.DAT', col.names = c('Tree.Number', 'Trunk.Girth.4.Years', 'Ext.Growth.4.Years', 'Trunk.Girth.15.Years', 'Weight.Above.Ground.15.Years'))
```

We proceed with the correlation matrix $R$ as the variables in the data
are not measured commensurately. Using $R$ over $S$ is generally the
preferred approach and is usually the default in most implementations
(such as the `psych` package).

Calculate the correlation matrix.

``` {.r}
R <- cor(root[,2:5])
```

The initial estimates of the communality are found by computing the
squared multiple correlation, which in the case of $R - \hat{\Psi}$ is
equal to the following:

$$ \hat{h}^2_i = 1 - \frac{1}{r^{ii}} $$

Where $r^{ii}$ is the $i$th diagonal element of $R^{-1}$.

``` {.r}
R.smc <- (1 - 1 / diag(solve(R)))
```

The estimates then replace the diagonal of $R$.

``` {.r}
diag(R) <- R.smc
```

The threshold for convergence of the communality is set to $0.001$. This
error threshold is also the default in the `psych` package
implementation of the iterated principal factor method. The `com.iter`
object will be used to store the communality iterations.

``` {.r}
min.error <- .001
com.iter <- c()
```

$\hat{h}^2_i$ is then found from
$\hat{h}^2_i = \sum^m_{j=1} \hat{\lambda}^2_{ij}$, which is simply the
sum of the diagonal of $R$ ($R$ will be replaced with $\hat{\Lambda}$ in
the iteration).

``` {.r}
h2 <- sum(diag(R))
error <- h2
```

The following loop implements the iterated principal factor method using
$R$ with the estimated communalities found earlier. While our
communality estimate remains above the error threshold of $0.001$, the
loop will continue to calculate new values of $\hat{\Lambda}$ by
replacing the previous estimates of communality with new ones.

``` {.r}
while (error > min.error) {
  r.eigen <- eigen(R) # Get the eigenvalues and eigenvectors of R
  
  # The lambda object is updated upon each iteration using new estimates of the communality
  lambda <- as.matrix(r.eigen$vectors[,1:2]) %*% diag(sqrt(r.eigen$values[1:2]))
  
  # R - Psi is then found by multiplying the lambda matrix by its transpose
  r.mod <- lambda %*% t(lambda)
  r.mod.diag <- diag(r.mod) # The diagonal of R - Psi is the new communality estimate
  
  # The sum of the new estimate is taken and compared with the previous estimate. If the
  # difference is less than the error threshold the loop stops
  h2.new <- sum(r.mod.diag) 
  error <- abs(h2 - h2.new)
  
  # If the difference between the previous and new estimate is not below the threshold, replace
  # the new estimate with the previous
  h2 <- h2.new
  
  # Store the iteration value (the sum of the estimate) and replace the diagonal of R with the
  # diagonal of R - Psi found previously
  com.iter <- append(com.iter, h2.new)
  diag(R) <- r.mod.diag
}
```

We now have the final $\hat{\Lambda}$. Find the communality, specific
variances and complexity and collect them into a `data.frame`

``` {.r}
h2 <- rowSums(lambda^2)
u2 <- 1 - h2
com <- rowSums(lambda^2)^2 / rowSums(lambda^4)

iter.fa.loadings <- data.frame(cbind(round(lambda,2), round(h2, 2), round(u2, 3), round(com, 2)))
colnames(iter.fa.loadings) <- c('Factor 1', 'Factor 2', 'h2', 'u2', 'com')
```

The proportion of variance explained by the factors is found by:

$$ \frac{\theta_j}{tr(R - \hat{\Psi})} = \frac{\theta_j}{\sum^p_{i=1} \theta_i} $$

Where $\theta_j$ is the $j$th eigenvalue of $R - \hat{\Psi}$. The
cumulative variance of the factors when factoring $R$ is found by:

$$ \frac{\sum^p_{i=1} \hat{\lambda}^2_{ij}}{tr(R)} = \frac{\theta_j}{p} $$

Where $p$ is the number of variables. Calculate these values and store
in a `data.frame`.

``` {.r}
prop.var <- r.eigen$values[1:2] / sum(diag(R))
var.cumulative <- r.eigen$values / 4

factor.var <- data.frame(rbind(round(prop.var[1:2], 2), round(var.cumulative[1:2], 2)))
rownames(factor.var) <- c('Proportion Explained', 'Cumulative Variance')
colnames(factor.var) <- c('Factor 1', 'Factor 2')
factor.var
```

    ##                      Factor 1 Factor 2
    ## Proportion Explained     0.74     0.26
    ## Cumulative Variance      0.68     0.24

The iterated principal factor method of factor analysis is complete, and
we can now print the results!

``` {.r}
iter.fa.res <- list(iter.fa.loadings, factor.var)
iter.fa.res
```

    ## [[1]]
    ##   Factor 1 Factor 2   h2    u2  com
    ## 1    -0.76     0.56 0.89 0.109 1.84
    ## 2    -0.82     0.46 0.88 0.116 1.57
    ## 3    -0.88    -0.42 0.94 0.055 1.44
    ## 4    -0.83    -0.52 0.96 0.042 1.68
    ## 
    ## [[2]]
    ##                      Factor 1 Factor 2
    ## Proportion Explained     0.74     0.26
    ## Cumulative Variance      0.68     0.24

Interpretation of the factor loadings should be held until the factors
are rotated. We will also compare the results of the iterated approach
to the principal component method. Let's compare our results with the
output of the `psych` package to verify.

Iterated Principal Factor Method with the `psych` Package
---------------------------------------------------------

The function `fa()` available in the [psych
package](https://cran.r-project.org/web/packages/psych/) defaults to the
iterated approach. We keep the `rotate` argument set to `none` for now
and the `fm` argument to `pa` (principal axis, another term for
principal factors).

``` {.r}
library(psych)
```

``` {.r}
root.cor.fa <- fa(root[,2:5], nfactors = 2, rotate = 'none', fm = 'pa')
root.cor.fa
```

    ## Factor Analysis using method =  pa
    ## Call: fa(r = root[, 2:5], nfactors = 2, rotate = "none", fm = "pa")
    ## Standardized loadings (pattern matrix) based upon correlation matrix
    ##                               PA1   PA2   h2    u2 com
    ## Trunk.Girth.4.Years          0.76  0.56 0.89 0.109 1.8
    ## Ext.Growth.4.Years           0.82  0.46 0.88 0.116 1.6
    ## Trunk.Girth.15.Years         0.88 -0.42 0.94 0.055 1.4
    ## Weight.Above.Ground.15.Years 0.83 -0.52 0.96 0.042 1.7
    ## 
    ##                        PA1  PA2
    ## SS loadings           2.71 0.97
    ## Proportion Var        0.68 0.24
    ## Cumulative Var        0.68 0.92
    ## Proportion Explained  0.74 0.26
    ## Cumulative Proportion 0.74 1.00
    ## 
    ## Mean item complexity =  1.6
    ## Test of the hypothesis that 2 factors are sufficient.
    ## 
    ## The degrees of freedom for the null model are  6  and the objective function was  4.19 with Chi Square of  187.92
    ## The degrees of freedom for the model are -1  and the objective function was  0.06 
    ## 
    ## The root mean square of the residuals (RMSR) is  0.01 
    ## The df corrected root mean square of the residuals is  NA 
    ## 
    ## The harmonic number of observations is  48 with the empirical chi square  0.03  with prob <  NA 
    ## The total number of observations was  48  with Likelihood Chi Square =  2.75  with prob <  NA 
    ## 
    ## Tucker Lewis Index of factoring reliability =  1.128
    ## Fit based upon off diagonal values = 1
    ## Measures of factor score adequacy             
    ##                                                    PA1  PA2
    ## Correlation of (regression) scores with factors   0.99 0.96
    ## Multiple R square of scores with factors          0.97 0.92
    ## Minimum correlation of possible factor scores     0.94 0.85

The output matches our results other than an arbitrary scaling of $-1$
on the first factor in our calculations (notice this does not affect the
communality or other computations as the loadings are squared). We can
also see the `fa()` function had the same iterations as our loop using
the `com.iter` object from earlier.

``` {.r}
com.iter
```

    ## [1] 3.553558 3.615064 3.645859 3.661351 3.669220 3.673293 3.675480 3.676730
    ## [9] 3.677517

``` {.r}
root.cor.fa$communality.iterations
```

    ## [1] 3.553558 3.615064 3.645859 3.661351 3.669220 3.673293 3.675480 3.676730
    ## [9] 3.677517

Rotation of Factors
-------------------

The factors should be rotated so the variables load highly on one factor
to better identify the groupings of the variables. Rotation also yields
a simple structure of the data which is denoted by the complexity value
calculated previously and improves interpretation of the factors.

The `varimax()` function can be used to rotate our computed factor
loadings. Varimax rotation is a type of orthogonal rotation, in which
the perpendicular axes remain perpendicular and the communality remains
the same after rotation. Orthogonal rotations also result in
uncorrelated factor loadings which can be useful for interpretation.

``` {.r}
lambda.v <- varimax(lambda)$loadings
lambda.v
```

    ## 
    ## Loadings:
    ##      [,1]   [,2]  
    ## [1,] -0.182  0.926
    ## [2,] -0.295  0.893
    ## [3,] -0.931  0.281
    ## [4,] -0.963  0.177
    ## 
    ##                 [,1]  [,2]
    ## SS loadings    1.912 1.765
    ## Proportion Var 0.478 0.441
    ## Cumulative Var 0.478 0.919

Otherwise, setting the `rotate` argument to `varimax` in the `fa()`
function will perform varimax rotation.

Comparison of Iterated Principal Factors and Principal Component Method
-----------------------------------------------------------------------

We saw the non-iterated principal factor approach previously, and the
[principal component method](https://aaronschlegel.me/factor-analysis-principal-component-method-r.html) reported similar
results; however, factor loadings from principal components loaded
slightly higher on their respective variables and represented the more
cumulative variance of the original data. Let's see if the iterated
method performs any better to the principal component method.

``` {.r}
root.cor.fa <- fa(root[,2:5], nfactors = 2, rotate = 'varimax', fm = 'pa')
root.cor.fa
```

    ## Factor Analysis using method =  pa
    ## Call: fa(r = root[, 2:5], nfactors = 2, rotate = "varimax", fm = "pa")
    ## Standardized loadings (pattern matrix) based upon correlation matrix
    ##                               PA1  PA2   h2    u2 com
    ## Trunk.Girth.4.Years          0.18 0.93 0.89 0.109 1.1
    ## Ext.Growth.4.Years           0.30 0.89 0.88 0.116 1.2
    ## Trunk.Girth.15.Years         0.93 0.28 0.94 0.055 1.2
    ## Weight.Above.Ground.15.Years 0.96 0.18 0.96 0.042 1.1
    ## 
    ##                        PA1  PA2
    ## SS loadings           1.91 1.77
    ## Proportion Var        0.48 0.44
    ## Cumulative Var        0.48 0.92
    ## Proportion Explained  0.52 0.48
    ## Cumulative Proportion 0.52 1.00
    ## 
    ## Mean item complexity =  1.1
    ## Test of the hypothesis that 2 factors are sufficient.
    ## 
    ## The degrees of freedom for the null model are  6  and the objective function was  4.19 with Chi Square of  187.92
    ## The degrees of freedom for the model are -1  and the objective function was  0.06 
    ## 
    ## The root mean square of the residuals (RMSR) is  0.01 
    ## The df corrected root mean square of the residuals is  NA 
    ## 
    ## The harmonic number of observations is  48 with the empirical chi square  0.03  with prob <  NA 
    ## The total number of observations was  48  with Likelihood Chi Square =  2.75  with prob <  NA 
    ## 
    ## Tucker Lewis Index of factoring reliability =  1.128
    ## Fit based upon off diagonal values = 1
    ## Measures of factor score adequacy             
    ##                                                    PA1  PA2
    ## Correlation of (regression) scores with factors   0.98 0.96
    ## Multiple R square of scores with factors          0.97 0.93
    ## Minimum correlation of possible factor scores     0.93 0.86

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

Similar to the previous case with the non-iterated method, the principal
component approach resulted in factors that loaded higher on their
respective variables and represents slightly more cumulative variance of
the data. The difference between the methods is rather small, yet one
would be inclined to use the principal component method results.

References
----------

Rencher, A. (2002). Methods of Multivariate Analysis (2nd ed.). Brigham
Young University: John Wiley & Sons, Inc.
