# Pelican R-Markdown Reader

This plugin lets you process R-Markdown files in [Pelican][0]. It is
an update of the [rmd_reader][1] plugin available as part of
[pelican-plugins][2]. It address three issues in `rmd_reader`:

1. [MathJAX][3] is now supported (`RmdReader` now inherits from
   `readers.MarkdownReader` instead of `readers.BaseReader`).
2. Plots are generated in separate directories for each `rmd` file, so
   plot output from identically-named blocks in separate `rmd` files
   will not get clobbered.
3. There is no need to include a special block in each `rmd` file to
   ensure that relative image links include a `{filename}` block.

## Installation

This package requires [Markdown][4] and [rpy2][5], which can be
installed with the command

    pip install rpy2 Markdown

The `rpy2` package requires that `R` has been compiled with the
`--enable-R-shlib` flag enabled. This package also requires `knitr`,
which you can install in `R` with the command

    install.packages("knitr")

## Usage

Make sure that the plugin is visible to Pelican by setting
`PLUGIN_PATHS` and `PLUGINS` appropriately (see
[the Pelican documentation][6]). Also, add the directory `figure` to
`STATIC_PATHS`:

    STATIC_PATHS = ['figure']

[0]: https://github.com/getpelican/pelican/
[1]: https://github.com/getpelican/pelican-plugins/tree/master/rmd_reader
[2]: https://github.com/getpelican/pelican-plugins
[3]: http://www.mathjax.org/
[4]: https://pypi.python.org/pypi/Markdown
[5]: http://rpy.sourceforge.net/
[6]: http://docs.getpelican.com/en/latest/settings.html
