Title: Linear Discriminant Analysis for the Classification of Several Groups
Date: 2018-08-28
Tags: R, linear algebra, classification, linear discriminant analysis
Category: Linear Algebra
Slug: linear-discriminant-analysis-classification-several-groups
Author: Aaron Schlegel
Summary: Similar to the two-group linear discriminant analysis for classification case, LDA for classification into several groups seeks to find the mean vector that the new observation $y$ is closest to and assign $y$ accordingly using a distance function. The several group case also assumes equal covariance matrices amongst the groups ($\Sigma_1 = \Sigma_2 = \cdots = \Sigma_k$).

Similar to the two-group linear discriminant analysis for classification case, LDA for classification into several groups seeks to find the mean vector that the new observation $y$ is closest to and assign $y$ accordingly using a distance function. The several group case also assumes equal covariance matrices amongst the groups ($\Sigma_1 = \Sigma_2 = \cdots = \Sigma_k$).

LDA for Classification into Several Groups
------------------------------------------

As in the two-group case, the common population covariance matrix S_{p1}$ must be estimated:

$$ S_{p1} = \frac{1}{N - k} \sum_{i=1}^k (n_i - 1)S_i = \frac{E}{N - k} $$

Where $n_i$ and $S_i$ are the sample size and covariance matrix of the $i^{th}$ group, $E$ is the error matrix as seen in one-way MANOVA and $N$ is the total sample size. The observation vector to be classified $y$ is then compared to each mean vector $\bar{y}_i, i = 1, 2, \cdots, k$ using the following distance function:

$$ D_i^2(y) = (y - \bar{y}_i)'S_{p1}^{-1}(y - \bar{y}_i) $$

The above distance function is then expanded, and the resulting unnecessary terms are dropped to obtain a linear classification function for several groups denoted by $L_i(y)$.

$$ L_i(y) = \bar{y}_i S_{p1}^{-1}y - \frac{1}{2} \bar{y}_i S_{p1}^{-1}\bar{y}_i \qquad i = 1, 2, \cdots, k $$

Thus the observation vector $y$ is assigned to the group that maximizes $L_i(y)$.

LDA for Several Group Classification in R
-----------------------------------------

We will classify observations from the rootstock data to demonstrate LDA for classification into several groups. The rootstock data were obtained from the [companion FTP site](ftp://ftp.wiley.com) of the book Methods of Multivariate Analysis by Alvin Rencher.

``` r
root <- read.table('ROOT.DAT', col.names = c('Tree.Number', 'Trunk.Girth.4.Years', 'Ext.Growth.4.Years', 'Trunk.Girth.15.Years', 'Weight.Above.Ground.15.Years'))
```

``` r
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

Split the data by the groups and calculate the group mean vectors.

``` r
root.group <- split(root[,2:5], root$Tree.Number)

root.means <- sapply(root.group, function(x) {
  apply(x, 2, mean)
}, simplify = 'data.frame')
```

Compute the error matrix $E$ and the pooled sample covariance matrix $S_{p1}$.

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

N <- dim(root)[1]
k <- length(unique(root$Tree.Number))
sp1 <- E / (N - k)
```

$L_i(y)$ is then computed for each observation in the rootstock dataset.

``` r
li.y <- apply(root[,2:5], 1, function(y) {
  sapply(root.group, function(x) {
    y.bar <- as.numeric(apply(x, 2, mean))
    y.bar %*% solve(sp1) %*% y - .5 * y.bar %*% solve(sp1) %*% y.bar
  }, simplify = 'data.frame')
})
```

The last step is to find the group that maximized the value of $L_i(y)$ for each observation.

``` r
root.prediction <- apply(t(li.y), 1, function(x) {
  which(x==max(x))
})
```

Print the classifications and the actual groups for comparison as well as a confusion matrix.

``` r
root.prediction
```

    ##  [1] 1 1 6 1 1 6 4 1 5 4 3 2 5 2 3 2 4 3 5 3 3 3 3 3 1 3 1 4 1 4 4 4 5 3 2
    ## [36] 5 6 2 5 2 6 6 6 5 6 1 1 5

``` r
root$Tree.Number
```

    ##  [1] 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 4 4 4 4 4 4 4 4 5 5 5
    ## [36] 5 5 5 5 5 6 6 6 6 6 6 6 6

``` r
table(root$Tree.Number, root.prediction, dnn = c('Actual Group','Predicted Group'))
```

    ##             Predicted Group
    ## Actual Group 1 2 3 4 5 6
    ##            1 5 0 0 1 0 2
    ##            2 0 3 2 1 2 0
    ##            3 0 0 6 1 1 0
    ##            4 3 0 1 4 0 0
    ##            5 0 3 1 0 3 1
    ##            6 2 0 0 0 2 4

It appears the classification function had decent success classifying observations in groups 1, 3, 4 and six but was less accurate in identifying observations belonging to the other groups.

Count the number of accurate classifications.

``` r
sum(root.prediction == root$Tree.Number)
```

    ## [1] 25

25 accurate classifications out of a total sample size of 48 give an error rate of 48%. We will see later in this post if cross-validation can improve the misclassification rate.

The function `lda()` available in the [MASS package](https://cran.r-project.org/web/packages/MASS/index.html) also performs classification into several groups.

``` r
library(MASS)
```

``` r
root.lda <- lda(Tree.Number ~ ., data = root)
lda.pred <- predict(root.lda)$class
table(root$Tree.Number, lda.pred, dnn = c('Actual Group','Predicted Group'))
```

    ##             Predicted Group
    ## Actual Group 1 2 3 4 5 6
    ##            1 5 0 0 1 0 2
    ##            2 0 3 2 1 2 0
    ##            3 0 0 6 1 1 0
    ##            4 3 0 1 4 0 0
    ##            5 0 3 1 0 3 1
    ##            6 2 0 0 0 2 4

Cross-Validation of Classifications
-----------------------------------

[Leave-one-out cross-validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics)#Leave-one-out_cross-validation) is employed on the rootstock dataset in the following code in hopes of finding a more accurate, as well as realistic, model for classifying new and unknown observations. Leave-one-out cross-validation is performed by using all but one of the sample observation vectors to determine the classification function and then using that classification function to predict the omitted observation's group membership. The procedure is repeated for each observation so that each is classified by a function of the other observations.

``` r
cv.prediction <- c()

for (r in 1:N) {

  holdout <- root[-r,]
  root.group <- split(holdout[,2:5], holdout$Tree.Number)

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
  
  sp1 <- E / (dim(holdout)[1] - length(unique(holdout$Tree.Number)))
  
  li <- sapply(root.group, function(x) {
    y.bar <- as.numeric(apply(x, 2, mean))
    y.bar %*% solve(sp1) %*% as.numeric(root[r,2:5]) - .5 * y.bar %*% solve(sp1) %*% y.bar
  }, simplify = 'data.frame')

  li.y <- apply(t(li), 1, function(y) {
    which(y == max(y))
  })

  cv.prediction <- append(cv.prediction, li.y)
}
```

``` r
table(root$Tree.Number, cv.prediction, dnn = c('Actual Group','Predicted Group'))
```

    ##             Predicted Group
    ## Actual Group 1 2 3 4 5 6
    ##            1 5 0 0 1 0 2
    ##            2 0 2 2 1 3 0
    ##            3 0 0 6 1 1 0
    ##            4 4 0 1 3 0 0
    ##            5 0 3 2 0 2 1
    ##            6 3 0 0 0 2 3

``` r
sum(cv.prediction == root$Tree.Number)
```

    ## [1] 21

The cross-validated results have a higher misclassification rate of 56%, which could be expected given the total sample size may yield a more optimistic and biased classification model without cross-validation. Though the misclassification rate may seem high in absolute terms, it is still much more accurate than simply guessing the observation's group membership, which would have an error rate of 83% $(1 - \frac{1}{6})$.

The `lda()` function also performs cross-validation with the `CV` argument set to `TRUE`.

``` r
root.cv <- lda(Tree.Number ~ ., CV = TRUE, data = root)
root.cv$class
```

    ##  [1] 1 1 6 1 1 6 4 1 5 4 3 2 5 5 3 2 4 3 5 3 3 3 3 3 1 3 1 4 1 4 4 1 5 3 2
    ## [36] 5 6 2 3 2 1 6 6 5 6 1 1 5
    ## Levels: 1 2 3 4 5 6

``` r
table(root$Tree.Number, root.cv$class, dnn = c('Actual Group','Predicted Group'))
```

    ##             Predicted Group
    ## Actual Group 1 2 3 4 5 6
    ##            1 5 0 0 1 0 2
    ##            2 0 2 2 1 3 0
    ##            3 0 0 6 1 1 0
    ##            4 4 0 1 3 0 0
    ##            5 0 3 2 0 2 1
    ##            6 3 0 0 0 2 3

References
----------

Rencher, A. (n.d.). Methods of Multivariate Analysis (2nd ed.). Brigham Young University: John Wiley & Sons, Inc.
