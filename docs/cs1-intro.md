# (PART) CoreStats 1: Simple hypothesis testing {.unnumbered}

# Introduction {#cs1-intro}

## Objectives
:::objectives
**Aim: To carry out basic one and two sample statistical tests.**

By the end of this section and practical participants should be able to achieve the following for each of the listed tests:

1.	Understand what the purpose of each test is
2.	Perform the test in R
3.	Interpret the test output
4.	Understand under what assumptions/conditions each test is appropriate
5.	Check for those assumptions
:::

The tests covered in this practical are:

1. [One-sample tests](#cs1-one-sample-tests)
    -	[One sample t-test](#cs1-one-sample-t-test)
    -	[One-sample Wilcoxon signed-rank test](#cs1-onesample-wilcoxon-signed-rank)
2. [Two-sample tests](#cs1-two-sample)
    -	[Student’s t-test](#cs1-students-t-test)
    -	[Mann-Whitney U test](#cs1-mannwhitney-u-test) 
    -	[Paired two-sample t-test](#cs1-paired-two-sample-t-test)
    -	[Wilcoxon signed-rank test](#cs1-twosample-wilcoxon-signed-rank)

## Background

This practical does not focus on the underlying mathematical theory of the tests although the demonstrators will be happy to answer any questions.
For each test there will be a section explaining its purpose, a section explaining how to perform the test in R, a section explaining the results that have been output to the screen, and a section covering the assumptions required to perform the test.
