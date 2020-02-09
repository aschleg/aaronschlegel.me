Title: Quadratic Discriminant Analysis of Several Groups
Date: 2018-09-03
Tags: R, linear algebra, matrix decomposition
Category: Linear Algebra
Slug: quadratic-discriminant-analysis-several-groups
Author: Aaron Schlegel
Summary: Quadratic discriminant analysis for classification is a modification of linear discriminant analysis that does not assume equal covariance matrices amongst the groups ($\Sigma_1, \Sigma_2, \cdots, \Sigma_k$). Similar to LDA for several groups, quadratic discriminant analysis for several groups classification seeks to find the group that maximizes the quadratic classification function and assign the observation vector $y$ to that group.

Quadratic discriminant analysis for classification is a modification of linear discriminant analysis that does not assume equal covariance matrices amongst the groups ($\Sigma_1, \Sigma_2, \cdots, \Sigma_k$). Similar to LDA for several groups, quadratic discriminant analysis for several groups classification seeks to find the group that maximizes the quadratic classification function and assign the observation vector $y$ to that group.

As noted in a previous post on quadratic discriminant analysis of two groups, QDA employs the group covariance matrix $S_i$ rather than the pooled covariance matrix $S_{p1}$. In the several group case, the prior probabilities $p_1, p_2, \cdots, p_k$ are also used in the quadratic classification function. If the prior probabilities of the groups are unknown, it is set to $p_i = n_i/N$.

The quadratic classification function is:

$$ Q_i(y) = -\frac{1}{2} ln \left|\Sigma_k \right| - \frac{1}{2}(y - \mu_k)^T \Sigma_k^{-1} (y - u_k) + ln \pi_k $$

The observation vector $y$ is assigned to the group which maximizes the function.

Quadratic Discriminant Analysis of Several Groups
-------------------------------------------------

The rootstock data from previous posts will be classified using quadratic discriminant analysis. The rootstock data were obtained from the [companion FTP site](ftp://ftp.wiley.com) of the book Methods of Multivariate Analysis by Alvin Rencher. The data contains four dependent variables as follows:

-   trunk girth at four years (mm × 100)
-   extension growth at four years (m)
-   trunk girth at 15 years (mm × 100)
-   weight of tree above ground at 15 years (lb × 1000)

Load the data and inspect the first few rows.

``` r
root <- read.table('ROOT.DAT', col.names = c('Tree.Number', 'Trunk.Girth.4.Years', 'Ext.Growth.4.Years', 'Trunk.Girth.15.Years', 'Weight.Above.Ground.15.Years'))

head(root)
```

    ##   Tree.Number Trunk.Girth.4.Years Ext.Growth.4.Years Trunk.Girth.15.Years
    ## 1           1                1.11              2.569                 3.58
    ## 2           1                1.19              2.928                 3.75
    ## 3           1                1.09              2.865                 3.93
    ## 4           1                1.25              3.844                 3.94
    ## 5           1                1.11              3.027                 3.60
    ## 6           1                1.08              2.336                 3.51
    ##   Weight.Above.Ground.15.Years
    ## 1                        0.760
    ## 2                        0.821
    ## 3                        0.928
    ## 4                        1.009
    ## 5                        0.766
    ## 6                        0.726

Before classifying the observations in the data first split the data into groups using the `split()` function. The groups' covariance matrix and mean vectors are then found.

``` r
root.group <- split(root[,2:5], root$Tree.Number)
Si <- lapply(root.group, function(x) cov(x))

root.means <- lapply(root.group, function(x) {
  c(apply(x, 2, mean))
})
```

The following loop performs quadratic discriminant analysis for several groups. For each observation vector $y$ in the data, the classification function above is calculated for each group. The group that maximizes the function is the predicted group the observation vector belongs and is thus appended to the `l2i.y` object.

``` r
l2i.y <- c() # Initialize the vector to store the classified results
for (i in 1:dim(root)[1]) {
  
  y <- root[i,2:5] # Get the observation vector y
  l2i <- c()
  
  for (j in 1:length(Si)) { # For each group, calculate the QDA function. 
    y.bar <- unlist(root.means[j])
    Si.j <- matrix(unlist(Si[j]), 4, byrow = TRUE)
    l2i <- append(l2i, -.5 * log(det(Si.j)) - .5 * as.numeric(y - y.bar) %*% solve(Si.j) %*% as.numeric(y - y.bar) + log(1/length(Si)))
  }
  
  l2i.y <- append(l2i.y, which.max(l2i)) # Append the group number which maximizes the function
}
```

Print a confusion matrix of the results compared to the actual groups.

``` r
table(root$Tree.Number, l2i.y, dnn = c('Actual Group','Predicted Group'))
```

    ##             Predicted Group
    ## Actual Group 1 2 3 4 5 6
    ##            1 8 0 0 0 0 0
    ##            2 0 7 0 1 0 0
    ##            3 1 0 6 0 1 0
    ##            4 0 0 1 7 0 0
    ##            5 0 3 0 0 4 1
    ##            6 2 0 0 0 1 5

It appears QDA was rather accurate in classifying observations, particularly in groups one through four. Count the number of successful classifications divided by the total sample size to get the error rate.

``` r
1 - sum(l2i.y == root$Tree.Number) / dim(root)[1]
```

    ## [1] 0.2291667

Out of 48 observations, the quadratic classification function correctly assigned 37 to their correct groups, giving an error rate of only 23%. This result seems quite optimistic and would likely not be as accurate in classifying new observations. We will perform cross-validation with QDA shortly in hopes of obtaining a more realistic model to use on new observations.

First, verify our results using the `qda()` function from the [MASS package](https://cran.r-project.org/web/packages/MASS/index.html).

``` r
library(MASS)
```

``` r
root.qda <- qda(Tree.Number ~ ., data = root)
root.qda
```

    ## Call:
    ## qda(Tree.Number ~ ., data = root)
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

``` r
predict(root.qda)$class
```

    ##  [1] 1 1 1 1 1 1 1 1 2 4 2 2 2 2 2 2 1 3 5 3 3 3 3 3 4 4 3 4 4 4 4 4 5 2 5
    ## [36] 5 6 2 5 2 1 6 6 6 6 6 1 5
    ## Levels: 1 2 3 4 5 6

Construct a confusion matrix with the results from the `qda()` function.

``` r
table(root$Tree.Number, predict(root.qda)$class, dnn = c('Actual Group','Predicted Group'))
```

    ##             Predicted Group
    ## Actual Group 1 2 3 4 5 6
    ##            1 8 0 0 0 0 0
    ##            2 0 7 0 1 0 0
    ##            3 1 0 6 0 1 0
    ##            4 0 0 1 7 0 0
    ##            5 0 3 0 0 4 1
    ##            6 2 0 0 0 1 5

The error rate of the `qda()` function also agrees with ours.

``` r
1 - sum(predict(root.qda)$class == root$Tree.Number) / dim(root)[1]
```

    ## [1] 0.2291667

Cross-Validation of Quadratic Discriminant Analysis of Several Groups
---------------------------------------------------------------------

As we've seen previously, cross-validation of classifications often leaves a higher misclassification rate but is typically more realistic in its application to new observations. As the rootstock data contains only eight observations for each group, it is likely the cross-validated model will have a much higher error rate than what was found earlier in the post.

The following code performs [leave-one-out cross-validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics)#Leave-one-out_cross-validation) with quadratic discriminant analysis. Leave-one-out cross-validation is performed by using all but one of the sample observation vectors to determine the classification function and then using that classification function to predict the omitted observation's group membership. The procedure is repeated for each observation so that each is classified by a function of the other observations.

``` r
l2i.y.cv <- c() # Vector to store classified results

for (r in 1:dim(root)[1]) {
  
  l2i <- c()
  
  holdout <- root[-r,] # The holdout group is all of the data except one observation
  
  # Split the data and calculate the covariance matrices and mean vectors of the groups
  root.group <- split(holdout[,2:5], holdout$Tree.Number)
  Si <- lapply(root.group, function(x) cov(x))

  root.means <- lapply(root.group, function(x) {
    c(apply(x, 2, mean))
  })

  y <- root[r,2:5] # The left out observation vector is stored in the variable y
  
  # Calculate the quadratic classification function using the y vector for each group to determine which maximizes the function
  for (j in 1:length(Si)) {
    y.bar <- unlist(root.means[j])
    Si.j <- matrix(unlist(Si[j]), 4, byrow = TRUE)
    l2i <- append(l2i, -.5 * log(det(Si.j)) - .5 * as.numeric(y - y.bar) %*% solve(Si.j) %*% as.numeric(y - y.bar) + log(1/length(Si)))
  }
  
  # The group that maximizes the classification function is stored in the initialized vector.
  l2i.y.cv <- append(l2i.y.cv, which.max(l2i))
}
```

Find the misclassification rate of the cross-validated results.

``` r
1 - sum(l2i.y.cv == root$Tree.Number) / dim(root)[1]
```

    ## [1] 0.6875

A 69% error rate is three times the rate we found with the non-cross-validated results above, which we expected due to the relatively small sample size of each group. The error rate is also higher than the 56% error rate found with the cross-validated linear discriminant analysis model. However, since quadratic discriminant analysis makes fewer assumptions regarding the groups and involves more parameters, it may be the recommended model for classifying new observations. The model is also more accurate than simply guessing group membership of observations, which would have an 83% error rate $(1 - \frac{1}{6})$.

The `qda()` function also performs cross-validation when the `CV` argument is `TRUE`.

``` r
root.qda.cv <- qda(Tree.Number ~ ., data = root, CV = TRUE)
root.qda.cv$class
```

    ##  [1] 1 6 5 4 4 6 4 1 5 4 4 2 5 2 2 6 1 3 5 3 3 2 3 2 2 3 3 3 6 1 4 4 5 2 2
    ## [36] 5 6 2 3 2 1 5 6 2 1 6 1 5
    ## Levels: 1 2 3 4 5 6

``` r
1 - sum(root.qda.cv$class == root$Tree.Number) / dim(root)[1]
```

    ## [1] 0.6875

References
----------

[Rencher, A. C. (2002). Methods of multivariate analysis. New York: J. Wiley.](https://amzn.to/39gsldt)

<https://onlinecourses.science.psu.edu/stat857/node/80>
