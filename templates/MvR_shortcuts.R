bookdown::render_book(output_dir = "docs", "index.Rmd", "bookdown::bs4_book")

::::: {.panelset}
::: {.panel}
[tidyverse]{.panel-name}
:::

::: {.panel}
[base R]{.panel-name}
:::

::: {.panel}
[Python]{.panel-name}
:::
:::::

# Exercise with different languages
:::exercise ::::::

::::: {.panelset}
::: {.panel}
[tidyverse]{.panel-name}
:::
::: {.panel}
[base R]{.panel-name}
:::
:::::

<details><summary>Answer</summary>
::::: {.panelset}
::: {.panel}
[tidyverse]{.panel-name}
:::
::: {.panel}
[base R]{.panel-name}
:::
:::::
</details>
::::::::::::::::::

```{python, results='hide'}
(
  ggplot(turtle_py, aes(x = "sex", y = "serum"))
  + geom_boxplot()
)
```

  in panelset.css:

  .panelset .panel-tabs {
    display: -webkit-box;
    display: flex;
    flex-wrap: wrap;
    -webkit-box-orient: horizontal;
    -webkit-box-direction: normal;
    flex-direction: row;
    -webkit-box-pack: start;
    justify-content: flex-start;
    -webkit-box-align: center;
    align-items: baseline;

par(mfrow=c(1,2))



# Section link

{#example}

[Link text](#example)

# Referring to chapter/section number:
  \@ref(section_name)

# Figures
  ```{r fig-name, echo=FALSE, fig.align='center', fig.cap='caption'}
  knitr::include_graphics("img/image.png")
  ```

R chunk with name, and fig.cap='caption'
Figure \@ref(fig:chunk_name)

  ::: exercise
  Exercise

  <details><summary>Answer</summary>

    Answer to exercise

  </details>

    :::


    echo=FALSE # don't display code
  results='hide' # text output hidden




  /*---- Image captions ----*/

    .figure {
      display: table;
      float: none;
      text-align: center;
      font-size: 13px;
      text-indent: 0;
      /*border: 1px solid;
      border-radius: 10px;*/
        box-shadow: grey 0 5px 15px;
      margin: 1.5em 0.5em 2em 0.5em;
      padding: 0.5em 0.5em 0 0.5em;
    }
  .caption {
    padding-top: 0.5em;
  }
  .caption:before {
    counter-increment: figure;
    font-weight: bold;
    content: "Figure " counter(figure) ": ";
  }

