The template `uoc_template.html` is based on the original `sub-section-without-left-navigation.html` from [Project Light](https://www.cam.ac.uk/web-support/project-light). See `templates/sub-section-without-left-navigation.html` for more details.

There are 3 style sheets in the `stylesheets` folder:

1. `full-stylesheet.css` contains the CSS for the UoC template
2. `styleguide.css` contains info for the UoC styleguide (unchanged)
3. `style.css` contains several tweaks for bookdown

Several changes have been made:

* The [bookdown](https://bookdown.org) template for bs4 (see `templates/template_bs4_book.html` for reference) has been integrated into the UoC template.
* The `Related links` column has been disabled
* The size of `.campl-column9` has been increased to 100% to accommodate the `bookdown` page and TOCs
* The `code` CSS from UoC has been disabled to enable use of the bookdown `code` and `kbd` styling
* The external link icon for the UoC template has been disabled
* List item spacing has been removed to improve readability
* The naming of the current materials page is now dynamic (e.g. `$title$` instead of `Core Statistics in R`)
* Font size has been inherited from the `bookdown` template to improve readability

The materials can be rendered using the `bookdown` command:

`bookdown::render_book(output_dir = "docs", "index.Rmd", "bookdown::bs4_book")`

This outputs the website to the `/docs` folder. On GitHub go to the repo > Settings > Pages > Publish website and select the correct branch and folder location.
