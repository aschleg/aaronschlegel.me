Title: Computing Working-Hotelling and Bonferroni Simultaneous Confidence Intervals
Date: 2018-06-01
Tags: R, statistics
Category: Statistics
Slug: computing-working-hotelling-bonferroni-simultaneous-confidence-intervals
Author: Aaron Schlegel
Summary: There are two procedures for forming simultaneous confidence intervals, the Working-Hotelling and Bonferroni procedures. Each estimates intervals of the mean response using a family confidence coefficient. The Working-Hotelling coefficient is defined by $W$ and Bonferroni $B$. In practice, it is recommended to perform both procedures to determine which results in a tighter interval. The Bonferroni method will be explored first.


In a previous post on multiple regression with two predictor variables, the relationship between the number of products and the distance traveled on total delivery time was examined in the [delivery dataset](https://vincentarelbundock.github.io/Rdatasets/doc/robustbase/delivery.html). Often there is a need to form confidence intervals for the parameters of a model to estimate the range in which the actual parameter supposedly lies (at a given level of confidence, which will hereby default to 95%). However, forming individual intervals for each parameter as discussed in an earlier post on simple regression confidence intervals does not lead to an overall 95 percent confidence that the estimates for each parameter are correct. For one regression parameter and the intercept, the confidence would actually be $.95^2 = .9025$. Therefore, to estimate a family of coefficients, the need for simulatenous confidence intervals arises. The essential difference between a family confidence coefficient and a statement confidence coefficient is the former indicates that the *entire* family of confidence intervals are correct assuming repeated sampling.

Simulatenous Confidence Intervals of Mean Response
--------------------------------------------------

There are two procedures for forming simultaneous confidence intervals, the Working-Hotelling and Bonferroni procedures. Each estimates intervals of the mean response using a family confidence coefficient. The Working-Hotelling coefficient is defined by $W$ and Bonferroni $B$. In practice, it is recommended to perform both procedures to determine which results in a tighter interval. The Bonferroni method will be explored first.

The Bonferroni Procedure for Simultaneous Estimation of Mean Responses
----------------------------------------------------------------------

The Bonferroni method is more general and conservative than Working-Hotelling. Confidence intervals are formed by adjusting each confidence coefficient to be higher than 1 − $\alpha$ so the overall family confidence coefficient stays at the desired level. The confidence limits of the Bonferroni procedure are defined as:

$$ \hat{Y}_h \pm Bs{\hat{Y}_h} $$

Where $\hat{Y}_h$ is equal to the matrix of the fitted response values and B is defined as:

$$ B = t_{1 − \frac{\alpha}{2g}, n − 2} $$

Working-Hotelling Procedure for Simultaneous Confidence Intervals
-----------------------------------------------------------------

The Working-Hotelling procedure is reminiscent of the familiar confidence band around a regression line. The confidence band contains all of the regression line and thus all mean responses. Due to this property, boundary values can be formed at various levels of the predictor variable in question. The confidence interval equation for the Working-Hotelling procedure is similar to the Bonferroni procedure with the exception of the former being F-distributed with 2 and *n* − 2 degrees of freedom:

$$ \hat{Y}_h \pm Ws{\hat{Y}_h} $$

Where:

$$ W^2 = 2F_{1 − \alpha, 2, n − 2} $$

The standard error in both simulatenous confidence interval procedures is defined as:

$$ s^2 {\hat{Y}_h} = MSE(X'_h (X'X)^{-1}X_h) = X'_h s^2{b}X_h $$

Forming Simultaneous Confidence Intervals in R
----------------------------------------------

With the definitions and equations out of the way, we can explore how to build the simulatenous confidence intervals in R. The [investr](https://cran.r-project.org/web/packages/investr/) is the only package I've found that performs the Bonferroni and Working-Hotelling procedures. Of course, not being satisified with just using a package and calling it a day as I often am, we will build a custom function that creates intervals using both procedures to verify our understanding.

Start by loading the necessary packages and the `delivery` dataset.

``` r
library(robustbase)
library(investr)
library(ggplot2)
library(gridExtra)
data("delivery")
```

Fit linear models with each predictor variable.

``` r
dist.lm <- lm(delTime ~ distance, data = delivery)
prod.lm <- lm(delTime ~ n.prod, data = delivery)
```

Using the `plotFit` function from the `investr` package, plot the Bonferroni and Working-Hotelling confidence intervals. Setting the argument `adjust` to `Scheffe` instructs the function to build Working-Hotelling intervals.

``` r
par(mfrow=c(2,2))

plotFit(dist.lm, interval = 'confidence', adjust = 'Scheffe', main = 'Working-Hotelling DelTime ~ Distance')
plotFit(prod.lm, interval = 'confidence', adjust = 'Scheffe', main = 'Working-Hotelling DelTime ~ Products')

plotFit(dist.lm, interval = 'confidence', k = 0.95, adjust = 'Bonferroni', main = 'Bonferroni DelTime ~ Distance')
plotFit(prod.lm, interval = 'confidence', k = 0.95, adjust = 'Bonferroni', main = 'Bonferroni DelTime ~ Products')
```

![](working_hotelling_bonferroni_files/figure-markdown_github/unnamed-chunk-3-1.png)

It appears the Bonferroni intervals are tighter than the Working-Hotelling intervals, though there is no reported test statistic to confirm this. To verify the results of the function and our understanding, we can write a function that implements both the Working-Hotelling and Bonferroni simultaneous confidence intervals.

``` r
working.hotelling.bonferroni.intervals <- function(x, y) {
  y <- as.matrix(y)
  x <- as.matrix(x)
  n <- length(y)

  # Get the fitted values of the linear model
  fit <- lm(y ~ x)
  fit <- fit$fitted.values
  
  # Find standard error as defined above
  se <- sqrt(sum((y - fit)^2) / (n - 2)) * 
    sqrt(1 / n + (x - mean(x))^2 / 
           sum((x - mean(x))^2))

  # Calculate B and W statistics for both procedures.
  W <- sqrt(2 * qf(p = 0.95, df1 = 2, df2 = n - 2))
  B <- 1-qt(.95/(2 * 3), n - 1)

  # Compute the simultaneous confidence intervals
  
  # Working-Hotelling
  wh.upper <- fit + W * se
  wh.lower <- fit - W * se
  
  # Bonferroni
  bon.upper <- fit + B * se
  bon.lower <- fit - B * se
  
  xy <- data.frame(cbind(x,y))
  
  # Plot the Working-Hotelling intervals
  wh <- ggplot(xy, aes(x=x, y=y)) + 
    geom_point(size=2.5) + 
    geom_line(aes(y=fit, x=x), size=1) + 
    geom_line(aes(x=x, y=wh.upper), colour='blue', linetype='dashed', size=1) + 
    geom_line(aes(x=x, wh.lower), colour='blue', linetype='dashed', size=1) +
    labs(title='Working-Hotelling')
  
  # Plot the Bonferroni intervals
  bonn <- ggplot(xy, aes(x=x, y=y)) + 
    geom_point(size=2.5) + 
    geom_line(aes(y=fit, x=x), size=1) + 
    geom_line(aes(x=x, y=bon.upper), colour='blue', linetype='dashed', size=1) + 
    geom_line(aes(x=x, bon.lower), colour='blue', linetype='dashed', size=1) +
    labs(title='Bonferroni')
  
  grid.arrange(wh, bonn, ncol = 2)
  
  # Collect results of procedures into a data.frame and return
  res <- data.frame(round(cbind(W, B), 3), row.names = c('Result'))
  colnames(res) <- c('W', 'B')
  
  return(res)
}

working.hotelling.bonferroni.intervals(delivery$n.prod, delivery$delTime)
```

![](working_hotelling_bonferroni_files/figure-markdown_github/unnamed-chunk-4-1.png)

    ##            W     B
    ## Result 2.616 2.023

``` r
working.hotelling.bonferroni.intervals(delivery$distance, delivery$delTime)
```

![](working_hotelling_bonferroni_files/figure-markdown_github/unnamed-chunk-4-2.png)

    ##            W     B
    ## Result 2.616 2.023

The graphs from our function mirror those from the `plotFit` function. As we suspected, the Bonferroni intervals are indeed tighter as evidenced by a smaller *B* value compared to *W*. Thus, the Bonferroni intervals should be used in this particular case. Notice the *W* and *B* values are the same regardless of the predictor variable being examined, this is due to the procedures using the family confidence coefficient rather than the statement confidence coefficient as mentioned previously.

Summary
-------

Simultaneous confidence intervals were explored and computed with the Bonferroni and Working-Hotelling procedures using the `investr` package and our own function. In the multiple regression setting, simulatenous confidence intervals are recommended as they provide certainty entire family of confidence coefficients are correct. Thus, the simulatenous intervals will always be wider than the statement confidence intervals as the former must take into account the joint confidence level of the coefficients. This [answer on StackExchange](http://stats.stackexchange.com/questions/188372/why-are-simultaneous-confidence-intervals-wider-than-the-normal-ones) goes into more detail regarding why the simulatenous intervals are wider than intervals formed with the statement confidence coefficient.

References
----------

Feng, Y. Simultaneous inferences and other topics in regression analysis. Retrieved from <http://www.stat.columbia.edu/~yangfeng/W4315/lectures/lecture-4/lecture_4.pdf>

[Kutner, M. H., Nachtsheim, C. J., Neter, J., Li, W., & Wasserman, W.
(2004). Applied linear statistical models (5th ed.). Boston, MA:
McGraw-Hill Higher Education.](https://amzn.to/2vcB1my)

Why are simultaneous confidence intervals wider than the normal ones? (2016). Retrieved from <http://stats.stackexchange.com/questions/188372/why-are-simultaneous-confidence-intervals-wider-than-the-normal-ones>
