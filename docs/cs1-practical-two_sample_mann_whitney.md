


# Mann-Whitney U test {#cs1-mannwhitney-u-test}
This test also compares two samples, however for this test (in contrast to Student’s t-test) we don’t have to assume that the parent distributions are normally distributed. In order to compare the medians of the two groups we do still need the parent distributions (and consequently the samples) to both have the same shape and variance. In this test we look to see if the medians of the two parent distributions differ significantly from each other.

## Section commands
No new commands used in this section.

## Data and hypotheses
Again, we use the `rivers` dataset. We want to test whether the median body length of male guppies differs between samples. We form the following null and alternative hypotheses:

-	$H_0$: The difference in median body length between the two groups is 0 $(\mu A - \mu G = 0)$
-	$H_1$: The difference in median body length between the two groups is not 0 $(\mu A - \mu G \neq 0)$

We use a two-tailed Mann-Whitney U test to see if we can reject the null hypothesis.

## Summarise and visualise
We did this in the [previous section](#cs1-students-sumvisual).

## Assumptions
We have checked these previously.

## Implement test
Perform a two-tailed, Mann-Whitney U test:


```r
rivers %>% 
  wilcox_test(length ~ river,
              alternative = "two.sided")
```

```
## # A tibble: 1 × 7
##   .y.    group1 group2     n1    n2 statistic        p
## * <chr>  <chr>  <chr>   <int> <int>     <dbl>    <dbl>
## 1 length Aripo  Guanapo    39    29       841 0.000646
```

*	The first argument must be in the formula format: `variable ~ category`
*	The second argument gives the type of alternative hypothesis and must be one of `two.sided`, `greater` or `less` 

## Interpret output and report results
You _may_ get a warning message in the console stating `cannot compute exact p-value with ties`. This just means that some of the data points have exactly the same value which affects the internal mathematics slightly. However, given that the p-value is so very small, this is not something that we need to worry about.

*	The first 5 columns give you information on the variable (`.y.`), groups and sample size of each group
* The `statistic` column gives the t-value of 841 (we need this for reporting)
* The `p` column gives us a p-value of 0.0006464.

Given that the p-value is less than 0.05 we can reject the null hypothesis at this confidence level.
Again, the p-value on the 3rd line is what we’re most interested in. Since the p-value is very small (much smaller than the standard significance level) we choose to say "that it is very unlikely that these two samples came from the same parent distribution and as such we can reject our null hypothesis".

To put it more completely, we can state that:

> A Mann-Whitney test indicated that the median body length of male guppies in the Guanapo river (18.8 mm) differs significantly from the median body length of male guppies in the Aripo river (20.1 mm) (W = 841, p = 0.0006).

## Exercise
:::exercise
Analyse the turtle dataset from before using a Mann Whitney test.

We follow the same process as with Student's t-test.

<details><summary>Answer</summary>

### Hypotheses

$H_0$ : male median $=$ female median

$H_1$ : male median $\neq$ female median

### Summarise and visualise
This is the same as before.

### Assumptions
We've already checked that the variances of the two groups are similar, so we're OK there. Whilst the Mann-Whitney test doesn't require normality or symmetry of distributions it does require that the distributions have the same shape. In this example, with just a handful of data points in each group, it's quite hard to make this call one way or another. My advice in this case would be say that unless it's obvious that the distributions are very different we can just allow this assumption to pass, and you're only going see obvious differences in distribution shape when you have considerably more data points than we have here.

### Carry out a Mann-Whitney test


```r
turtle %>% 
  wilcox_test(serum ~ sex,
              alternative = "two.sided")
```

```
## # A tibble: 1 × 7
##   .y.   group1 group2    n1    n2 statistic     p
## * <chr> <chr>  <chr>  <int> <int>     <dbl> <dbl>
## 1 serum Female Male       6     7        26 0.534
```

This gives us exactly the same conclusion that we got from the two-sample t-test _i.e_. that there isn't any significant difference between the two groups.

A Mann-Whitney test indicated that there wasn't a significant difference in the median Serum Cholesterol levels between male and female turtles (W = 26, p = 0.534)

</details>
:::
