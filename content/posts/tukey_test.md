Title: Tukey's Test for Post-Hoc Analysis
Date: 2018-09-07
Tags: R, statistics
Category: Statistics
Slug: tukeys-test-post-hoc-analysis
Author: Aaron Schlegel
Summary: After a multivariate test, it is often desired to know more about the specific groups to find out if they are significantly different or similar. This step after analysis is referred to as 'post-hoc analysis' and is a major step in hypothesis testing. One common and popular method of post-hoc analysis is Tukey's Test. The test is known by several different names. Tukey's test compares the means of all treatments to the mean of every other treatment and is considered the best available method in cases when confidence intervals are desired or if sample sizes are unequal.

In a [previous example](https://rpubs.com/aaronsc32/anova-compare-more-than-two-groups), ANOVA (Analysis of Variance) was performed to test a hypothesis concerning more than two groups. Although ANOVA is a powerful and useful parametric approach to analyzing approximately normally distributed data with more than two groups (referred to as 'treatments'), it does not provide any deeper insights into patterns or comparisons between specific groups.

After a multivariate test, it is often desired to know more about the specific groups to find out if they are significantly different or similar. This step after analysis is referred to as 'post-hoc analysis' and is a major step in hypothesis testing.

One common and popular method of post-hoc analysis is Tukey's Test. The test is known by several different names. Tukey's test compares the means of all treatments to the mean of every other treatment and is considered the best available method in cases when confidence intervals are desired or if sample sizes are unequal ([Wikipedia](https://en.wikipedia.org/wiki/Tukey%27s_range_test#Advantages_and_disadvantages)).

The test statistic used in Tukey's test is denoted $q$ and is essentially a modified t-statistic that corrects for multiple comparisons. $q$ can be found similarly to the t-statistic:

$$ q_{\alpha, k, N - k} $$

The studentized range distribution of $q$ is defined as:

$$ q_s = \frac{Y_{max} - Y_{min}}{SE} $$

Where $Y_{max}$ and $Y_{min}$ are the larger and smaller means of the two groups being compared. $SE$ is defined as the standard error of the entire design.

In this example, Tukey's Test will be performed on the `PlantGrowth` dataset that was analyzed previously with ANOVA. The outputs from two different (but similar) implementations of Tukey's Test will be examined along with how to manually calculate the test. Other methods of post-hoc analysis will be explored in future posts.

Getting Started
---------------

Begin by loading the packages that will be needed and the `PlantGrowth` dataset.

``` r
library(agricolae)
data("PlantGrowth")
```

Tukey's Test
------------

Since Tukey's test is a post-hoc test, we must first fit a linear regression model and perform ANOVA on the data. ANOVA in this example is done using the `aov()` function.

``` r
plant.lm <- lm(weight ~ group, data = PlantGrowth)
plant.av <- aov(plant.lm)
summary(plant.av)
```

    ##             Df Sum Sq Mean Sq F value Pr(>F)  
    ## group        2  3.766  1.8832   4.846 0.0159 *
    ## Residuals   27 10.492  0.3886                 
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

The summary of the `aov()` output is the same as the output of the `anova()` function that was used in the previous example. As before, ANOVA reports a p-value far below 0.05, indicating there are differences in the means in the groups. To investigate more into the differences between all groups, Tukey's Test is performed.

The `TukeyHSD()` function is available in base R and takes a fitted `aov` object.

``` r
tukey.test <- TukeyHSD(plant.av)
tukey.test
```

    ##   Tukey multiple comparisons of means
    ##     95% family-wise confidence level
    ## 
    ## Fit: aov(formula = plant.lm)
    ## 
    ## $group
    ##             diff        lwr       upr     p adj
    ## trt1-ctrl -0.371 -1.0622161 0.3202161 0.3908711
    ## trt2-ctrl  0.494 -0.1972161 1.1852161 0.1979960
    ## trt2-trt1  0.865  0.1737839 1.5562161 0.0120064

The output gives the difference in means, confidence levels and the adjusted p-values for all possible pairs. The confidence levels and p-values show the only significant between-group difference is for treatments 1 and 2. Note the other two pairs contain 0 in the confidence intervals and thus, have no significant difference. The results can also be plotted.

``` r
plot(tukey.test)
```

![](tukey_test_files/figure-markdown_github/tukey_plot-1.png)

Another way of performing Tukey's Test is provided by the [agricolae](https://cran.r-project.org/web/packages/agricolae/index.html) package. The `HSD.test()` function in the `agricolae` package performs Tukey's Test and outputs several additional statistics.

``` r
tukey.test2 <- HSD.test(plant.av, trt = 'group')
tukey.test2
```

    ## $statistics
    ##     MSerror Df  Mean       CV       MSD
    ##   0.3885959 27 5.073 12.28809 0.6912161
    ## 
    ## $parameters
    ##    test name.t ntr StudentizedRange alpha
    ##   Tukey  group   3         3.506426  0.05
    ## 
    ## $means
    ##      weight       std  r  Min  Max    Q25   Q50    Q75
    ## ctrl  5.032 0.5830914 10 4.17 6.11 4.5500 5.155 5.2925
    ## trt1  4.661 0.7936757 10 3.59 6.03 4.2075 4.550 4.8700
    ## trt2  5.526 0.4425733 10 4.92 6.31 5.2675 5.435 5.7350
    ## 
    ## $comparison
    ## NULL
    ## 
    ## $groups
    ##      weight groups
    ## trt2  5.526      a
    ## ctrl  5.032     ab
    ## trt1  4.661      b
    ## 
    ## attr(,"class")
    ## [1] "group"

The `HSD.test()` implementation provides the Honestly Significant Difference, another statistic that can be used to determine if a comparison is significant, the calculated $q$ value, and the mean square error, which was found in the previous example on ANOVA. The test shows in the `$groups` output the control is similar to both treatments but treatment 1 and two are significantly different from each other, just as the previous test showed.

Manually Calculating Tukey's Test
---------------------------------

The results from both tests can be verified manually. We'll start with the latter test (`HSD.test`) with the MSE and also define some common variables to make it all easier to keep straight. The MSE calculation is the same as the previous example.

``` r
N <- length(PlantGrowth$weight) # total sample size
k <- length(unique(PlantGrowth$group)) # number of treatments
n <- length(PlantGrowth$weight) / k # number of samples per group (since sizes are equal)

# Mean Square
plants <- split(PlantGrowth, PlantGrowth$group)

sse <- sum(Reduce('+', lapply(plants, function(x) {
  (length(x[,1]) - 1) * sd(x[,1])^2
})))

mse <- sse / (N - k)
mse
```

    ## [1] 0.3885959

Next, find the q-value. Computing the q-value is done with the `qtukey()` function.

``` r
# q-value
q.value <- qtukey(p = 0.95, nmeans = k, df = N - k)
q.value
```

    ## [1] 3.506426

With the q-value found, the Honestly Significant Difference can be determined. The Honestly Significant Difference is defined as the q-value multiplied by the square root of the MSE divided by the sample size.

$$ HSD = q_{\alpha,k,N-k} \sqrt{\frac{MSE}{n}} $$

``` r
# Tukey Honestly Signficant Difference
tukey.hsd <- q.value * sqrt(mse / n)
tukey.hsd
```

    ## [1] 0.6912161

As mentioned earlier, the Honestly Significant Difference is a statistic that can be used to determine significant differences between groups. If the absolute value of the difference of the two groups' means is greater than or equal to the HSD, the difference is significant.

$$|Y_1 − Y_2| \geq HSD $$

The means of each group can be found using the `tapply()` function. Since there's only three groups, I went ahead and just calculated the differences manually. With the differences obtained, compare the absolute value of the difference to the HSD. I used a quick and dirty `for()` loop to do this.

``` r
means <- tapply(PlantGrowth$weight, PlantGrowth$group, mean)
trt1.ctrl.diff <- means[2] - means[1]
trt2.ctrl.diff <- means[3] - means[1]
trt2.trt1.diff <- means[3] - means[2]

for (i in list(trt1.ctrl.diff, trt2.ctrl.diff, trt2.trt1.diff)) {
  print(abs(i) >= tukey.hsd)
}
```

    ##  trt1 
    ## FALSE 
    ##  trt2 
    ## FALSE 
    ## trt2 
    ## TRUE

The output of the for loop shows the only significant difference higher than the HSD is between treatment 1 and 2.

Calculating Tukey's Test Confidence Intervals
---------------------------------------------

Intervals for Tukey's Test can also be estimated, as seen in the output of the `TukeyHSD()` function. Since the test uses the studentized range, estimation is similar to the t-test setting. Intervals with $1 − \alpha$ confidence can be found using the Tukey-Kramer method. The Tukey-Kramer method allows for unequal sample sizes between the treatments and is, therefore, more often applicable (though it doesn't matter in this case since the sample sizes are equal). The Tukey-Kramer method is defined as:

$$ y_i - y_j \pm q_{\alpha,k,N-k} \sqrt{\left(\frac{MSE}{2}\right) \left(\frac{1}{n_i} + \frac{1}{n_j}\right)} $$

Entering the values that were found earlier into the equation yields the same intervals as was found from the `TukeyHSD()` output.

``` r
trt1.ctrl.diff.upper <- trt1.ctrl.diff + q.value * sqrt(mse / 2 * (2 / n))
trt1.ctrl.diff.lower <- trt1.ctrl.diff - q.value * sqrt(mse / 2 * (2 / n))
```

    ## [1] ( -1.0622161 0.3202161 )

``` r
trt2.ctrl.diff.upper <- trt2.ctrl.diff + q.value * sqrt(mse / 2 * (2 / n))
trt2.ctrl.diff.lower <- trt2.ctrl.diff - q.value * sqrt(mse / 2 * (2 / n))
```

    ## [1] ( -0.1972161 1.1852161 )

``` r
trt2.trt1.diff.upper <- trt2.trt1.diff + q.value * sqrt(mse / 2 * (2 / n))
trt2.trt1.diff.lower <- trt2.trt1.diff - q.value * sqrt(mse / 2 * (2 / n))
```

    ## [1] ( 0.1737839 1.5562161 )

``` r
tukey.test
```

    ##   Tukey multiple comparisons of means
    ##     95% family-wise confidence level
    ## 
    ## Fit: aov(formula = plant.lm)
    ## 
    ## $group
    ##             diff        lwr       upr     p adj
    ## trt1-ctrl -0.371 -1.0622161 0.3202161 0.3908711
    ## trt2-ctrl  0.494 -0.1972161 1.1852161 0.1979960
    ## trt2-trt1  0.865  0.1737839 1.5562161 0.0120064

The table from the `TukeyHSD()` output is reconstructed below. Adjusted p-values are left out intentionally.

| Comparison | diff   | lwr        | upr       |
|------------|--------|------------|-----------|
| trt1-ctrl  | -0.371 | -1.0622161 | 0.3202161 |
| trt2-ctrl  | 0.494  | -0.1972161 | 1.1852161 |
| trt2-trt1  | 0.865  | 0.1737839  | 1.5562161 |

Conclusion
----------

In this example, hypothesis testing was taken a step further into the realm of post-hoc analysis. Post-hoc analysis often provides much greater insight into the differences or similarities between specific groups and is, therefore, an important step in data analysis. Tukey's Test is just one of many methods available in post-hoc analysis and as mentioned, is considered to be the best method in a wide variety of cases.
