# -*- coding: utf-8 -*-

"""
# Knitr Support for Pelican

This plugin allows you to render .Rmd files with pelican. I wrote it
because the `rmd_reader` and `render_math` in `pelican-plugins` are
incompatible with each other. Eventually I'll write a pull request.
"""

import os

from pelican import readers, settings, signals

_EXTENSIONS = ["Rmd", "rmd"]

## NB. base.dir only sets the location of output plots. This should
## escape path and basename, but it doesn't.

_KNIT_TEMPLATE = """
require(knitr)

opts_knit$set(base.dir = "{path}", base.url = "{{filename}}")
opts_chunk$set(fig.path = "{figures}")
knit("{source}", "{dest}", encoding = "UTF-8")
"""

try:
    from rpy2 import robjects
    _RMD = True
except ImportError:
    _RMD = False

## NB. I am using settings.DEFAULT_CONFIG.get('PATH')) + "/content"
## for content_dir, but the former is just the current os directory.
## It is wrong.

## From knitr/R/output.R:

## If the `output` argument is a file path, it is strongly recommended
## to be in the current working directory (e.g. `foo.tex` instead of
## `somewhere/foo.tex`), especially when the output has external
## dependencies such as figure files. If you want to write the output
## to a different directory, you are recommended to set the working
## directory to that directory before you knit a document. For
## example, if the source document is `foo.Rmd`, and the expected
## output is `out/foo.md`, you can do `setwd('out/');
## knit('../foo.Rmd')`, instead of `knit('foo.Rmd', 'out/foo.md')`.

class RmdReader(readers.MarkdownReader):
    """Reader for R-Markdown files."""

    enabled = readers.MarkdownReader.enabled and _RMD
    file_extensions = _EXTENSIONS

    def read(self, source_path):
        """Parse content and metadata of R Markdown (.Rmd) files."""
        filename, _ = os.path.splitext(source_path)
        knitr_output = os.path.basename(filename) + '.md'
        content_dir = os.path.abspath(self.settings['PATH'])
        cwd = os.getcwd()
        try:
            os.chdir(content_dir)
            robjects.r(_KNIT_TEMPLATE.format(
                source=source_path,
                dest=knitr_output,
                path=content_dir,
                figures=os.path.join("figure", os.path.basename(filename), "")
            ))
            content, metadata = super(RmdReader, self).read(knitr_output)
        finally:
            if os.path.exists(knitr_output):
                os.remove(knitr_output)
            os.chdir(cwd)
        return (content, metadata)

def add_reader(readers):
    for extension in _EXTENSIONS:
        readers.reader_classes[extension] = RmdReader

def register():
    signals.readers_init.connect(add_reader)
