Title: Linear Discriminant Analysis for the Classification of Two Groups 
Date: 2018-08-24
Tags: R, linear algebra, classification, linear discriminant analysis
Category: Linear Algebra
Slug: linear-discriminant-analysis-classification-two-groups
Author: Aaron Schlegel
Summary: In this post, we will use the discriminant functions found in the first post to classify the observations. We will also employ cross-validation on the predicted groups to get a realistic sense of how the model would perform in practice on new observations. Linear classification analysis assumes the populations have equal covariance matrices ($\Sigma_1 = \Sigma_2$) but does not assume the data are normally distributed.

The second objective of linear discriminant analysis is the classification of observations. A previous post explored the [descriptive aspect of linear discriminant analysis](http://wp.me/p4aZEo-5Os) with data collected on two groups of beetles. In this post, we will use the discriminant functions found in the first post to classify the observations. We will also employ cross-validation on the predicted groups to get a realistic sense of how the model would perform in practice on new observations. Linear classification analysis assumes the populations have equal covariance matrices ($\Sigma_1 = \Sigma_2$) but does not assume the data are normally distributed.

Classification with Linear Discriminant Analysis
------------------------------------------------

The classification portion of LDA can be employed after calculating $\bar{y}_1, \bar{y}_2$ and $S_{p1}$. The procedure for classifying observations is based on the discriminant functions:

$$ z = a'y = (\bar{y}_1 - \bar{y}_2)'S_{p1}^{-1}y $$

$y$ is the vector of measurements to be classified. The discriminant functions $z_1$ and $z_2$ for the two groups are used to determine to which group the observation vector belongs. The classification procedure assigns the observation vector $y$ to group 1 if its discriminant function $z = a′y$ is closer to $z_1$ or group 2 if its discriminant function is closer to $z$.

$$ z > \frac{1}{2}(\bar{z}_1 + \bar{z}_2) $$

We can now express the classification function regarding the observation vector $y$.

$$ \frac{1}{2}(\bar{z}_1 + \bar{z}_2) = \frac{1}{2}(\bar{y}_1 - \bar{y}_2)'S_{p1}^{-1}(\bar{y}_1 + \bar{y}_2) $$

Thus the observation vector $y$ is assigned to a group determined by the following:

Assign $y$ to group 1 if:
$$ a'y = (\bar{y}_1 - \bar{y}_2)'S_{p1}y > \frac{1}{2}(\bar{y}_1 - \bar{y}_2)'S_{p1}^{-1}(\bar{y}_1 + \bar{y}_2) $$

Or assign $y$ to group 2 if:
$$ a'y = (\bar{y}_1 - \bar{y}_2)'S_{p1}y < \frac{1}{2}(\bar{y}_1 - \bar{y}_2)'S_{p1}^{-1}(\bar{y}_1 + \bar{y}_2) $$

This classification rule is where the discriminant function comes into play. Note the discriminant function acts as a linear classification function only in the two-group case.

Classification with Linear Discriminant Analysis in R
-----------------------------------------------------

The following steps should be familiar from the discriminant function post. We first calculate the group means $\bar{y}_1$ and $\bar{y}_2$ and the pooled sample variance $S_{p1}$. The beetle data were obtained from the [companion FTP site](ftp://ftp.wiley.com) of the book Methods of Multivariate Analysis by Alvin Rencher.

``` r
beetles <- read.table('BEETLES.DAT', col.names = c('Measurement.Number', 'Species', 'transverse.groove.dist', 'elytra.length', 'second.antennal.joint.length', 'third.antennal.joint.length'))
```

Find the group means and the pooled sample variance.

``` r
beetle1 <- beetles[beetles$Species == 1,][,3:6]
beetle2 <- beetles[beetles$Species == 2,][,3:6]

n1 <- nrow(beetle1)
n2 <- nrow(beetle2)

beetle1.means <- apply(beetle1, 2, mean)
beetle2.means <- apply(beetle2, 2, mean)

w1 <- (n1 - 1) * var(beetle1)
w2 <- (n2 - 1) * var(beetle2)

sp1 <- 1 / (n1 + n2 - 2) * (w1 + w2)
```

The cutoff point to determine group membership of the observation vector is then found.

``` r
cutoff <- .5 * (beetle1.means - beetle2.means) %*% solve(sp1) %*% (beetle1.means + beetle2.means)
cutoff
```

    ##           [,1]
    ## [1,] -15.80538

Thus if $z$ is greater than −15.81, the observation is assigned to group 1. Otherwise, it is assigned to group 2. We can apply the computed discriminant functions to the beetle data already collected to determine how well it performs in classifying observations.

``` r
species.prediction <- apply(beetles[,3:6], 1, function(y) {
  z <- (beetle1.means - beetle2.means) %*% solve(sp1) %*% y # Calculate the discriminate function for the observation vector y
  ifelse(z > cutoff, 1, 2)
})
```

Print a confusion matrix to display how the observations were assigned compared to their actual groups.

``` r
table(beetles$Species, species.prediction, dnn = c('Actual Group','Predicted Group'))
```

    ##             Predicted Group
    ## Actual Group  1  2
    ##            1 19  0
    ##            2  1 19

Our predictions classified all of group 1's observations correctly but incorrectly assigned a group 2 observation to group 1. The error rate is simply the number of misclassifications divided by the total sample size.

``` r
n <- dim(beetles)[1]
1 / n
```

    ## [1] 0.02564103

Thus our predictions were rather close to actual with only a 2.6% error rate. However, predictions tend to be rather optimistic when sample sizes are small, as in this case. Therefore, we will also perform leave-one-out cross-validation to find a more realistic error rate.

The `lda()` function from the [MASS package](https://cran.r-project.org/web/packages/MASS/index.html) can also be used to make predictions on the supplied data or a new data set.

``` r
library(MASS)
```

The `predict()` function accepts a lda object.

``` r
beetle.lda <- lda(Species ~ .-Measurement.Number, data = beetles)
lda.pred <- predict(beetle.lda)$class
```

As before, print a confusion matrix to display the results of the predictions compared to the actual group memberships.

``` r
table(beetles$Species, lda.pred, dnn = c('Actual Group','Predicted Group'))
```

    ##             Predicted Group
    ## Actual Group  1  2
    ##            1 19  0
    ##            2  1 19

Cross-Validation of Predicted Groups
------------------------------------

As mentioned previously, in cases with small sample sizes, prediction error rates can tend to be optimistic. [Cross-validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics)) is a technique used to estimate how accurate a predictive model may be in actual practice. When larger sample sizes are available, the more common approach of splitting the data into test and training sets may still be employed. There are many different approaches to cross-validation, including [leave-p-out](https://en.wikipedia.org/wiki/Cross-validation_(statistics)#Leave-p-out_cross-validation) and [k-fold](https://en.wikipedia.org/wiki/Cross-validation_(statistics)#k-fold_cross-validation) cross-validation. One particular case of leave-p-out cross-validation is the leave-one-out approach, also known as the holdout method.

Leave-one-out cross-validation is performed by using all but one of the sample observation vectors to determine the classification function and then using that classification function to predict the omitted observation's group membership. The procedure is repeated for each observation so that each is classified by a function of the other observations. The leave-one-out technique is demonstrated on the beetle data below. The approach to building the discriminant and classification functions remain the same as before, with the exception that all but $N − 1$ observations are used.

``` r
cv.prediction <- c()

for (i in 1:n) {
  holdout <- beetles[-i,]
  
  holdout1 <- holdout[holdout$Species == 1,][,3:6]
  holdout2 <- holdout[holdout$Species == 2,][,3:6]
  
  holdout1.means <- apply(holdout1, 2, mean)
  holdout2.means <- apply(holdout2, 2, mean)
  
  n1 <- nrow(holdout1)
  n2 <- nrow(holdout2)

  w1 <- (n1 - 1) * var(holdout1)
  w2 <- (n2 - 1) * var(holdout2)

  sp1 <- 1 / (n1 + n2 - 2) * (w1 + w2)

  cutoff <- .5 * (holdout1.means - holdout2.means) %*% solve(sp1) %*% (holdout1.means + holdout2.means)
  
  ay <- (holdout1.means - holdout2.means) %*% solve(sp1) %*% as.numeric(beetles[i,3:6])
  group <- ifelse(ay > cutoff, 1, 2)
  cv.prediction <- append(cv.prediction, group)
}
```

Construct a confusion matrix to display how the observations were classified.

``` r
table(beetles$Species, cv.prediction, dnn = c('Actual Group','Predicted Group'))
```

    ##             Predicted Group
    ## Actual Group  1  2
    ##            1 19  0
    ##            2  3 17

As before, all of group 1's observations were correctly classified; however, three of group 2's observations were incorrectly assigned to group 1. Although the cross-validated error rate has increased three times to about 7.7%, it is a more realistic estimate compared to the non-cross-validated result.

Cross-validation is also available in the `lda()` function with the `cv` argument.

``` r
beetle.cv <- lda(Species ~ .-Measurement.Number, CV=TRUE, data = beetles)

table(beetles$Species, beetle.cv$class, dnn = c('Actual Group','Predicted Group'))
```

    ##             Predicted Group
    ## Actual Group  1  2
    ##            1 19  0
    ##            2  3 17

Summary
-------

This post explored the predictive aspect of linear discriminant analysis as well as a brief introduction to cross-validation through the leave-one-out method. As noted, it is often important to perform some form of cross-validation on datasets with few observations to get a more realistic indication of how accurate the model will be in practice. Future posts will examine classification with linear discriminant analysis for more than two groups as well as quadratic discriminant analysis.

References
----------

[Rencher, A. C. (2002). Methods of multivariate analysis. New York: J. Wiley.](https://amzn.to/39gsldt)
