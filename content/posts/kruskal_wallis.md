Title: Kruskal-Wallis One-Way Analysis of Variance of Ranks
Date: 2018-09-03
Tags: R, statistics
Category: Statistics
Slug: kruskal-wallis-one-way-analysis-variance-ranks
Author: Aaron Schlegel
Summary: The Kruskal-Wallis test extends the Mann-Whitney-Wilcoxon Rank Sum test for more than two groups. The test is nonparametric similar to the Mann-Whitney test and as such does not assume the data are normally distributed and can, therefore, be used when the assumption of normality is violated. This example will employ the Kruskal-Wallis test on the `PlantGrowth` dataset as used in previous examples. Although the data appear to be approximately normally distributed as seen before, the Kruskal-Wallis test performs just as well as a parametric test.

The Kruskal-Wallis test extends the Mann-Whitney-Wilcoxon Rank Sum test for more than two groups. The test is nonparametric similar to the Mann-Whitney test and as such does not assume the data are normally distributed and can, therefore, be used when the assumption of normality is violated. This example will employ the Kruskal-Wallis test on the `PlantGrowth` dataset as used in previous examples. Although the data appear to be approximately normally distributed as seen before, the Kruskal-Wallis test performs just as well as a parametric test.

Several packages exist that can perform the Kruskal-Wallis test, including the [agricolae](https://cran.r-project.org/package=agricolae) and [coin](https://cran.r-project.org/web/packages/coin/index.html) packages. Base R also provides a `kruskal.test()` function.

The Kruskal-Wallis Test
-----------------------

Since the Kruskal-Wallis test is nonparametric similar to the Mann-Whitney test, it involves ranking the data from 1 (the smallest) to the largest with ties replaced by the mean of the ranks the values would have received. The sum of the ranks for each treatment is typically denoted $T_i$ or $R_i$. Forming the hypothesis is the same as before, there is no reason to assume there is a difference between the control and treatment groups.

$$ H_0: \mu_c = \mu_{t_1} = \mu_{t_2} $$
$H_A$: Not all populations are equal.

The test statistic is denoted as $H$ and can be defined as the following when the data does not contain ties.

$$ H = \frac{12}{N(N + 1)} \bigg[ \frac{\sum_{i=1}^k T_{i}^2}{n_i} - 3(N + 1) \bigg] $$

If the data contains ties, a correction can be used by dividing $H$ by:

$$ 1 - \frac{\sum_{t=1}^G (t_i^3 - t_i)}{N^3 - N} $$

Where $G$ is the number of groups of tied ranks and $t_i$ is the number of tied values within the $i^{th}$ group ([Wikipedia](https://en.wikipedia.org/wiki/Kruskal%E2%80%93Wallis_one-way_analysis_of_variance#Method)). The p-value is usually approximated using a Chi-Square distribution as calculating exact probabilities can be computationally intensive for larger sample sizes. See this [paper](http://faculty.virginia.edu/kruskal-wallis/paper/A%20comparison%20of%20the%20Exact%20Kruskal-v4.pdf) for a much deeper look into the Kruskal-Wallis test and calculating exact probabilities for larger sample sizes.

Load the packages and data that will be used in the example.

``` r
library(agricolae)
library(coin)
```

    ## Loading required package: survival

``` r
data("PlantGrowth")
```

Since the `PlantGrowth` dataset has been explored previously, we'll proceed to the test. The `kruskal()` function is provided by the `agricolae` package.

``` r
kruskal.test(weight ~ group, data = PlantGrowth)
```

    ## 
    ##  Kruskal-Wallis rank sum test
    ## 
    ## data:  weight by group
    ## Kruskal-Wallis chi-squared = 7.9882, df = 2, p-value = 0.01842

``` r
kruskal(PlantGrowth$weight, PlantGrowth$group, console = TRUE)
```

    ## 
    ## Study: PlantGrowth$weight ~ PlantGrowth$group
    ## Kruskal-Wallis test's
    ## Ties or no Ties
    ## 
    ## Critical Value: 7.988229
    ## Degrees of freedom: 2
    ## Pvalue Chisq  : 0.01842376 
    ## 
    ## PlantGrowth$group,  means of the ranks
    ## 
    ##      PlantGrowth.weight  r
    ## ctrl              14.75 10
    ## trt1              10.35 10
    ## trt2              21.40 10
    ## 
    ## Post Hoc Analysis
    ## 
    ## t-Student: 2.051831
    ## Alpha    : 0.05
    ## Minimum Significant Difference: 7.125387 
    ## 
    ## Treatments with the same letter are not significantly different.
    ## 
    ##      PlantGrowth$weight groups
    ## trt2              21.40      a
    ## ctrl              14.75     ab
    ## trt1              10.35      b

Both functions output the chi-squared value, degrees of freedom and p-value. The `agricolae` package output provides more statistics like the t-value and Least Significant Difference and further comparisons between the groups. Both functions reported a p-value well below 0.05. Therefore, it can be concluded there are differences between the control and treatment groups. The output from the `kruskal()` function shows there is a difference between treatment one and two while the control is not significantly different from either treatment. Note Tukey's test reported a similar conclusion after ANOVA was performed in a [previous example](http://rpubs.com/aaronsc32/anova-compare-more-than-two-groups), evidence the Kruskal-Wallis test is as performant on approximately normally distributed data.

Manually Calculating the Kruskal-Wallis Test
--------------------------------------------

The above outputs of the two functions can be replicated manually to verify the results. The procedure is similar to the Mann-Whitney test in that the data is sorted and then the test statistic is calculated on the rank values. The `PlantGrowth` data are sorted on the weight variable and then ranked as before.

``` r
plants.sorted <- PlantGrowth[order(PlantGrowth$weight),]
plants.sorted$ranked <- rank(plants.sorted$weight, ties.method = 'average')
```

Before getting into the calculations, it's easier to define the variables to make it easier to keep it all straight.

``` r
N <- length(PlantGrowth$weight)
k <- length(unique(PlantGrowth$group))
n <- N / k

plants <- split(plants.sorted, plants.sorted$group)

t_ctrl <- sum(plants$ctrl$ranked)^2
t_trt1 <- sum(plants$trt1$ranked)^2
t_trt2 <- sum(plants$trt2$ranked)^2
```

Can then proceed to calculating the $H$ value. The equation is broken into several pieces to keep it easier to track.

``` r
hvalue.part1 <- 12 / (N * (N + 1))
hvalue.part2 <- sum(t_ctrl / n, t_trt1 / n, t_trt2 / n)

h.value <- hvalue.part1 * hvalue.part2 - (3 * (N + 1))
h.value
```

    ## [1] 7.986452

Notice the computed $H$ value is slightly different than the value reported earlier. The difference is caused by the presence of ties in the `PlantGrowth` dataset. Thus, the correction mentioned previously can be applied. There are only two tied values comprising one group in the dataset so that the value can be directly inputted into the correction equation.

``` r
correction <- 1 - (2^3 - 2) / (N^3 - N)

corrected.h.value <- h.value / correction
corrected.h.value
```

    ## [1] 7.988229

The $H$ value now matches the reported value from the two functions. The $H$ value is approximated by the chi-square distribution. Therefore the p-value is found using the corrected $H$ value and $k − 1$ degrees of freedom, denoted as:

$$ Pr(\chi^2_{k − 1} \geq HSD) $$

``` r
p.value <- 1 - pchisq(corrected.h.value, df = k - 1)
p.value
```

    ## [1] 0.01842376

The t-value reported from the `agricolae` package is computed using the $\alpha$ level and $n$ − $k$ degrees of freedom.

``` r
t.value <- qt(p = 1 - 0.05 / 2, N - k)
t.value
```

    ## [1] 2.051831

The Least Significant Difference reported from the `kruskal()` function can also be found by finding the mean square error of the computed rank values. The Least Significant Difference is another test statistic that was developed by Ronald Fisher. The basic idea of the LSD is to find the smallest difference between two sample means and conclude a significant difference if a comparison between two other group means exceeds the LSD. Here is an excellent resource for more information on the [Least Significant Difference](https://www.utd.edu/~herve/abdi-LSD2010-pretty.pdf). The LSD can be calculated using the following equation:

$$ LSD = t_{\alpha, N-k} \sqrt{MSE \frac{2}{n}} $$

A quick way to get the $MSE$ is to use the `anova()` function and extract the value from the reported table.

``` r
mse <- anova(lm(ranked ~ group, data = plants.sorted))[[3]][2]
mse
```

    ## [1] 60.29815

The LSD can then be found using the t-value and $MSE$.

``` r
lsd <- t.value * sqrt(mse * 2 / n)
lsd
```

    ## [1] 7.125387

Conclusion
----------

In this post, the Kruskal-Wallis test for comparing more than two groups with non-normal distributions was investigated using two implementations in base R and the `agricolae` package. The test was also manually calculated to verify the results. As demonstrated in this post, the Kruskal-Wallis test performs just as well with approximately normally distributed data.
