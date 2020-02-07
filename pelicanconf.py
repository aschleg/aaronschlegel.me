#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

AUTHOR = 'Aaron Schlegel'
SITENAME = "Aaron Schlegel's Notebook of Interesting Things"
SITESUBTITLE = ''
SITEURL = 'https://aaronschlegel.me'

MARKUP = ('md', 'ipynb')

PLUGIN_PATHS = ['./plugins']
PLUGINS = ['ipynb.markup', 'rmd_reader', 'render_math']

THEME = 'themes/gum'

# RMD_READER_RENAME_PLOT = 'directory'
# RMD_READER_KNITR_OPTS_CHUNK = {'fig.path': 'figure/'}

PATH = 'content'
STATIC_PATHS = ['figure']
ARTICLE_PATHS = ['posts']

IGNORE_FILES = ['content/draft', '.ipynb_checkpoints']

#Gum Theme Options
GITHUB_URL = 'https://github.com/aschleg'
TWITTER_URL = 'http://www.twitter.com/Aaron_Schlegel'
GOOGLEPLUS_URL = 'https://plus.google.com/u/0/102881569650657098667'

GOOGLE_ANALYTICS_ID = 'UA-48350829-2'
GOOGLE_ANALYTICS_SITENAME = 'aaronschlegel.me'

TIMEZONE = 'America/Los_Angeles'
DEFAULT_LANG = 'English'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Python.org', 'http://python.org/'),)

# Social widget
SOCIAL = (('Github', 'https://github.com/aschleg'),
          ('Linkedin', 'https://linkedin.com/in/aaronschlegel'),
          ('Twitter', 'http://www.twitter.com/Aaron_Schlegel'),)

DEFAULT_PAGINATION = 100

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
