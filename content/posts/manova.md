Title: Calculating and Performing One-way Multivariate Analysis of Variance (MANOVA)
Date: 2018-07-24
Tags: R, statistics
Category: Statistics
Slug: calculating-performing-one-way-multivariate-analysis-of-variance-manova
Author: Aaron Schlegel
Summary: MANOVA, or Multiple Analysis of Variance, is an extension of Analysis of Variance (ANOVA) to several dependent variables. The approach to MANOVA is similar to ANOVA in many regards and requires the same assumptions (normally distributed dependent variables with equal covariance matrices).

MANOVA, or Multiple Analysis of Variance, is an extension of Analysis of Variance (ANOVA) to several dependent variables. The approach to MANOVA is similar to ANOVA in many regards and requires the same assumptions (normally distributed dependent variables with equal covariance matrices). This post will explore how MANOVA is performed and interpreted by analyzing the growth of six different apple tree rootstocks from 1918 to 1934 (Andrews and Herzberg 1985, pp. 357-360).

Multiple Analysis of Variance
-----------------------------

In the MANOVA setting, each observation vector can have a model denoted as:

$$ y_{ij} = \mu_i + \epsilon_{ij} \qquad  i = 1, 2, \cdots, k; \qquad j = 1, 2, \cdots, n $$

An 'observation vector' is a set of observations measured over several variables. With $p$ variables, $y_{ij} becomes:

$$\begin{bmatrix}
  y_{ij1} \\ y_{ij2} \\ \vdots \\ y_{ijp}
\end{bmatrix} = \begin{bmatrix}
  \mu_{i1} \\ \mu_{i2} \\ \vdots \\ \mu_{ip}
\end{bmatrix} + \begin{bmatrix}
  \epsilon_{ij1} \\ \epsilon_{ij2} \\ \vdots \\ \epsilon_{ijp}
\end{bmatrix}$$

Thus, for the $r^{th}$ variable in $(r = 1, 2, \cdots, p)$ in each vector $y_{ij}$, the model takes the form:

$$ y_{ij} = \mu_r + \epsilon_{ijr} $$

As before in ANOVA, the goal is to compare the groups to see if there are any significant differences. However, instead of a single variable, the comparisons will be made with the mean vectors of the samples. The null hypothesis $H_0$ can be formalized the same way in MANOVA:

$$ H_0 : \mu_1 = \mu_2 = \cdots = \mu_k $$

With an alternative hypothesis $H_a$ that at least two *μ* are unequal. There are $p(k − 1)$, where $k$ is the number of groups in the data, equalities that must be true for $H_0$ to be accepted.

MANOVA Between and Within Variation
-----------------------------------

The totals and means of the samples in the data are defined as:

-   Total of the $i$th sample: $y_{i.} = \sum^n_{j=1} y_{ij}$
-   Overall total: $y_{..} = \sum^k_{i=1} \sum^n_{j=1} y_{ij}$
-   Mean of the ith sample: $\bar{y}_{i.} = y_{i.} / n$
-   Overall mean: $\bar{y}_{..} = y_{..} / kn$

Similar to ANOVA, we are interested in partitioning the data's total variation into variation between and within groups. In the case of ANOVA, this partitioning is done by calculating $SSH$ and $SSE$; however, in the multivariate case, we must extend this to encompass the variation in all the $p$ variables. Therefore, we must compute the between and within sum of squares for each possible comparison. This procedure results in the $H$ "hypothesis matrix" and $E$ "error matrix."

The $H$ matrix is a square $p \times p$ with the form:

$$H =
\begin{bmatrix}
  SSH_{11} & SPH_{21} & \dots & SPH_{1p} \\
  SPH_{12} & SSH_{22} & \dots & SPH\_{2p} \\
  \vdots & \vdots & & \vdots \\
  SPH_{1p} & SPH_{2p} & \cdots & SSH_{pp}
\end{bmatrix}$$

Where the entries are equal to:

$$ H = n \sum^k_{i=1} (\bar{y}_{i.} - \bar{y}_{..}) (\bar{y}_{i.} - \bar{y}_{..})' $$

Thus, for example, the above equation for the entries $SSH_{11}$ and $SPH_{23}$ would take the form:

$$ SSH_{11} = n \sum^k_{i=1} (\bar{y}_{i.1} - \bar{y}_{..1})^2 $$
$$ SPH_{23} = n \sum^k_{i=1} (\bar{y}_{i.2} - \bar{y}_{..2}) (\bar{y}_{i.3} - \bar{y}_{..3}) $$

The error matrix $E$ is also $p \times p$ and can be expressed similarly to $H$.

$$E = 
\begin{bmatrix}
  SSE_{11} & SPE_{12} & \cdots & SPE_{1p} \\
  SPE_{12} & SSE_{22} & \cdots & SPE_{2p} \\
  \vdots & \vdots & & \vdots \\
  SPE_{1p} & SPE_{2p} & \cdots & SSE_{pp}
\end{bmatrix}$$

With the entries equal to:

$$ E = \sum^k_{i=1} \sum^n_{j=1} (y_{ij} - \bar{y}_{i.}) (y_{ij} - \bar{y}_{i.})' $$

Therefore for corresponding entries $SSE_{11}$ and $SPE_{23}$, the above equation is expressed as the following:

$$ SSE_{11} = \sum^k_{i=1} \sum^n_{j=1} (y_{ij1} - \bar{y}_{i.1})^2 $$
$$ SPE_{23} = \sum^k_{i=1} \sum^n_{j=1} (y_{ij2} - \bar{y}_{i.2}) (y_{ij3} - \bar{y}_{i.3}) $$

Once the $H$ and $E$ matrices are constructed, the mean vectors can be compared to determine if significant differences exist. There are several test statistics, of which the most common are Wilk's lambda, Roy's test, Pillai, and Lawley-Hotelling, that can be employed to test for significant differences. Each test statistic has specific properties and power and will be discussed in a future post. For now, the default Pillai test statistic from the `manova()` function will suffice (and is the recommended statistic to use in most cases according to the documentation in `?summary(manova())`).

The rootstock data were obtained from the [companion FTP site](ftp://ftp.wiley.com) of the book Methods of Multivariate Analysis by Alvin Rencher. The data contains four dependent variables as follows:

-   trunk girth at four years (mm × 100)
-   extension growth at four years (m)
-   trunk girth at 15 years (mm × 100)
-   weight of tree above ground at 15 years (lb × 1000)

``` r
root <- read.table('ROOT.DAT', col.names = c('Tree.Number', 'Trunk.Girth.4.Years', 'Ext.Growth.4.Years', 'Trunk.Girth.15.Years', 'Weight.Above.Ground.15.Years'))

root$Tree.Number <- as.factor(root$Tree.Number)
```

MANOVA in R
-----------

The `manova()` function accepts a formula argument with the dependent variables formatted as a matrix and the grouping factor on the right of the `~`.

``` r
dependent.vars <- cbind(root$Trunk.Girth.4.Years, root$Ext.Growth.4.Years, root$Trunk.Girth.15.Years, root$Weight.Above.Ground.15.Years)
```

Perform MANOVA and output a summary of the results.

``` r
root.manova <- summary(manova(dependent.vars ~ root$Tree.Number))
root.manova
```

    ##                  Df Pillai approx F num Df den Df    Pr(>F)    
    ## root$Tree.Number  5 1.3055   4.0697     20    168 1.983e-07 ***
    ## Residuals        42                                            
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

The resultant MANOVA model reports a Pillai test statistic of 1.3055 and a p-value below 0.05, thus $H_0$ is rejected and it is concluded there are significant differences in the means.

Although the test rejected $H_0$, we can test each variable individually with an ANOVA test. The `aov()` function can output tests on individual variables when wrapped in a `summary()` call.

``` r
summary(aov(dependent.vars ~ root$Tree.Number))
```

    ##  Response 1 :
    ##                  Df  Sum Sq   Mean Sq F value Pr(>F)
    ## root$Tree.Number  5 0.07356 0.0147121   1.931 0.1094
    ## Residuals        42 0.31999 0.0076187               
    ## 
    ##  Response 2 :
    ##                  Df  Sum Sq Mean Sq F value Pr(>F)  
    ## root$Tree.Number  5  4.1997 0.83993  2.9052 0.0243 *
    ## Residuals        42 12.1428 0.28911                 
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ##  Response 3 :
    ##                  Df Sum Sq Mean Sq F value    Pr(>F)    
    ## root$Tree.Number  5 6.1139 1.22279  11.969 3.112e-07 ***
    ## Residuals        42 4.2908 0.10216                      
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ##  Response 4 :
    ##                  Df Sum Sq Mean Sq F value    Pr(>F)    
    ## root$Tree.Number  5 2.4931 0.49862  12.158 2.587e-07 ***
    ## Residuals        42 1.7225 0.04101                      
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Only the first variable, trunk girth at four years, reports a p-value above 0.05. Thus it is concluded there are significant differences in the means for the variables except for trunk girth at four years amongst the six groups.

Replicating MANOVA in R
-----------------------

For a deeper understanding of how MANOVA is calculated, we can replicate the results of the `manova()` function by computing the $H$ and $E$ matrices as mentioned above. To calculate these matrices, first split the data into a list by group and find the mean vectors of each group. The sample sizes $n_i$ of each group, and the total mean vector will also be required.

``` r
root.group <- split(root[,2:5], root$Tree.Number)

root.means <- sapply(root.group, function(x) {
  apply(x, 2, mean)
}, simplify = 'data.frame')


n <- dim(root)[1] / length(unique(root$Tree.Number))

total.means <- colMeans(root[,2:5])
```

The $H$ and $E$ matrices can be computed with the following code.

``` r
H = matrix(data = 0, nrow = 4, ncol = 4)
for (i in 1:dim(H)[1]) {
  for (j in 1:i) {
    H[i,j] <- n * sum((root.means[i,] - total.means[i]) * (root.means[j,] - total.means[j]))
    H[j,i] <- n * sum((root.means[j,] - total.means[j]) * (root.means[i,] - total.means[i]))
  }
}
H
```

    ##            [,1]      [,2]      [,3]     [,4]
    ## [1,] 0.07356042 0.5373852 0.3322646 0.208470
    ## [2,] 0.53738521 4.1996619 2.3553885 1.637108
    ## [3,] 0.33226458 2.3553885 6.1139354 3.781044
    ## [4,] 0.20847000 1.6371084 3.7810438 2.493091

``` r
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

Verify the results by comparing the computed matrices to the output of `summary(manova())`.

``` r
root.manova$SS[1]
```

    ## $`root$Tree.Number`
    ##            [,1]      [,2]      [,3]     [,4]
    ## [1,] 0.07356042 0.5373852 0.3322646 0.208470
    ## [2,] 0.53738521 4.1996619 2.3553885 1.637108
    ## [3,] 0.33226458 2.3553885 6.1139354 3.781044
    ## [4,] 0.20847000 1.6371084 3.7810437 2.493091

``` r
H
```

    ##            [,1]      [,2]      [,3]     [,4]
    ## [1,] 0.07356042 0.5373852 0.3322646 0.208470
    ## [2,] 0.53738521 4.1996619 2.3553885 1.637108
    ## [3,] 0.33226458 2.3553885 6.1139354 3.781044
    ## [4,] 0.20847000 1.6371084 3.7810438 2.493091

``` r
root.manova$SS[2]
```

    ## $Residuals
    ##           [,1]      [,2]      [,3]     [,4]
    ## [1,] 0.3199875  1.696564 0.5540875 0.217140
    ## [2,] 1.6965637 12.142790 4.3636125 2.110214
    ## [3,] 0.5540875  4.363612 4.2908125 2.481656
    ## [4,] 0.2171400  2.110214 2.4816562 1.722525

``` r
E
```

    ##           [,1]      [,2]      [,3]     [,4]
    ## [1,] 0.3199875  1.696564 0.5540875 0.217140
    ## [2,] 1.6965637 12.142790 4.3636125 2.110214
    ## [3,] 0.5540875  4.363613 4.2908125 2.481656
    ## [4,] 0.2171400  2.110214 2.4816563 1.722525

The Pillai test statistic is denoted as $V^{(s)}$ and defined as:

$$ V^{(s)} = tr[(E + H)^{-1} H] = \sum^s_{i=1} \frac{\lambda_i}{1 + \lambda_i} $$

Where $\lambda_i$ represents the $i$th nonzero eigenvalue of $E^{−1}H$. Thus we can manually calculate the Pillai statistic with either of the following:

``` r
vs <- sum(diag(solve(E + H) %*% H)) # Will be used later in the post to find approximate F-statistic
vs
```

    ## [1] 1.305472

``` r
sum((eigen(solve(E) %*% H)$values) / (1 + eigen(solve(E) %*% H)$values))
```

    ## [1] 1.305472

Which is the same as the `manova()` function output. The Pillai statistic is then used to determine the significance of differences of the mean vectors by comparing it to the critical value $V_{\alpha}^(s)$. The critical Pillai value is found by computing $s$, $m$, and $N$ which are also employed in Roy's test (the Pillai test is an extension of Roy's test). The values are defined as:

$$ s = min(p, V_h) \qquad m = \frac{1}{2} (\left| V_h - p \right| - 1) \qquad N = \frac{1}{2} (V_E - p - 1) $$

An approximate F-statistic can be found with the following equation:

$$ F = \frac{(2N + s + 1)V^{(s)}}{(2m + s + 1)(s - V^{(s)})} $$

``` r
k <- length(unique(root$Tree.Number))
p <- length(root[,2:5])
vh <- k - 1
ve <- dim(root)[1] - k
```

Where $v_H$ is the degrees of freedom for the hypothesis and $v_E$ is the degrees of freedom for the error.

``` r
s <- min(vh, p)
m <- .5 * (abs(vh - p) - 1)
N <- .5 * (ve - p - 1)

f.approx <- ((2 * N + s + 1) * vs) / ((2 * m + s + 1) * (s - vs))
f.approx
```

    ## [1] 4.069718

``` r
root.manova$stats[,3][1]
```

    ## root$Tree.Number 
    ##         4.069718

The calculated approximate F-statistic matches what was reported in the `manova()` function.

Summary
-------

This post explored the extension of ANOVA to multiple dependent variables known as MANOVA and how to perform the procedure with built-in R functions and manual computations. The concepts of ANOVA are extended and generalized to encompass *p* variables, and thus the intuition and logic behind ANOVA also apply to the multivariate case. Future posts will examine more topics related to MANOVA including additional test statistics, unbalanced (unequal sample sizes) approaches and two-way classification.

References
----------

[Andrews, D. F., and Herzberg, A. M. (1985), Data, New York: Springer-Verlag.](https://amzn.to/2HizNch)

[Rencher, A. C. (2002). Methods of multivariate analysis. New York: J. Wiley.](https://amzn.to/39gsldt)
