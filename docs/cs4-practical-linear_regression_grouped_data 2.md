

# Linear regression with grouped data

## Objectives
:::objectives
**Questions**

- How do I perform a linear regression on grouped data?

**Objectives**

- Be able to perform a linear regression on grouped data in R
- Calculate the linear regression for individual groups and visualise these with the data
- Understand and be able to create equations of the regression line
- Be able to deal with interactions in this context
:::

## Purpose and aim
A linear regression analysis with grouped data is used when we have one categorical predictor variable (or factor), and one continuous predictor variable. The response variable must still be continuous however.

For example in an experiment that looks at light intensity in woodland, how is light intensity (continuous: lux) affected by the height at which the measurement is taken, recorded as depth measured from the top of the canopy (continuous: metres) and by the type of woodland (categorical: Conifer or Broad leaf).

<img src="cs4-practical-linear_regression_grouped_data_files/figure-html/unnamed-chunk-2-1.png" width="672" />

When analysing these type of data we want to know:

1.	Is there a difference between the groups?
2.	Does the continuous predictor variable affect the continuous response variable (does canopy depth affect measured light intensity?)
3.	Is there any interaction between the two predictor variables? Here an interaction would display itself as a difference in the slopes of the regression lines for each group, so for example perhaps the conifer dataset has a significantly steeper line than the broad leaf woodland dataset.

In this case, no interaction means that the regression lines will have the same slope.
Essentially the analysis is identical to two-way ANOVA (and R doesn’t really notice the difference).

1. We will plot the data and visually inspect it.
2. We will test for an interaction and if it doesn’t exist then:
    a. We can test to see if either predictor variable has an effect (i.e. do the regression lines have different intercepts? and is the common gradient significantly different from zero?)
    
We will first consider how to visualise the data before then carrying out an appropriate statistical test.

## Section commands
New commands used in this section:

| Function| Description|
|:- |:- |
|`library(broom)`| A package (part of tidyverse) that converts statistical objects from R into tidy tibbles. |
|`augment()`| Augment accepts a model object and a dataset and adds information about each observation in the dataset.|

## Data and hypotheses
The data are stored in `data/tidy/CS4-treelight.csv`.

Read in the data and inspect it:


```r
# read in the data
treelight <- read_csv("data/tidy/CS4-treelight.csv")

# inspect the data
treelight
```

```
## # A tibble: 23 × 4
##       id light depth species
##    <dbl> <dbl> <dbl> <chr>  
##  1     1 4106.  1    Conifer
##  2     2 4934.  1.75 Conifer
##  3     3 4417.  2.5  Conifer
##  4     4 4529.  3.25 Conifer
##  5     5 3443.  4    Conifer
##  6     6 4640.  4.75 Conifer
##  7     7 3082.  5.5  Conifer
##  8     8 2368.  6.25 Conifer
##  9     9 2777.  7    Conifer
## 10    10 2419.  7.75 Conifer
## # … with 13 more rows
```

`treelight` is a data frame with four variables; `id`, `light`, `depth` and `species`. `light` is the continuous response variable, `depth` is the continuous predictor variable and `species` is the categorical predictor variable.

## Summarise and visualise


```r
# plot the data
treelight %>% 
  ggplot(aes(x = depth, y = light, colour = species)) +
  geom_point() +
  scale_color_brewer(palette = "Dark2") +
  labs(x = "Depth (m)",
       y = "Light intensity (lux)")
```

<img src="cs4-practical-linear_regression_grouped_data_files/figure-html/unnamed-chunk-4-1.png" width="672" />

It looks like there is a slight negative correlation between depth and light intensity, with light intensity reducing as the canopy depth increases. It would be useful to plot the regression lines in this plot. We can do this as follows, by updating our code:


```r
# plot the data
treelight %>% 
  ggplot(aes(x = depth, y = light, colour = species)) +
  geom_point() +
  # add regression lines
  geom_smooth(method = "lm", se = FALSE) +
  scale_color_brewer(palette = "Dark2") +
  labs(x = "Depth (m)",
       y = "Light intensity (lux)")
```

<img src="cs4-practical-linear_regression_grouped_data_files/figure-html/unnamed-chunk-5-1.png" width="672" />

Looking at this plot, there doesn’t appear to be any significant interaction between the woodland type (`Broadleaf` and `Conifer`) and the depth at which light measurements were taken (`depth`) on the amount of light intensity getting through the canopy as the gradients of the two lines appear to be very similar. There does appear to be a noticeable slope to both lines and both lines look as though they have very different intercepts. All of this suggests that there isn’t any interaction but that both `depth` and `species` have a significant effect on `Light` independently.

## Implement the test
In this case we're going to implement the test before checking the assumptions (I know, let's live a little!). You'll find out why soon...

We can test for a possible interaction more formally:


```r
anova(lm(light ~ depth * species,
         data = treelight))
```

Remember that `depth * species` is a shorthand way of writing the full set of `depth + species + depth:species` terms in R _i.e._ both main effects and the interaction effect.

## Interpret output and present results
This gives the following output:


```
## Analysis of Variance Table
## 
## Response: light
##               Df   Sum Sq  Mean Sq  F value    Pr(>F)    
## depth          1 30812910 30812910 107.8154 2.861e-09 ***
## species        1 51029543 51029543 178.5541 4.128e-11 ***
## depth:species  1   218138   218138   0.7633    0.3932    
## Residuals     19  5430069   285793                       
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```

As with two-way ANOVA we have a row in the table for each of the different effects that we’ve asked R to consider. The last column is the important one as this contains the p-values. We need to look at the interaction row first.
`depth:species` has a p-value of 0.393 (which is bigger than 0.05) and so we can conclude that the interaction between `depth` and `species` isn’t significant. As such we can now consider whether each of the predictor variables independently has an effect. Both `depth` and `species` have very small p-values (2.86x10<sup>-9</sup> and 4.13x10 <sup>-11</sup>) and so we can conclude that they do have a significant effect on `light`.

This means that the two regression lines should have the same non-zero slope, but different intercepts. We would now like to know what those values are.

### Finding intercept values
Unfortunately, R doesn’t make this obvious and easy for us and there is some deciphering required getting this right.
For a simple straight line such as the linear regression for the conifer dataset by itself, the output is relatively straightforward.


```r
# filter the Conifer data and fit a linear model
treelight %>% 
  filter(species == "Conifer") %>% 
  lm(light ~ depth, data = .)
```

```
## 
## Call:
## lm(formula = light ~ depth, data = .)
## 
## Coefficients:
## (Intercept)        depth  
##      5014.0       -292.2
```

And we can interpret this as meaning that the intercept of the regression line is 5014 and the coefficient of the depth variable (the number in front of it in the equation) is -292.2.

So, the equation of the regression line is given by:

\begin{equation}
Light = 5014 + -292.2 \cdot Depth
\end{equation} 

This came from fitting a simple linear model using the conifer dataset, and has the meaning that for every extra 1 m of depth of forest canopy we lose 292.2 lux of light.

When we looked at the full dataset, we found that interaction wasn’t important. This means that we will have a model with two distinct intercepts but only a single slope (that’s what you get for a linear regression without any interaction), so we need to ask R to calculate that specific combination. The command for that is simply:


```r
lm(light ~ depth + species,
   data = treelight)
```

```
## 
## Call:
## lm(formula = light ~ depth + species, data = treelight)
## 
## Coefficients:
##    (Intercept)           depth  speciesConifer  
##         7962.0          -262.2         -3113.0
```

Notice the `+` symbol in the argument, as opposed to the `*` symbol used earlier. This means that we are explicitly _not_ including an interaction term in this fit, and consequently we are forcing R to calculate the equation of lines which have the same gradient.

Ideally we would like R to give us two equations, one for each forest type, so four parameters in total.
Unfortunately, R is parsimonious and doesn’t do that. Instead R gives you three coefficients, and these require a bit of interpretation.

The first two numbers that R returns (underneath `Intercept` and `depth`) are the exact intercept and slope coefficients for one of the lines (in this case they correspond to the data for `Broadleaf` woodlands).

For the coefficients belonging to the other line, R uses these first two coefficients as baseline values and expresses the other coefficients relative to these ones. R also doesn’t tell you explicitly which group it is using as its baseline reference group! (Did I mention that R can be very helpful at times 😉?)

So, how to decipher the above output?

First, I need to work out which group has been used as the baseline.

* It will be the group that comes first alphabetically, so it should be `Broadleaf`
* The other way to check would be to look and see which group is not mentioned in the above table. `Conifer` is mentioned (in the `SpeciesConifer` heading) and so again the baseline group is `Broadleaf.`

This means that the intercept value and `depth` coefficient correspond to the `Broadleaf` group and as a result I know what the equation of one of my lines is:

Broadleaf:

\begin{equation}
Light = 7962 + -262.2 \cdot Depth
\end{equation} 

In this example we know that the gradient is the same for both lines (because we explicitly asked R not to include an interaction), so all I need to do is find the intercept value for the `Conifer` group. Unfortunately, the final value given underneath `SpeciesConifer` does not give me the intercept for `Conifer`, instead it tells me the difference between the `Conifer` group intercept and the baseline intercept i.e. the equation for the regression line for conifer woodland is given by:

\begin{equation}
Light = (7962 + -3113) + -262.2 \cdot Depth
\end{equation} 

\begin{equation}
Light = 4829 + -262.2 \cdot Depth
\end{equation} 

### Adding custom regression lines
In the example above we determined that the interaction term `species:depth` was not significant. It would be good to visualise the model without the interaction term. 

This is relatively straightforward if we understand the output of the model a bit better.

First of all, we load the `broom` library. This is part of tidyverse, so you don't have to install it. It is not loaded by default, hence us loading it. What broom does it changes the format of many common base R outputs into a more tidy format, so we can work with the output in our analyses more easily.

The function we use here is called `augment()`. What this does is take a model object and a dataset and adds information about each observation in the dataset.


```r
# define the model without interaction term
lm_additive <- lm(light ~ species + depth,
                  data = treelight)

# load the broom package
library(broom)

# augment the model
lm_additive %>% augment()
```

```
## # A tibble: 23 × 9
##    light species depth .fitted .resid   .hat .sigma .cooksd .std.resid
##    <dbl> <chr>   <dbl>   <dbl>  <dbl>  <dbl>  <dbl>   <dbl>      <dbl>
##  1 4106. Conifer  1      4587.  -481. 0.191    531. 0.0799      -1.01 
##  2 4934. Conifer  1.75   4390.   544. 0.156    528. 0.0766       1.11 
##  3 4417. Conifer  2.5    4194.   223. 0.128    542. 0.00985      0.449
##  4 4529. Conifer  3.25   3997.   532. 0.105    530. 0.0440       1.06 
##  5 3443. Conifer  4      3800.  -358. 0.0896   538. 0.0163      -0.706
##  6 4640. Conifer  4.75   3604.  1037. 0.0801   486. 0.120        2.03 
##  7 3082. Conifer  5.5    3407.  -325. 0.0769   540. 0.0113      -0.637
##  8 2368. Conifer  6.25   3210.  -842. 0.0801   507. 0.0793      -1.65 
##  9 2777. Conifer  7      3014.  -237. 0.0896   542. 0.00719     -0.468
## 10 2419. Conifer  7.75   2817.  -398. 0.105    537. 0.0247      -0.792
## # … with 13 more rows
```

The output shows us lots of data. Our original `light` values are in the `light` column and it's the same for `species` and `depth`. What has been added is information about the fitted (or predicted) values based on the `light ~ depth + species` model we defined.

The fitted or predicted values are in the `.fitted` column, with corresponding residuals in the `.resid` column. Remember, your data = predicted values + error, so if you would add `.fitted` + `resid` then you would end up with your original data again.

Using this information we can now plot the regression lines by `species`:


```r
# plot the regression lines by species
lm_additive %>%
  augment() %>% 
  ggplot(aes(x = depth, y = .fitted, colour = species)) +
  geom_line() +
  scale_color_brewer(palette = "Dark2")
```

<img src="cs4-practical-linear_regression_grouped_data_files/figure-html/unnamed-chunk-11-1.png" width="672" />

Lastly, if we would want to plot the data and regression lines together, we could change the code as follows:


```r
# plot the regression lines
lm_additive %>%
  augment() %>% 
  ggplot(aes(x = depth, y = .fitted, colour = species)) +
  # add the original data points
  geom_point(data = treelight,
             aes(x = depth, y = light, colour = species)) +
  geom_line() +
  scale_color_brewer(palette = "Dark2") +
  labs(x = "Depth (m)",
       y = "Light intensity (lux)")
```

<img src="cs4-practical-linear_regression_grouped_data_files/figure-html/unnamed-chunk-12-1.png" width="672" />

## Assumptions
In this case we first wanted to check if the interaction was significant, prior to checking the assumptions. If we would have checked the assumptions first, then we would have done that one the full model (with the interaction), then done the ANOVA if everything was OK. We would have then found out that the interaction was not significant, meaning we'd have to re-check the assumptions with the new model. In what order you do it is a bit less important here. The main thing is that you check the assumptions and report on it!

Anyway, hopefully you’ve got the gist of checking assumptions for linear models by now: diagnostic plots!


```r
lm_additive %>% 
  resid_panel(plots = c("resid", "qq", "ls", "cookd"),
              smoother = TRUE)
```

<img src="cs4-practical-linear_regression_grouped_data_files/figure-html/unnamed-chunk-13-1.png" width="672" />

* The **Residuals plot** looks OK, no systematic pattern.
* The **Q-Q plot** isn’t perfect, but I’m happy with the normality assumption.
* The **Location-Scale plot** is OK, some very slight suggestion of heterogeneity of variance, but nothing to be too worried about.
* The **Cook's D plot** shows that all of the points are OK

Woohoo!

## Dealing with interaction
If there _had been_ a significant interaction between the two predictor variables (for example, if light intensity had dropped off significantly faster in conifer woods than in broad leaf woods, in addition to being lower overall, then we would again be looking for two equations for the linear regression, but this time the gradients vary as well.
In this case interaction is important and so we need the output from a linear regression that explicitly includes the interaction term:


```r
lm(light ~ depth + species + depth:species,
   data = treelight)
```

or written using the short-hand:


```r
lm(light ~ depth * species,
   data = treelight)
```

There really is absolutely no difference in the end result.
Either way this gives us the following output:


```
## 
## Call:
## lm(formula = light ~ depth * species, data = treelight)
## 
## Coefficients:
##          (Intercept)                 depth        speciesConifer  
##              7798.57               -221.13              -2784.58  
## depth:speciesConifer  
##               -71.04
```

As before the Broadleaf line is used as the baseline regression and we can read off the values for its intercept and slope directly:

Broadleaf:
\begin{equation}
Light = 7798.57 + -221.13 \cdot Depth
\end{equation}

Note that this is different from the previous section, by allowing for an interaction all fitted values will change.

For the conifer line we will have a different intercept value and a different gradient value. As before the value underneath `speciesConifer` gives us the difference between the intercept of the conifer line and the broad leaf line. The new, additional term `depth:speciesConifer` tells us how the coefficient of `depth` varies for the conifer line i.e. how the gradient is different. Putting these two together gives us the following equation for the regression line conifer woodland:

Conifer:
\begin{equation}
Light = (7798.57 + -2784.58) + (-221.13 + -71.04) \cdot Depth
\end{equation}

\begin{equation}
Light = 5014 + -292.2 \cdot Depth
\end{equation}

These also happen to be exactly the regression lines that you would get by calculating a linear regression on each group’s data separately.

## Exercise: Clover and yarrow
:::exercise
Clover and yarrow field trials

The `data/tidy/CS4-clover.csv` dataset contains information on field trials at three different farms (`A`, `B` and `C`). Each farm recorded the yield of clover in each of ten fields along with the density of yarrow stalks in each field.

* Investigate how clover yield is affected by yarrow stalk density. Is there evidence of competition between the two species?
* Is there a difference between farms?

<details><summary>Answer</summary>


```r
clover <- read_csv("data/tidy/CS4-clover.csv")
```

This dataset has three variables; `yield` (which is the response variable), `yarrow` (which is a continuous predictor variable) and `farm` (which is the categorical predictor variables). As always we'll visualise the data first:


```r
# plot the data
clover %>% 
  ggplot(aes(x = yarrow, y = yield,
             colour = farm)) +
  geom_point() +
  scale_color_brewer(palette = "Dark2")
```

<img src="cs4-practical-linear_regression_grouped_data_files/figure-html/unnamed-chunk-18-1.png" width="672" />

Looking at this plot as it stands, it's pretty clear that yarrow density has a significant effect on yield, but it's pretty hard to see from the plot whether there is any effect of `farm`, or whether there is any interaction. In order to work that out we'll want to add the regression lines for each `farm` separately.


```r
# plot the data
clover %>% 
  ggplot(aes(x = yarrow, y = yield,
             colour = farm, group = farm)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE) +
  scale_color_brewer(palette = "Dark2")
```

<img src="cs4-practical-linear_regression_grouped_data_files/figure-html/unnamed-chunk-19-1.png" width="672" />

The regression lines are very close together, and it looks very much as if there isn't any interaction, but also that there isn't any effect of `farm`. Let's carry out the analysis:


```r
lm_clover <- lm(yield ~ yarrow * farm,
                data = clover)

anova(lm_clover)
```

```
## Analysis of Variance Table
## 
## Response: yield
##             Df Sum Sq Mean Sq F value    Pr(>F)    
## yarrow       1 8538.3  8538.3 28.3143 1.847e-05 ***
## farm         2    3.8     1.9  0.0063    0.9937    
## yarrow:farm  2  374.7   187.4  0.6213    0.5457    
## Residuals   24 7237.3   301.6                      
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```

This confirms our suspicions from looking at the plot. There isn't any interaction between `yarrow` and `farm.` `yarrow` density has a statistically significant effect on `yield` but there isn't any difference between the different farms on the yields of clover.

Let's check the assumptions:


```r
lm_clover %>% 
  resid_panel(plots = c("resid", "qq", "ls", "cookd"),
              smoother = TRUE)
```

<img src="cs4-practical-linear_regression_grouped_data_files/figure-html/unnamed-chunk-21-1.png" width="672" />

This is a borderline case.

1. Normality is fine (Q-Q plot)
2. There aren't any highly influential points (Cook's D plot)
3. There is a strong suggestion of heterogeneity of variance (Location-Scale plot). Most of the points are relatively close to the regression lines, but the there is a much great spread of points low yarrow density (which corresponds to high yield values, which is what the predicted values correspond to).
4. Finally, there is a slight suggestion that the data might not be linear, that it might curve slightly (Residual plot).

We have two options; both of which are arguably OK to do in real life.

1. We can claim that these assumptions are well enough met and just report the analysis that we've just done.
2. We can decide that the analysis is not appropriate and look for other options.
    a. We can try to transform the data by taking logs of `yield.` This might fix both of our problems: taking logs of the response variable has the effect of improving heterogeneity of variance when the Residuals plot is more spread out on the right vs. the left (like ours). It also is appropriate if we think the true relationship between the response and predictor variables is exponential rather than linear (which we might have). We do have the capabilities to try this option.
    b. We could try a permutation based approach (beyond the remit of this course, and actually a bit tricky in this situation). This wouldn't address the non-linearity but it would deal with the variance assumption.
    c. We could come up with a specific functional, mechanistic relationship between yarrow density and clover yield based upon other aspects of their biology. For example there might be a threshold effect such that for yarrow densities below a particular value, clover yields are unaffected, but as soon as yarrow values get above that threshold the clover yield decreases (maybe even linearly). This would require a much better understanding of clover-yarrow dynamics (of which I personally know very little).

Let's do a quick little transformation of the data, and repeat our analysis see if our assumptions are better met this time (just for the hell of it):


```r
# plot log-transformed data
clover %>% 
  ggplot(aes(x = yarrow, y = log(yield), colour = farm)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE) +
  scale_color_brewer(palette = "Dark2")
```

<img src="cs4-practical-linear_regression_grouped_data_files/figure-html/unnamed-chunk-22-1.png" width="672" />

Again, this looks plausible. There's a noticeable outlier from Farm B (data point at the bottom of the plot) but otherwise we see that: there probably isn't an interaction; there is likely to be an effect of `yarrow` on `log(yield)`; and there probably isn't any difference between the farms.

Let's do the analysis:


```r
# define linear model
lm_log_clover <- lm(log(yield) ~ yarrow * farm,
                    data = clover)

anova(lm_log_clover)
```

```
## Analysis of Variance Table
## 
## Response: log(yield)
##             Df  Sum Sq Mean Sq F value   Pr(>F)    
## yarrow       1 10.6815 10.6815 27.3233 2.34e-05 ***
## farm         2  0.0862  0.0431  0.1103   0.8960    
## yarrow:farm  2  0.8397  0.4199  1.0740   0.3575    
## Residuals   24  9.3823  0.3909                     
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```

Woop. All good so far. We have the same conclusions as before in terms of what is significant and what isn't. Now we just need to check the assumptions:


```r
lm_log_clover %>% 
  resid_panel(plots = c("resid", "qq", "ls", "cookd"),
              smoother = TRUE)
```

<img src="cs4-practical-linear_regression_grouped_data_files/figure-html/unnamed-chunk-24-1.png" width="672" />

Well, this is actually a better set of diagnostic plots. Whilst one data point (for example in the Q-Q plot) is a clear outlier, if we ignore that point then all of the other plots do look better.

So now we know that `yarrow` is a significant predictor of `yield` and we're happy that the assumptions have been met.

</details>
:::

## Key points

:::keypoints
- A linear regression analysis with grouped data is used when we have one categorical and one continuous predictor variable, together with one continuous response variable
- We can visualise the data by plotting a regression line together with the raw data
- When performing an ANOVA, we need to check for interaction terms
- Again, we check the underlying assumptions using diagnostic plots
- We can create an equation for the regression line for each group in the data using the `lm()` output
:::
