`<style>.panelset{--panel-tab-font-family: inherit;}</style>`{=html}







# Mann-Whitney U test {#cs1-mannwhitney-u-test}
This test also compares two samples, however for this test (in contrast to Student’s t-test) we don’t have to assume that the parent distributions are normally distributed. In order to compare the medians of the two groups we do still need the parent distributions (and consequently the samples) to both have the same shape and variance. In this test we look to see if the medians of the two parent distributions differ significantly from each other.

## Libraries and functions
::::: {.panelset}

::: {.panel}
[tidyverse]{.panel-name}

| Libraries| Description|
|:- |:- |
|`library(tidyverse)`| A collection of R packages designed for data science |
|`library(rstatix)`| Converts base R stats functions to a tidyverse-friendly format. Also contains extra functionality that we'll use.|

| Functions| Description|
|:- |:- |
|`rstatix::wilcox_test()`| Performs one- and two-sample Wilcoxon tests on vectors of data; the latter is also known as 'Mann-Whitney' test |
:::

::: {.panel}
[base R]{.panel-name}

| Functions| Description|
|:- |:- |
|`wilcox.test()`| Performs one- and two-sample Wilcoxon tests on vectors of data; the latter is also known as 'Mann-Whitney' test |
:::

::: {.panel}
[Python]{.panel-name}

| Libraries| Description|
|:- |:- |
|`pandas`| A Python data analysis and manipulation tool.|
|`scipy.stats`| A Python module containing statistical functions.|

| Functions| Description|
|:- |:- |
|`pandas.DataFrame.pivot()`|Return reshaped DataFrame organised by given index / column values.|
|`scipy.stats.mannwhitneyu()`|Calculate the Mann-Whitney U test|
:::
:::::

## Data and hypotheses
Again, we use the `rivers` data set. We want to test whether the median body length of male guppies differs between samples. We form the following null and alternative hypotheses:

-	$H_0$: The difference in median body length between the two groups is 0 $(\mu A - \mu G = 0)$
-	$H_1$: The difference in median body length between the two groups is not 0 $(\mu A - \mu G \neq 0)$

We use a two-tailed Mann-Whitney U test to see if we can reject the null hypothesis.

## Summarise and visualise
We did this in the [previous section](#cs1-students-sumvisual).

## Assumptions
We have checked these previously.

## Implement and interpret the test
Perform a two-tailed, Mann-Whitney U test:

::::: {.panelset}
::: {.panel}
[tidyverse]{.panel-name}


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

You _may_ get a warning message in the console stating `cannot compute exact p-value with ties`. This just means that some of the data points have exactly the same value which affects the internal mathematics slightly. However, given that the p-value is so very small, this is not something that we need to worry about.

*	The first 5 columns give you information on the variable (`.y.`), groups and sample size of each group
* The `statistic` column gives the t-value of 841 (we need this for reporting)
* The `p` column gives us a p-value of 0.0006464.
:::

::: {.panel}
[base R]{.panel-name}

```r
wilcox.test(length ~ river, data = rivers_r,
            alternative = "two.sided")
```

```
## 
## 	Wilcoxon rank sum test with continuity correction
## 
## data:  length by river
## W = 841, p-value = 0.0006464
## alternative hypothesis: true location shift is not equal to 0
```

You may get a warning message in the console stating `cannot compute exact p-value with ties`. This just means that some of the data points have exactly the same value which affects the internal mathematics slightly. However, given that the p-value is so very small, this is not something that we need to worry about.

After the warning message:

-	The 1st line gives the name of the test and the 2nd line reminds you what the dataset was called, and what variables were used
-	The 3rd line contains the two key outputs from the test:
    - The calculated W-value is 841 (we’ll use this in reporting)
    - The p-value is 0.0006464. 
-	The 4th line simply states the alternative hypothesis in terms of the difference between the two sample medians in that if there were a difference then one distribution would be shifted relative to the other. 
:::

::: {.panel}
[Python]{.panel-name}

Before we can implement the Mann-Whitney U test, we need to reformat our data a bit.

The `stats.mannwhitneyu()` function requires the numerical input for the two groups it needs to compare.

The easiest way is to reformat our data from the _long_ format where all the data are stacked on top of one another to the _wide_ format, where the `length` values are in separate columns for the two rivers.

We can do this with the `pd.pivot()` function. We save the output in a new object and then access the values as required. It keeps all the data separate, meaning that there will be missing values `NaN` in this format. The `stats.mannwhitneyu()` function doesn't ignore missing values by default and we can specify this in the `nan_policy`, by setting this argument to `omit`.


```python
# reformat the data into a 'wide' format
rivers_py_wide = pd.pivot(rivers_py,
                          columns = 'river',
                          values = 'length')
      
# have a look at the format
rivers_py_wide.head()
```

```
## river  Aripo  Guanapo
## 0        NaN     19.1
## 1        NaN     23.3
## 2        NaN     18.2
## 3        NaN     16.4
## 4        NaN     19.7
```


```python
# perform the Mann-Whitney U test
# ignoring the missing values
stats.mannwhitneyu(rivers_py_wide['Aripo'],
                   rivers_py_wide['Guanapo'],
                   nan_policy = 'omit')
```

```
## MannwhitneyuResult(statistic=841.0, pvalue=0.0006463668392349246)
```

:::
:::::

Given that the p-value is less than 0.05 we can reject the null hypothesis at this confidence level.
Again, the p-value on the 3rd line is what we’re most interested in. Since the p-value is very small (much smaller than the standard significance level) we choose to say "that it is very unlikely that these two samples came from the same parent distribution and as such we can reject our null hypothesis".

To put it more completely, we can state that:

A Mann-Whitney test indicated that the median body length of male guppies in the Guanapo river (18.8 mm) differs significantly from the median body length of male guppies in the Aripo river (20.1 mm) (W = 841, p = 0.0006).

## Exercise
:::exercise ::::::
Analyse the turtle data set from before using a Mann-Whitney U test.

We follow the same process as with Student's t-test.

<details><summary>Answer</summary>

### Hypotheses

$H_0$ : male median $=$ female median

$H_1$ : male median $\neq$ female median

### Summarise and visualise
This is the same as before.

### Assumptions
We've already checked that the variances of the two groups are similar, so we're OK there. Whilst the Mann-Whitney U test doesn't require normality or symmetry of distributions it does require that the distributions have the same shape. In this example, with just a handful of data points in each group, it's quite hard to make this call one way or another. My advice in this case would be say that unless it's obvious that the distributions are very different we can just allow this assumption to pass, and you're only going see obvious differences in distribution shape when you have considerably more data points than we have here.

### Carry out a Mann-Whitney test
::::: {.panelset}
::: {.panel}
[tidyverse]{.panel-name}


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
:::

::: {.panel}
[base R]{.panel-name}

```r
wilcox.test(serum ~ sex,
            data = turtle_r,
            alternative = "two.sided")
```

```
## 
## 	Wilcoxon rank sum exact test
## 
## data:  serum by sex
## W = 26, p-value = 0.5338
## alternative hypothesis: true location shift is not equal to 0
```
:::

::: {.panel}
[Python]{.panel-name}

```python
# reformat the data into a 'wide' format
turtle_py_wide = pd.pivot(turtle_py,
                          columns = 'sex',
                          values = 'serum')
      
# have a look at the format
turtle_py_wide.head()
```

```
## sex  Female   Male
## 0       NaN  220.1
## 1       NaN  218.6
## 2       NaN  229.6
## 3       NaN  228.8
## 4       NaN  222.0
```


```python
# perform the Mann-Whitney U test
# ignoring the missing values
stats.mannwhitneyu(turtle_py_wide['Male'],
                   turtle_py_wide['Female'],
                   nan_policy = 'omit')
```

```
## MannwhitneyuResult(statistic=16.0, pvalue=0.5337995337995338)
```
:::
:::::
This gives us exactly the same conclusion that we got from the two-sample t-test _i.e_. that there isn't any significant difference between the two groups.

A Mann-Whitney test indicated that there wasn't a significant difference in the median Serum Cholesterol levels between male and female turtles (W = 26, p = 0.534)

</details>
::::::::::::::::::
