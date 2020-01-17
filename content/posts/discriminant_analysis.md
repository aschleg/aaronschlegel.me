Title: Discriminant Analysis for Group Separation
Date: 2018-08-20
Tags: R, linear algebra, classification, linear discriminant analysis
Category: Linear Algebra
Slug: discriminant-analysis-group-separation
Author: Aaron Schlegel
Summary: Discriminant analysis assumes the two samples or populations being compared have the same covariance matrix $\Sigma$ but distinct mean vectors $\mu_1$ and $\mu_2$ with $p$ variables. The discriminant function that maximizes the separation of the groups is the linear combination of the $p$ variables. The linear combination denoted $z = a′y$ transforms the observation vectors to a scalar. The discriminant functions thus take the form:

The term 'discriminant analysis' is often used interchangeably to represent two different objectives. These objectives of discriminant analysis are:

-   Description of group separation. Linear combinations of variables, known as discriminant functions, of the dependent variables that maximize the separation between the groups are used to identify the relative contribution of the $p$ variables that best predict group membership.

-   Prediction of observations to groups using either linear or quadratic discriminant functions, known as LDA and QDA, respectively.

This post will explore the first objective of discriminant analysis with two groups. Future posts will examine the classification and prediction objective of discriminant analysis.

Discriminant Analysis for Two Groups
------------------------------------

Discriminant analysis assumes the two samples or populations being compared have the same covariance matrix $\Sigma$ but distinct mean vectors $\mu_1$ and $\mu_2$ with $p$ variables. The discriminant function that maximizes the separation of the groups is the linear combination of the $p$ variables. The linear combination denoted $z = a′y$ transforms the observation vectors to a scalar. The discriminant functions thus take the form:

$$ z_{1i} = a′y_{1i} = a_1 y_{1i1} + a_2 y_{1i2} + \cdots + a_p y_{1ip} \qquad i = 1, 2, \cdots, n_1 $$
$$ z_{2i} = a′y_{2i} = a_2 y_{2i1} + a_2 y_{2i2} + \cdots + a_p y_{2ip} \qquad  i = 1, 2, \cdots, n_2 $$

To compute the discriminant function coefficients, first find the sample means $\bar{z}_1$ and $\bar{z}_2$. The mean can be found by averaging the $n$ values or as a linear combination of the sample mean vector $y_1$, $\bar{y}$

$$ \bar{z}_1 = \frac{1}{n_1} \sum^{n_1}_{i=1} z_{1i} = a'\bar{y}_1 $$
$$ \bar{z}_2 = \frac{1}{n_2} \sum^{n_2}_{i=1} z_{2i} = a'\bar{y}_2 $$

Where,

$$ \bar{y}_1 = \sum^{n_1}_{i=1} \frac{y_{1i}}{n_1} $$
$$ \bar{y}_1 = \sum^{n_2}_{i=1} \frac{y_{2i}}{n_2} $$

The goal is to then find a vector $a$ that maximizes the standardized squared difference $(\bar{z}_1 - \bar{z}_2)^2 / s^2_z$. The sample variance $s_z^2$ is the sample variance of $z_1, z_2, \cdots, z_n$ or from the vector $a$ and the sample covariance matrix of the mean vectors $y_1, y_2, \cdots, y_n$, denoted by $S$.

$$ s^2_z = \frac{\sum^n_{i=1}(z_i - \bar{z})^2}{n - 1} = a'Sa $$

Thus the standardized squared distance $(\bar{z}_1 - \bar{z}_2)^2 / s^2_z$ can also be written as the following:

$$ \frac{(\bar{z}_1 - \bar{z}_2)^2}{s^2_z} = \frac{[a'(\bar{y}_1 - \bar{y}_2)]^2}{a'S_{p1}a} $$

Where $S_{p1}$ is an unbiased estimator of the covariance matrix $\Sigma$. $S_{p1}$ is defined as:

$$ S_{p1} = \frac{1}{n_1 + n_2 - 2}(W_1 + W_2) $$

Where $W_1$ and $W_2$ are defined as matrices of the sample sum of squares and cross products.

$$ W_1 = \sum^{n_1}_{i=1}(y_{1i} - \bar{y}_1)(y_{1i} - \bar{y}_1)' = (n_1 - 1)S_1 $$
$$ W_2 = \sum^{n_2}_{i=1}(y_{2i} - \bar{y}_2)(y_{2i} - \bar{y}_2)' = (n_2 - 1)S_2 $$

For $S_{p1}$ to exist, $n_1 + n_2 − 2 > p$ must be satisified.

The maximum of the above function is found when $a$ is equivalent or a multiple of the following:

$$ a = S_{p1}^{-1}(\bar{y}_1 - \bar{y}_2) $$

Since $a$ can be a multiple of the above, it is not unique; however, its direction is unique. By 'direction', it is implied the relative values of the vector $a, $a_1, a_2, \cdots, a_p$ are unique.

Discriminant Analysis in R
--------------------------

The data we are interested in is four measurements of two different species of flea beetles. All measurements are in micrometers ($\mu m$) except for the elytra length which is in units of .01 mm. The data were obtained from the [companion FTP site](ftp://ftp.wiley.com) of the book Methods of Multivariate Analysis by Alvin Rencher.

Read the data and give the columns names for reference.

``` r
beetles <- read.table('BEETLES.DAT', col.names = c('Measurement.Number', 'Species', 'transverse.groove.dist', 'elytra.length', 'second.antennal.joint.length', 'third.antennal.joint.length'))
```

The [dplyr package](https://cran.r-project.org/web/packages/dplyr/index.html) will be used for simple data manipulation.

``` r
library(dplyr)
```

Separate the two groups into different data frames.

``` r
beetle1 <- filter(beetles, Species == 1)[,3:6]
beetle2 <- filter(beetles, Species == 2)[,3:6]
```

Store the sample size and means of the two groups for later.

``` r
n1 <- nrow(beetle1)
n2 <- nrow(beetle2)

beetle1.means <- apply(beetle1, 2, mean)
beetle2.means <- apply(beetle2, 2, mean)
```

First, $S_{p1}$ must be calculated.

``` r
w1 <- (n1 - 1) * var(beetle1)
w2 <- (n2 - 1) * var(beetle2)

sp1 <- 1 / (n1 + n2 - 2) * (w1 + w2)
```

As mentioned above, the groups are maximally separated when $a = S_{p1}^{-1}(\bar{y}_1 - \bar{y}_2)$.

``` r
a <- solve(sp1) %*% (beetle1.means - beetle2.means)
a
```

    ##                                    [,1]
    ## transverse.groove.dist        0.3452490
    ## elytra.length                -0.1303878
    ## second.antennal.joint.length -0.1064338
    ## third.antennal.joint.length  -0.1433533

The output of which gives us the linear discriminant function coefficients. However, as noted earlier, the data is not commensurate and therefore needs to be scaled to provide any meaningful interpretation. The linear discriminant analysis coefficients can be standardized by $diag(S_{p1})^{1/2}a$.

``` r
diag(sp1)^(1/2) * a
```

    ##                                   [,1]
    ## transverse.groove.dist        4.136640
    ## elytra.length                -2.500550
    ## second.antennal.joint.length -1.157705
    ## third.antennal.joint.length  -2.067833

Which gives us the following discriminant function:

$$ z = 4.137y_1 − 2.501y_2 − 1.158y_3 − 2.068y_4 $$

The interpretation of the discriminant function can be made in several ways. The most simple is to rank the absolute value of the coefficients and determine contribution based on the order of the coefficients. Another method is to perform a partial F-test to find the significance of the variables.

Judging from our discriminant function, it appears the first measurement is the most significant while the second and third measurements have similar contribution to group separation.

The [MASS package](https://cran.r-project.org/web/packages/MASS/index.html) contains the function `lda()` for performing linear discriminant analysis.

``` r
library(MASS)
```

    ## 
    ## Attaching package: 'MASS'

    ## The following object is masked from 'package:dplyr':
    ## 
    ##     select

The `lda()` function takes a formula argument.

``` r
beet.lda <- lda(Species ~ .-Measurement.Number, data = beetles)
beet.lda$scaling
```

    ##                                      LD1
    ## transverse.groove.dist       -0.09327642
    ## elytra.length                 0.03522706
    ## second.antennal.joint.length  0.02875538
    ## third.antennal.joint.length   0.03872998

Note the discriminant function coefficients are different than what we computed earlier. This difference is due to another scaling method employed by the `lda()` function. Since any multiple of $a$ can be taken as the maximum vector, either vector would suffice as the solution. We can see the coefficients are scaled differently than the $a$ vector we found earlier. Despite this difference in scaling, output of the `lda()` function would still provide the same interpretation of the coefficients if they were ordered by their absolute values.

``` r
beet.lda$scaling / a
```

    ##                                     LD1
    ## transverse.groove.dist       -0.2701715
    ## elytra.length                -0.2701715
    ## second.antennal.joint.length -0.2701715
    ## third.antennal.joint.length  -0.2701715

The group separation can be plotted by using the `plot()` function from the MASS package. Note since we are only concerned with one discriminant function the plot will be a histogram rather than a scatterplot.

``` r
plot(beet.lda)
```

![](figure/discriminant_analysis/group_separation.png)

Summary
-------

This post explored the objective of group separation using discriminant function analysis. By performing and interpreting a discriminant analysis function, one can get a better sense of what contributes the most distinction between the sample groups. As we will see in future posts, the discriminant function can also be used to classify and predict future observations.

References
----------

Rencher, A. (n.d.). Methods of Multivariate Analysis (2nd ed.). Brigham Young University: John Wiley & Sons, Inc.
