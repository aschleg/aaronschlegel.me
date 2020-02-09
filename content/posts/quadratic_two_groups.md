Title: Quadratic Discriminant Analysis of Two Groups
Date: 2018-08-31
Tags: R, linear algebra, matrix decomposition
Category: Linear Algebra
Slug: quadratic-discriminant-analysis-two-groups
Author: Aaron Schlegel
Summary: LDA assumes the groups in question have equal covariance matrices ($\Sigma_1 = \Sigma_2 = \cdots = \Sigma_k$). Therefore, when the groups do not have equal covariance matrices, observations are frequently assigned to groups with large variances on the diagonal of its corresponding covariance matrix (Rencher, n.d., pp. 321). Quadratic discriminant analysis is a modification of LDA that does not assume equal covariance matrices amongst the groups. In quadratic discriminant analysis, the respective covariance matrix $S_i$ of the $i^{th}$ group is employed in predicting the group membership of an observation, rather than the pooled covariance matrix $S_{p1}$ in linear discriminant analysis.


As mentioned in the post on classification with linear discriminant analysis, LDA assumes the groups in question have equal covariance matrices ($\Sigma_1 = \Sigma_2 = \cdots = \Sigma_k$). Therefore, when the groups do not have equal covariance matrices, observations are frequently assigned to groups with large variances on the diagonal of its corresponding covariance matrix (Rencher, n.d., pp. 321). Quadratic discriminant analysis is a modification of LDA that does not assume equal covariance matrices amongst the groups. In quadratic discriminant analysis, the respective covariance matrix $S_i$ of the $i^{th}$ group is employed in predicting the group membership of an observation, rather than the pooled covariance matrix $S_{p1}$ in linear discriminant analysis. The classification function in QDA is, therefore:

$$ D_i^2(y) = (y - \bar{y}_i)'S_i^{-1}(y - \bar{y}_i), \qquad i = 1, 2, \cdots, k $$

As in LDA, the observation *y* is assigned to the group for which $D_i^2(y)$ is smallest.

One caveat to quadratic discriminant analysis is each group's sample size $n_i$ must be greater than the number of dependent variables $p$.

Quadratic Discriminant Analysis in R
------------------------------------

The beetles data, obtained from the [companion FTP site](ftp://ftp.wiley.com) of the book Methods of Multivariate Analysis by Alvin Rencher, will be analyzed by quadratic discriminant analysis.

``` r
beetles <- read.table('BEETLES.DAT', col.names = c('Measurement.Number', 'Species', 'transverse.groove.dist', 'elytra.length', 'second.antennal.joint.length', 'third.antennal.joint.length'))

head(beetles)
```

    ##   Measurement.Number Species transverse.groove.dist elytra.length
    ## 1                  1       1                    189           245
    ## 2                  2       1                    192           260
    ## 3                  3       1                    217           276
    ## 4                  4       1                    221           299
    ## 5                  5       1                    171           239
    ## 6                  6       1                    192           262
    ##   second.antennal.joint.length third.antennal.joint.length
    ## 1                          137                         163
    ## 2                          132                         217
    ## 3                          141                         192
    ## 4                          142                         213
    ## 5                          128                         158
    ## 6                          147                         173

The following function implements quadratic discriminant analysis to predict the group membership of the beetle observations. The function computes the group means and covariance matrices and then calculates $D_i^2(y)$, as shown above, and outputs the predicted group, confusion matrix, and error rate.

``` r
two.group.quadratic.classification <- function(data, grouping, newdata) {
  dat.split <- split(data, grouping)
  g1 <- as.data.frame(dat.split[1])
  g2 <- as.data.frame(dat.split[2])
  g1.means <- apply(g1, 2, mean)
  g2.means <- apply(g2, 2, mean)
  g1.covar <- cov(g1)
  g2.covar <- cov(g2)
  
  prediction <- apply(newdata, 1, function(y) {
    d2.y1 <- (y - g1.means) %*% solve(g1.covar) %*% (y - g1.means)
    d2.y2 <- (y - g2.means) %*% solve(g2.covar) %*% (y - g2.means)
    ifelse(d2.y1^2 > d2.y2^2, 2, 1)
  })
  
  class.table <- table(grouping, prediction, dnn = c('Actual Group','Predicted Group'))
  pred.errors <- sum(diag(t(apply(class.table, 2, rev)))) / dim(data)[1]
  results <- list('Prediction'=prediction, 'Table of Predictions'=class.table, 'Error Rate'=pred.errors)
  
  return(results)
}
```

Run the function with the observed data as the `newdata` argument.

``` r
beetle.quad <- two.group.quadratic.classification(beetles[,3:6], beetles[,2], beetles[,3:6])
beetle.quad
```

    ## $Prediction
    ##  [1] 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2
    ## [36] 2 2 2 2
    ## 
    ## $`Table of Predictions`
    ##             Predicted Group
    ## Actual Group  1  2
    ##            1 19  0
    ##            2  1 19
    ## 
    ## $`Error Rate`
    ## [1] 0.02564103

The [Mass package](https://cran.r-project.org/web/packages/MASS/index.html) also supplies the `qda()` function to perform quadratic discriminant analysis.

``` r
library(MASS)
```

Similar to the `lda()` function in the `MASS` package, the `qda()` function takes a formula argument.

``` r
beetle.qda <- qda(Species ~.-Measurement.Number, data = beetles)

qda.pred <- predict(beetle.qda)$class
qda.pred
```

    ##  [1] 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2
    ## [36] 2 2 2 2
    ## Levels: 1 2

``` r
table(beetles$Species, qda.pred, dnn = c('Actual Group','Predicted Group'))
```

    ##             Predicted Group
    ## Actual Group  1  2
    ##            1 19  0
    ##            2  1 19

Quadratic discriminant analysis predicted the same group membership as LDA. As noted in the previous post on linear discriminant analysis, predictions with small sample sizes, as in this case, tend to be rather optimistic and it is therefore recommended to perform some form of cross-validation on the predictions to yield a more realistic model to employ in practice.

Cross-Validation of Quadratic Discriminant Analysis Classifications
-------------------------------------------------------------------

As before, we will use [leave-one-out cross-validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics)#Leave-one-out_cross-validation) to find a more realistic and less optimistic model for classifying observations in practice. Leave-one-out cross-validation is performed by using all but one of the sample observation vectors to determine the classification function and then using that classification function to predict the omitted observation's group membership. The procedure is repeated for each observation so that each is classified by a function of the other observations. The approach to building the quadratic discriminant functions remains the same as before, with the exception that all but $N − 1$ observations are used.

``` r
cv.prediction <- c()

for (i in 1:dim(beetles)[1]) {
  holdout <- beetles[-i,]
  y <- as.numeric(beetles[i,3:6])
  
  holdout1 <- holdout[holdout$Species == 1,][,3:6]
  holdout2 <- holdout[holdout$Species == 2,][,3:6]
  
  holdout1.means <- apply(holdout1, 2, mean)
  holdout2.means <- apply(holdout2, 2, mean)
  
  holdout1.covar <- cov(holdout1)
  holdout2.covar <- cov(holdout2)

  d2.y1 <- (y - holdout1.means) %*% solve(holdout1.covar) %*% (y - holdout1.means)
  d2.y2 <- (y - holdout2.means) %*% solve(holdout2.covar) %*% (y - holdout2.means)
  
  group <- ifelse(d2.y1^2 > d2.y2^2, 2, 1)
  cv.prediction <- append(cv.prediction, group)
}

table(beetles$Species, cv.prediction, dnn = c('Actual Group','Predicted Group'))
```

    ##             Predicted Group
    ## Actual Group  1  2
    ##            1 17  2
    ##            2  2 18

The cross-validated results show two misclassified observations for each group, giving an error rate of approximately 10.3%. This error rate is slightly higher than the 7.7% error rate we found with cross-validated linear discriminant classifications. One could potentially test both models on new observations to determine their predictive power; however, as quadratic discriminant analysis makes fewer assumptions regarding the data and involves more parameters, it is likely that model would be more realistic in classifying observations.

Cross-validation can also be done with the `qda()` function with the `CV` argument set to `TRUE`.

``` r
beetle.qda.cv <- qda(Species ~.-Measurement.Number, CV = TRUE, data = beetles)
table(beetles$Species, beetle.qda.cv$class, dnn = c('Actual Group','Predicted Group'))
```

    ##             Predicted Group
    ## Actual Group  1  2
    ##            1 17  2
    ##            2  2 18

The cross-validated results from the `qda()` function agree with our results.

References
----------

[Rencher, A. C. (2002). Methods of multivariate analysis. New York: J. Wiley.](https://amzn.to/39gsldt)
